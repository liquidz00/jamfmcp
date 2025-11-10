# JamfMCP

![](https://img.shields.io/badge/Python-3.13+-3776AB.svg?style=flat&logo=python&logoColor=white)&nbsp;![](https://img.shields.io/github/v/release/liquidz00/jamfmcp?color=orange)&nbsp;![](https://github.com/liquidz00/jamfmcp/actions/workflows/run-tests.yml/badge.svg)&nbsp;![](https://img.shields.io/pypi/v/jamfmcp?color=yellow)&nbsp;![](https://img.shields.io/badge/macOS-10.13%2B-blueviolet?logo=apple&logoSize=auto)

> ⚠️ **Important** ⚠️
>
> This project is currently in active development and should be considered **alpha-quality software**.
> The API, features, and functionality are subject to change without notice. Users should expect:
> - Breaking changes between versions
> - Incomplete features and documentation
> - Potential bugs and unexpected behavior
> - API endpoints and tool signatures may change
>
> **Use in production environments at your own risk.** Contributions and feedback are welcome!

An async MCP (Model Context Protocol) server for Jamf Pro integration, providing AI assistants with tools for computer health analysis, inventory management, and policy monitoring.

## Features

- **Computer Health Analysis**: Generate comprehensive health scorecards with security compliance, CVE analysis, and system diagnostics
- **Inventory Management**: Search and retrieve detailed computer inventory information
- **Policy & Configuration**: Access policies, configuration profiles, scripts, and packages
- **Security Intelligence**: Integrate with macadmins SOFA feed for macOS security vulnerability tracking
- **Organizational Data**: Query buildings, departments, sites, network segments, and more
- **Async Architecture**: Built with modern async Python for high performance
- **Flexible Authentication**: Support for both basic auth and OAuth client credentials

## Installation

```bash
pip install jamfmcp
```

## Quick Setup

Use the JamfMCP CLI tool for automated setup:

```bash
# For Claude Desktop
jamfmcp setup -p claude-desktop

# For Cursor
jamfmcp setup -p cursor

# For other platforms
jamfmcp setup -p <platform>
```

The CLI will guide you through the entire configuration process.

## Documentation

For detailed installation, configuration, and usage instructions, please visit the **[full documentation](https://jamfmcp.readthedocs.io/en/latest)**.

### Key Documentation Sections:

- **[Getting Started](https://jamfmcp.readthedocs.io/en/latest/getting-started/)** - Installation and prerequisites
- **[CLI Setup Guide](https://jamfmcp.readthedocs.io/en/latest/getting-started/cli-setup.html)** - Automated configuration tool
- **[Quickstart Guide](https://jamfmcp.readthedocs.io/en/latest/getting-started/quickstart.html)** - Example queries and workflows
- **[Configuration](https://jamfmcp.readthedocs.io/en/latest/getting-started/configuration-overview.html)** - Platform-specific setup
- **[Troubleshooting](https://jamfmcp.readthedocs.io/en/latest/troubleshooting/)** - Common issues and solutions

### Important Notes for Claude Desktop Users

Claude Desktop requires `uv` to be installed via Homebrew on macOS. See the [prerequisites documentation](https://jamfmcp.readthedocs.io/en/latest/getting-started/prerequisites.html) for critical setup requirements.

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
jamfmcp setup -p <platform> --local
```

See the [development documentation](https://jamfmcp.readthedocs.io/en/latest/development/) for detailed contribution guidelines.

## Support

- **Documentation**: [Project Docs](https://jamfmcp.readthedocs.io/en/latest)
- **Issues**: [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues)
- **Discussions**: [MacAdmins Slack #jamfmcp](https://macadmins.slack.com/archives/C07EH1R7LB0)

## Contributing

Contributions are welcome! Please see our [contributing guide](https://jamfmcp.readthedocs.io/en/latest/development/contributing.html) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Security intelligence from [macadmins SOFA](https://sofa.macadmins.io/)
- Jamf Pro API documentation: [developer.jamf.com](https://developer.jamf.com/)
