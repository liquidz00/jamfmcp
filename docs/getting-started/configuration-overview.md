# Configuration Overview

JamfMCP runs as an MCP server that your AI assistant connects to. This guide covers the different ways to configure JamfMCP for various clients.

:::::{tip}
**New to JamfMCP?** Use the automated CLI setup tool - it's the fastest way to get started!

```bash
pip install jamfmcp
jamfmcp setup -p <platform>
```
:::::

## {fas}`rocket` Quick Setup (Recommended)

The JamfMCP CLI tool automates the entire configuration process:

```bash
# For Claude Desktop
jamfmcp setup -p claude-desktop

# For Cursor
jamfmcp setup -p cursor

# For other platforms
jamfmcp setup -p <platform>
```

The CLI handles:
- ✅ Prerequisite verification
- 🔑 Credential collection
- 🌐 Connection validation
- ⚙️ Automatic configuration
- 📝 Platform-specific instructions

[Learn more about CLI setup →](cli-setup)

## {fas}`desktop` Supported Clients

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`desktop` Claude Desktop
:link: claude-desktop
:link-type: doc
:class-header: bg-light

Configure JamfMCP with Claude Desktop for AI-powered Jamf Pro management
::::

::::{grid-item-card} {fas}`code` Cursor
:link: cursor
:link-type: doc
:class-header: bg-light

Set up JamfMCP in Cursor IDE for code-integrated Jamf queries
::::

::::{grid-item-card} {fas}`terminal` Gemini CLI
:link: https://github.com/google-gemini/gemini-cli
:link-type: url
:class-header: bg-light

Use JamfMCP with Cline VS Code extension
::::

::::{grid-item-card} {fas}`network-wired` Other MCP Clients
:link: cli-setup
:link-type: doc
:class-header: bg-light

Generate configuration for any MCP-compatible client
::::
:::::

## {fas}`cog` Manual Configuration (Advanced)

All MCP clients follow a similar pattern:

1. **Specify the command** to run JamfMCP
2. **Set environment variables** for authentication
3. **Restart the client** to load configuration

### Basic Structure

:::::{tab-set}
::::{tab-item} PyPI Installation
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
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "your-client-id",
        "JAMF_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```
::::
::::{tab-item} Local Development
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
        "JAMF_URL": "https://your-instance.jamfcloud.com",
        "JAMF_AUTH_TYPE": "basic",
        "JAMF_USERNAME": "your-username",
        "JAMF_PASSWORD": "your-password"
      }
    }
  }
}
```
::::

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `JAMF_URL` | Jamf Pro server URL (include https://) | Yes | - |
| `JAMF_AUTH_TYPE` | `basic` or `client_credentials` | No | `basic` |
| `JAMF_USERNAME` | Username for basic auth | If basic | - |
| `JAMF_PASSWORD` | Password for basic auth | If basic | - |
| `JAMF_CLIENT_ID` | OAuth client ID | If OAuth | - |
| `JAMF_CLIENT_SECRET` | OAuth client secret | If OAuth | - |

### Configuration File Locations

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Cursor
**Location:** `~/.cursor/mcp.json`

Project-specific: `.cursor/mcp.json` in workspace
::::

::::{grid-item-card} Claude Desktop
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:** `~/.config/Claude/claude_desktop_config.json`
::::
:::::
:::::

## {fas}`key` Authentication Methods

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`user` Basic Authentication
:class-header: bg-warning

**For testing and development:**
```json
"env": {
  "JAMF_URL": "https://your.jamfcloud.com",
  "JAMF_AUTH_TYPE": "basic",
  "JAMF_USERNAME": "api-user",
  "JAMF_PASSWORD": "secure-password"
}
```
::::

::::{grid-item-card} {fas}`shield-alt` OAuth Client Credentials
:class-header: bg-success

**Recommended for production:**
```json
"env": {
  "JAMF_URL": "https://your.jamfcloud.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "abc123def456",
  "JAMF_CLIENT_SECRET": "your-secret-key"
}
```
::::
:::::

:::::{seealso}
For detailed API setup instructions, see the [Jamf API Setup Guide](jamf-api-setup).
:::::

## {fas}`shield` Security Best Practices

:::::{warning}
**Important Security Considerations**

1. {fas}`ban` **Never commit** configuration files to version control
2. {fas}`key` **Use OAuth** for production environments
3. {fas}`eye` **Create read-only** API accounts - JamfMCP doesn't need write access
4. {fas}`lock` **Rotate credentials** regularly
5. {fas}`user-shield` **Limit API permissions** to minimum required
:::::

## {fas}`exclamation-triangle` Common Configuration Issues

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`times-circle` Invalid JSON Syntax
**Symptoms:** MCP client fails to start

**Fix:** Validate JSON syntax - remove trailing commas, check quotes
::::

::::{grid-item-card} {fas}`lock` Authentication Failures
**Symptoms:** 401/403 errors

**Fix:** Verify credentials and API permissions
::::

::::{grid-item-card} {fas}`globe` Wrong URL Format
**Symptoms:** Connection refused

**Fix:** Include https:// and remove trailing slashes
::::
:::::

## {fas}`arrow-right` Next Steps

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fas}`terminal` Use CLI Setup
:link: cli-setup
:link-type: doc

Automated configuration for all platforms
::::

::::{grid-item-card} {fas}`desktop` Platform Guides
Choose your client:
- [Claude Desktop](claude-desktop)
- [Cursor](cursor)
::::

::::{grid-item-card} {fas}`play-circle` Test Your Setup
:link: quickstart
:link-type: doc

Verify everything works with examples
::::
:::::

:::::{seealso}
- [Authentication Guide](authentication) - Detailed auth setup
- [Environment Variables](environment) - Complete variable reference
- [Troubleshooting](../troubleshooting/configuration) - Solve configuration issues
:::::
