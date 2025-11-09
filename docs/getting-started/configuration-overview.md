# Configuration

JamfMCP runs as an MCP server that your AI assistant connects to. This section covers how to configure various MCP clients to work with JamfMCP.

## Supported Clients

::::{grid} 2
:gutter: 3

:::{grid-item-card} Cursor
:link: cursor
:link-type: doc

Configure JamfMCP for use with Cursor IDE
:::

:::{grid-item-card} Claude Desktop  
:link: claude-desktop
:link-type: doc

Set up JamfMCP with Claude Desktop (Chat/Code)
:::
::::

## Configuration Overview

All MCP clients use a similar configuration pattern:

1. **Specify the command** to run JamfMCP
2. **Set environment variables** for Jamf Pro authentication
3. **Restart the client** to load the configuration

### Basic Configuration Structure

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/jamfmcp",
        "fastmcp",
        "run",
        "src/jamfmcp/server.py:mcp"
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

## Environment Variables

Configure these in your MCP client's `env` section:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `JAMF_URL` | Jamf Pro server URL (FQDN or full URL) | Yes | - |
| `JAMF_AUTH_TYPE` | Authentication type: `basic` or `client_credentials` | No | `basic` |
| `JAMF_USERNAME` | Username for basic authentication | If using basic auth | - |
| `JAMF_PASSWORD` | Password for basic authentication | If using basic auth | - |
| `JAMF_CLIENT_ID` | OAuth client ID | If using OAuth | - |
| `JAMF_CLIENT_SECRET` | OAuth client secret | If using OAuth | - |

## Authentication Methods

### Basic Authentication

Simple username/password authentication:

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "basic",
  "JAMF_USERNAME": "api-user",
  "JAMF_PASSWORD": "secure-password"
}
```

### OAuth Client Credentials

More secure OAuth-based authentication:

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "your-client-id",
  "JAMF_CLIENT_SECRET": "your-client-secret"
}
```

:::{tip}
Both authentication methods are supported. See the [Jamf API Setup Guide](jamf-api-setup) for detailed setup instructions.
:::

## Configuration File Locations

MCP configuration files are stored in different locations depending on your client and operating system:

### Cursor
- **macOS/Linux**: `~/.cursor/mcp.json`

### Claude Desktop
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Troubleshooting

For help with configuration issues, see the [Configuration Troubleshooting Guide](../troubleshooting/configuration).

## Security Considerations

:::{warning}
**Important Security Notes**

1. **Never commit** configuration files to version control
2. **Choose authentication** method based on your security requirements
3. **Use read-only** API accounts
:::

## Next Steps

Choose your MCP client to continue:
- [Configure Cursor](cursor)
- [Configure Claude Desktop](claude-desktop)

After configuration, try the [Quickstart Guide](quickstart) to verify everything is working.
