# CLI Setup Guide

:::{rst-class} lead
The JamfMCP CLI tool automates the entire setup process for connecting JamfMCP to your AI assistant. This guide covers all CLI features and options.
:::

:::::{tip}
The CLI is the **recommended method** for setting up JamfMCP. It handles all the complex configuration automatically and validates your setup before applying changes.
:::::

## Quick Setup with CLI

After installation, use the JamfMCP CLI tool to automatically configure your MCP client:

:::::{tab-set}
::::{tab-item} {iconify}`material-icon-theme:claude` Claude
:sync: claude

```bash
jamfmcp-cli -p claude-desktop
```
::::

::::{tab-item} {iconify}`vscode-icons:file-type-cursorrules` Cursor
:sync: cursor

```bash
jamfmcp-cli -p cursor
```
::::

::::{tab-item} {iconify}`vscode-icons:file-type-gemini` Gemini
:sync: other

```bash
jamfmcp-cli -p gemini-cli
```
::::

::::{tab-item} Other Platforms
:sync: other

```bash
jamfmcp-cli -p <platform>
```
::::
:::::

The CLI will:
1. {fas}`check` Verify prerequisites
2. {fas}`key` Prompt for your Jamf Pro credentials if not provided
3. {fas}`server` Test the connection to your Jamf Pro server
4. {fas}`cog` Generate the appropriate configuration
5. {fas}`rocket` Set up your MCP client automatically

:::{dropdown} Example Session
:animate: fade-in-slide-down
```
$ jamfmcp-cli -p claude-desktop

🚀 Setting up JamfMCP for claude-desktop

Jamf Pro server URL: https://mycompany.jamfcloud.com
Client ID: api-user
Client Secret: ****

Validating Jamf Pro connection...
✓ Successfully connected to Jamf Pro

✓ Successfully configured claude-desktop

📝 Next steps:
1. Restart Claude Desktop completely
2. Look for the hammer icon (🔨) in the input box
3. Your JamfMCP tools are now available!
```
:::

(cli_options_reference)=
## CLI Options Reference

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--platform` | `-p` | Target platform (required) | `claude-desktop`, `cursor`, `claude-code` |
| `--url` | `-u` | Jamf Pro server URL | `https://company.jamfcloud.com` |
| `--client-id` | | OAuth client ID | `abc123` |
| `--client-secret` | | OAuth client secret | Will prompt if not provided |
| `--workspace` | `-w` | Cursor workspace directory | `/path/to/project` |
| `--skip-validation` | | Skip connection test | Not recommended |
| `--verbose` | `-v` | Show detailed output | Helpful for debugging |
| `--dry-run` | | Preview without changes | See what would be configured |
| `--dev` | `-l` | Use local installation | For development from source |
| `--write` | | Write configuration file to disk | For setup |

## Usage Examples

### Dry Run Mode

Preview what will be configured without making changes:

```bash
jamfmcp-cli -p claude-desktop --dry-run
```

### Non-Interactive Setup

Provide all options via command line (useful for automation):

```bash
jamfmcp-cli -p claude-desktop \
  --url https://company.jamfcloud.com \
  --client-id "$CLIENT_ID" \
  --client-secret "$CLIENT_SECRET" \
  --skip-validation
```
