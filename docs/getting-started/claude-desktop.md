# Claude Desktop Configuration

This guide walks you through configuring JamfMCP for use with [Claude Desktop](https://claude.ai/download).

:::::{danger}
**Critical PATH Requirement for Claude Desktop**

Claude Desktop runs in an isolated environment that **cannot access user-specific PATH locations**. You MUST install `uv` via Homebrew on macOS:

```bash
brew install uv
```

This is the #1 cause of setup failures. Installing `uv` any other way (pip, curl, etc.) will result in "spawn uv ENOENT" errors.

[Learn why this matters →](#claude_desktop_requirements)
:::::

## {fas}`rocket` Quick Setup with CLI (Recommended)

The fastest way to set up JamfMCP for Claude Desktop:

```bash
# Install JamfMCP
pip install jamfmcp

# Run automated setup
jamfmcp setup -p claude-desktop
```

The CLI will:
1. ✅ Verify `uv` is installed correctly
2. 🔑 Collect your Jamf Pro credentials
3. 🌐 Test the connection
4. ⚙️ Configure Claude Desktop automatically
5. 🎉 Provide next steps

:::::{tip}
**That's it!** The CLI handles all the complex configuration for you. Just restart Claude Desktop after setup completes.
:::::

## {fas}`cog` Manual Configuration (Advanced)

:::::{dropdown} {fas}`code` Manual Configuration Steps
:color: warning

While the CLI is recommended, you can manually configure Claude Desktop if needed.

### Step 1: Locate Configuration File

Claude Desktop stores MCP configuration in different locations by OS:

::::{tab-set}
:::{tab-item} macOS
:sync: macos-config

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```bash
# Open config directory
open ~/Library/Application\ Support/Claude/

# Or edit directly
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```
:::

:::{tab-item} Linux
:sync: linux-config

**Location:** `~/.config/Claude/claude_desktop_config.json`

```bash
# Create directory if needed
mkdir -p ~/.config/Claude

# Edit config
nano ~/.config/Claude/claude_desktop_config.json
```
:::
::::

### Step 2: Add JamfMCP Configuration

Add this to your `claude_desktop_config.json`:

::::{tab-set}
:::{tab-item} PyPI Installation
:sync: pypi-config

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
:::

:::{tab-item} Local Development
:sync: local-config

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
:::
::::

### Step 3: Configure Authentication

Choose your authentication method:

::::{tab-set}
:::{tab-item} OAuth (Recommended)
:sync: oauth-env

```json
"env": {
  "JAMF_URL": "https://your-instance.jamfcloud.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "abc123def456",
  "JAMF_CLIENT_SECRET": "your-secret-key"
}
```
:::

:::{tab-item} Basic Auth
:sync: basic-env

```json
"env": {
  "JAMF_URL": "https://your-instance.jamfcloud.com",
  "JAMF_AUTH_TYPE": "basic",
  "JAMF_USERNAME": "api-user",
  "JAMF_PASSWORD": "secure-password"
}
```
:::
::::

### Step 4: Restart Claude Desktop

1. **Completely quit** Claude Desktop (Cmd+Q on macOS)
2. **Relaunch** Claude Desktop
3. **Verify** the 🔨 icon appears in the input area
:::::

## {fas}`check-circle` Verifying Your Setup

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`plug` Check MCP Icon
Look for the 🔨 icon in Claude's text input area - this indicates MCP tools are available
::::

::::{grid-item-card} {fas}`list` View Available Tools
Click the 🔨 icon to see "jamfmcp" listed with tool count (e.g., "49 tools")
::::

::::{grid-item-card} {fas}`heartbeat` Test Connection
Type: "Ping the Jamf MCP server" to verify connectivity
::::

::::{grid-item-card} {fas}`play` Try a Query
Test with: "List all available Jamf MCP tools"
::::
:::::

## {fas}`comment` Example Queries

Once configured, try these queries in Claude Desktop:

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`heartbeat` Computer Health
> "Analyze the health of computer with serial ABC123 and provide recommendations"

> "Show me all computers with critical health issues"
::::

::::{grid-item-card} {fas}`search` Inventory Search
> "Find all MacBook Pro computers that haven't checked in for 7 days"

> "List computers with FileVault disabled"
::::

::::{grid-item-card} {fas}`shield-alt` Security Analysis
> "Check for CVEs affecting computers running macOS 14.x"

> "Which computers are missing critical security updates?"
::::

::::{grid-item-card} {fas}`cog` Configuration Review
> "List all configuration profiles and their scope"

> "Show me policies targeting the Sales department"
::::
:::::

## {fas}`exclamation-triangle` Troubleshooting

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`bug` "spawn uv ENOENT" Error
:class-header: bg-danger text-white

**This is the #1 Claude Desktop issue!**

**Solution:**
```bash
# MUST install uv via Homebrew
brew install uv

# Verify it's in system PATH
which uv
# Should show: /opt/homebrew/bin/uv or /usr/local/bin/uv
```

**Why this happens:** Claude Desktop cannot access user-installed programs in `~/.local/bin`
::::

::::{grid-item-card} {fas}`times-circle` No MCP Tools Available
:class-header: bg-warning

**Solutions:**
1. Completely quit Claude Desktop (Cmd+Q)
2. Check configuration file for syntax errors
3. Re-run `jamfmcp setup -p claude-desktop`
4. Verify 🔨 icon appears after restart
::::

::::{grid-item-card} {fas}`lock` Authentication Failures
:class-header: bg-warning

**Test your credentials:**
```bash
jamfmcp validate --url https://your-instance.jamfcloud.com
```

**Common issues:**
- Wrong URL format (needs https://)
- Incorrect credentials
- Missing API permissions
::::

::::{grid-item-card} {fas}`network-wired` Connection Issues
:class-header: bg-warning

**Check:**
- Jamf Pro server is accessible
- No proxy blocking connections
- Firewall allows HTTPS traffic
- URL has no trailing slash
::::
:::::

:::::{dropdown} {fas}`terminal` Debug Commands
:color: info

**Test JamfMCP directly:**
```bash
# For PyPI installation
uv run --with jamfmcp jamfmcp

# For local development
cd /path/to/jamfmcp
uv run fastmcp run src/jamfmcp/server.py:mcp
```

**Check Claude Desktop logs:**
```bash
# macOS
tail -f ~/Library/Logs/Claude/*.log

# Linux
tail -f ~/.config/Claude/logs/*.log
```

**Verify Python version:**
```bash
python --version  # Should be 3.13+
```
:::::

## {fas}`cogs` Advanced Configuration

:::::{dropdown} {fas}`server` Multiple Jamf Environments
:color: info

Configure multiple Jamf instances with different names:

```bash
# Production instance
jamfmcp setup -p claude-desktop --server-name jamf-prod \
  --url https://prod.jamfcloud.com

# Sandbox instance  
jamfmcp setup -p claude-desktop --server-name jamf-sandbox \
  --url https://sandbox.jamfcloud.com
```

This creates separate MCP servers you can query:
> "Using jamf-prod, check health of serial ABC123"
> "Using jamf-sandbox, list all policies"
:::::

:::::{dropdown} {fas}`path` Custom uv Path
:color: info

If Claude Desktop can't find `uv`, specify the full path:

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "/opt/homebrew/bin/uv",  // Full path to uv
      "args": ["run", "jamfmcp"],
      "env": {
        // ... your config ...
      }
    }
  }
}
```

Common uv locations:
- Apple Silicon Mac: `/opt/homebrew/bin/uv`
- Intel Mac: `/usr/local/bin/uv`
- Linux: `/usr/local/bin/uv`
:::::

## {fas}`lightbulb` Tips for Claude Desktop

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`bullseye` Effective Prompts
- Use specific identifiers (serials, IDs)
- Ask for summaries of large datasets
- Chain queries for deeper analysis
- Request specific formats (tables, CSV)
::::

::::{grid-item-card} {fas}`rocket` Performance Tips
- Large queries take 3-5 seconds
- Claude shows tool execution status
- Results are auto-formatted
- Use specific queries for speed
::::
:::::

## {fas}`graduation-cap` Learning Resources

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fas}`play-circle` Video Tutorials
:link: https://youtube.com/@YourChannel
:link-type: url

Coming soon: Video walkthroughs
::::

::::{grid-item-card} {fas}`users` Community Examples
:link: https://github.com/liquidz00/jamfmcp/discussions
:link-type: url

Share and discover use cases
::::

::::{grid-item-card} {fas}`book` Best Practices
:link: computer-health
:link-type: doc

Learn advanced health analysis
::::
:::::

## {fas}`arrow-right` Next Steps

Now that Claude Desktop is configured:

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fas}`rocket` Try Examples
:link: quickstart
:link-type: doc

Run through quickstart examples
::::

::::{grid-item-card} {fas}`wrench` Explore Tools
:link: tools-overview
:link-type: doc

Discover all 40+ available tools
::::

::::{grid-item-card} {fas}`heartbeat` Health Analysis
:link: computer-health
:link-type: doc

Master computer health monitoring
::::
:::::

:::::{seealso}
- [CLI Setup Guide](cli-setup) - Detailed CLI documentation
- [Troubleshooting Guide](../troubleshooting/configuration) - Solve configuration issues
- [Claude Desktop Docs](https://support.anthropic.com/en/articles/8325610) - Official Claude documentation
:::::
