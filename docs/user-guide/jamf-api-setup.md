(jamf_api_setup)=
# Jamf API Setup Guide

:::{rst-class} lead
This guide walks you through setting up API access for JamfMCP with the appropriate privileges following the principle of least privilege.
:::

## Authentication Methods

JamfMCP **only** suports OAuth client credentials for authentication. OAuth client credentials provide token-based authentication using the OAuth 2.0 standard.

### Create an API Role

1. Navigate to **Settings** → **System** → **API roles and clients** in Jamf Pro
2. Select the **API Roles** tab, then click **New** in the upper right hand corner to create a new API role
3. Name it something descriptive like "JamfMCP Read-Only"
4. Grant the following privileges:

:::{admonition} Required Privileges Checklist
:class: hint

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

### Create an API Client

1. Navigate to **Settings** → **System** → **API roles and clients**
2. Select the **API Clients** tab, then click **New** to create a new API client
3. Configure the client:
   - **Display Name**: "JamfMCP Client"
   - **API Role**: Select the role created in Step 1
   - **Client ID**: Auto-generated (save this!)
   - **Client Secret**: Click "Generate" (save this securely!)

:::{warning}
The client secret is only shown once! Save it immediately in a secure location.
:::

## Server URL Format

The `JAMF_URL` can be specified in several formats:

- **FQDN only**: `your-server.jamfcloud.com`
- **With protocol**: `https://your-server.jamfcloud.com`
- **With port**: `https://your-server.com:8443`
- **With path**: `https://your-server.com/jamf`

JamfMCP will automatically handle the URL formatting.

## API Rate Limits and Best Practices

Jamf Pro implements [API rate limiting](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-scalability-best-practices#rate-limiting) to protect server performance. JamfMCP respects these limits and implements automatic retry logic with exponential backoff.

**Best Practices:**
- Avoid excessive concurrent requests
- Use targeted queries rather than full inventory pulls when possible
- Consult the [Jamf Pro API documentation](https://developer.jamf.com/jamf-pro/reference) for endpoint-specific guidance

:::{danger}
JamfMCP's read-only operations are meant to be low-impact, but sustained high-volume API usage on any platform can affect server responsiveness. Although rare it is technically possible with automated or repeated large-scale queries.
:::

:::{seealso}
- [Jamf Pro API Documentation](https://developer.jamf.com/jamf-pro/docs)
- [Client Credentials Guide](https://developer.jamf.com/jamf-pro/docs/client-credentials)
- [API Roles and Clients](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/API_Roles_and_Clients.html)
:::
