---
layout: landing
---

# JamfMCP Documentation

:::{rst-class} lead
A [FastMCP](https://gofastmcp.com) server providing AI assistants with tools to interact with [Jamf Pro APIs](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview)
:::

:::{container} buttons
[Docs](user-guide/index.md)
[GitHub](https://github.com/liquidz00/jamfmcp)
:::

:::{important}
**Early Release Software**: JamfMCP is in active development with evolving features and APIs. While core functionality has been tested in production environments, some features may have limited testing. We welcome feedback and contributions from the macadmin community to help improve reliability and coverage.

**What this means:**
- Core computer health analysis and inventory tools are stable
- Some advanced features may have edge cases
- API interfaces may change between minor versions
- Please report issues or unexpected behavior via [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues/new)
:::

## Key Features

- **🏥 Computer Health Analysis**: Generate comprehensive health scorecards with security compliance, CVE analysis, and system diagnostics
- **📦 Inventory Management**: Search and retrieve detailed computer inventory information
- **📋 Policy & Configuration**: Access policies, configuration profiles, scripts, and packages
- **🔒 Security Intelligence**: Integrate with [macadmins SOFA feed](https://sofa.macadmins.io/) for macOS security vulnerability tracking
- **🏢 Organizational Data**: Query buildings, departments, sites, network segments, and more
- **⚡ Async Architecture**: Built with modern async Python for high performance

## Quick Links

- [Installation Guide](user-guide/install)
- [Jamf API Setup](user-guide/jamf-api-setup)
- [Tool Categories](user-guide/mcp-tools-reference)
- [GitHub Repository](https://github.com/liquidz00/jamfmcp)
- [FastMCP Documentation](https://gofastmcp.com)
- [Jamf Developer Portal](https://developer.jamf.com)

## Requirements

- {iconify}`material-icon-theme:python` Python 3.13+
- {iconify}`material-icon-theme:uv` [uv](https://github.com/astral-sh/uv) package manager
- {iconify}`mdi:server` Access to a Jamf Pro server with API credentials
- {iconify}`material-icon-theme:claude` MCP-compatible client (Cursor, Claude Desktop)

## Getting Help

- {iconify}`devicon:slack` [MacAdmins Slack](https://macadmins.slack.com/archives/C09RR0UGF0W) - Join the `#jamfmcp` channel
- {iconify}`mdi:github` [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues) - Report bugs or request features
- 📖 [Jamf Nation](https://community.jamf.com) - Jamf Pro community resources

## License

JamfMCP is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/liquidz00/jamfmcp/blob/main/LICENSE) file for details.

---

Built with 💙 for the MacAdmins community

```{toctree}
:caption: 🚀 Getting Started
:hidden:

user-guide/prereqs
user-guide/install
user-guide/jamf-api-setup
```

```{toctree}
:caption: ⚙️ Configuration
:hidden:

user-guide/cli-setup
user-guide/manual-configuration
user-guide/jamf-deployment
```

```{toctree}
:caption: 🔧 MCP Tools
:hidden:

user-guide/mcp-tools-reference
```

```{toctree}
:caption: ⛑️ Support
:hidden:

user-guide/troubleshooting
user-guide/support
```

```{toctree}
:caption: 🤝 Contributing
:hidden:

contributing/contributor-guide
contributing/development-guide
contributing/security-considerations
contributing/fastmcp-logging
contributing/testing
```

```{toctree}
:caption: 📖 API Reference
:hidden:

api-reference/health-analyzer
api-reference/sofa-integration
api-reference/server
api-reference/cli
```
