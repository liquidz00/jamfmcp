# Prerequisites

Before installing JamfMCP, ensure you have the necessary requirements and access configured.

(claude_desktop_requirements)=
:::::{danger}
**Critical: Claude Desktop Requirements**

Claude Desktop runs in an isolated environment that **cannot access user-installed programs**. For Claude Desktop users, you MUST install `uv` via Homebrew:

```bash
# macOS - REQUIRED for Claude Desktop
brew install uv
```

Installing `uv` via pip, curl, or other methods will place it in paths like `~/.local/bin` that Claude Desktop cannot access, resulting in "spawn uv ENOENT" errors.

**Why this matters**: Claude Desktop's security model isolates it from user PATH locations. Only system-wide installations (like those from Homebrew to `/opt/homebrew/bin` or `/usr/local/bin`) are accessible.
:::::

## {fas}`desktop` System Requirements

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fab}`python` Python 3.13+
:class-header: bg-light

JamfMCP requires modern Python features available in 3.13 or higher
::::

::::{grid-item-card} {fas}`cube` uv Package Manager
:class-header: bg-light

Modern, fast Python package management - **install via Homebrew for Claude Desktop!**
::::

::::{grid-item-card} {fas}`server` Jamf Pro Server
:class-header: bg-light

Cloud or on-premise instance with API access enabled
::::

::::{grid-item-card} {fas}`plug` MCP Client
:class-header: bg-light

Claude Desktop, Cursor, Cline, or other MCP-compatible clients
::::
:::::

:::::{note}
JamfMCP is built on [FastMCP](https://gofastmcp.com), which handles the MCP protocol implementation.
:::::

## {fas}`download` Installing uv

:::::{tab-set}
::::{tab-item} macOS (Homebrew)
:sync: macos

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install uv via Homebrew
brew install uv

# Verify installation location (should be /opt/homebrew/bin/uv or /usr/local/bin/uv)
which uv
```

::::

::::{tab-item} Linux
:sync: linux

**For Linux users (Note: Claude Desktop on Linux still requires system-wide installation):**

```bash
# Install to system location
curl -LsSf https://astral.sh/uv/install.sh | sudo sh

# Or if you have Homebrew on Linux
brew install uv

# Verify installation
which uv
```
::::
:::::

After installing uv, verify it's accessible:

```bash
# Check version
uv --version

# Check installation path
which uv  # macOS/Linux

# For Claude Desktop users - ensure path is NOT in home directory
# Good: /opt/homebrew/bin/uv, /usr/local/bin/uv
# Bad: ~/.local/bin/uv, ~/bin/uv
```

:::{important}
For Claude Desktop, `uv` **MUST** be installed via Homebrew. Other installation methods will fail.
:::

## {fas}`shield-alt` Jamf Pro Setup

### API Access Requirements

JamfMCP requires API access to your Jamf Pro server. Choose your authentication method:

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`user` Basic Authentication
:class-header: bg-warning

**For testing and development**
- Username/password authentication
- Simple setup process
- Not recommended for production
::::

::::{grid-item-card} {fas}`key` OAuth Client Credentials
:class-header: bg-success

**Recommended for production**
- More secure authentication
- Better access control
- Follows Jamf Pro best practices
::::
:::::

### Required API Privileges

:::::{important}
**Least Privilege Principle**

JamfMCP is designed as a **read-only** tool. Grant only the minimum required privileges:

- Read access to computers, mobile devices, and users
- Read access to policies, profiles, and packages
- Read access to buildings, departments, and categories
- No write/update/delete permissions needed

For detailed setup instructions, see the [Jamf API Setup Guide](jamf-api-setup).
:::::

## {fas}`network-wired` Network Requirements

:::::{grid} 1
:gutter: 2

::::{grid-item-card} {fas}`lock` Required Connections
- **HTTPS access** to your Jamf Pro server
- **Outbound HTTPS** to `sofafeed.macadmins.io` (for CVE data)
- **No inbound connections** - JamfMCP operates as a client only
::::
:::::

## {fas}`rocket` Next Steps

Once all prerequisites are confirmed:

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} 1. {fas}`download` Install JamfMCP
:link: installation
:link-type: doc

Install from PyPI and set up the CLI tool
::::

::::{grid-item-card} 2. {fas}`key` Configure API Access
:link: jamf-api-setup
:link-type: doc

Create API credentials with appropriate privileges
::::

::::{grid-item-card} 3. {fas}`terminal` Run Setup
:link: cli-setup
:link-type: doc

Use the CLI to configure your MCP client automatically
::::
:::::

:::::{seealso}
- [Jamf Pro API Overview](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview)
- [FastMCP Installation](https://gofastmcp.com/getting-started/installation)
- [uv Documentation](https://github.com/astral-sh/uv)
:::::
