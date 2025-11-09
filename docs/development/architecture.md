# Architecture

This document describes the architectural design and implementation details of JamfMCP.

## System Overview

JamfMCP is built as a layered architecture with clear separation of concerns:

### Architecture Layers

**MCP Clients**
- Cursor
- Claude Desktop  
- Other MCP Clients

**JamfMCP Server Components**
- FastMCP Server Layer - Handles MCP protocol communication
- Tool Functions - Exposed API methods for client interaction
- API Client Layer - Manages Jamf Pro API requests
- Authentication Layer - Handles credential management
- Health Analysis Engine - Processes computer health metrics
- SOFA Integration - Security vulnerability analysis

**External Services**
- Jamf Pro API - Primary data source
- SOFA Feed API - Security vulnerability feed

## Core Components

### FastMCP Server Layer

The server layer handles MCP protocol implementation:

- **Protocol Handling**: JSON-RPC communication
- **Tool Discovery**: Automatic tool registration
- **Parameter Validation**: Schema generation from type hints
- **Error Handling**: Consistent error responses
- **Async Execution**: Non-blocking tool execution

### Tool Functions

Tools are the primary interface for MCP clients:

- **49 Tools**: Comprehensive Jamf Pro functionality
- **Decorator Pattern**: `@mcp.tool` for registration
- **Type Safety**: Full type hints for parameters
- **Documentation**: Sphinx-style docstrings
- **Error Handling**: Structured error responses

### API Client Layer

The `JamfApi` class provides abstraction over Jamf Pro APIs:

```python
class JamfApi:
    def __init__(self, auth: JamfAuth):
        self.auth = auth
        self.server = auth.server
        self.credentials = auth.get_credentials_provider()

    async def get_computer_inventory(self, serial: str) -> dict:
        # Implementation
        pass
```

Key features:
- **Unified Interface**: Abstracts Pro and Classic APIs
- **Response Parsing**: Handles API response formats
- **Error Translation**: Converts HTTP errors to user-friendly messages
- **Retry Logic**: Automatic retry for transient failures

### Authentication Layer

Flexible authentication supporting multiple methods:

```python
class JamfAuth:
    def __init__(self, auth_type: str = "basic", ...):
        self.auth_type = auth_type
        # Configuration

    def get_credentials_provider(self) -> CredentialsProvider:
        if self.auth_type == "basic":
            return UserCredentialsProvider(...)
        else:
            return ApiClientCredentialsProvider(...)
```

Features:
- **Multiple Auth Types**: Basic and OAuth
- **Token Management**: Automatic token refresh
- **Credential Providers**: Pluggable authentication
- **Security**: No credential storage in memory

### Health Analysis Engine

Sophisticated health scoring system:

```python
class HealthAnalyzer:
    CATEGORY_WEIGHTS = {
        "security": 0.35,
        "system_health": 0.25,
        "compliance": 0.25,
        "maintenance": 0.15,
    }

    def generate_health_scorecard(self) -> HealthScorecard:
        # Complex scoring logic
        pass
```

Components:
- **Multi-Category Analysis**: Security, health, compliance, maintenance
- **Weighted Scoring**: Configurable category weights
- **CVE Integration**: Real-time vulnerability assessment
- **Recommendations**: Actionable improvement suggestions

### SOFA Integration

Security vulnerability tracking via macadmins SOFA:

```python
async def get_sofa_feed() -> dict:
    # Fetch latest feed
    pass

def get_cves_for_version(feed: SOFAFeed, version: str) -> tuple[set, set]:
    # Analyze CVEs
    pass
```

Features:
- **Real-time CVE Data**: Latest vulnerability information
- **Version Analysis**: OS currency assessment
- **Exploit Detection**: Identify actively exploited CVEs
- **Performance**: Efficient feed parsing and caching

## Data Flow

### Request Flow

1. **MCP Client** sends request via JSON-RPC
2. **FastMCP** validates and routes to tool
3. **Tool Function** processes request
4. **API Client** makes authenticated calls
5. **Response** flows back through layers

### Authentication Flow

The authentication process works as follows:

1. **Initialization**
   - Client initializes JamfAuth
   - JamfAuth creates appropriate credential provider

2. **Token Acquisition**
   - Client requests credentials from JamfAuth
   - JamfAuth requests token from credential provider
   - Credential provider authenticates with Jamf Pro
   - Jamf Pro returns authentication token

3. **Client Setup**
   - Token flows back through credential provider to JamfAuth
   - JamfAuth returns authenticated client ready for API calls

### Health Analysis Flow

The health analysis process follows this sequence:

1. **Data Collection**
   - Tool requests computer inventory from Jamf API
   - Tool requests computer history from Jamf API
   - Tool fetches CVE feed from SOFA

2. **Analysis**
   - Analyzer receives collected data
   - Calculates health scores across categories
   - Generates actionable recommendations

3. **Results**
   - Returns comprehensive HealthScorecard to tool

## Design Patterns

### Decorator Pattern

Tools use decorators for registration:

```python
@mcp.tool
async def tool_function(param: str) -> dict:
    """Tool implementation"""
    pass
```

### Factory Pattern

Authentication uses factory for credential providers:

```python
def get_credentials_provider(self) -> CredentialsProvider:
    if self.auth_type == "basic":
        return UserCredentialsProvider(...)
    return ApiClientCredentialsProvider(...)
```

### Strategy Pattern

Health scoring uses strategies for different categories:

```python
def _calculate_security_score(self) -> HealthScore:
    # Security-specific logic
    pass

def _calculate_compliance_score(self) -> HealthScore:
    # Compliance-specific logic
    pass
```

### Async/Await Pattern

All I/O operations are async:

```python
async def get_data(self) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

## Performance Considerations

### Async Architecture

- **Non-blocking I/O**: All API calls are async
- **Concurrent Requests**: Multiple operations in parallel
- **Connection Pooling**: Reuse HTTP connections
- **Efficient Memory**: Stream large responses

### Caching Strategy

```python
class CachedSOFAFeed:
    def __init__(self, ttl_seconds: int = 3600):
        self._cache = {}
        self._ttl = ttl_seconds

    async def get_feed(self) -> SOFAFeed:
        if self._is_cache_valid():
            return self._cache['feed']
        return await self._refresh_cache()
```

### Rate Limiting

- **Respect API Limits**: Track request counts
- **Backoff Strategy**: Exponential backoff on 429
- **Batch Operations**: Combine related requests
- **Pagination Handling**: Efficient large dataset retrieval

## Security Architecture

### Credential Management

- **No Hardcoding**: All credentials from environment
- **Token Rotation**: Automatic token refresh
- **Secure Storage**: Use OS keychain when available
- **Least Privilege**: Request minimal permissions

### Input Validation

```python
def validate_serial(serial: str) -> str:
    if not serial or not serial.strip():
        raise ValueError("Serial cannot be empty")
    # Additional validation
    return serial.strip().upper()
```

### Error Handling

- **No Sensitive Data**: Sanitize error messages
- **Structured Errors**: Consistent error format
- **Logging**: Secure logging practices
- **Graceful Degradation**: Handle failures safely

## Extensibility

### Adding New Tools

1. Add function to `server.py`
2. Use `@mcp.tool` decorator
3. Follow naming conventions
4. Add comprehensive tests

### Custom Analyzers

```python
class CustomAnalyzer(HealthAnalyzer):
    def _calculate_custom_score(self) -> HealthScore:
        # Custom scoring logic
        pass
```

### Plugin Architecture

Future consideration for plugin support:

```python
class ToolPlugin:
    def register_tools(self, mcp: FastMCP):
        @mcp.tool
        async def custom_tool():
            pass
```

## Testing Architecture

### Test Organization

```
tests/
├── conftest.py          # Shared fixtures
├── fixtures/            # Test data
├── test_auth.py        # Auth tests
├── test_health_analyzer.py  # Health tests
├── test_mcp_tools.py   # Tool tests
└── test_sofa.py        # SOFA tests
```

### Test Patterns

```python
@pytest.mark.asyncio
async def test_tool_function(mock_api):
    # Arrange
    mock_api.return_value = {"data": "test"}

    # Act
    result = await tool_function("param")

    # Assert
    assert result["data"] == "test"
```

## Deployment Architecture

### Container Support

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["fastmcp", "run", "jamfmcp.server:mcp"]
```

### Configuration Management

- **Environment Variables**: Primary configuration
- **Config Files**: MCP client configuration
- **Secrets Management**: External secret stores
- **Multi-Environment**: Dev/staging/production

## Future Architecture Considerations

### Scalability

- **Horizontal Scaling**: Multiple server instances
- **Load Balancing**: Distribute requests
- **Caching Layer**: Redis for shared cache
- **Queue System**: Async job processing

### Monitoring

- **Metrics Collection**: Prometheus integration
- **Distributed Tracing**: OpenTelemetry support
- **Health Endpoints**: Liveness/readiness probes
- **Performance Monitoring**: APM integration

### API Evolution

- **Versioning**: Support multiple API versions
- **Deprecation**: Graceful feature retirement
- **Feature Flags**: Progressive rollout
- **Backward Compatibility**: Maintain compatibility

:::{seealso}
- [FastMCP Architecture](https://gofastmcp.com/servers/overview)
- [MCP Protocol Design](https://modelcontextprotocol.io/docs/architecture)
- [Python Async Patterns](https://docs.python.org/3/library/asyncio-task.html)
:::
