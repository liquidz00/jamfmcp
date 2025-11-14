# Installing JamfMCP

This guide walks you through installing JamfMCP and setting it up with your MCP client using the automated CLI tool.

:::{important}
**Before you begin**: Ensure you have completed the [prerequisites](#prereqs), especially the critical `uv` installation requirements for Claude Desktop users.
:::

:::::{tab-set}
::::{tab-item} PyPI (uv)
:sync: uv

**Recommended method using uv:**

```bash
# Install JamfMCP from PyPI
uv pip install jamfmcp

# Verify installation
jamfmcp-cli --version
```

:::{tip}
Using `uv` is faster and more reliable than traditional pip. It handles dependencies better and provides cleaner virtual environments.
:::
::::

::::{tab-item} PyPI (pip)
:sync: pip

**Traditional pip installation:**

```bash
# Install JamfMCP from PyPI
pip install jamfmcp

# Verify installation
jamfmcp-cli --version
```
::::

::::{tab-item} From Source
:sync: source

**For development or testing latest features:**

```bash
# Clone the repository
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp

# Install in development mode
make install-dev

# For CLI setup, use the --dev flag
jamfmcp-cli -p claude-desktop --dev
```

:::{important}
When installing from source, always use the `--dev` flag with the CLI to ensure proper path resolution.
:::
::::
:::::

:::{seealso}
- [CLI Setup Guide](cli-setup) - Detailed CLI usage and options
- [FastMCP Documentation](https://gofastmcp.com) - Underlying MCP framework
- [MCP Protocol Overview](https://modelcontextprotocol.io) - Protocol specification
:::
