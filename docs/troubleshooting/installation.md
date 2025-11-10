# Installation Troubleshooting

This guide helps resolve common installation issues for JamfMCP, with the most critical issues first.

:::::{danger}
**Critical: "spawn uv ENOENT" Error (Claude Desktop)**

This is the **#1 installation failure** for Claude Desktop users. It means `uv` is installed in a location Claude Desktop cannot access.

**Solution:** You MUST install `uv` via Homebrew on macOS:
```bash
brew install uv
```

**Why this happens:** Claude Desktop runs in an isolated environment that cannot access user paths like `~/.local/bin`. Only system-wide installations (Homebrew) work.

[Full details in Prerequisites →](#claude_desktop_requirements)
:::::

## {fas}`exclamation-triangle` Most Common Issues

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`bug` spawn uv ENOENT (Claude Desktop)
:class-header: bg-danger text-white

**Symptoms:**
- Error: "spawn uv ENOENT"
- Claude Desktop can't start JamfMCP
- MCP tools don't appear

**Solution:**
```bash
# MUST use Homebrew on macOS
brew install uv

# Verify installation location
which uv
# Good: /opt/homebrew/bin/uv or /usr/local/bin/uv
# Bad: ~/.local/bin/uv
```

**Prevention:**
- Never install uv via pip or curl for Claude Desktop
- Always use system package managers
::::

::::{grid-item-card} {fas}`terminal` uv: command not found
:class-header: bg-warning

**Problem:** The `uv` package manager is not installed.

**Solutions by platform:**

**macOS:**
```bash
# Recommended (works for all MCP clients)
brew install uv
```

**Linux:**
```bash
# System-wide installation
curl -LsSf https://astral.sh/uv/install.sh | sudo sh
```
::::

::::{grid-item-card} {fas}`lock` Permission Denied
:class-header: bg-warning

**Problem:** Installation fails with permission errors.

**Solutions:**
- Don't use `sudo` with pip/uv commands
- Create a virtual environment first
- Check directory ownership: `ls -la`
- For system installs, use package managers
::::
:::::

## {fab}`python` Python & Environment Issues

:::::{dropdown} {fas}`code-branch` Python Version Mismatch
:color: warning

**Problem:** Wrong Python version detected.

**Solutions:**
```bash
# Check current version
python --version  # Need 3.13+

# Install Python 3.13
# macOS
brew install python@3.13

# Ubuntu/Debian
sudo apt update
sudo apt install python3.13

# Use uv to manage Python
uv python install 3.13
```
:::::

:::::{dropdown} {fas}`box` Virtual Environment Issues
:color: warning

**Problem:** Virtual environment not creating properly.

**Solutions:**
```bash
# Clean up existing environment
rm -rf .venv

# Create fresh environment with uv
uv venv --python 3.13

# For development from source
cd jamfmcp
make install-dev
```

**Common causes:**
- Conflicting Python installations
- Corrupted venv directory
- Missing system packages
:::::

:::::{dropdown} {fas}`puzzle-piece` Dependency Resolution Failures
:color: warning

**Problem:** uv cannot resolve dependencies.

**Quick fixes:**
```bash
# Update uv to latest
uv self update

# Clear uv cache
uv cache clean

# Force fresh install
uv pip install --force-reinstall jamfmcp

# For development
uv sync --refresh --extra dev
```
:::::

## {fas}`plug` MCP Client Connection Issues

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`times-circle` MCP Client Can't Find JamfMCP
:class-header: bg-warning

**Symptoms:**
- "Server not found" errors
- No tools available in AI client
- 🔨 icon missing or empty

**Solutions:**
1. Re-run setup: `jamfmcp setup -p <platform>`
2. Verify `jamfmcp --version` works
3. Check MCP client logs for errors
4. Test server directly:
   ```bash
   # PyPI installation
   uv run --with jamfmcp jamfmcp

   # Local development
   uv run fastmcp run src/jamfmcp/server.py:mcp
   ```
::::

::::{grid-item-card} {fas}`file-alt` Configuration File Issues
:class-header: bg-warning

**Common problems:**
- Invalid JSON syntax
- Wrong file location
- Missing required fields

**Validation steps:**
```bash
# Validate JSON syntax
python -m json.tool < claude_desktop_config.json

# Check file exists
ls -la ~/Library/Application\ Support/Claude/

# Test with minimal config first
```
::::
:::::

## {fas}`desktop` Platform-Specific Issues

:::::{tab-set}
::::{tab-item} macOS
:sync: macos-issues

**Command Line Tools Missing:**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

**Homebrew Python Conflicts:**
```bash
# Use specific Python version
python3.13 -m pip install jamfmcp

# Fix PATH priority
export PATH="/opt/homebrew/bin:$PATH"

# Check which Python is active
which python3
```

**Apple Silicon (M1/M2) Issues:**
- Ensure using native arm64 versions
- Check architecture: `arch`
- Use Homebrew arm64: `/opt/homebrew`
::::

::::{tab-item} Linux
:sync: linux-issues

**Missing Development Headers:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# RHEL/CentOS/Fedora
sudo yum install python3-devel gcc

# Arch Linux
sudo pacman -S python base-devel
```

**Permission Issues:**
- Don't use sudo with pip
- Use `--user` flag or virtual environments
- Check systemd service permissions
::::

:::::

## {fas}`check-circle` Verification Steps

After resolving issues, verify your installation:

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} 1. {fas}`terminal` Check Core Tools
```bash
# Verify uv installation and location
uv --version
which uv  # Should be system path

# Verify Python version
python --version  # 3.13+

# Verify JamfMCP CLI
jamfmcp --version
```
::::

::::{grid-item-card} 2. {fas}`server` Test MCP Server
```bash
# Test server directly
uv run --with jamfmcp jamfmcp

# Should see FastMCP startup message
# Press Ctrl+C to exit
```
::::

::::{grid-item-card} 3. {fas}`plug` Validate Connection
```bash
# Test Jamf Pro connection
jamfmcp validate \
  --url https://your.jamfcloud.com
```
::::

::::{grid-item-card} 4. {fas}`check` Final Setup
```bash
# Run full setup
jamfmcp setup -p <platform>

# Restart your MCP client
# Test with: "Ping Jamf MCP"
```
::::
:::::

## {fas}`life-ring` Getting Help

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fab}`github` GitHub Issues
:link: https://github.com/liquidz00/jamfmcp/issues
:link-type: url

Search existing issues or create new ones
::::

::::{grid-item-card} {fab}`slack` MacAdmins Slack
:link: https://macadmins.slack.com/archives/C07EH1R7LB0
:link-type: url

Join #jamfmcp for community support
::::

::::{grid-item-card} {fas}`clipboard-list` What to Include
When reporting issues, provide:
- OS and version
- Python version (`python --version`)
- uv version (`uv --version`)
- Complete error message
- Steps to reproduce
::::
:::::

:::::{tip}
**Debug Mode**: Run setup with `-v` for verbose output:
```bash
jamfmcp setup -p claude-desktop -v
```
:::::

## {fas}`arrow-right` Next Steps

Once installation issues are resolved:

- Return to [Installation Guide](../getting-started/installation)
- Continue with [CLI Setup](../getting-started/cli-setup)
- Try the [Quickstart Guide](../getting-started/quickstart)

:::::{seealso}
- [Prerequisites Guide](../getting-started/prerequisites) - System requirements
- [Configuration Troubleshooting](configuration) - Post-installation issues
- [FastMCP Troubleshooting](https://gofastmcp.com/troubleshooting) - Framework issues
:::::
