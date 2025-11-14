# User Guide

Welcome to JamfMCP! This guide will help you get up and running with the Jamf Pro MCP server.

## Overview

JamfMCP enables AI assistants like Cursor and Claude Desktop to interact with your Jamf Pro environment through the Model Context Protocol (MCP). This allows you to:

- {fas}`heartbeat` **Analyze** computer health and security compliance
- {fas}`search` **Query** inventory and organizational data  
- {fas}`shield-alt` **Review** policies, profiles, and configurations
- {fas}`exclamation-triangle` **Track** CVE vulnerabilities with SOFA integration
- {fas}`chart-line` **Generate** comprehensive reports and recommendations

## {fas}`rocket` Quick Start Path

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`check-circle` Prerequisites & Installation
:link: prereqs
:link-type: doc

Satisfying prerequisites and installing JamfMCP from PyPI
::::

::::{grid-item-card} {fas}`key` Jamf API Setup
:link: jamf-api-setup
:link-type: doc

Set up API credentials with least-privilege access for security
::::

::::{grid-item-card} {fas}`terminal` JamfMCP CLI
:link: cli-setup
:link-type: doc

Use `jamfmcp-cli` to automatically configure your AI assistant
::::

::::{grid-item-card} {fas}`plug` Connect Your Platform
:link: manual-configuration
:link-type: doc

Platform-specific guides for Claude Desktop, Cursor, and more
::::

::::{grid-item-card} {fas}`play-circle` Available Tools
:link: mcp-tools-reference
:link-type: doc

Try your first commands and explore JamfMCP capabilities
::::

::::{grid-item-card} {fas}`bug` Troubleshooting
:link: troubleshooting
:link-type: doc

Solutions for common MCP issues
::::
:::::


```{toctree}
:caption: 🚀 Getting Started
:maxdepth: 3
:hidden:

prereqs
install
jamf-api-setup
```

```{toctree}
:caption: ⚙️ Configuration
:maxdepth: 3
:hidden:

cli-setup
manual-configuration
jamf-deployment
```

```{toctree}
:caption: 🔧 MCP Tools
:maxdepth: 3
:hidden:

mcp-tools-reference
```

```{toctree}
:caption: 🤝 Troubleshooting & Support
:maxdepth: 3
:hidden:

troubleshooting
support
```
