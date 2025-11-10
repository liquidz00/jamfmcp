# Installation

This guide walks you through installing JamfMCP and setting it up with your MCP client using the automated CLI tool.

:::::{important}
**Before you begin**: Ensure you have completed the [prerequisites](prerequisites), especially the critical `uv` installation requirements for Claude Desktop users.
:::::

## {fas}`box-open` Install JamfMCP

:::::{tab-set}
::::{tab-item} PyPI (uv)
:sync: uv

**Recommended method using uv:**

```bash
# Install JamfMCP from PyPI
uv pip install jamfmcp

# Verify installation
jamfmcp --version
```

:::{tip}
Using `uv` is faster and more reliable than traditional pip. It handles dependencies better and provides cleaner virtual environments.
:::
::::

::::{tab-item} PyPI (pip)
:sync: pip

**Traditional pip installation:**

```bash
# Install JamfMCP from PyPI
pip install jamfmcp

# Verify installation
jamfmcp --version
```

:::{note}
If you encounter dependency conflicts, consider using `uv` instead or creating a fresh virtual environment.
:::
::::

::::{tab-item} From Source
:sync: source

**For development or testing latest features:**

```bash
# Clone the repository
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp

# Install in development mode
make install-dev

# For CLI setup, use the --local flag
jamfmcp setup -p claude-desktop --local
```

:::{important}
When installing from source, always use the `--local` flag with the CLI to ensure proper path resolution.
:::
::::
:::::

## {fas}`terminal` Quick Setup with CLI

After installation, use the JamfMCP CLI tool to automatically configure your MCP client:

```bash
# For Claude Desktop
jamfmcp setup -p claude-desktop

# For Cursor
jamfmcp setup -p cursor

# For other platforms
jamfmcp setup -p <platform>
```

The CLI will:
1. {fas}`check` Verify prerequisites (uv, fastmcp)
2. {fas}`key` Collect your Jamf Pro credentials
3. {fas}`server` Test the connection to your Jamf Pro server
4. {fas}`cog` Generate the appropriate configuration
5. {fas}`rocket` Set up your MCP client automatically

:::::{seealso}
For detailed CLI usage and options, see the [CLI Setup Guide](cli-setup).
:::::

## {fas}`check-circle` Post-Installation Steps

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`wrench` Verify Installation
Run `jamfmcp --version` to confirm the CLI is installed correctly
::::

::::{grid-item-card} {fas}`key` Prepare Credentials
Have your Jamf Pro URL and API credentials ready for setup
::::

::::{grid-item-card} {fas}`terminal` Run CLI Setup
Use `jamfmcp setup -p <platform>` for automated configuration
::::

::::{grid-item-card} {fas}`play` Test Connection
The CLI will verify your Jamf Pro connection during setup
::::
:::::

## {fas}`cog` Manual Configuration (Advanced)

While the CLI handles configuration automatically, you can manually configure your MCP client if needed.

**Environment Variables Required:**

| Variable | Description | Required |
|----------|-------------|----------|
| `JAMF_URL` | Your Jamf Pro server URL | Yes |
| `JAMF_AUTH_TYPE` | `basic` or `client_credentials` | No (default: `basic`) |
| `JAMF_USERNAME` | Username for basic auth | If using basic auth |
| `JAMF_PASSWORD` | Password for basic auth | If using basic auth |
| `JAMF_CLIENT_ID` | OAuth client ID | If using OAuth |
| `JAMF_CLIENT_SECRET` | OAuth client secret | If using OAuth |

**Example MCP Configuration:**
```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "jamfmcp",
        "jamfmcp"
      ],
      "env": {
        "JAMF_URL": "https://your-instance.jamfcloud.com",
        "JAMF_CLIENT_ID": "your_client_id",
        "JAMF_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

:::{warning}
Never set these environment variables in your shell or commit them to version control.
:::

## {fas}`sync` Updating JamfMCP

:::::{tab-set}
::::{tab-item} PyPI Installation
:sync: pypi-update

```bash
# Update using uv
uv pip install --upgrade jamfmcp

# Or using pip
pip install --upgrade jamfmcp
```
::::

::::{tab-item} Source Installation
:sync: source-update

```bash
cd /path/to/jamfmcp
git pull
make install  # or make install-dev
```
::::
:::::

## {fas}`trash` Uninstalling

To remove JamfMCP:

```bash
# If installed via pip/uv
pip uninstall jamfmcp

# If installed from source
cd /path/to/jamfmcp
make uninstall
```

Then remove the JamfMCP configuration from your MCP client.

## {fas}`exclamation-triangle` Troubleshooting

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`bug` Common Issues
:link: ../troubleshooting/installation
:link-type: doc

- "spawn uv ENOENT" errors
- Permission denied during install
- Python version mismatches
- Dependency conflicts
::::
:::::

## {fas}`rocket` Next Steps

With JamfMCP installed:

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fas}`terminal` Use CLI Setup
:link: cli-setup
:link-type: doc

Run `jamfmcp setup` to configure your MCP client automatically
::::

::::{grid-item-card} {fas}`key` Configure API Access
:link: jamf-api-setup
:link-type: doc

Set up Jamf Pro API credentials if not already done
::::

::::{grid-item-card} {fas}`play-circle` Try Examples
:link: quickstart
:link-type: doc

Test your setup with example queries and commands
::::
:::::

:::::{seealso}
- [CLI Setup Guide](cli-setup) - Detailed CLI usage and options
- [FastMCP Documentation](https://gofastmcp.com) - Underlying MCP framework
- [MCP Protocol Overview](https://modelcontextprotocol.io) - Protocol specification
:::::
