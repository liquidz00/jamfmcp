# Authentication Troubleshooting

This guide helps resolve authentication-related issues with JamfMCP.

## Common Authentication Errors

### 401 Unauthorized

**Error Message:**
```
401 Unauthorized
Failed to authenticate with Jamf Pro
```

**Possible Causes:**
1. Incorrect credentials
2. Expired password (basic auth)
3. Revoked client credentials (OAuth)
4. Account locked or disabled
5. API access not enabled

**Solutions:**

#### Check Credentials
```bash
# Test basic auth
curl -u username:password \
  https://your-server.com/api/v1/auth/token

# Test OAuth
curl -X POST https://your-server.com/api/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_ID&client_secret=YOUR_SECRET&grant_type=client_credentials"
```

#### Verify in Jamf Pro
1. Log into Jamf Pro web interface
2. Navigate to **Settings** → **System** → **User Accounts**
3. Verify account is:
   - Enabled
   - Not locked
   - Has "Access to Jamf Pro API" privilege

### 403 Forbidden

**Error Message:**
```
403 Forbidden
Insufficient privileges to access this resource
```

**Possible Causes:**
1. Missing API privileges
2. Wrong API role assigned
3. Site restrictions
4. IP address restrictions

**Solutions:**

#### Check API Privileges
For OAuth:
1. Go to **Settings** → **System** → **API Roles**
2. Find your role and verify it has:
   - Read privileges for all needed resources
   - No unnecessary restrictions

For Basic Auth:
1. Check user account privileges
2. Ensure all required read permissions are granted

#### Required Minimum Privileges
```
Computers:
✓ Read Computers
✓ Read Computer Inventory Collection
✓ Read Computer Groups
✓ Read Computer Extension Attributes

Policies:
✓ Read Policies
✓ Read macOS Configuration Profiles
✓ Read Scripts
✓ Read Packages

Organization:
✓ Read Buildings
✓ Read Departments
✓ Read Sites
```

### Invalid Authentication Type

**Error Message:**
```
Invalid JAMF_AUTH_TYPE. Must be 'basic' or 'client_credentials'
```

**Solution:**
Check your MCP configuration:

```json
{
  "env": {
    "JAMF_AUTH_TYPE": "basic"  // or "client_credentials"
  }
}
```

## Authentication Configuration Issues

### Missing Environment Variables

**Error:**
```
Missing required credentials for basic authentication
JAMF_USERNAME and JAMF_PASSWORD must be provided
```

**Solution:**
Add missing variables to MCP config:

```json
{
  "env": {
    "JAMF_URL": "your-server.com",
    "JAMF_AUTH_TYPE": "basic",
    "JAMF_USERNAME": "api-user",
    "JAMF_PASSWORD": "secure-password"
  }
}
```

### OAuth Client Issues

**Error:**
```
Client authentication failed
invalid_client
```

**Common Causes:**
1. Client ID/Secret mismatch
2. Client has been deleted
3. Client is disabled
4. Typo in credentials

**Debug Steps:**
1. Copy client ID from Jamf Pro exactly
2. Regenerate client secret if unsure
3. Update configuration immediately
4. Test with curl before using in MCP

## Token Management Issues

### Token Expiration

**Symptoms:**
- Works initially, then fails
- Intermittent authentication errors
- "Token expired" messages

**Understanding Token Lifetimes:**
- Basic Auth tokens: 30 minutes default
- OAuth tokens: 60 minutes typical
- Tokens auto-refresh in JamfMCP

**If Auto-Refresh Fails:**
1. Check network connectivity
2. Verify credentials still valid
3. Restart MCP client
4. Check for clock skew

### Token Caching Issues

**Symptoms:**
- Old credentials still being used
- Changes not taking effect

**Solution:**
1. Restart MCP client completely
2. Clear any credential cache:
   ```bash
   # No persistent cache in JamfMCP
   # Just restart the client
   ```

## Server URL Issues

### Invalid Server URL

**Error:**
```
Jamf Pro server URL not provided
Failed to connect to Jamf Pro
```

**Common Problems:**

#### Missing Protocol
```json
// ❌ Wrong
"JAMF_URL": "your-server.com:8443"

// ✅ Correct (protocol optional)
"JAMF_URL": "your-server.com"
"JAMF_URL": "https://your-server.com:8443"
```

#### Trailing Slash
```json
// ❌ Wrong
"JAMF_URL": "https://your-server.com/"

// ✅ Correct
"JAMF_URL": "https://your-server.com"
```

#### Wrong Port
```json
// Default HTTPS port (443) - no port needed
"JAMF_URL": "your-server.jamfcloud.com"

// Custom port
"JAMF_URL": "https://your-server.com:8443"
```

## SSL/TLS Issues

### Certificate Verification Failed

**Error:**
```
SSL: CERTIFICATE_VERIFY_FAILED
unable to get local issuer certificate
```

**Causes:**
1. Self-signed certificate
2. Expired certificate
3. Missing intermediate certificates
4. Corporate proxy

**Solutions:**

#### For Testing Only (Insecure)
```python
# DO NOT USE IN PRODUCTION
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

#### Proper Solutions
1. Use valid SSL certificate
2. Add CA certificate to system trust store
3. Configure proxy settings if applicable

## Debugging Authentication

### Enable Debug Logging

Add to MCP configuration:
```json
{
  "env": {
    "LOG_LEVEL": "DEBUG",
    // ... other settings
  }
}
```

### Test Script

Save as `test_auth.py`:

```python
#!/usr/bin/env python3
"""Test Jamf authentication."""

import os
import asyncio
import sys

async def test_auth():
    try:
        from jamfmcp.auth import JamfAuth
        from jamfmcp.jamfsdk import JamfProClient

        print("Creating auth provider...")
        auth = JamfAuth()
        print(f"✓ Server: {auth.server}")
        print(f"✓ Auth Type: {auth.auth_type}")

        print("\nCreating client...")
        client = JamfProClient(
            server=auth.server,
            credentials=auth.get_credentials_provider()
        )

        print("\nTesting authentication...")
        # This will attempt to get a token
        token = await client.get_access_token()
        print(f"✓ Token obtained: {token[:20]}...")

        print("\n✅ Authentication successful!")

    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        return False

    return True

if __name__ == "__main__":
    # Set test credentials
    os.environ['JAMF_URL'] = input("Jamf URL: ")
    os.environ['JAMF_AUTH_TYPE'] = input("Auth type (basic/client_credentials): ")

    if os.environ['JAMF_AUTH_TYPE'] == 'basic':
        os.environ['JAMF_USERNAME'] = input("Username: ")
        os.environ['JAMF_PASSWORD'] = input("Password: ")
    else:
        os.environ['JAMF_CLIENT_ID'] = input("Client ID: ")
        os.environ['JAMF_CLIENT_SECRET'] = input("Client Secret: ")

    success = asyncio.run(test_auth())
    sys.exit(0 if success else 1)
```

### Manual Token Test

```bash
# Get token with basic auth
TOKEN=$(curl -s -u username:password \
  https://your-server.com/api/v1/auth/token \
  | jq -r .token)

echo "Token: $TOKEN"

# Test token
curl -H "Authorization: Bearer $TOKEN" \
  https://your-server.com/api/v1/jamf-pro-version
```

## Best Practices

### Credential Security

1. **Never commit credentials** to version control
2. **Use OAuth** instead of basic auth for production
3. **Rotate credentials** regularly
4. **Use least privilege** - only grant needed permissions
5. **Monitor usage** in Jamf Pro logs

### Configuration Management

```json
// Development
{
  "env": {
    "JAMF_URL": "dev.jamfcloud.com",
    "JAMF_AUTH_TYPE": "basic",
    "JAMF_USERNAME": "dev-user",
    "JAMF_PASSWORD": "dev-pass"
  }
}

// Production (better)
{
  "env": {
    "JAMF_URL": "prod.jamfcloud.com",
    "JAMF_AUTH_TYPE": "client_credentials",
    "JAMF_CLIENT_ID": "prod-client-id",
    "JAMF_CLIENT_SECRET": "prod-secret"
  }
}
```

## When All Else Fails

If you've tried everything:

1. **Create fresh credentials**:
   - New API client for OAuth
   - New service account for basic auth

2. **Test outside JamfMCP**:
   - Use Postman or curl
   - Verify API works at all

3. **Check Jamf Pro logs**:
   - Look for authentication attempts
   - Check for specific error messages

4. **Contact support**:
   - Jamf support for API issues
   - GitHub issues for JamfMCP problems

## Related Issues

- [Connectivity Problems](connectivity) - Network-related issues
- [Configuration Guide](../getting-started/authentication) - Proper setup
- [Jamf API Setup](../getting-started/jamf-api-setup) - Creating credentials

:::{seealso}
- [Jamf Pro API Authentication](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview#authentication-and-authorization)
- [OAuth 2.0 Client Credentials](https://oauth.net/2/grant-types/client-credentials/)
- [FastMCP Authentication](https://gofastmcp.com/servers/authentication)
:::
