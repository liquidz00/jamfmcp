# Manual Configuration

This guide covers the different ways to manually configure JamfMCP for various clients.

## MCP Configuration Pattern

All MCP clients follow a similar pattern:

1. **Specify the command** to run JamfMCP
2. **Set environment variables** for authentication
3. **Restart the client** to load configuration

```json
{
  "<server-name>": {
    "command": "<executable>",
    "args": ["<arg1>", "<arg2>", "..."],
    "env": {
      "<ENV_VAR>": "<value>"
    }
  }
}
```

### FastMCP CLI Usage

:::{important}
The FastMCP CLI assumes that you're building a server from scratch _OR_ you've installed the server **from source**. It is not recommended to use if you've installed JamfMCP via `uv` or `pip`
:::

The FastMCP CLI tool can assist in streamlining the process of configuring the JamfMCP locally. Reference FastMCP docs for your specific AI Platform:

- [Claude Desktop](https://gofastmcp.com/integrations/claude-desktop#install-the-server)
- [Claude Code](https://gofastmcp.com/integrations/claude-code#install-the-server)
- [Cursor](https://gofastmcp.com/integrations/cursor#install-the-server)
- [Gemini CLI](https://gofastmcp.com/integrations/gemini-cli#install-the-server)

## Installation-specific Configuration

Depending how you chose to install JamfMCP, the configuration file syntax differs ever so slightly.

:::{note}
The JSON examples below are **only** of the JamfMCP configuration. Actual MCP configurations will have a top-level key `"mcpServers"` that the JamfMCP configuration would be nested under.
:::

:::::{tab-set}
::::{tab-item} `uvx`
```json
{
  "jamfmcp": {
    "command": "uvx",
    "args": ["jamfmcp"],
    "env": {
      "JAMF_URL": "https://your-instance.jamfcloud.com",
      "JAMF_CLIENT_ID": "your-client-id",
      "JAMF_CLIENT_SECRET": "your-client-secret"
    }
  }
}
```
::::

::::{tab-item} PyPI Installation (via `pip`)
```json
{
  "jamfmcp": {
    "command": "uv",
    "args": [
      "run",
      "--with", "jamfmcp",
      "jamfmcp"
    ],
    "env": {
      "JAMF_URL": "https://your-instance.jamfcloud.com",
      "JAMF_CLIENT_ID": "your-client-id",
      "JAMF_CLIENT_SECRET": "your-client-secret"
    }
  }
}
```
::::

::::{tab-item} Local Development
```json
{
  "jamfmcp": {
    "command": "uv",
    "args": [
      "run",
      "--directory", "/path/to/cloned/jamfmcp",
      "fastmcp",
      "run",
      "src/jamfmcp/server.py:main"
    ],
    "env": {
      "JAMF_URL": "https://your-instance.jamfcloud.com",
      "JAMF_CLIENT_ID": "your-client-id",
      "JAMF_CLIENT_SECRET": "your-client-secret"
    }
  }
}
```
::::
:::::

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `JAMF_URL` | Jamf Pro server URL (include https://) | Yes | - |
| `JAMF_CLIENT_ID` | OAuth client ID | Yes | - |
| `JAMF_CLIENT_SECRET` | OAuth client secret | Yes | - |

### Configuration File Locations

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Cursor
**Global Location:** `~/.cursor/mcp.json`

**Project-specific:** `.cursor/mcp.json` in workspace
::::

::::{grid-item-card} Claude
According to the [following document](https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code/), Claude Code and Claude Desktop both utilize the **same file location** for MCP server configurations:

`~/Library/Application Support/Claude/claude_desktop_config.json`

::::
:::::

:::{seealso}
- [MCP Tools Reference](mcp-tools-reference)
- [Jamf API Setup](jamf-api-setup)
- [Troubleshooting](troubleshooting)
:::
