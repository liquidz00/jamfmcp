# Getting Started

Welcome to JamfMCP! This guide will help you get up and running with the Jamf Pro MCP server.

:::::{danger}
**Critical for Claude Desktop Users**

Claude Desktop runs in an isolated environment that cannot access user-specific PATH locations. You **MUST** install `uv` via Homebrew on macOS:

```bash
brew install uv
```

Installing `uv` any other way (pip, curl, etc.) will result in "spawn uv ENOENT" errors. This is the #1 setup failure.

[Learn more about this requirement →](#claude_desktop_requirements)
:::::

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

::::{grid-item-card} {fas}`check-circle` Prerequisites
:link: prerequisites
:link-type: doc

Ensure you have Python 3.13+, `uv` (via Homebrew!), and Jamf Pro API access ready
::::

::::{grid-item-card} {fas}`download` Install JamfMCP
:link: installation
:link-type: doc

Install from PyPI with `pip install jamfmcp` and set up the CLI tool
::::

::::{grid-item-card} {fas}`key` Configure Jamf API
:link: jamf-api-setup
:link-type: doc

Set up API credentials with least-privilege access for security
::::

::::{grid-item-card} {fas}`terminal` Run CLI Setup
:link: cli-setup
:link-type: doc

Use `jamfmcp setup` to automatically configure your AI assistant
::::

::::{grid-item-card} {fas}`plug` Connect Your Client
:link: configuration-overview
:link-type: doc

Platform-specific guides for Claude Desktop, Cursor, and more
::::

::::{grid-item-card} {fas}`play-circle` Start Using Tools
:link: quickstart
:link-type: doc

Try your first commands and explore JamfMCP capabilities
::::
:::::

## {fas}`clock` What You'll Need

:::::{grid} 2 2 3 3
:gutter: 2

::::{grid-item-card}
{fas}`hourglass-half` **15 minutes**

For basic setup and configuration
::::

::::{grid-item-card}
{fas}`user-shield` **Admin access**

To create Jamf Pro API credentials
::::

::::{grid-item-card}
{fab}`python` **Python 3.13+**

Modern Python required
::::

::::{grid-item-card}
{fas}`desktop` **MCP client**

Claude Desktop, Cursor, etc.
::::

::::{grid-item-card}
{fas}`terminal` **uv via Homebrew**

Critical for Claude Desktop!
::::

::::{grid-item-card}
{fas}`globe` **Internet access**

For API and SOFA feed
::::
:::::

## {fas}`life-ring` Support Resources

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} {fab}`slack` MacAdmins Slack
:link: https://macadmins.slack.com/archives/C07EH1R7LB0
:link-type: url

Join **#jamfmcp** for community support and discussions
::::

::::{grid-item-card} {fab}`github` GitHub Repository  
:link: https://github.com/liquidz00/jamfmcp
:link-type: url

Report issues, contribute code, or browse source
::::

::::{grid-item-card} {fas}`book` Documentation
:link: https://liquidz00.github.io/jamfmcp
:link-type: url

You're here! Full guides and API reference
::::
:::::

## {fas}`arrow-right` Next Steps

Ready to get started? Head to the [Prerequisites](prerequisites) page to ensure your environment is ready for JamfMCP.

```{toctree}
:caption: 🚀 Getting Started
:maxdepth: 2
:hidden:

prerequisites
installation
cli-setup
jamf-api-setup
quickstart
```

```{toctree}
:caption: ⚙️ Configuration
:maxdepth: 2
:hidden:

configuration-overview
claude-desktop
cursor
authentication
environment
```

```{toctree}
:caption: 🔧 MCP Tools
:maxdepth: 2
:hidden:

tools-overview
computer-health
inventory
security
policies
organization
utility
```
