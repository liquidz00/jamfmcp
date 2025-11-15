# Command Line Interface (CLI)

:::{rst-class} lead
Configuration tool for setting up the JamfMCP server with AI platforms.
:::

## Overview

This CLI helps users configure JamfMCP to work with various AI platforms like
Claude Desktop, Cursor, and others. It handles two installation modes:

1. PyPI Mode (default): For users who installed JamfMCP from PyPI
2. Development Mode (``--dev``): For developers working on JamfMCP source code

Both modes configure the MCP server to run locally on the user's machine.
The difference is how the server is invoked (``uvx`` vs ``uv run``).

### Standalone functions

```{eval-rst}
.. automodule:: jamfmcp.cli
    :members:
    :undoc-members:
```

:::{tip}
For a list of all options to pass to the CLI, see the [CLI setup guide](#cli_options_reference)
:::
