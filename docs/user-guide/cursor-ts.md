# Cursor Troubleshooting

:::{rst-class} lead
Cursor-specific troubleshooting. For general JamfMCP troubleshooting, see the [main troubleshooting guide](troubleshooting).
:::

## Cursor Configuration Issues

**Common Problems:**
- Configuration file location varies by platform
- Environment variables not being passed correctly
- MCP server not starting

**Solutions:**

1. **Verify Config Location**
   - macOS: `~/Library/Application Support/Cursor/User/globalStorage/cursor-ai/settings.json`
   - Linux: `~/.config/Cursor/User/globalStorage/cursor-ai/settings.json`
   - Windows: `%APPDATA%\Cursor\User\globalStorage\cursor-ai\settings.json`

2. **Check MCP Server Configuration**
   ```json
   {
     "mcpServers": {
       "jamfmcp": {
         "command": "uvx",
         "args": ["jamfmcp"],
         "env": {
           "JAMF_URL": "https://your-instance.jamfcloud.com",
           "JAMF_CLIENT_ID": "your_client_id",
           "JAMF_CLIENT_SECRET": "your_client_secret"
         }
       }
     }
   }
   ```

3. **Verify Server is Running**
   - Check the Cursor logs for MCP server startup messages
   - Look for any error messages related to authentication or connection

:::{seealso}
- [Main Troubleshooting Guide](troubleshooting)
- [Manual Configuration](manual-configuration)
- [CLI Setup Guide](cli-setup)
:::
