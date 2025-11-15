# Installing JamfMCP

:::{rst-class} lead
This guide walks you through installing JamfMCP for different use cases.
:::

:::{attention}
**Before you begin**: Ensure you have completed the [prerequisites](prereqs), especially the critical `uv` installation requirements for Claude Desktop users.
:::

## User Installation

For most users who want to use JamfMCP with their MCP client:

:::::{tab-set}
::::{tab-item} {iconify}`material-icon-theme:uv` uv
:sync: uv

```bash
# Install JamfMCP from PyPI
uv pip install jamfmcp

# Verify installation
jamfmcp-cli --version
```

::::

::::{tab-item} {iconify}`devicon:pypi` pip
:sync: pip

```bash
# Install JamfMCP from PyPI
pip install jamfmcp

# Verify installation
jamfmcp-cli --version
```
::::
:::::

## Development Installation

For contributors and developers working on JamfMCP:

```bash
# Clone the repository
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp

# Install development dependencies
make install-dev

# Verify installation
jamfmcp-cli --version

# Run tests
make test
```

:::{note}
When using a development installation with the CLI, always use the `--dev` flag:
```bash
jamfmcp-cli -p claude-desktop --dev
```
:::

:::{seealso}
- [CLI Setup Guide](cli-setup) - Detailed CLI usage and options
- [Development Guide](../contributing/development-guide) - Complete development workflow
- [Testing Guide](../contributing/testing) - Running and writing tests
- [FastMCP Documentation](https://gofastmcp.com) - Underlying MCP framework
- [MCP Protocol Overview](https://modelcontextprotocol.io) - Protocol specification
:::
