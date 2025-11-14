# Troubleshooting

This section helps you diagnose and resolve common issues with JamfMCP.

## Jamf API Troubleshooting

Common errors experienced resulting from Jamf API issues.

### 401 Unauthorized

**Error Message:**
```
401 Unauthorized
Failed to authenticate with Jamf Pro
```

**Possible Causes:**
1. Incorrect credentials
2. Expired password (basic auth)
3. Revoked client credentials (OAuth)
4. Account locked or disabled
5. API access not enabled

**Solutions:**

#### Verify in Jamf Pro
1. Log into Jamf Pro web interface
2. Navigate to **Settings** → **System** → **User Accounts**
3. Verify account is:
   - Enabled
   - Not locked
   - Has "Access to Jamf Pro API" privilege

### 403 Forbidden

**Error Message:**
```
403 Forbidden
Insufficient privileges to access this resource
```

**Possible Causes:**
1. Missing API privileges
2. Wrong API role assigned
3. Site restrictions
4. IP address restrictions

**Solutions:**

#### Check API Privileges
1. Go to **Settings** → **System** → **API roles and clients**
2. Select the **API Roles** tab
2. Find your role and verify it has:
   - Read privileges for all needed resources
   - No unnecessary restrictions

:::{seealso}
For a full list of required API privileges, visit the [Jamf API Setup](#jamf_api_setup) doc.
:::

### Manual Token Test

```bash
#!/bin/bash

url="https://yourserver.jamfcloud.com"
client_id="your-client-id"
client_secret="yourClientSecret"

response=$(curl -fsL -X POST "${url}/api/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=${client_id}" \
  -d "grant_type=client_credentials" \
  -d "client_secret=${client_secret}")

token=$(echo "$response" | plutil -extract access_token raw -)

echo "Token: $token"

# Test token
curl -H "Authorization: Bearer $token" "${url}/api/v1/jamf-pro-version"
```

## Server Configuration Troubleshooting

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`times-circle` Invalid JSON Syntax
**Symptoms:** MCP client fails to start

**Fix:** Validate JSON syntax - remove trailing commas, check quotes
::::

::::{grid-item-card} {fas}`lock` Wrong Port Used
**Symptoms:** Failed connecting to Jamf Pro

**Fix:** Use default port (443) for HTTPS
::::

::::{grid-item-card} {fas}`globe` Wrong URL Format
**Symptoms:** Connection refused

**Fix:** Include https:// and remove trailing slashes
```json
// ❌ Wrong
"JAMF_URL": "https://your-server.com/"

// ✅ Correct
"JAMF_URL": "https://your-server.com"
```
::::

::::{grid-item-card} {fas}`globe` MCP Server Not Starting
**Symptoms:** Tools don't appear in MCP clients / No response from JamfMCP

**Fix:** Verify installation and MCP client configuration file syntax
::::
:::::

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

## Troubleshooting CLI Issues

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`times-circle` `"command not found: jamfmcp-cli"`
- Ensure JamfMCP is installed: `pip install jamfmcp`
- Check your `PATH` includes pip's `bin` directory
::::

::::{grid-item-card} {fas}`exclamation-triangle` `"spawn uv ENOENT"`
- This means `uv` is not accessible to your MCP client
- For Claude Desktop: Install `uv` via Homebrew
- See [Prerequisites](prereqs) for details
::::
:::::

## Getting Help

### Self-Diagnostic Script

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
    optional = ["JAMF_CLIENT_ID", "JAMF_CLIENT_ID"]

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
5. Output of self-diagnostic script (if ran)

### Support Channels

- **GitHub Issues**: [New Issue](https://github.com/liquidz00/jamfmcp/issues)
- **MacAdmins Slack**: [#jamfmcp](https://macadmins.slack.com/archives/C09RR0UGF0W)

:::{seealso}
- [FastMCP Troubleshooting](https://gofastmcp.com/patterns/testing#debugging)
- [Jamf Pro API Troubleshooting](https://developer.jamf.com/jamf-pro/docs)
- [MCP Protocol Debugging](https://modelcontextprotocol.io/docs/debugging)
:::

```{toctree}
:caption: Troubleshooting AI Platforms
:maxdepth: 3
:hidden:

claude-ts
cursor-ts
```
