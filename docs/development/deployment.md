# Deployment Guide

This guide covers various deployment options for JamfMCP, from local development to production environments.

## Deployment Overview

JamfMCP can be deployed in several ways:

- **Local Development**: Direct execution with uv
- **MCP Client Integration**: Cursor, Claude Desktop
- **Container Deployment**: Docker/Podman
- **Cloud Deployment**: AWS, Azure, GCP
- **Package Distribution**: PyPI (planned)

## Local Development Deployment

### Direct Execution

```bash
# Clone and install
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp
make install

# Run directly
uv run fastmcp run src/jamfmcp/server.py:mcp
```

### Environment Configuration

```bash
# Create .env file (not tracked in git)
cat > .env << EOF
JAMF_URL=your-server.jamfcloud.com
JAMF_AUTH_TYPE=client_credentials
JAMF_CLIENT_ID=your-client-id
JAMF_CLIENT_SECRET=your-client-secret
EOF

# Run with environment
source .env && uv run fastmcp run src/jamfmcp/server.py:mcp
```

## MCP Client Deployment

### Cursor Configuration

Location: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/absolute/path/to/jamfmcp",
        "fastmcp",
        "run",
        "src/jamfmcp/server.py:mcp"
      ],
      "env": {
        "JAMF_URL": "your-server.jamfcloud.com",
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "your-client-id",
        "JAMF_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Claude Desktop Configuration

Location varies by OS:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Same configuration format as Cursor.

## Container Deployment

### Dockerfile

```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy application
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose MCP port (if needed)
EXPOSE 8080

# Run MCP server
CMD ["fastmcp", "run", "jamfmcp.server:mcp"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  jamfmcp:
    build: .
    container_name: jamfmcp-server
    restart: unless-stopped
    environment:
      - JAMF_URL=${JAMF_URL}
      - JAMF_AUTH_TYPE=${JAMF_AUTH_TYPE}
      - JAMF_CLIENT_ID=${JAMF_CLIENT_ID}
      - JAMF_CLIENT_SECRET=${JAMF_CLIENT_SECRET}
      - LOG_LEVEL=INFO
    ports:
      - "8080:8080"
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Building and Running

```bash
# Build image
docker build -t jamfmcp:latest .

# Run container
docker run -d \
  --name jamfmcp \
  -e JAMF_URL=your-server.com \
  -e JAMF_AUTH_TYPE=client_credentials \
  -e JAMF_CLIENT_ID=your-id \
  -e JAMF_CLIENT_SECRET=your-secret \
  jamfmcp:latest

# Using docker-compose
docker-compose up -d
```

## Cloud Deployment

### AWS ECS/Fargate

Task definition example:

```json
{
  "family": "jamfmcp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [{
    "name": "jamfmcp",
    "image": "your-ecr-repo/jamfmcp:latest",
    "essential": true,
    "environment": [
      {"name": "JAMF_URL", "value": "your-server.com"},
      {"name": "JAMF_AUTH_TYPE", "value": "client_credentials"}
    ],
    "secrets": [
      {
        "name": "JAMF_CLIENT_ID",
        "valueFrom": "arn:aws:secretsmanager:region:account:secret:jamf-client-id"
      },
      {
        "name": "JAMF_CLIENT_SECRET",
        "valueFrom": "arn:aws:secretsmanager:region:account:secret:jamf-client-secret"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/jamfmcp",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jamfmcp
  labels:
    app: jamfmcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: jamfmcp
  template:
    metadata:
      labels:
        app: jamfmcp
    spec:
      containers:
      - name: jamfmcp
        image: your-registry/jamfmcp:latest
        ports:
        - containerPort: 8080
        env:
        - name: JAMF_URL
          value: "your-server.com"
        - name: JAMF_AUTH_TYPE
          value: "client_credentials"
        - name: JAMF_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: jamf-credentials
              key: client-id
        - name: JAMF_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: jamf-credentials
              key: client-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: jamfmcp
spec:
  selector:
    app: jamfmcp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### Azure Container Instances

```bash
# Create resource group
az group create --name jamfmcp-rg --location eastus

# Create container instance
az container create \
  --resource-group jamfmcp-rg \
  --name jamfmcp \
  --image your-acr.azurecr.io/jamfmcp:latest \
  --cpu 1 \
  --memory 1 \
  --environment-variables \
    JAMF_URL=your-server.com \
    JAMF_AUTH_TYPE=client_credentials \
  --secure-environment-variables \
    JAMF_CLIENT_ID=$CLIENT_ID \
    JAMF_CLIENT_SECRET=$CLIENT_SECRET
```

## Security Considerations

### Secrets Management

#### AWS Secrets Manager

```python
import boto3
import json

def get_secret():
    session = boto3.session.Session()
    client = session.client('secretsmanager')

    response = client.get_secret_value(SecretId='jamf-credentials')
    secret = json.loads(response['SecretString'])

    return {
        'JAMF_CLIENT_ID': secret['client_id'],
        'JAMF_CLIENT_SECRET': secret['client_secret']
    }
```

#### Azure Key Vault

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secrets():
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url="https://your-vault.vault.azure.net/",
        credential=credential
    )

    return {
        'JAMF_CLIENT_ID': client.get_secret("jamf-client-id").value,
        'JAMF_CLIENT_SECRET': client.get_secret("jamf-client-secret").value
    }
```

#### HashiCorp Vault

```python
import hvac

def get_secrets():
    client = hvac.Client(url='https://vault.company.com')
    client.token = 'your-vault-token'

    secret = client.read('secret/data/jamf')
    return secret['data']['data']
```

### Network Security

#### Firewall Rules

Required outbound connections:
- HTTPS (443) to Jamf Pro server
- HTTPS (443) to sofafeed.macadmins.io

No inbound connections required for MCP operation.

#### TLS Configuration

```python
# Enforce minimum TLS version
import ssl
import httpx

ssl_context = ssl.create_default_context()
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

client = httpx.AsyncClient(verify=ssl_context)
```

## Monitoring and Logging

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "api_call",
    method="GET",
    endpoint="/computers",
    duration=0.123,
    status=200
)
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
api_requests = Counter('jamfmcp_api_requests_total',
                      'Total API requests',
                      ['method', 'endpoint'])
api_duration = Histogram('jamfmcp_api_duration_seconds',
                        'API request duration')

# Start metrics server
start_http_server(8000)

# Use in code
with api_duration.time():
    api_requests.labels(method='GET', endpoint='/computers').inc()
    # API call
```

### Health Checks

```python
from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check Jamf connectivity
        await jamf_api.ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}
```

## Performance Tuning

### Connection Pooling

```python
import httpx

# Configure connection limits
limits = httpx.Limits(
    max_keepalive_connections=5,
    max_connections=10,
    keepalive_expiry=30.0
)

client = httpx.AsyncClient(limits=limits)
```

### Caching Configuration

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedData:
    def __init__(self, data, expires_at):
        self.data = data
        self.expires_at = expires_at

    @property
    def is_expired(self):
        return datetime.now() > self.expires_at

@lru_cache(maxsize=128)
def get_cached_data(key: str) -> CachedData:
    # Fetch and cache data
    pass
```

### Resource Limits

```yaml
# Docker resource limits
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

## Deployment Checklist

### Pre-Deployment

- [ ] Test in development environment
- [ ] Verify Jamf Pro connectivity
- [ ] Test authentication credentials
- [ ] Review security settings
- [ ] Plan rollback strategy

### Deployment

- [ ] Deploy to staging first
- [ ] Verify health checks pass
- [ ] Test core functionality
- [ ] Monitor logs for errors
- [ ] Check performance metrics

### Post-Deployment

- [ ] Monitor for 24 hours
- [ ] Review error rates
- [ ] Check API usage limits
- [ ] Document any issues
- [ ] Update runbooks

## Troubleshooting Deployment

### Common Issues

#### Connection Refused
```bash
# Check if service is running
docker ps | grep jamfmcp

# Check logs
docker logs jamfmcp

# Test connectivity
curl http://localhost:8080/health
```

#### Authentication Failures
```bash
# Verify credentials
echo $JAMF_CLIENT_ID

# Test API directly
curl -X POST https://your-server.com/api/oauth/token \
  -d "client_id=$JAMF_CLIENT_ID&client_secret=$JAMF_CLIENT_SECRET&grant_type=client_credentials"
```

#### Performance Issues
```bash
# Check resource usage
docker stats jamfmcp

# Review slow queries
grep "duration" logs/jamfmcp.log | awk '{if ($NF > 1.0) print}'
```

## Future Deployment Options

### PyPI Distribution

Once available on PyPI:

```bash
# Install globally
pip install jamfmcp

# Run directly
jamfmcp serve

# Or with uv run
uv run --with jamfmcp jamfmcp serve
```

### FastMCP Cloud

Planned support for FastMCP Cloud deployment:

```bash
# Deploy to FastMCP Cloud
fastmcp deploy jamfmcp
```

:::{seealso}
- [FastMCP Deployment](https://gofastmcp.com/servers/deployment)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
:::
