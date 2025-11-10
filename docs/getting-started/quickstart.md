# Quickstart Guide

Get up and running with JamfMCP in minutes! This guide walks you through setup and your first queries.

:::::{tip}
**New to JamfMCP?** Start with the automated CLI setup - it handles all the configuration for you!
:::::

## {fas}`rocket` Setup in 3 Steps

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item-card} 1. {fas}`download` Install
```bash
pip install jamfmcp
```
::::

::::{grid-item-card} 2. {fas}`terminal` Configure
```bash
jamfmcp setup -p claude-desktop
```
::::

::::{grid-item-card} 3. {fas}`play` Use
Ask your AI: "Check health of serial ABC123"
::::
:::::

## {fas}`desktop` Platform-Specific Quickstart

:::::{tab-set}
::::{tab-item} Claude Desktop
:sync: claude-quickstart

**1. Install JamfMCP:**
```bash
# Install via pip
pip install jamfmcp

# CRITICAL: Ensure uv is installed via Homebrew
brew install uv
```

**2. Run Setup:**
```bash
jamfmcp setup -p claude-desktop
```

**3. Enter Credentials:**
```
Jamf Pro server URL: https://mycompany.jamfcloud.com
Username: api-user
Password: ****
```

**4. Restart Claude Desktop and Test:**
> "Ping the Jamf MCP server"

:::{tip}
Look for the 🔨 icon in Claude's input box - this indicates MCP tools are available!
:::
::::

::::{tab-item} Cursor
:sync: cursor-quickstart

**1. Install JamfMCP:**
```bash
pip install jamfmcp
```

**2. Run Setup:**
```bash
# For global installation
jamfmcp setup -p cursor

# For project-specific
jamfmcp setup -p cursor --workspace .
```

**3. Configure and Test:**
Follow the prompts, then in Cursor:
> "List all available Jamf MCP tools"
::::

::::{tab-item} From Source
:sync: source-quickstart

**1. Clone and Install:**
```bash
git clone https://github.com/liquidz00/jamfmcp.git
cd jamfmcp
make install-dev
```

**2. Setup with --local flag:**
```bash
jamfmcp setup -p claude-desktop --local
```

**3. Test Your Development Setup:**
> "Get computer inventory for serial ABC123"
::::
:::::

## {fas}`check-circle` Verify Your Setup

After setup, test these commands with your AI assistant:

### Test Connection
> "Ping the Jamf MCP server"

Expected: Confirmation that the server is responding

### List Available Tools
> "What Jamf MCP tools are available?"

Expected: List of 40+ available tools

### Basic Query
> "Get computer inventory for serial ABC123XYZ"

Expected: Detailed inventory data (or "not found" if serial doesn't exist)

## {fas}`star` Common Use Cases

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`heartbeat` Health Analysis
**Generate comprehensive health scorecards:**

> "Generate a health scorecard for serial ABC123XYZ"

**Returns:**
- Overall score (0-100) with letter grade
- Security compliance status
- CVE vulnerability analysis
- Maintenance recommendations
::::

::::{grid-item-card} {fas}`shield-alt` Security Analysis
**Check for vulnerabilities:**

> "What CVEs affect computer ABC123XYZ?"

**Returns:**
- Applicable CVEs
- Actively exploited vulnerabilities
- Patch recommendations
- Days since last update
::::

::::{grid-item-card} {fas}`search` Inventory Queries
**Search computers by criteria:**

> "Find MacBook Pros that haven't checked in for 7 days"

> "Show computers in Engineering department"

> "List computers with less than 20GB free space"
::::

::::{grid-item-card} {fas}`cog` Policy Management
**Review configurations:**

> "List all configuration profiles"

> "Show details of policy ID 42"

> "What scripts are available?"
::::
:::::

## {fas}`code` Example Queries by Category

:::::{dropdown} {fas}`desktop` Computer Management
:open:

**Inventory Lookups:**
- "Get full inventory for serial C02ABC123DEF"
- "Show hardware details for computer 'CEO-MacBook'"
- "List all applications installed on serial ABC123"

**Health Checks:**
- "Analyze health of all computers in Sales department"
- "Which computers have critical security issues?"
- "Show computers needing OS updates"

**Usage Analytics:**
- "Find computers with uptime over 30 days"
- "Show computers with battery health below 80%"
- "List computers with FileVault disabled"
:::::

:::::{dropdown} {fas}`shield-alt` Security & Compliance

**CVE Analysis:**
- "Check CVE vulnerabilities for macOS 14.5 computers"
- "Show actively exploited vulnerabilities"
- "Which computers are missing critical security updates?"

**Compliance Checks:**
- "List computers not meeting security baseline"
- "Show computers without antivirus installed"
- "Find computers with SIP disabled"
:::::

:::::{dropdown} {fas}`building` Organization & Policies

**Organizational Queries:**
- "List all buildings and their computer counts"
- "Show departments with most computers"
- "What network segments are configured?"

**Policy Information:**
- "Show all policies targeting Finance department"
- "List configuration profiles by scope"
- "What packages are available for deployment?"
:::::

## {fas}`chart-line` Understanding Output

:::::{note}
Your AI assistant interprets JamfMCP's responses and presents them conversationally. You won't see raw JSON - the AI formats everything for readability.
:::::

### Success Indicators

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} {fas}`check-circle` Successful Queries
- Detailed, formatted responses
- Health scores with A-F grades
- Clear recommendations
- Organized data tables
::::

::::{grid-item-card} {fas}`times-circle` Error Responses
- "Computer not found" messages
- "Permission denied" for restricted data
- Connection timeout notices
- Clear error explanations
::::
:::::

### Requesting Specific Data

You can request specific inventory sections:

:::::{dropdown} {fas}`database` Available Data Sections
- **GENERAL** - Basic computer information
- **HARDWARE** - Hardware specifications  
- **OPERATING_SYSTEM** - OS details
- **USER_AND_LOCATION** - Assignment information
- **APPLICATIONS** - Installed software
- **STORAGE** - Disk information
- **SECURITY** - Security settings
- **ALL** - Everything (default)

**Example:** "Get only hardware and OS info for serial ABC123XYZ"
:::::

## {fas}`lightbulb` Tips and Best Practices

:::::{tip}
**Pro Tips for Power Users**

1. {fas}`bullseye` **Be Specific** - Use exact serial numbers or computer names
2. {fas}`comments` **Natural Language** - The AI understands context and intent
3. {fas}`link` **Chain Queries** - Ask follow-up questions based on results
4. {fas}`compress` **Request Summaries** - "Summarize the health issues for all Sales computers"
5. {fas}`file-export` **Export Data** - "Format this as a CSV" or "Create a table"
:::::

### Performance Tips

:::::{grid} 1 1 3 3
:gutter: 2

::::{grid-item}
{fas}`clock` **Response Times**

Large queries may take 3-5 seconds
::::

::::{grid-item}
{fas}`sync` **Auto-Pagination**

AI handles large result sets automatically
::::

::::{grid-item}
{fas}`globe` **Network Required**

CVE analysis needs internet access
::::
:::::

## {fas}`exclamation-triangle` Common Issues

:::::{dropdown} {fas}`question-circle` Troubleshooting Quick Fixes
:color: warning

**"No MCP tools available"**
- Restart your AI client completely
- Check the 🔨 icon is visible
- Re-run `jamfmcp setup`

**"spawn uv ENOENT"**
- Claude Desktop specific issue
- Install uv via Homebrew: `brew install uv`
- See [Prerequisites](prerequisites)

**"Connection refused"**
- Verify Jamf Pro URL
- Check network connectivity
- Validate credentials with `jamfmcp validate`
:::::

## {fas}`rocket` What's Next?

Now that you're up and running:

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} {fas}`wrench` Explore All Tools
:link: tools-overview
:link-type: doc

Discover 40+ available MCP tools for Jamf Pro
::::

::::{grid-item-card} {fas}`heartbeat` Master Health Analysis
:link: computer-health
:link-type: doc

Deep dive into health scorecards and compliance
::::

::::{grid-item-card} {fas}`shield-alt` Security Features
:link: security
:link-type: doc

Learn about CVE tracking and security analysis
::::

::::{grid-item-card} {fas}`chart-line` Build Workflows
:link: inventory
:link-type: doc

Create automated monitoring and reporting flows
::::
:::::

:::::{seealso}
- [CLI Setup Guide](cli-setup) - Detailed CLI documentation
- [Configuration Overview](configuration-overview) - Platform-specific setup
- [Troubleshooting Guide](../troubleshooting/index) - Solve common issues
:::::
