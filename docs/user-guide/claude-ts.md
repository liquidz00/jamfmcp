# Claude Troubleshooting (Desktop & Code)

:::{rst-class} lead
Claude-specific troubleshooting. For general JamfMCP troubleshooting, see the [main troubleshooting guide](troubleshooting).
:::

(claude-desktop-configuration-issues)=
## Claude Desktop Configuration Issues

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
