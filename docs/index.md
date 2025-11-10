# JamfMCP Documentation

::::{grid} 2
:gutter: 3

:::{grid-item-card} 🚀 Getting Started
:link: getting-started/index
:link-type: doc

New to JamfMCP? Start here with installation and setup guides.
:::

:::{grid-item-card} 🔧 MCP Tools Reference
:link: getting-started/tools-overview
:link-type: doc

Explore all 49 available MCP tools for Jamf Pro integration.
:::

:::{grid-item-card} ⚙️ Configuration
:link: getting-started/configuration-overview
:link-type: doc

Configure JamfMCP for Cursor, Claude Desktop, and other MCP clients.
:::

:::{grid-item-card} 📚 API Reference
:link: api-reference/index
:link-type: doc

Detailed API documentation with autodoc-generated references.
:::

:::{grid-item-card} 🛠️ Development
:link: development/index
:link-type: doc

Architecture, contributing guidelines, and development resources.
:::

:::{grid-item-card} 🔍 Troubleshooting
:link: troubleshooting/index
:link-type: doc

Solutions for common issues and debugging tips.
:::
::::

## What is JamfMCP?

JamfMCP is an async MCP server built with [FastMCP](https://gofastmcp.com) that provides AI assistants
with tools to interact with [Jamf Pro APIs](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview).

:::{warning}
**Early Release Software**: JamfMCP is in active development with evolving features and APIs. While core functionality has been tested in production environments, some features may have limited testing. We welcome feedback and contributions from the macadmin community to help improve reliability and coverage.

**What this means:**
- Core computer health analysis and inventory tools are stable
- Some advanced features may have edge cases
- API interfaces may change between minor versions
- Please report issues or unexpected behavior via [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues)
:::

## Key Features

- **🏥 Computer Health Analysis**: Generate comprehensive health scorecards with security compliance, CVE analysis, and system diagnostics
- **📦 Inventory Management**: Search and retrieve detailed computer inventory information
- **📋 Policy & Configuration**: Access policies, configuration profiles, scripts, and packages
- **🔒 Security Intelligence**: Integrate with [macadmins SOFA feed](https://sofa.macadmins.io/) for macOS security vulnerability tracking
- **🏢 Organizational Data**: Query buildings, departments, sites, network segments, and more
- **⚡ Async Architecture**: Built with modern async Python for high performance
- **🔐 Flexible Authentication**: Support for both basic auth and OAuth client credentials

## Quick Links

- [Installation Guide](getting-started/installation)
- [Jamf API Setup](getting-started/jamf-api-setup)
- [Tool Categories](getting-started/tools-overview)
- [GitHub Repository](https://github.com/liquidz00/jamfmcp)
- [FastMCP Documentation](https://gofastmcp.com)
- [Jamf Developer Portal](https://developer.jamf.com)

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Access to a Jamf Pro server with API credentials
- MCP-compatible client (Cursor, Claude Desktop)

## Getting Help

- {fab}`slack` [MacAdmins Slack](https://macadmins.slack.com/archives/C09RR0UGF0W) - Join the `#jamfmcp` channel
- {fab}`github` [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues) - Report bugs or request features
- 📖 [Jamf Nation](https://community.jamf.com) - Jamf Pro community resources

## License

JamfMCP is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/liquidz00/jamfmcp/blob/main/LICENSE) file for details.

---

Built with 💙 for the MacAdmins community

```{toctree}
:hidden:
:maxdepth: 2
:caption: Documentation

getting-started/index
api-reference/index
development/index
troubleshooting/index
```
