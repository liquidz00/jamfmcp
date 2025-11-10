# CLI Setup Guide

The JamfMCP CLI tool automates the entire setup process for connecting JamfMCP to your AI assistant. This guide covers all CLI features and options.

:::::{tip}
The CLI is the **recommended method** for setting up JamfMCP. It handles all the complex configuration automatically and validates your setup before applying changes.
:::::

## {fas}`terminal` CLI Overview

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`rocket` Automated Setup
Configures your MCP client with a single command
::::

::::{grid-item-card} {fas}`check-circle` Connection Validation
Tests Jamf Pro connectivity before applying configuration
::::

::::{grid-item-card} {fas}`shield-alt` Secure Credential Handling
Prompts for credentials interactively without exposing them
::::

::::{grid-item-card} {fas}`desktop` Multi-Platform Support
Works with Claude Desktop, Cursor, Cline, and more
::::
:::::

## {fas}`play-circle` Quick Start

```bash
# Basic setup for Claude Desktop
jamfmcp setup -p claude-desktop

# Setup with specific Jamf URL
jamfmcp setup -p cursor --url https://your-instance.jamfcloud.com

# Setup with OAuth authentication
jamfmcp setup -p claude-desktop --auth-type oauth
```

## {fas}`desktop` Platform-Specific Setup

:::::{tab-set}
::::{tab-item} Claude Desktop
:sync: claude-desktop

**Setup for Claude Desktop (macOS/Linux):**

```bash
jamfmcp setup -p claude-desktop
```

The CLI will:
1. Check that `uv` is installed via Homebrew (critical!)
2. Prompt for your Jamf Pro URL and credentials
3. Validate the connection
4. Update `~/Library/Application Support/Claude/claude_desktop_config.json`
5. Instruct you to restart Claude Desktop

:::{important}
Remember: Claude Desktop requires `uv` installed via Homebrew on macOS. The CLI will check this requirement.
:::

**Example Session:**
```
$ jamfmcp setup -p claude-desktop

🚀 Setting up JamfMCP for claude-desktop

Jamf Pro server URL: https://mycompany.jamfcloud.com
Username: api-user
Password: ****

Validating Jamf Pro connection...
✓ Successfully connected to Jamf Pro

✓ Successfully configured claude-desktop

📝 Next steps:
1. Restart Claude Desktop completely
2. Look for the hammer icon (🔨) in the input box
3. Your JamfMCP tools are now available!
```
::::

::::{tab-item} Cursor
:sync: cursor

**Setup for Cursor:**

```bash
# Global installation
jamfmcp setup -p cursor

# Project-specific installation
jamfmcp setup -p cursor --workspace /path/to/project
```

The CLI will:
1. Check prerequisites
2. Collect credentials
3. Validate connection
4. Generate configuration
5. Prompt to install in Cursor

**Workspace Option:**
- Use `--workspace` for project-specific MCP servers
- Omit for global Cursor configuration

**Example Session:**
```
$ jamfmcp setup -p cursor --workspace .

🚀 Setting up JamfMCP for cursor

Jamf Pro server URL: https://mycompany.jamfcloud.com
Client ID: abc123def456
Client Secret: ****

Validating Jamf Pro connection...
✓ Successfully connected to Jamf Pro

✓ Successfully configured cursor

📝 Next steps:
1. Open Cursor in workspace: .
2. JamfMCP tools should now be available
```
::::

::::{tab-item} Cline
:sync: cline

**Setup for Cline (VS Code extension):**

```bash
jamfmcp setup -p cline
```

The CLI configures Cline's MCP settings in VS Code.

**Note**: Ensure Cline extension is installed in VS Code first.
::::

::::{tab-item} Other Platforms
:sync: other

**For other MCP-compatible platforms:**

```bash
# Generate MCP JSON configuration
jamfmcp setup -p mcp-json > mcp-config.json
```

This outputs a standard MCP configuration that you can adapt for any MCP client.
::::
:::::

## {fas}`key` Authentication Options

:::::{tab-set}
::::{tab-item} Basic Auth
:sync: basic

**Username/Password Authentication (default):**

```bash
jamfmcp setup -p claude-desktop --auth-type basic
```

You'll be prompted for:
- Jamf Pro URL
- Username
- Password

:::{tip}
Use basic auth for testing and development. For production, use OAuth.
:::
::::

::::{tab-item} OAuth
:sync: oauth

**OAuth Client Credentials (recommended):**

```bash
jamfmcp setup -p claude-desktop --auth-type oauth
```

You'll be prompted for:
- Jamf Pro URL
- Client ID
- Client Secret

:::{important}
OAuth is more secure and follows Jamf Pro best practices. See [Jamf API Setup](jamf-api-setup) for creating OAuth credentials.
:::
::::
:::::

## {fas}`cog` CLI Options Reference

### setup Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--platform` | `-p` | Target platform (required) | `claude-desktop`, `cursor`, `cline` |
| `--auth-type` | `-a` | Authentication method | `basic` (default), `oauth` |
| `--url` | `-u` | Jamf Pro server URL | `https://company.jamfcloud.com` |
| `--username` | | Username for basic auth | `api-user` |
| `--password` | | Password for basic auth | Will prompt if not provided |
| `--client-id` | | OAuth client ID | `abc123` |
| `--client-secret` | | OAuth client secret | Will prompt if not provided |
| `--workspace` | `-w` | Cursor workspace directory | `/path/to/project` |
| `--server-name` | `-n` | Custom server name | `jamfmcp-prod` (default: `jamfmcp`) |
| `--skip-validation` | | Skip connection test | Not recommended |
| `--verbose` | `-v` | Show detailed output | Helpful for debugging |
| `--dry-run` | | Preview without changes | See what would be configured |
| `--local` | `-l` | Use local installation | For development from source |

### validate Command

Test your Jamf Pro connection without configuring anything:

```bash
jamfmcp validate --url https://company.jamfcloud.com
```

## {fas}`code` Local Development Setup

:::::{dropdown} {fas}`wrench` Using --local Flag for Development
:color: info

When developing or testing JamfMCP from source, use the `--local` flag:

```bash
# Clone and install from source
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp
make install-dev

# Setup with local installation
jamfmcp setup -p claude-desktop --local
```

The `--local` flag:
- Uses your local development installation instead of PyPI package
- Resolves paths correctly for the cloned repository
- Adds the project directory to the MCP configuration
- Essential for testing changes before publishing

**Example with --local:**
```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/Users/you/dev/jamfmcp",
        "fastmcp",
        "run",
        "src/jamfmcp/server.py:mcp"
      ]
    }
  }
}
```
:::::

## {fas}`bug` Troubleshooting CLI Issues

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`times-circle` "command not found: jamfmcp"
- Ensure JamfMCP is installed: `pip install jamfmcp`
- Check your PATH includes pip's bin directory
- Try: `python -m jamfmcp.cli` as alternative
::::

::::{grid-item-card} {fas}`lock` "Failed to connect to Jamf Pro"
- Verify your Jamf Pro URL (include https://)
- Check credentials are correct
- Ensure API user has appropriate permissions
- Try `jamfmcp validate` to test connection
::::

::::{grid-item-card} {fas}`exclamation-triangle` "spawn uv ENOENT"
- This means `uv` is not accessible to your MCP client
- For Claude Desktop: Install uv via Homebrew
- See [Prerequisites](prerequisites) for details
::::
:::::

## {fas}`lightbulb` Advanced Usage

### Multiple Environments

Set up multiple Jamf instances with different server names:

```bash
# Production instance
jamfmcp setup -p claude-desktop --server-name jamf-prod \
  --url https://prod.jamfcloud.com

# Sandbox instance  
jamfmcp setup -p claude-desktop --server-name jamf-test \
  --url https://sandbox.jamfcloud.com
```

### Dry Run Mode

Preview what will be configured without making changes:

```bash
jamfmcp setup -p claude-desktop --dry-run
```

### Non-Interactive Setup

Provide all options via command line (useful for automation):

```bash
jamfmcp setup -p claude-desktop \
  --url https://company.jamfcloud.com \
  --auth-type oauth \
  --client-id "$CLIENT_ID" \
  --client-secret "$CLIENT_SECRET" \
  --skip-validation
```

## {fas}`arrow-right` Next Steps

After successful CLI setup:

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fas}`play-circle` Test Your Setup
:link: quickstart
:link-type: doc

Try example queries to verify everything works
::::

::::{grid-item-card} {fas}`book` Explore Tools
:link: tools-overview
:link-type: doc

Learn about all available MCP tools
::::

::::{grid-item-card} {fas}`cog` Platform Guides
:link: configuration-overview
:link-type: doc

Platform-specific configuration details
::::
:::::

:::::{seealso}
- [Installation Guide](installation) - Installing JamfMCP
- [Claude Desktop Setup](claude-desktop) - Claude-specific details
- [Cursor Setup](cursor) - Cursor-specific details
- [Troubleshooting](../troubleshooting/installation) - Common issues
:::::
