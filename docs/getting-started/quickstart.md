# Quickstart Guide

Get hands-on with JamfMCP! This guide shows you how to use common tools and features after installation.

## First Steps

Once you have JamfMCP configured in your MCP client, try these commands to verify everything is working:

### Test Connection

Ask your AI assistant:
> "Ping the Jamf MCP server"

Chances are your AI assistant will not show you the raw output, but if it does, it should look like this:
```json
{
  "message": "pong",
  "status": "ok"
}
```
> See more about [expected responses and formats](#understanding-responses) below

### Basic Computer Lookup

> "Get computer inventory for serial number ABC123XYZ"

This returns detailed inventory including hardware, OS, applications, and more.

## Common Use Cases

### Health Analysis

Generate a comprehensive health scorecard for a computer:

> "Generate a health scorecard for serial ABC123XYZ"

This provides:
- Overall health score (0-100) with letter grade
- Security compliance analysis
- System health metrics
- Policy compliance status
- Maintenance recommendations
- CVE vulnerability analysis

### Security Analysis

Check for CVEs affecting a specific computer:

> "What CVEs affect the computer with serial ABC123XYZ?"

Returns:
- List of applicable CVEs
- Actively exploited vulnerabilities
- Patch recommendations
- Days since last security update

### Inventory Queries

Search for computers by various criteria:

> "Search for all computers with 'MacBook Pro' in the name"

> "Find computers that haven't checked in for 7 days"

> "Show me computers in the Engineering department"

### Policy and Configuration

Review policies and profiles:

> "List all configuration profiles"

> "Show me the details of policy ID 42"

> "What scripts are available in Jamf?"

### Organizational Data

Query organizational information:

> "List all buildings in Jamf"

> "Show me all network segments"

> "What departments are configured?"

(understanding_responses)=
## Understanding Responses

JamfMCP returns structured data that your AI assistant will interpret. Here's what to expect:

:::{note}
**About JSON Examples**

The JSON examples shown below represent the data structure that JamfMCP returns to the AI assistant. You won't see raw JSON in your conversation - the AI will interpret this data and present it in a natural, conversational format based on your request.
:::

### Successful Responses

- Detailed JSON data with requested information
- Health scores include grades (A-F) and recommendations
- Inventory data includes hardware, software, and configuration details

### Error Responses

Common error patterns:
```json
{
  "error": "Computer not found",
  "message": "No computer found with serial: XYZ",
  "serial": "XYZ"
}
```

### Data Sections

When requesting computer inventory, you can specify sections:
- `GENERAL` - Basic computer information
- `HARDWARE` - Hardware specifications  
- `OPERATING_SYSTEM` - OS details
- `USER_AND_LOCATION` - Assignment information
- `APPLICATIONS` - Installed software
- `STORAGE` - Disk information
- `SECURITY` - Security settings
- `ALL` - Everything (default)

Example:
> "Get only hardware and OS info for serial ABC123XYZ"

## Tips and Best Practices

:::{tip}
**Pro Tips for Using JamfMCP**

1. **Start specific** - Use exact serial numbers or IDs when known
2. **Use natural language** - The AI understands context
3. **Chain commands** - Ask follow-up questions based on results
4. **Request summaries** - Ask the AI to summarize large datasets
5. **Export friendly** - Request data in specific formats (CSV, table, etc.)
:::

### Performance Considerations

- Large queries may take a few seconds
- The AI will handle pagination automatically
- CVE analysis requires internet access to SOFA feed

### Security Notes

- JamfMCP is read-only by design
- No modifications are made to Jamf Pro
- Sensitive data is handled according to your Jamf Pro permissions

## What's Next?

Now that you've tried the basics:

1. Explore the [Tools Reference](tools-overview) for all available commands
2. Learn about [Computer Health Analysis](computer-health) in detail
3. Set up [regular health monitoring](inventory) workflows
4. Review [troubleshooting tips](../troubleshooting/index) for common issues

:::{seealso}
- [Complete Tools Reference](tools-overview)
- [FastMCP Documentation](https://gofastmcp.com)
- [Jamf Pro API Reference](https://developer.jamf.com/jamf-pro/reference)
:::
