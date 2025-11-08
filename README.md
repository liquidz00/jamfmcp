# JamfMCP

> **� ACTIVE DEVELOPMENT - ALPHA SOFTWARE**
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

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Access to a Jamf Pro server with API credentials

### Via PyPI (Coming Soon)

JamfMCP will be available on PyPI for easy installation:

```bash
pip install jamfmcp
```

> **Note**: PyPI distribution is planned but not yet available. For now, please use the installation from source method below.

### From Source (Current Method)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jamfmcp.git
cd jamfmcp
```

2. Install dependencies:
```bash
make install
```

## Configuration

JamfMCP is configured through AI tool's MCP configuration file. **Do not export environment variables** - instead, add them to the appropriate configuration file for your tool.

### Cursor

Add the following to your `~/.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/jamfmcp",
        "run",
        "fastmcp",
        "run",
        "jamfmcp.server:mcp"
      ],
      "env": {
        "JAMF_URL": "your-jamf-server.com",
        "JAMF_AUTH_TYPE": "basic",
        "JAMF_USERNAME": "your-username",
        "JAMF_PASSWORD": "your-password"
      }
    }
  }
}
```

### Claude Desktop (Chat/Code)

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/jamfmcp",
        "run",
        "fastmcp",
        "run",
        "jamfmcp.server:mcp"
      ],
      "env": {
        "JAMF_URL": "your-jamf-server.com",
        "JAMF_AUTH_TYPE": "basic",
        "JAMF_USERNAME": "your-username",
        "JAMF_PASSWORD": "your-password"
      }
    }
  }
}
```

### ChatGPT Desktop

ChatGPT Desktop's MCP configuration method is currently undocumented. Check OpenAI's official documentation for the latest MCP integration details.

### OAuth Client Credentials

If using OAuth instead of basic authentication, replace the `env` section with:

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "your-client-id",
  "JAMF_CLIENT_SECRET": "your-client-secret"
}
```

### Configuration Notes

- Replace `/path/to/jamfmcp` with the absolute path to your cloned repository
- Replace `your-jamf-server.com` with your actual Jamf Pro server URL (FQDN or full URL)
- Replace authentication credentials with your actual Jamf Pro credentials
- After updating the configuration, restart your AI tool to load the MCP server

> **Note**: Once JamfMCP is available on PyPI, the configuration will be simplified. You'll be able to use `uvx --from jamfmcp fastmcp run jamfmcp.server:mcp` or install it globally and use `fastmcp run jamfmcp.server:mcp` directly.

## Usage

### Available Tools

The MCP server exposes the following tools:

- `get_computer_inventory` - Retrieve detailed computer inventory by serial number
- `get_computer_history` - Get policy logs and management history
- `search_computers` - Search for computers by name or serial
- `get_health_scorecard` - Generate comprehensive health analysis with grades and recommendations
- `get_basic_diagnostics` - Get basic diagnostic information
- `get_cves` - Analyze CVE vulnerabilities for a computer
- `get_policies`, `get_policy_details` - Policy management
- `get_configuration_profiles`, `get_profile_details` - Configuration profile access
- `get_scripts`, `get_script_details` - Script management
- `get_packages`, `get_package_details` - Package information
- Many more for users, groups, buildings, departments, network segments, etc.

## Development

For contributors and developers working on JamfMCP:

### Setup for Development

1. Clone the repository and install with dev dependencies:
```bash
git clone https://github.com/yourusername/jamfmcp.git
cd jamfmcp
make install-dev  # Installs testing, linting, and documentation tools
```

2. Set environment variables for local testing:
```bash
export JAMF_URL="your-jamf-server.com"
export JAMF_AUTH_TYPE="basic"
export JAMF_USERNAME="your-username"
export JAMF_PASSWORD="your-password"
```

Or create a `.env` file in the project root (not tracked in git).

### Run Tests

```bash
make test              # Run all tests
make test-cov          # Run with coverage report
make test-cov-html     # Generate HTML coverage report
```

### Code Quality

```bash
make lint              # Check code style
make format            # Auto-format code
make pre-commit-run    # Run pre-commit hooks
```

### Building

```bash
make build             # Build distribution packages
```

### Running Locally (Development)

To run the MCP server directly for testing:

```bash
uv run fastmcp run jamfmcp.server:mcp
```

Or for development with auto-reload:

```bash
uv run fastmcp dev jamfmcp.server:mcp
```

## Architecture

- **FastMCP**: Framework for building MCP servers
- **httpx**: Async HTTP client for Jamf Pro API calls
- **Pydantic**: Data validation and serialization
- **Jamf SDK**: Embedded SDK with models for Pro and Classic APIs

## Configuration Reference

The following environment variables should be set in your AI tool's `mcp.json` configuration file (see [Configuration](#configuration) section above):

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `JAMF_URL` | Jamf Pro server URL (FQDN or full URL) | Yes | - |
| `JAMF_AUTH_TYPE` | Authentication type: `basic` or `client_credentials` | No | `basic` |
| `JAMF_USERNAME` | Username for basic authentication | If using basic auth | - |
| `JAMF_PASSWORD` | Password for basic authentication | If using basic auth | - |
| `JAMF_CLIENT_ID` | OAuth client ID | If using OAuth | - |
| `JAMF_CLIENT_SECRET` | OAuth client secret | If using OAuth | - |

## Contributing

Contributions are welcome! Please ensure:
- All tests pass: `make test`
- Code is formatted: `make format`
- Pre-commit hooks pass: `make pre-commit-run`
- New features include tests and Sphinx-style docstrings

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Security intelligence from [macadmins SOFA](https://sofa.macadmins.io/)
- Jamf Pro API documentation: [developer.jamf.com](https://developer.jamf.com/)
