# Authentication Configuration

JamfMCP supports two authentication methods for connecting to Jamf Pro. This guide covers both methods and helps you choose the right one for your use case.

## Authentication Methods Overview

| Method | Security | Use Case | Complexity |
|--------|----------|----------|------------|
| Basic Auth | ⭐⭐ | Testing, Development | Simple |
| OAuth Client Credentials | ⭐⭐⭐⭐⭐ | Production, Long-term | Moderate |

## Basic Authentication

Basic authentication uses a username and password combination.

### When to Use

- Quick testing and development
- Proof of concept deployments
- Environments where OAuth isn't available

### Configuration

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "basic",
  "JAMF_USERNAME": "api-user",
  "JAMF_PASSWORD": "secure-password"
}
```

### Pros and Cons

| Advantages | Disadvantages |
| -----------|---------------|
| ✅ Simple to set up | ❌ Less secure than OAuth |
| ✅ No additional configuration in Jamf Pro | ❌ Password stored in configuration |
| ✅ Works with existing user accounts | ❌ Subject to password policies (expiration, complexity) |

## OAuth Client Credentials

OAuth uses client ID and secret for authentication, following the OAuth 2.0 client credentials flow.

### When to Use

- Production environments
- Long-running integrations
- When enhanced security is required
- Automated systems

### Configuration

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "abc123def456",
  "JAMF_CLIENT_SECRET": "super-secret-key-789xyz"
}
```

### Setup in Jamf Pro

1. **Create API Role** (Settings → System → API Roles)
2. **Create API Client** (Settings → System → API Clients)
3. **Assign Role** to the client
4. **Save credentials** securely

:::{tip}
See the [Jamf API Setup Guide](../getting-started/jamf-api-setup) for detailed steps.
:::

### Pros and Cons

| Advantages | Disadvantages |
| -----------|---------------|
| ✅ Token-based authentication | ❌ Requires Jamf Pro 10.49.0 or later |
| ✅ No password expiration | ❌ More complex initial setup |
| ✅ Detailed audit trail | ❌ Client secret only shown once when created |
| ✅ Follows Oauth 2.0 standards |  |
| ✅ Can be revoked without affecting user accounts |  |

## Server URL Configuration

The `JAMF_URL` supports multiple formats:

### Supported Formats

```json
// FQDN only (recommended)
"JAMF_URL": "mycompany.jamfcloud.com"

// With protocol
"JAMF_URL": "https://mycompany.jamfcloud.com"

// With custom port
"JAMF_URL": "https://jamf.internal:8443"

// With context path
"JAMF_URL": "https://server.com/jamf"
```

JamfMCP automatically handles URL normalization.

### URL Best Practices

1. **Use FQDN** without protocol for simplicity
2. **Include port** only if non-standard (not 443)
3. **Add path** only if Jamf Pro isn't at root
4. **No trailing slash** needed

## Token Management

JamfMCP handles token management automatically:

### Basic Auth Tokens
- Tokens are requested as needed
- Cached for session duration
- Automatically renewed on expiration
- 30-minute default lifetime

### OAuth Tokens
- Client credentials flow used
- Tokens cached and reused
- Automatic refresh before expiration
- Typically 60-minute lifetime

## Security Considerations

### Credential Storage

:::{warning}
**Never store credentials in:**
- Version control systems
- Plain text files
- Environment variables in shell profiles
- Shared or public locations
:::

**Recommended storage:**
- MCP client configuration files only
- With restricted file permissions
- Encrypted if possible
- In secure key management systems

## Troubleshooting Authentication

### Common Errors

#### 401 Unauthorized

**Causes:**
- Incorrect credentials
- Expired password (basic auth)
- Revoked client (OAuth)
- Account locked/disabled

**Solutions:**
1. Verify credentials are correct
2. Test with curl:
   ```bash
   # Basic auth
   curl -u username:password https://server.jamfcloud.com/api/v1/auth/token

   # OAuth
   curl -X POST https://server.jamfcloud.com/api/oauth/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id=YOUR_ID&client_secret=YOUR_SECRET&grant_type=client_credentials"
   ```
3. Check account status in Jamf Pro

#### 403 Forbidden

**Causes:**
- Insufficient API privileges
- IP restrictions
- API access disabled

**Solutions:**
1. Verify API role permissions
2. Check IP allowlist settings
3. Ensure API access is enabled

#### SSL/TLS Errors

**Causes:**
- Self-signed certificates
- Certificate chain issues
- TLS version mismatch

**Solutions:**
1. Use valid certificates
2. Update to supported TLS version
3. Check certificate chain validity

## Migration Guide

### From Basic to OAuth

1. **Create OAuth credentials** in Jamf Pro
2. **Test OAuth** separately before switching
3. **Update configuration** with new auth type
4. **Verify functionality** with test queries
5. **Remove basic auth** credentials

### Example Migration

Before:
```json
"env": {
  "JAMF_URL": "server.com",
  "JAMF_AUTH_TYPE": "basic",
  "JAMF_USERNAME": "api-user",
  "JAMF_PASSWORD": "old-password"
}
```

After:
```json
"env": {
  "JAMF_URL": "server.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "new-client-id",
  "JAMF_CLIENT_SECRET": "new-secret"
}
```

## Best Practices Summary

1. **Choose authentication method** based on organizational requirements
2. **Use dedicated API accounts** not personal credentials
3. **Document your setup** for team members
4. **Test authentication** before deploying

## Next Steps

- Review [Environment Variables](environment) reference
- Set up authentication in [Cursor](cursor) or [Claude Desktop](claude-desktop)
- Follow the [Quickstart Guide](quickstart)

:::{seealso}
- [Jamf Pro API Authentication](https://developer.jamf.com/jamf-pro/docs)
- [OAuth 2.0 Client Credentials](https://oauth.net/2/grant-types/client-credentials/)
- [FastMCP Authentication](https://gofastmcp.com/servers/authentication)
:::
