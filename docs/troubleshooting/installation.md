# Installation Troubleshooting

This guide helps resolve common installation issues for JamfMCP.

## Common Installation Issues

### uv: command not found

**Problem:** The `uv` package manager is not installed.

**Solution:**
- Install uv first: See [uv installation guide](https://github.com/astral-sh/uv#installation)
- On macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- On Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Permission denied during install

**Problem:** Installation fails with permission errors.

**Solutions:**
- Don't use `sudo` with make commands
- Ensure you have write permissions to the directory
- Check that your user owns the project directory

### Python Version Mismatch

**Problem:** Wrong Python version detected.

**Solutions:**
- JamfMCP requires Python 3.13 or later
- Check version: `python --version`
- Install Python 3.13: `brew install python@3.13` (macOS)
- Use uv to manage Python versions automatically

### Virtual Environment Issues

**Problem:** Virtual environment not creating properly.

**Solutions:**
```bash
# Clean up existing venv
rm -rf .venv

# Create fresh venv with uv
uv venv

# Activate and install
source .venv/bin/activate  # macOS/Linux
uv sync --extra dev
```

### Dependency Resolution Failures

**Problem:** uv cannot resolve dependencies.

**Solutions:**
- Update uv: `uv self update`
- Clear cache: `uv cache clean`
- Force reinstall: `uv sync --refresh`

### MCP Client Can't Find JamfMCP

**Problem:** MCP client shows "server not found" errors.

**Solutions:**
- Verify installation path is correct in MCP config
- Check that `uv` is in your PATH
- Use absolute paths in configuration
- Test directly: `uv run fastmcp run src/jamfmcp/server.py:mcp`

## Platform-Specific Issues

### macOS

**Command Line Tools Missing:**
```bash
xcode-select --install
```

**Homebrew Python Conflicts:**
- Use `python3.13` explicitly if multiple versions installed
- Set PATH to prioritize correct Python

### Linux

**Missing Development Headers:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev build-essential

# RHEL/CentOS
sudo yum install python3-devel gcc
```

## Verification Steps

After installation, verify everything works:

1. **Check Installation:**
```bash
# Verify uv
uv --version

# Verify Python
python --version

# Verify JamfMCP
uv run fastmcp run src/jamfmcp/server.py:mcp
```

2. **Test MCP Connection:**
- Configure your MCP client
- Run: "Ping the Jamf MCP server"
- Check for "pong" response

## Getting Help

If issues persist:
1. Check [GitHub Issues](https://github.com/liquidz00/jamfmcp/issues)
2. Ask in [MacAdmins Slack #jamfmcp](https://macadmins.slack.com/archives/C07EH1R7LB0)
3. Include:
   - OS and version
   - Python version
   - uv version
   - Complete error message
