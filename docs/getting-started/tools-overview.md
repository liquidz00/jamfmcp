# MCP Tools Reference

JamfMCP provides 49 tools for interacting with Jamf Pro through the Model Context Protocol. These tools are organized by category for easy reference.

## Tool Categories

::::{grid} 2
:gutter: 3

:::{grid-item-card} 🏥 Computer Health
:link: computer-health
:link-type: doc

Health analysis, diagnostics, and CVE scanning
- Health scorecards
- Basic diagnostics
- CVE vulnerability analysis
:::

:::{grid-item-card} 📦 Inventory Management
:link: inventory
:link-type: doc

Computer inventory and search capabilities
- Detailed inventory retrieval
- Computer search
- History and logs
:::

:::{grid-item-card} 📋 Policies & Configuration
:link: policies
:link-type: doc

Policy and profile management tools
- Configuration profiles
- Policies
- Scripts and packages
:::

:::{grid-item-card} 🔒 Security & Compliance
:link: security
:link-type: doc

Security analysis and compliance tools
- Compliance status
- Restricted software
- Licensed software
- Device lock PINs
:::

:::{grid-item-card} 🏢 Organization
:link: organization
:link-type: doc

Organizational data and structure
- Buildings and departments
- Sites and categories
- Network segments
- Users and groups
:::

:::{grid-item-card} 🔧 Utility Tools
:link: utility
:link-type: doc

Additional utility and management tools
- JCDS files
- Webhooks
- LDAP and directory bindings
- System utilities
:::
::::

## Quick Tool Reference

### Most Common Tools

| Tool | Description | Category |
|------|-------------|----------|
| `get_health_scorecard` | Generate comprehensive health analysis | Health |
| `get_computer_inventory` | Get detailed computer information | Inventory |
| `search_computers` | Find computers by criteria | Inventory |
| `get_cves` | Check CVE vulnerabilities | Security |
| `get_policies` | List all policies | Policies |
| `get_configuration_profiles` | List configuration profiles | Policies |

## Using Tools with AI Assistants

### Natural Language

Ask your AI assistant naturally:
> "Show me the health status of computer ABC123"

The AI will translate to:
```python
get_health_scorecard(serial="ABC123")
```

### Direct Tool Calls

You can also request specific tools:
> "Use get_computer_inventory to check serial ABC123"

### Chaining Tools

Combine tools for complex queries:
> "Find all computers in the Sales department and check their health scores"

## Response Formats

All tools return JSON data that your AI assistant will interpret. Common patterns:

### Successful Response
```json
{
  "data": { /* requested information */ },
  "metadata": { /* additional context */ }
}
```

### Error Response
```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "context": { /* relevant context */ }
}
```

### List Responses
```json
[
  { "id": 1, "name": "Item 1" },
  { "id": 2, "name": "Item 2" }
]
```

## Performance Considerations

- **Pagination**: Handled automatically for large datasets
- **Rate Limiting**: Respects Jamf Pro API limits
- **Caching**: Some responses cached for efficiency
- **Timeouts**: Long operations may take 10-30 seconds

## Best Practices

1. **Start Specific**: Use exact identifiers when known
2. **Use Sections**: Request only needed data sections
3. **Handle Errors**: Check for error responses
4. **Chain Wisely**: Combine tools for complex workflows
5. **Monitor Usage**: Be aware of API rate limits

## Tool Documentation Format

Each tool category page includes:

- **Tool signature** with parameters
- **Description** of functionality
- **Parameters** with types and defaults
- **Return value** structure
- **Example usage** in context
- **Related tools** for workflows

## Getting Help

- **In AI Assistant**: Ask "What tools are available for [task]?"
- **Tool Details**: Ask "How do I use [tool_name]?"
- **Examples**: Request "Show me an example of [tool_name]"
- **Errors**: Share error messages for troubleshooting

## Next Steps

Explore specific tool categories:
- [Computer Health Tools](computer-health)
- [Inventory Management](inventory)
- [Policy Tools](policies)
- [Security Tools](security)
- [Organization Tools](organization)
- [Utility Tools](utility)

:::{seealso}
- [Quickstart Guide](quickstart)
- [Jamf Pro API Reference](https://developer.jamf.com/jamf-pro/reference)
- [FastMCP Tools Documentation](https://gofastmcp.com/servers/core-components#tools)
:::
