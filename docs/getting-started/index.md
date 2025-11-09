# Getting Started

Welcome to JamfMCP! This guide will help you get up and running with the Jamf Pro MCP server.

## Overview

JamfMCP enables AI assistants like Cursor and Claude Desktop to interact with your Jamf Pro environment through the Model Context Protocol (MCP). This allows you to:

- Analyze computer health and security compliance
- Query inventory and organizational data
- Review policies, profiles, and configurations
- Track CVE vulnerabilities with SOFA integration
- Generate comprehensive reports and recommendations

## Quick Start Path

::::{grid} 1
:gutter: 2

:::{grid-item}
**1. Check Prerequisites** → [Prerequisites Guide](prerequisites)

Ensure you have Python 3.13+, `uv`, and Jamf Pro API access
:::

:::{grid-item}
**2. Install JamfMCP** → [Installation Guide](installation)

Clone the repository and install dependencies
:::

:::{grid-item}
**3. Configure Jamf API** → [Jamf API Setup](jamf-api-setup)

Set up API credentials with least-privilege access
:::

:::{grid-item}
**4. Configure MCP Client** → [Configuration Guides](configuration-overview)

Connect your AI assistant to JamfMCP
:::

:::{grid-item}
**5. Start Using Tools** → [Quickstart Examples](quickstart)

Try your first commands and explore capabilities
:::
::::

## What You'll Need

- **15 minutes** for basic setup
- **Admin access** to create Jamf Pro API credentials
- **Python 3.13+** installed on your system
- **An MCP client** (Cursor, Claude Desktop, etc.)

## Architecture Overview

JamfMCP acts as a bridge between AI assistants and your Jamf Pro infrastructure:

- **AI Assistant (Cursor/Claude)** ← MCP Protocol → **JamfMCP Server**
- **JamfMCP Server** ← HTTPS API → **Jamf Pro Server**
- **JamfMCP Server** ← HTTPS → **SOFA Feed (CVE Data)**

This architecture enables AI assistants to securely interact with your Jamf Pro environment while incorporating security vulnerability data from the SOFA feed.

## Support Resources

:::{admonition} Getting Help
:class: tip

- **Documentation**: You're here! Browse the guides for detailed information
- **Slack**: Join [#jamfmcp on MacAdmins Slack](https://macadmins.slack.com/archives/C09RR0UGF0W)
- **GitHub**: Report issues or contribute at [github.com/liquidz00/jamfmcp](https://github.com/liquidz00/jamfmcp)
:::

## Next Steps

Ready to get started? Head to the [Prerequisites](prerequisites) page to ensure your environment is ready for JamfMCP.

```{toctree}
:caption: Getting Started
:maxdepth: 3
:hidden:

prerequisites
installation
jamf-api-setup
quickstart
```

```{toctree}
:caption: Configuration
:maxdepth: 3
:hidden:

configuration-overview
authentication
claude-desktop
cursor
environment
```

```{toctree}
:caption: MCP Tools
:maxdepth: 3
:hidden:

tools-overview
computer-health
inventory
organization
policies
security
utility
```
