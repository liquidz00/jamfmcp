# Prerequisites

Before installing JamfMCP, ensure you have the necessary requirements and access configured.

## System Requirements

- **Python 3.13 or higher** - JamfMCP requires Python 3.13+
- **[uv](https://github.com/astral-sh/uv) package manager** - Modern Python package management
- **A Jamf Pro server** - Cloud or on-premise instance
- **MCP-compatible client** - Cursor, Claude Desktop, or other MCP clients

:::{note}
JamfMCP is built on [FastMCP](https://gofastmcp.com), which handles the MCP protocol implementation.
:::

## Jamf Pro Setup

### API Access Requirements

JamfMCP requires API access to your Jamf Pro server. You can use either:

1. **Basic Authentication** (username/password)
   - Simple setup for testing
   - Not recommended for production use

2. **OAuth Client Credentials** (recommended for production)
   - More secure
   - Better access control
   - Follows Jamf Pro best practices

### Required API Privileges

When setting up API access, follow the [Jamf Pro API documentation](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview)
for authentication setup. For OAuth Client Credentials, create an API role with these **minimum** privileges:

:::{admonition} Least Privilege Principle
:class: important

Grant only the minimum required privileges for read-only operations. JamfMCP is designed to be a read-only tool that analyzes and reports on your Jamf Pro data.
:::

#### Computers
- Read Computer Inventory
- Read Computer History  
- Read Computer Groups
- Read Computer Extension Attributes
- Read Computer MDM Commands (for device lock PIN retrieval)

#### Policies & Profiles
- Read Policies
- Read Configuration Profiles
- Read Scripts
- Read Packages
- Read Patch Management

#### Organization
- Read Buildings
- Read Departments
- Read Network Segments
- Read Sites
- Read Categories

#### Users & Groups
- Read Users
- Read User Groups
- Read LDAP Servers
- Read Directory Bindings

#### Security & Compliance
- Read Restricted Software
- Read Licensed Software
- Read Advanced Computer Searches
- Read Webhooks

:::{tip}
For detailed instructions on creating API roles and client credentials, see the [Jamf API Setup Guide](jamf-api-setup).
:::

## Network Requirements

- **HTTPS access** to your Jamf Pro server
- **Outbound HTTPS** to `sofafeed.macadmins.io` for CVE data (optional but recommended)
- **No inbound connections** required - JamfMCP operates as a client

## Next Steps

Once you have confirmed all prerequisites are met:

1. [Install JamfMCP](installation) using the installation guide
2. [Configure your MCP client](configuration-overview) (Cursor, Claude Desktop, etc.)
3. [Set up Jamf API access](jamf-api-setup) with the appropriate privileges

:::{seealso}
- [Jamf Pro API Overview](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview)
- [FastMCP Installation](https://gofastmcp.com/getting-started/installation)
- [uv Installation Guide](https://github.com/astral-sh/uv#installation)
:::
