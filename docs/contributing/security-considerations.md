(security_considerations)=
# Security Considerations

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

- **No Sensitive Data**: Sanitize error messages
- **Structured Errors**: Consistent error format
- **Logging**: Secure logging practices

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

**External Services**
- Jamf Pro API - Primary data source
- SOFA Feed API - Security vulnerability feed

## Secrets Manager

The following has not been tested whatsoever but hypothetcially could work.

### AWS Secrets Manager

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

### Azure Key Vault

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

### HashiCorp Vault

```python
import hvac

def get_secrets():
    client = hvac.Client(url='https://vault.company.com')
    client.token = 'your-vault-token'

    secret = client.read('secret/data/jamf')
    return secret['data']['data']
```

## Network Security

### Firewall Rules

Required outbound connections:
- HTTPS (443) to Jamf Pro server
- HTTPS (443) to sofafeed.macadmins.io

No inbound connections required for MCP operation.

## Future Deployment Options - FastMCP Cloud

Planned support for FastMCP Cloud deployment:

```bash
# Deploy to FastMCP Cloud
fastmcp deploy jamfmcp
```

:::{seealso}
- [FastMCP Deployment](https://gofastmcp.com/servers/deployment)
:::
