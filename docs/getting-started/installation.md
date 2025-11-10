# Installation

JamfMCP is installed and run using [FastMCP](https://gofastmcp.com/getting-started/installation). This guide walks you through the installation process.

## Install from Source

:::{note}
PyPI distribution is planned but not yet available. Currently, installation from source is the only method.
:::

### Step 1: Clone the Repository

```bash
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp
```

### Step 2: Install Dependencies

JamfMCP uses [uv](https://github.com/astral-sh/uv) for dependency management. If you don't have uv installed, [install it first](https://github.com/astral-sh/uv#installation).

Using the provided Makefile:

```bash
# For basic installation (recommended for users)
make install

# For development (includes testing and documentation tools)  
make install-dev
```

This will:
1. Create a virtual environment in `.venv`
2. Install all required dependencies
3. Set up JamfMCP for use with FastMCP

### Step 3: Verify Installation

Test that JamfMCP is properly installed:

```bash
# Run the MCP server directly
uv run fastmcp run src/jamfmcp/server.py:mcp
```

You should see output indicating the server is starting. Press `Ctrl+C` to stop it.

## Configuration

JamfMCP doesn't run standalone - it needs to be configured with an MCP client. The server is started automatically by your MCP client (Cursor, Claude Desktop, etc.) when configured properly.

### Configure Your MCP Client

See the configuration guides for your specific client:

- [Cursor Setup](cursor)
- [Claude Desktop Setup](claude-desktop)

:::{note}
Guides for other model configurations are on their way. A CLI will also be available to assist in automating configurations.
:::

### Environment Variables

JamfMCP requires these environment variables, which are set in your MCP client configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| `JAMF_URL` | Your Jamf Pro server URL | Yes |
| `JAMF_AUTH_TYPE` | Authentication type: `basic` or `client_credentials` | No (default: `basic`) |
| `JAMF_USERNAME` | Username for basic auth | If using basic auth |
| `JAMF_PASSWORD` | Password for basic auth | If using basic auth |
| `JAMF_CLIENT_ID` | OAuth client ID | If using OAuth |
| `JAMF_CLIENT_SECRET` | OAuth client secret | If using OAuth |

:::{warning}
Never set these environment variables in your shell or commit them to version control. Always configure them through your MCP client's configuration file.
:::

## Installation Methods Comparison

| Method | Status | Use Case | Command |
|--------|--------|----------|---------|
| Source (Current) | ✅ Available | All users | `git clone` + `make install` |
| PyPI (Future) | 🚧 Planned | Quick install | `pip install jamfmcp` |
| uvx (Future) | 🚧 Planned | No install needed | `uvx jamfmcp` |

## Updating JamfMCP

To update to the latest version:

```bash
cd /path/to/jamfmcp
git pull
make install  # or make install-dev
```

## Uninstalling

To remove JamfMCP:

```bash
cd /path/to/jamfmcp
make uninstall  # Removes virtual environment
```

Then remove the JamfMCP configuration from your MCP client.

## Troubleshooting

For installation issues, see the [Installation Troubleshooting Guide](../troubleshooting/installation).

## Next Steps

With JamfMCP installed:

1. [Set up Jamf API access](jamf-api-setup) if you haven't already
2. [Configure your MCP client](configuration-overview) to connect to JamfMCP
3. Try the [Quickstart guide](quickstart) for your first commands

:::{seealso}
- [FastMCP Installation Guide](https://gofastmcp.com/getting-started/installation)
- [uv Documentation](https://github.com/astral-sh/uv)
- [MCP Protocol Overview](https://modelcontextprotocol.io/introduction)
:::
