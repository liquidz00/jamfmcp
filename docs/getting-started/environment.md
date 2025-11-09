# Environment Variables Reference

This page provides a complete reference for all environment variables used by JamfMCP.

## Required Variables

### Jamf URL

The URL of your Jamf Pro server.

- **Key Name**: `JAMF_URL`
- **Type**: String
- **Required**: Yes
- **Default**: None
- **Examples**:
  ```
  mycompany.jamfcloud.com
  https://mycompany.jamfcloud.com
  https://jamf.internal.corp:8443
  https://server.com/jamfpro
  ```

:::{note}
JamfMCP automatically handles URL formatting. You can provide just the FQDN or a full URL.
:::

## Authentication Variables

### Authentication Type

Specifies the authentication method to use.

- **Key Name**: `JAMF_AUTH_TYPE`
- **Type**: String
- **Required**: No
- **Default**: `basic`
- **Values**: `basic`, `client_credentials`
- **Example**:
  ```json
  "JAMF_AUTH_TYPE": "client_credentials"
  ```

### Basic Authentication

Required when `JAMF_AUTH_TYPE` is `basic` or not specified.

#### Jamf Username

- **Key Name**: `JAMF_USERNAME`
- **Type**: String
- **Required**: Yes (for basic auth)
- **Default**: None
- **Example**: `api-readonly-user`

#### Jamf Password

- **Key Name**: `JAMF_PASSWORD`
- **Type**: String
- **Required**: Yes (for basic auth)
- **Default**: None
- **Example**: `SecurePassword123!`

### OAuth Authentication

Required when `JAMF_AUTH_TYPE` is `client_credentials`.

#### Client ID

- **Key Name**: `JAMF_CLIENT_ID`
- **Type**: String
- **Required**: Yes (for OAuth)
- **Default**: None
- **Example**: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

#### Client Secret

- **Key Name**: `JAMF_CLIENT_SECRET`  
- **Type**: String  
- **Required**: Yes (for OAuth)
- **Default**: None
- **Example**: `super-secret-key-xyz789`

## Configuration Examples

### Basic Authentication Setup

```json
{
  "env": {
    "JAMF_URL": "mycompany.jamfcloud.com",
    "JAMF_AUTH_TYPE": "basic",
    "JAMF_USERNAME": "mcp-service",
    "JAMF_PASSWORD": "P@ssw0rd123!"
  }
}
```

### OAuth Client Credentials Setup

```json
{
  "env": {
    "JAMF_URL": "mycompany.jamfcloud.com",
    "JAMF_AUTH_TYPE": "client_credentials",
    "JAMF_CLIENT_ID": "12345678-abcd-efgh-ijkl-1234567890ab",
    "JAMF_CLIENT_SECRET": "vErY-sEcReT-kEy-12345"
  }
}
```

## Environment Variable Priority

JamfMCP reads environment variables in this order:

1. **MCP Client Configuration** (recommended)
   - Set in `mcp.json` or `claude_desktop_config.json`
   - Most secure method
   - Isolated to MCP usage

2. **Direct Environment** (not recommended)
   - Set in shell or system
   - Less secure
   - May interfere with other tools

:::{warning}
**Security Warning**: Never set Jamf credentials as system environment variables. Always use MCP client configuration files.
:::

## Variable Validation

JamfMCP validates variables on startup:

### URL Validation
- Must be valid hostname or URL
- Automatically adds `https://` if missing
- Strips trailing slashes
- Validates port numbers

### Authentication Validation
- Checks required variables for auth type
- Validates credential format
- Tests authentication on first API call

### Error Messages

Common validation errors:

```
"Jamf Pro server URL not provided. Set JAMF_URL environment variable."
"Missing required credentials for basic authentication"
"Invalid JAMF_AUTH_TYPE. Must be 'basic' or 'client_credentials'"
```

## Troubleshooting

For help with these issues, see the [Configuration Troubleshooting Guide](../troubleshooting/configuration).

### Testing Variables

Test your configuration outside of MCP:

```python
# test_config.py
import os
from jamfmcp.auth import JamfAuth

# Manually set for testing
os.environ['JAMF_URL'] = 'your-server.com'
os.environ['JAMF_AUTH_TYPE'] = 'basic'
os.environ['JAMF_USERNAME'] = 'test-user'
os.environ['JAMF_PASSWORD'] = 'test-pass'

try:
    auth = JamfAuth()
    print(f"✓ Server: {auth.server}")
    print(f"✓ Auth Type: {auth.auth_type}")
    print("✓ Configuration valid!")
except Exception as e:
    print(f"✗ Error: {e}")
```

## Best Practices

1. **Choose appropriate authentication** for your environment
2. **Never commit** environment variables to version control
3. **Validate URLs** before configuring
4. **Use descriptive** client IDs in Jamf Pro
5. **Document** your configuration for team members

## Migration Scenarios

### Switching Authentication Methods

From Basic to OAuth:
```json
// Before
{
  "env": {
    "JAMF_URL": "server.com",
    "JAMF_USERNAME": "old-user",
    "JAMF_PASSWORD": "old-pass"
  }
}

// After  
{
  "env": {
    "JAMF_URL": "server.com",
    "JAMF_AUTH_TYPE": "client_credentials",
    "JAMF_CLIENT_ID": "new-id",
    "JAMF_CLIENT_SECRET": "new-secret"
  }
}
```

### Changing Servers

```json
// Development
{
  "env": {
    "JAMF_URL": "dev.jamfcloud.com",
    // ... auth variables ...
  }
}

// Production
{
  "env": {
    "JAMF_URL": "prod.jamfcloud.com",
    // ... auth variables ...
  }
}
```

## Related Documentation

- [Authentication Guide](authentication) - Detailed auth setup
- [Cursor Configuration](cursor) - Cursor-specific setup
- [Claude Desktop Configuration](claude-desktop) - Claude-specific setup
- [Jamf API Setup](jamf-api-setup) - Creating API credentials

:::{seealso}
- [FastMCP Environment Variables](https://gofastmcp.com/servers/deployment#environment-variables)
- [Jamf Pro API Authentication](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview#authentication-and-authorization)
:::
