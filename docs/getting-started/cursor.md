# Cursor Configuration

This guide walks you through configuring JamfMCP for use with [Cursor](https://cursor.sh/), the AI-powered code editor.

:::::{tip}
**New to JamfMCP?** Use the automated CLI setup - it's much faster than manual configuration!
:::::

## {fas}`rocket` Quick Setup with CLI (Recommended)

The fastest way to configure JamfMCP for Cursor:

:::::{tab-set}
::::{tab-item} Global Setup
:sync: global

**For system-wide Cursor configuration:**

```bash
# Install JamfMCP
pip install jamfmcp

# Run automated setup
jamfmcp setup -p cursor
```

This configures JamfMCP globally for all Cursor projects.
::::

::::{tab-item} Project-Specific
:sync: project

**For individual project configuration:**

```bash
# Navigate to your project
cd /path/to/your/project

# Install JamfMCP
pip install jamfmcp

# Setup with workspace flag
jamfmcp setup -p cursor --workspace .
```

This creates a project-specific MCP configuration.
::::
:::::

The CLI will:
1. ✅ Check prerequisites
2. 🔑 Collect Jamf Pro credentials
3. 🌐 Validate connection
4. ⚙️ Configure Cursor automatically
5. 📝 Provide next steps

## {fas}`cog` Manual Configuration (Advanced)

:::::{dropdown} {fas}`code` Manual Configuration Steps
:color: warning

If you prefer manual setup or need custom configuration:

### Step 1: Locate Configuration File

Cursor stores MCP configuration in: `~/.cursor/mcp.json`

### Step 2: Add JamfMCP Configuration

:::::{tab-set}
::::{tab-item} PyPI Installation
:sync: pypi-cursor

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
:sync: local-cursor

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
:::::

### Step 3: Restart Cursor

1. **Completely quit** Cursor (Cmd+Q on macOS)
2. **Relaunch** Cursor
3. **Verify** MCP tools are available
:::::

## {fas}`check-circle` Verifying Your Setup

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`terminal` Test Connection
Open chat with **Cmd+K** and type:
> "Ping the Jamf MCP server"

Expected: Confirmation of connection
::::

::::{grid-item-card} {fas}`list` Check Available Tools
Ask Cursor:
> "List all available Jamf MCP tools"

Expected: List of 40+ tools
::::

::::{grid-item-card} {fas}`heartbeat` Run Test Query
Try a simple query:
> "Get computer inventory for serial ABC123"

Expected: Inventory data or "not found"
::::

::::{grid-item-card} {fas}`check` Verify in Terminal
Open terminal chat and test:
> "Using JamfMCP, list all buildings"

Expected: List of configured buildings
::::
:::::

## {fas}`keyboard` Using JamfMCP in Cursor

JamfMCP integrates with all Cursor AI features:

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`comment` Chat (Cmd+K)
**Query your Jamf environment:**
- "Show me all computers that haven't checked in for 30 days"
- "Generate a health report for serial ABC123"
- "What configuration profiles are deployed?"
- "Find computers with critical CVEs"
::::

::::{grid-item-card} {fas}`magic` Composer (Cmd+I)
**Generate code using Jamf data:**
- "Create a script that processes computers with low disk space based on Jamf data"
- "Generate a report template for computer compliance status"
- "Build a function to analyze policy deployment success rates"
::::

::::{grid-item-card} {fas}`terminal` Terminal Chat
**Use in integrated terminal:**
- "Check health of all Engineering computers"
- "Export inventory data for Finance department"
- "List all packages available in Jamf"
::::

::::{grid-item-card} {fas}`code` Inline Edits
**Reference Jamf data while coding:**
- Get real computer names for scripts
- Verify policy IDs and scopes
- Check actual inventory values
::::
:::::

## {fas}`exclamation-triangle` Troubleshooting

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`lock` Authentication Errors
:class-header: bg-warning

**Symptoms:** 401 or 403 errors when using tools

**Solutions:**
```bash
# Test credentials
jamfmcp validate --url https://your.jamfcloud.com

# Re-run setup
jamfmcp setup -p cursor
```

**Check:**
- Correct JAMF_URL format (include https://)
- Valid API credentials
- Proper API permissions
::::

::::{grid-item-card} {fas}`times-circle` No MCP Tools
:class-header: bg-warning

**Symptoms:** Tools don't appear in Cursor

**Solutions:**
1. Quit and restart Cursor completely
2. Check `~/.cursor/mcp.json` exists
3. Validate JSON syntax:
   ```bash
   python -m json.tool < ~/.cursor/mcp.json
   ```
4. Re-run: `jamfmcp setup -p cursor`
::::

::::{grid-item-card} {fas}`clock` Timeouts
:class-header: bg-warning

**Symptoms:** Commands hang or timeout

**Debug steps:**
1. Test network: `ping your.jamfcloud.com`
2. Check firewall allows HTTPS
3. Try simpler query first
4. Verify Jamf Pro is accessible
::::
:::::

## {fas}`cogs` Advanced Configuration

:::::{dropdown} {fas}`server` Multiple Jamf Instances
:color: info

Configure multiple environments:

```bash
# Production
jamfmcp setup -p cursor --server-name jamf-prod \
  --url https://prod.jamfcloud.com

# Sandbox
jamfmcp setup -p cursor --server-name jamf-sandbox \
  --url https://sandbox.jamfcloud.com
```

Then specify which to use:
> "Using jamf-prod, check health of serial ABC123"
:::::

:::::{dropdown} {fas}`folder` Project-Specific Config
:color: info

For per-project MCP servers:

```bash
cd /path/to/project
jamfmcp setup -p cursor --workspace .
```

This creates `.cursor/mcp.json` in your project directory.
:::::

:::::{dropdown} {fab}`python` Custom Python Path
:color: info

If you need a specific Python version:

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--python", "python3.13",
        "jamfmcp"
      ],
      "env": {
        // ... your config ...
      }
    }
  }
}
```
:::::

## {fas}`lightbulb` Tips for Cursor

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`keyboard` Keyboard Shortcuts
- **Cmd+K**: Open chat for queries
- **Cmd+I**: Composer for code generation
- **Cmd+L**: Add context to chat
- **Option+Enter**: Apply AI suggestions
::::

::::{grid-item-card} {fas}`brain` Effective Prompts
- Reference specific serials/IDs
- Ask for formatted output (tables, CSV)
- Chain queries for analysis
- Use context from open files
::::

::::{grid-item-card} {fas}`code` Code Generation
- "Generate Python script to analyze Jamf health data"
- "Create report template for compliance"
- "Build dashboard for inventory metrics"
::::

::::{grid-item-card} {fas}`sync` Workflow Tips
- Keep Jamf data queries in chat history
- Use composer for report generation
- Reference real data in your code
::::
:::::

## {fas}`arrow-right` Next Steps

Now that Cursor is configured:

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fas}`play-circle` Try Examples
:link: quickstart
:link-type: doc

Work through quickstart scenarios
::::

::::{grid-item-card} {fas}`wrench` Explore Tools
:link: tools-overview
:link-type: doc

Learn about all available tools
::::

::::{grid-item-card} {fas}`chart-line` Build Reports
:link: computer-health
:link-type: doc

Create health analysis workflows
::::
:::::

:::::{seealso}
- [CLI Setup Guide](cli-setup) - Detailed CLI documentation
- [Cursor Docs](https://cursor.sh/docs) - Official Cursor documentation
- [FastMCP Clients](https://gofastmcp.com/clients) - MCP client configuration
:::::
