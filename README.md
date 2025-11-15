# JamfMCP

![](https://img.shields.io/badge/Python-3.13+-3776AB.svg?style=flat&logo=python&logoColor=white)&nbsp;![](https://img.shields.io/github/v/release/liquidz00/jamfmcp?color=orange)&nbsp;![](https://github.com/liquidz00/jamfmcp/actions/workflows/run-tests.yml/badge.svg)&nbsp;![](https://img.shields.io/pypi/v/jamfmcp?color=yellow)&nbsp;![](https://img.shields.io/badge/macOS-10.13%2B-blueviolet?logo=apple&logoSize=auto)

An async MCP (Model Context Protocol) server for Jamf Pro integration, providing AI assistants with tools for computer health analysis, inventory management, and policy monitoring.

> [!IMPORTANT]
>
> This project is currently in active development and should be considered **alpha-quality software**.
> The API, features, and functionality are subject to change without notice. Users should expect:
>
> - Breaking changes between versions
> - Incomplete features and documentation
> - Potential bugs and unexpected behavior
> - API endpoints and tool signatures may change
>
> **Use in production environments at your own risk.** Contributions and feedback are welcome!

## Features

- **Computer Health Analysis**: Generate comprehensive health scorecards with security compliance, CVE analysis, and system diagnostics
- **Inventory Management**: Search and retrieve detailed computer inventory information
- **Policy & Configuration**: Access policies, configuration profiles, scripts, and packages
- **Security Intelligence**: Integrate with macadmins SOFA feed for macOS security vulnerability tracking
- **Organizational Data**: Query buildings, departments, sites, network segments, and more
- **Async Architecture**: Built with modern async Python for high performance

## Installation

```bash
pip install jamfmcp
```

## Quick Setup

Use the JamfMCP CLI tool for automated setup:

```bash
# For Claude Desktop
jamfmcp-cli -p claude-desktop

# For Cursor
jamfmcp-cli -p cursor

# For other platforms
jamfmcp-cli -p <platform>
```

The CLI will guide you through the entire configuration process.

## Documentation

For detailed installation, configuration, and usage instructions, please visit the **[full documentation](https://jamfmcp.readthedocs.io/en/latest)**.

### Key Documentation Sections:

- **[Getting Started](https://jamfmcp.readthedocs.io/en/latest/user-guide/prereqs.html)** - Installation and prerequisites
- **[CLI Setup Guide](https://jamfmcp.readthedocs.io/en/latest/user-guide/cli-setup.html)** - Automatically sets up JamfMCP with Claude or Cursor
- **[Manual Configuration](https://jamfmcp.readthedocs.io/en/latest/user-guide/manual-configuration.html)** - Manually configuring JamfMCP with your preferred AI Platform
- **[Troubleshooting](https://jamfmcp.readthedocs.io/en/latest/user-guide/troubleshooting)** - Common issues and solutions

### Important Notes for Claude Desktop Users

Claude Desktop requires `uv` to be installed via Homebrew on macOS. See the [prerequisites documentation](https://jamfmcp.readthedocs.io/en/latest/user-guide/prereqs.html) for critical setup requirements.

## Basic Usage

Once configured, you can ask your AI assistant questions like:

- "Generate a health scorecard for computer with serial ABC123"
- "Find all computers that haven't checked in for 30 days"
- "What CVEs affect computers running macOS 14.5?"
- "List all configuration profiles and their scope"

## Development

For contributors and developers:

```bash
# Clone and install for development
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp
make install-dev

# Run tests
make test

# For local development setup
jamfmcp-cli -p <platform> --dev
```

See the [development documentation](https://jamfmcp.readthedocs.io/en/latest/contributing/contributor-guide.html) for detailed contribution guidelines.

## Support

- **Documentation**: [Project Docs](https://jamfmcp.readthedocs.io/en/latest)
- **Issues**: [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues)
- **Discussions**: [MacAdmins Slack #jamfmcp](https://macadmins.slack.com/archives/C07EH1R7LB0)

## Contributing

Contributions are welcome! Please see our [contributing guide](https://jamfmcp.readthedocs.io/en/latest/development/contributing/index.html) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Security intelligence from [macadmins SOFA](https://sofa.macadmins.io/)
- Jamf Pro API documentation: [developer.jamf.com](https://developer.jamf.com/)
