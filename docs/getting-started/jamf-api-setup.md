# Jamf API Setup Guide

This guide walks you through setting up API access for JamfMCP with the appropriate privileges following the principle of least privilege.

## Authentication Methods

JamfMCP supports two authentication methods:

### Option 1: OAuth Client Credentials

OAuth client credentials provide token-based authentication using the OAuth 2.0 standard.

#### Step 1: Create an API Role

1. Navigate to **Settings** → **System** → **API Roles** in Jamf Pro
2. Click **New** to create a new API role
3. Name it something descriptive like "JamfMCP Read-Only"
4. Grant the following privileges:

:::{admonition} Required Privileges Checklist
:class: important

**Computers**
- [x] Read Computers
- [x] Read Computer Inventory Collection
- [x] Read Computer Groups  
- [x] Read Computer Extension Attributes
- [x] Read Computer Check-In
- [x] Read Computer MDM Command Information

**Policies & Profiles**
- [x] Read Policies
- [x] Read macOS Configuration Profiles
- [x] Read Scripts
- [x] Read Packages
- [x] Read Patch Management Software Titles
- [x] Read Patch Policies

**Organization**
- [x] Read Buildings
- [x] Read Departments
- [x] Read Network Segments
- [x] Read Sites
- [x] Read Categories

**Users & Groups**
- [x] Read Users
- [x] Read User Groups
- [x] Read LDAP Servers
- [x] Read Directory Bindings

**Security & Compliance**
- [x] Read Restricted Software
- [x] Read Licensed Software
- [x] Read Advanced Computer Searches
- [x] Read Webhooks
- [x] Read Extension Attributes
:::

#### Step 2: Create API Client

1. Navigate to **Settings** → **System** → **API Clients**
2. Click **New** to create a new API client
3. Configure the client:
   - **Display Name**: "JamfMCP Client"
   - **API Role**: Select the role created in Step 1
   - **Client ID**: Auto-generated (save this!)
   - **Client Secret**: Click "Generate" (save this securely!)

:::{warning}
The client secret is only shown once! Save it immediately in a secure location.
:::

#### Step 3: Configure JamfMCP

Use these credentials in your MCP client configuration:

```json
{
  "env": {
    "JAMF_URL": "your-jamf-server.com",
    "JAMF_AUTH_TYPE": "client_credentials",
    "JAMF_CLIENT_ID": "your-client-id",
    "JAMF_CLIENT_SECRET": "your-client-secret"
  }
}
```

### Option 2: Basic Authentication

Basic authentication uses username and password credentials.

#### Step 1: Create or Use Service Account

1. Navigate to **Settings** → **System** → **User Accounts**
2. Create a new user or use existing
3. Grant the same privileges as listed above for the API role

#### Step 2: Configure JamfMCP

```json
{
  "env": {
    "JAMF_URL": "your-jamf-server.com",
    "JAMF_AUTH_TYPE": "basic",
    "JAMF_USERNAME": "your-username",
    "JAMF_PASSWORD": "your-password"
  }
}
```

## Server URL Format

The `JAMF_URL` can be specified in several formats:

- **FQDN only**: `your-server.jamfcloud.com`
- **With protocol**: `https://your-server.jamfcloud.com`
- **With port**: `https://your-server.com:8443`
- **With path**: `https://your-server.com/jamf`

JamfMCP will automatically handle the URL formatting.

## Verifying Access

After configuration, you can verify API access by:

1. Starting your MCP client with JamfMCP configured
2. Running a simple test command like "ping the Jamf MCP server"
3. Checking for successful authentication in the response

## Security Considerations

:::{admonition} Important Security Notes
:class: warning

1. **Choose appropriate authentication** based on your organization's requirements
2. **Rotate credentials** regularly
3. **Use read-only privileges** - JamfMCP doesn't need write access
4. **Store credentials securely** - never commit them to version control
:::

## Troubleshooting

For help with these issues, see the [Authentication Troubleshooting Guide](../troubleshooting/authentication).

**403 Forbidden**
- Check API role has all required privileges
- Verify the user/client is assigned the correct role
- Ensure no IP restrictions are blocking access

**Connection Failed**
- Verify the JAMF_URL is correct
- Check network connectivity to Jamf Pro
- Ensure HTTPS/TLS is properly configured

### API Rate Limits

Jamf Pro implements API rate limiting. JamfMCP handles this automatically, but be aware:

- Default limit is typically 5000 requests per hour
- Limits may vary based on your Jamf Pro configuration
- Contact Jamf support if you need higher limits

## Next Steps

With API access configured, you're ready to:

1. [Install JamfMCP](installation) if you haven't already
2. [Configure your MCP client](configuration-overview) with the credentials
3. Start using JamfMCP tools to analyze your Jamf Pro environment

:::{seealso}
- [Jamf Pro API Documentation](https://developer.jamf.com/jamf-pro/docs)
- [Client Credentials Guide](https://developer.jamf.com/jamf-pro/docs/client-credentials)
- [API Roles and Clients](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/API_Roles_and_Clients.html)
:::
