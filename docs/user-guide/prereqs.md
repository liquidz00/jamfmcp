(prereqs)=
# Prerequisites & Installation

Ensuring you have the necessary requirements and access configured for a smooth installation experience.

(claude_desktop_requirements)=
:::{important}
**Claude Desktop Requirements**

Claude Desktop runs in an isolated environment that cannot access user-install programs. This means `uv` **must** be installed via [Homebrew](https://brew.sh/) for proper access: `brew install uv`.

Installing `uv` via `pip`, `curl` or other methods will place it in paths like `~/.local/bin` that Claude Desktop cannot access, resulting in `spawn uv ENOENT` errors.

**Why does this matter?** Glad you asked! Claude Desktop's security model isolates it from user `PATH` locations. Only system-wide installations (like those from Homebrew to `/opt/homebrew/bin` or `/usr/local/bin`) are accessible.
:::

## {fas}`desktop` System Requirements

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fab}`python` Python 3.13+
:class-header: bg-light

JamfMCP requires modern Python features available in 3.13 or higher
::::

::::{grid-item-card} {fas}`cube` uv Package Manager
:class-header: bg-light

Modern, fast Python package management
::::

::::{grid-item-card} {fas}`server` Jamf Pro Server
:class-header: bg-light

Cloud or on-premise instance with API access enabled
::::

::::{grid-item-card} {fas}`plug` MCP Client
:class-header: bg-light

Claude Desktop, Cursor, or other MCP-compatible clients
::::
:::::

## {fas}`download` Installing `uv`

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

:::{seealso}
- [Jamf Pro API Overview](https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview)
- [FastMCP Installation](https://gofastmcp.com/getting-started/installation)
- [uv Documentation](https://github.com/astral-sh/uv)
:::
