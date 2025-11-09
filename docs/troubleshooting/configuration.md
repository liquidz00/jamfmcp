# Configuration Troubleshooting

This guide helps resolve common configuration issues with JamfMCP and MCP clients.

## Server Issues

### Server Won't Start

**Symptoms:**
- MCP client shows "server not found"
- No response from JamfMCP
- Error messages about missing modules

**Solutions:**
1. **Verify Installation Path**
   ```bash
   # Check JamfMCP is installed
   ls -la /path/to/jamfmcp
   ```

2. **Ensure uv is Available**
   ```bash
   # Check uv installation
   which uv
   uv --version
   ```

3. **Verify Python Version**
   ```bash
   python --version  # Should be 3.13+
   ```

4. **Check Virtual Environment**
   ```bash
   cd /path/to/jamfmcp
   uv sync --extra dev
   ```

### MCP Client Can't Find Server

**Symptoms:**
- "No MCP servers configured"
- Server appears offline
- Connection refused errors

**Solutions:**
1. **Restart MCP Client**
   - Completely quit and restart your client
   - Configuration changes require restart

2. **Validate JSON Configuration**
   ```bash
   # Check for syntax errors
   python -m json.tool < ~/.cursor/mcp.json
   ```

3. **Verify Server Name**
   - Ensure server name is exactly "jamfmcp"
   - Check for typos in configuration

4. **Check File Permissions**
   ```bash
   # Ensure config is readable
   ls -la ~/.cursor/mcp.json  # or appropriate path
   ```

## Installation Issues

### Installation Failures

See the main [Installation Guide](../getting-started/installation) for prerequisites.

**Common Issues:**
- Missing Python 3.13+
- No uv installed
- Permission errors
- Network restrictions

**Solutions:**
1. **Update Python**
   ```bash
   # macOS with Homebrew
   brew install python@3.13

   # Or use pyenv
   pyenv install 3.13.0
   ```

2. **Install uv**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Fix Permissions**
   ```bash
   # Clone to user-writable location
   cd ~/dev
   git clone https://github.com/liquidz00/jamfmcp.git
   ```

## MCP Client Configuration

(cursor_configuration_issues)=
### Cursor Configuration Issues

**Common Problems:**
- Config file in wrong location
- Incorrect path format
- Missing environment variables

**Solutions:**
1. **Verify Config Location**
   - macOS/Linux: `~/.cursor/mcp.json`

2. **Use Absolute Paths**
   ```json
   {
     "mcpServers": {
       "jamfmcp": {
         "command": "uv",
         "args": [
           "run",
           "--directory", "/Users/username/dev/jamfmcp",
           "fastmcp",
           "run",
           "src/jamfmcp/server.py:mcp"
         ]
       }
     }
   }
   ```
(claude-desktop-configuration-issues)=
### Claude Desktop Configuration Issues

**Common Problems:**
- Different config file name
- Platform-specific paths
- Permission restrictions

**Solutions:**
1. **Verify Config Location**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Platform-Specific Paths**
   ```json
   {
     "mcpServers": {
       "jamfmcp": {
         "command": "uv",
         "args": [
           "run",
           "--directory", "/full/path/to/jamfmcp",
           "fastmcp",
           "run",
           "src/jamfmcp/server.py:mcp"
         ]
       }
     }
   }
   ```

(environment_variable_issues)=
## Environment Variable Issues

### Missing Environment Variables

**Symptoms:**
- "JAMF_URL not provided" errors
- Authentication failures
- Empty credential errors

**Solutions:**
1. **Check Variable Names**
   - Must be exactly as documented
   - Case-sensitive

2. **Verify in Config**
   ```json
   "env": {
     "JAMF_URL": "your-server.jamfcloud.com",
     "JAMF_AUTH_TYPE": "basic",
     "JAMF_USERNAME": "api-user",
     "JAMF_PASSWORD": "password"
   }
   ```

3. **No Quotes in Values**
   - Correct: `"JAMF_URL": "server.com"`
   - Wrong: `"JAMF_URL": "'server.com'"`

(oauth_configuration_issues)=
### OAuth Configuration Issues

**Symptoms:**
- Client credentials not working
- Token refresh failures
- 401 errors with OAuth

**Solutions:**
1. **Verify OAuth Setup**
   ```json
   "env": {
     "JAMF_URL": "your-server.jamfcloud.com",
     "JAMF_AUTH_TYPE": "client_credentials",
     "JAMF_CLIENT_ID": "your-client-id",
     "JAMF_CLIENT_SECRET": "your-secret"
   }
   ```

2. **Check Jamf Pro OAuth App**
   - Ensure app is enabled
   - Verify client ID matches
   - Regenerate secret if needed

## Related Guides

- [Authentication Troubleshooting](authentication) - Credential and permission issues
- [Connectivity Troubleshooting](connectivity) - Network and API connection problems
- [Getting Started](../getting-started/index) - Initial setup guide

## Getting Help

If these solutions don't resolve your issue:

1. **Collect Information**
   - Configuration file (sanitized)
   - Error messages
   - Debug logs
   - System information

2. **Get Support**
   - [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues)
   - [MacAdmins Slack #jamfmcp](https://macadmins.slack.com/archives/C09RR0UGF0W)
