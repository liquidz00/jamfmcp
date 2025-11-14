# Command Line Interface (CLI)

## Overview

JamfMCP CLI - Configuration tool for setting up JamfMCP with AI platforms.

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

### Main entry

CLI is written using [asyncclick](https://github.com/python-trio/asyncclick/). Parameters of the CLI are as follows:

:::{card}
``parameter`` **required**
^^^
Which AI platform to configure (``claude-code``, ``claude-desktop``, ``cursor``, ``gemini-cli``)
:::

:::{card}
``dev`` (_bool_)
^^^
Configure for development mode (local source) instead of PyPI package
:::

:::{card}
``url`` (_str | None_)
^^^
Jamf Pro Server URL (optional)
+++
Optional - if not provided you will be prompted for it
:::

:::{card}
``client_id`` (_str | None_)
^^^
Jamf Pro API client ID
+++
Optional - if not provided you will be prompted for it
:::

:::{card}
``client_secret`` (_str | None_)
^^^
Jamf Pro API client secret
+++
Optional - if not provided you will be prompted for it
:::

:::{card}
``workspace`` (_Path | None_)
^^^
Workspace directory for Cursor/Gemini project-specific installation (optional)
:::

:::{card}
``skip_validation`` (_bool_)
^^^
Skip automatic Jamf Pro validation checks
:::

:::{card}
``verbose`` (_bool_)
^^^
Enables verbose output to ``stdout``
:::

:::{card}
``dry_run`` (_bool_)
^^^
Shows what actions would be taken without making changes
:::

:::{card}
``write`` (_bool_)
^^^
Attempts to rite directly to configuration file
+++
:::
