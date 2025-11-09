# Claude Desktop Configuration

This guide walks you through configuring JamfMCP for use with [Claude Desktop](https://claude.ai/download), including both Claude Chat and Claude Code.

## Prerequisites

Before configuring:
- [Install JamfMCP](../getting-started/installation)
- [Set up Jamf API access](../getting-started/jamf-api-setup)
- Have Claude Desktop installed on your system

## Configuration Steps

### Step 1: Locate Configuration File

Claude Desktop stores MCP configuration in different locations by OS:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

:::{tip}
On macOS, you can open the config directory with:
```bash
open ~/Library/Application\ Support/Claude/
```
:::

### Step 2: Edit Configuration

Create or edit the `claude_desktop_config.json` file:

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

:::{important}
Replace `/path/to/jamfmcp` with the absolute path to your JamfMCP installation directory.
:::

### Step 3: Configure Authentication

#### Option A: Basic Authentication

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "basic",
  "JAMF_USERNAME": "api-user",
  "JAMF_PASSWORD": "secure-password"
}
```

#### Option B: OAuth Client Credentials (Recommended)

```json
"env": {
  "JAMF_URL": "your-jamf-server.com",
  "JAMF_AUTH_TYPE": "client_credentials",
  "JAMF_CLIENT_ID": "your-client-id",
  "JAMF_CLIENT_SECRET": "your-client-secret"
}
```

### Step 4: Restart Claude Desktop

After saving the configuration:
1. Completely quit Claude Desktop
2. Relaunch Claude Desktop
3. The MCP server will start automatically

## Verifying Configuration

To verify JamfMCP is working:

1. Open Claude Desktop
2. Look for the 🔌 icon in the text input area
3. Click it to see available MCP servers
4. JamfMCP should appear as "jamfmcp"
5. Test with: "Ping the Jamf MCP server"

You should see:
```json
{
  "message": "pong",
  "status": "ok"
}
```

## Platform-Specific Examples

### macOS Configuration

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/Users/username/Developer/jamfmcp",
        "fastmcp",
        "run",
        "src/jamfmcp/server.py:mcp"
      ],
      "env": {
        "JAMF_URL": "mycompany.jamfcloud.com",
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "abc123def456",
        "JAMF_CLIENT_SECRET": "super-secret-key"
      }
    }
  }
}
```

### Linux Configuration

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/home/username/projects/jamfmcp",
        "fastmcp",
        "run",
        "src/jamfmcp/server.py:mcp"
      ],
      "env": {
        "JAMF_URL": "mycompany.jamfcloud.com",
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "abc123def456",
        "JAMF_CLIENT_SECRET": "super-secret-key"
      }
    }
  }
}
```

## Using JamfMCP in Claude Desktop

### Available Tools Indicator

When JamfMCP is properly configured, you'll see:
- A 🔌 icon in the text input area
- Clicking it shows "jamfmcp" as an available server
- Tool count indicator (e.g., "49 tools available")

### Example Queries

Try these queries to explore JamfMCP capabilities:

**Computer Health**
> "Analyze the health of computer with serial ABC123 and provide recommendations"

**Inventory Search**
> "Find all MacBook Pro computers that haven't checked in for 7 days"

**Security Analysis**
> "Check for CVEs affecting computers running macOS 14.x"

**Policy Review**
> "List all configuration profiles and their scope"

**Organizational Data**
> "Show me all departments and how many computers are in each"

## Troubleshooting

For help with these issues, see the [Configuration Troubleshooting Guide](#claude-desktop-configuration-issues).

**Verify installation**:
```bash
# Test JamfMCP directly
cd /path/to/jamfmcp
uv run fastmcp run src/jamfmcp/server.py:mcp
```

### Authentication Failures

**Error**: "Failed to authenticate with Jamf Pro"

**Solutions**:
1. Double-check credentials in config
2. Verify API user has correct permissions
3. Test credentials with curl:
   ```bash
   curl -u username:password https://your-server.com/api/v1/auth/token
   ```

### Connection Issues

**Error**: "Cannot connect to Jamf Pro server"

**Solutions**:
1. Check JAMF_URL format (no trailing slash)
2. Verify network access to Jamf Pro
3. Check for proxy/firewall restrictions

### Tools Not Working

**Symptoms**: Tools appear but return errors

**Debug steps**:
1. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
2. Look for Python errors or missing dependencies
3. Verify Python 3.13+ is being used

## Advanced Configuration

### Multiple Environments

Configure multiple Jamf instances:

```json
{
  "mcpServers": {
    "jamf-production": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/jamfmcp", "fastmcp", "run", "src/jamfmcp/server.py:mcp"],
      "env": {
        "JAMF_URL": "prod.jamfcloud.com",
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "prod-id",
        "JAMF_CLIENT_SECRET": "prod-secret"
      }
    },
    "jamf-sandbox": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/jamfmcp", "fastmcp", "run", "src/jamfmcp/server.py:mcp"],
      "env": {
        "JAMF_URL": "sandbox.jamfcloud.com",
        "JAMF_AUTH_TYPE": "basic",
        "JAMF_USERNAME": "test-user",
        "JAMF_PASSWORD": "test-pass"
      }
    }
  }
}
```

### Custom uv Path

If uv isn't in your PATH:

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "/usr/local/bin/uv",
      "args": [
        "run",
        "--directory", "/path/to/jamfmcp",
        "fastmcp",
        "run",
        "src/jamfmcp/server.py:mcp"
      ],
      "env": {
        // ... authentication config ...
      }
    }
  }
}
```

## Tips for Claude Desktop

### Effective Prompts

- Be specific with identifiers (serial numbers, IDs)
- Ask for summaries of large datasets
- Chain queries for deeper analysis
- Request specific output formats (tables, CSV)

### Performance

- Large queries may take a few seconds
- Claude will indicate when tools are running
- Results are automatically formatted for readability

## Next Steps

- Explore the [Quickstart Guide](quickstart)
- Learn about [Available Tools](tools-overview)
- Try [Computer Health Analysis](computer-health)

:::{seealso}
- [Claude Desktop Documentation](https://support.anthropic.com/en/articles/8325610)
- [FastMCP Client Setup](https://gofastmcp.com/clients/essentials)
- [MCP Protocol Overview](https://modelcontextprotocol.io)
:::
