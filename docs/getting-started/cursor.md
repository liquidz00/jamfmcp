# Cursor Configuration

This guide walks you through configuring JamfMCP for use with [Cursor](https://cursor.sh/), the AI-powered code editor.

## Prerequisites

Before configuring:
- [Install JamfMCP](../getting-started/installation)
- [Set up Jamf API access](../getting-started/jamf-api-setup)
- Have Cursor installed on your system

## Configuration Steps

### Step 1: Locate Configuration File

Cursor stores MCP configuration in **macOS/Linux**: `~/.cursor/mcp.json`

### Step 2: Edit Configuration

Open the `mcp.json` file and add the JamfMCP server configuration:

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

### Step 4: Restart Cursor

After saving the configuration:
1. Completely quit Cursor (Cmd+Q on macOS)
2. Relaunch Cursor
3. The MCP server will start automatically

## Verifying Configuration

To verify JamfMCP is working in Cursor:

1. Open a new chat (Cmd+K or Ctrl+K)
2. Type: "Ping the Jamf MCP server"
3. You should receive a response like:
   ```json
   {
     "message": "pong",
     "status": "ok"
   }
   ```

## Example Configuration

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/Users/username/projects/jamfmcp",
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

## Using JamfMCP in Cursor

Once configured, you can use JamfMCP in several ways:

### In Chat (Cmd+K)

Ask questions about your Jamf environment:
- "Show me all computers that haven't checked in for 30 days"
- "Generate a health report for serial ABC123"
- "What configuration profiles are deployed?"

### In Composer (Cmd+I)

Use JamfMCP data to help write code:
- "Create a script that processes computers with low disk space based on Jamf data"
- "Generate a report template for computer compliance status"

### In Terminal

JamfMCP tools are available in Cursor's integrated terminal chat as well.

## Troubleshooting

For help with these issues, see the [Configuration Troubleshooting Guide](#cursor_configuration_issues).

**Common issues**:
- Incorrect path to JamfMCP
- Missing uv installation
- Python version mismatch

### Authentication Errors

**Symptoms**: 401 or 403 errors when using tools

**Solutions**:
1. Verify credentials in `mcp.json`
2. Check Jamf API user permissions
3. Ensure JAMF_URL is correct format

### No Response from Tools

**Symptoms**: Commands seem to hang or timeout

**Solutions**:
1. Check network connectivity to Jamf Pro
2. Verify firewall allows HTTPS to Jamf
3. Test with a simple ping command first

### JSON Parsing Errors

**Symptoms**: "Invalid JSON" errors on startup

**Solutions**:
1. Validate JSON syntax (remove trailing commas)
2. Ensure all strings are properly quoted
3. Use a JSON validator tool

## Advanced Configuration

### Multiple Jamf Instances

You can configure multiple Jamf servers:

```json
{
  "mcpServers": {
    "jamfmcp-prod": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/jamfmcp", "fastmcp", "run", "src/jamfmcp/server.py:mcp"],
      "env": {
        "JAMF_URL": "prod.jamfcloud.com",
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "prod-client",
        "JAMF_CLIENT_SECRET": "prod-secret"
      }
    },
    "jamfmcp-test": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/jamfmcp", "fastmcp", "run", "src/jamfmcp/server.py:mcp"],
      "env": {
        "JAMF_URL": "test.jamfcloud.com",
        "JAMF_AUTH_TYPE": "client_credentials",
        "JAMF_CLIENT_ID": "test-client",
        "JAMF_CLIENT_SECRET": "test-secret"
      }
    }
  }
}
```

### Custom Python Path

If you need to specify a Python executable:

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "/usr/local/bin/uv",
      "args": [
        "run",
        "--python", "/usr/local/bin/python3.13",
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

## Next Steps

- Try the [Quickstart Guide](quickstart)
- Explore [Available Tools](tools-overview)
- Learn about [Computer Health Analysis](computer-health)

:::{seealso}
- [Cursor Documentation](https://cursor.sh/docs)
- [FastMCP Configuration](https://gofastmcp.com/servers/deployment)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
:::
