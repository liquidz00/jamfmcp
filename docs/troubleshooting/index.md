# Troubleshooting

This section helps you diagnose and resolve common issues with JamfMCP.

## Quick Troubleshooting

::::{grid} 2
:gutter: 3

:::{grid-item-card} 🔐 Authentication Issues
:link: authentication
:link-type: doc

Problems with API credentials and authentication
:::

:::{grid-item-card} 🌐 Connectivity Problems
:link: connectivity
:link-type: doc

Network and connection troubleshooting
:::
::::

## Common Issues

### MCP Server Not Starting

**Symptoms:**
- Tools don't appear in MCP client
- No response from JamfMCP

**Quick Checks:**
1. Verify JamfMCP is installed: `uv run fastmcp run src/jamfmcp/server.py:mcp`
2. Check MCP client configuration file syntax
3. Ensure path to JamfMCP is correct
4. Restart MCP client

### Authentication Failures

**Symptoms:**
- 401 Unauthorized errors
- "Failed to authenticate" messages

**Quick Checks:**
1. Verify credentials are correct
2. Check API user is enabled in Jamf Pro
3. Ensure proper auth type is set
4. Test credentials directly with curl

### No Data Returned

**Symptoms:**
- Empty results from tools
- "Not found" errors

**Quick Checks:**
1. Verify items exist in Jamf Pro
2. Check API user permissions
3. Ensure computer has checked in recently
4. Verify serial numbers are correct

## Diagnostic Commands

### Test JamfMCP Installation

```bash
# Check if JamfMCP runs
cd /path/to/jamfmcp
uv run fastmcp run src/jamfmcp/server.py:mcp

# Check Python version
python --version  # Should be 3.13+

# Check dependencies
uv pip list | grep fastmcp
```

### Test Jamf Connectivity

```bash
# Test basic auth
curl -u username:password \
  https://your-server.com/api/v1/auth/token

# Test OAuth
curl -X POST https://your-server.com/api/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_ID&client_secret=YOUR_SECRET&grant_type=client_credentials"

# Test API endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-server.com/api/v1/computers-inventory?section=GENERAL&page=0&page-size=1
```

### Check MCP Configuration

```bash
# Cursor
cat ~/.cursor/mcp.json | jq .

# Claude Desktop (macOS)
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .

# Validate JSON syntax
python -m json.tool < config.json
```

## Debug Mode

Enable debug logging for detailed information:

### In MCP Configuration

```json
{
  "mcpServers": {
    "jamfmcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/jamfmcp", "fastmcp", "run", "src/jamfmcp/server.py:mcp"],
      "env": {
        "LOG_LEVEL": "DEBUG",
        // ... other env vars
      }
    }
  }
}
```

### View Logs

**Cursor:**
```bash
# macOS/Linux
tail -f ~/.cursor/logs/main.log
```

**Claude Desktop:**
```bash
# macOS
tail -f ~/Library/Logs/Claude/

# Linux
tail -f ~/.config/Claude/logs/
```

## Error Messages

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Jamf Pro server URL not provided` | Missing JAMF_URL | Add JAMF_URL to env configuration |
| `401 Unauthorized` | Invalid credentials | Check username/password or client ID/secret |
| `403 Forbidden` | Insufficient permissions | Verify API role has required privileges |
| `Computer not found` | Invalid serial or no access | Check serial number and permissions |
| `Connection refused` | Network issue | Verify Jamf Pro URL and network access |
| `SSL certificate verify failed` | Certificate issue | Check certificate validity or proxy settings |

## Performance Issues

### Slow Response Times

**Possible Causes:**
- Large inventory sections requested
- Network latency
- Jamf Pro server load
- Rate limiting

**Solutions:**
1. Request only needed inventory sections
2. Check network connection
3. Try during off-peak hours
4. Implement result caching

### Timeouts

**Symptoms:**
- Operations take too long
- "Request timeout" errors

**Solutions:**
1. Increase timeout values in client
2. Reduce data requested
3. Check Jamf Pro performance
4. Use pagination for large datasets

## Getting Help

### Information to Provide

When reporting issues, include:

1. **Error messages** - Complete error text
2. **Configuration** - Sanitized config (no secrets)
3. **Versions**:
   ```bash
   python --version
   uv --version
   uv pip show jamfmcp
   ```
4. **Steps to reproduce** - What you did before the error
5. **Logs** - Debug output if available

### Support Channels

- **GitHub Issues**: [github.com/liquidz00/jamfmcp/issues](https://github.com/liquidz00/jamfmcp/issues)
- **MacAdmins Slack**: #jamfmcp channel
- **Discussions**: GitHub Discussions for questions

## Self-Diagnostic Script

Save this as `diagnose.py`:

```python
#!/usr/bin/env python3
"""JamfMCP diagnostic script."""

import os
import sys
import json
import asyncio
from pathlib import Path

def check_python():
    """Check Python version."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 13):
        print("❌ Python 3.13+ required")
        return False
    print("✅ Python version OK")
    return True

def check_env():
    """Check environment variables."""
    required = ["JAMF_URL"]
    optional = ["JAMF_USERNAME", "JAMF_CLIENT_ID"]

    print("\nEnvironment variables:")
    for var in required:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

    for var in optional:
        value = os.getenv(var)
        if value:
            print(f"ℹ️  {var}: Set")

def check_imports():
    """Check if imports work."""
    print("\nChecking imports:")
    try:
        import jamfmcp
        print("✅ jamfmcp imports successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

    try:
        from fastmcp import FastMCP
        print("✅ FastMCP available")
    except ImportError:
        print("❌ FastMCP not found")
        return False

    return True

async def check_connection():
    """Check Jamf connection."""
    print("\nChecking Jamf connection:")
    try:
        from jamfmcp.auth import JamfAuth
        from jamfmcp.api import JamfApi

        auth = JamfAuth()
        api = JamfApi(auth)
        print("✅ Authentication configured")

        # Try a simple API call
        # This would need actual implementation
        print("ℹ️  Skipping API test (would require live connection)")

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

    return True

def main():
    """Run diagnostics."""
    print("JamfMCP Diagnostic Tool")
    print("=" * 50)

    checks = [
        check_python(),
        check_imports(),
        check_env(),
    ]

    # Run async check
    loop = asyncio.get_event_loop()
    checks.append(loop.run_until_complete(check_connection()))

    print("\n" + "=" * 50)
    if all(checks):
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed. See above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Run with: `python diagnose.py`

## Next Steps

If you're still experiencing issues:

1. Check specific guides:
   - [Authentication Troubleshooting](authentication)
   - [Connectivity Troubleshooting](connectivity)

2. Enable debug logging and collect logs

3. Search existing GitHub issues

4. Create a new issue with diagnostic information

:::{seealso}
- [FastMCP Troubleshooting](https://gofastmcp.com/patterns/testing#debugging)
- [Jamf Pro API Troubleshooting](https://developer.jamf.com/jamf-pro/docs)
- [MCP Protocol Debugging](https://modelcontextprotocol.io/docs/debugging)
:::

```{toctree}
:hidden:
:maxdepth: 1

installation
configuration
authentication
connectivity
tools
```
