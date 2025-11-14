# FastMCP Client Logging Implementation

This document describes the FastMCP client logging implementation in the JamfMCP server.

## Overview

All MCP tools now support optional Context-based logging that sends log messages directly to MCP clients. This provides better visibility into tool execution, progress tracking, and error reporting.

## Key Features

### 1. Optional Context Parameter
All 49 MCP tools accept an optional `ctx: Context | None = None` parameter:

```python
@mcp.tool
async def get_computer_inventory(
    serial: str,
    sections: list[str] | None = None,
    ctx: Context | None = None
) -> dict[str, Any]:
```

### 2. Log Levels

- **Debug**: Detailed execution information (API calls, data processing)
- **Info**: Normal execution milestones (successful operations, summaries)
- **Warning**: Non-critical issues (fallback behaviors, missing optional data)
- **Error**: Recoverable errors with context

### 3. Structured Logging

:::{danger}
Ensure all sensitive information is sanitized properly from logs. Code changes will not be approved if proper code sanitization has not been performed. This includes but is not limited to user information such as phone numbers, location, job title, etc. For more, visit the [security considerations](#security_considerations) doc.
:::

All log methods support an optional `extra` parameter for structured data:

```python
if ctx:
    await ctx.info(
        f"Successfully retrieved inventory for {serial}",
        extra={
            "serial": serial,
            "computer_id": result.get("id"),
            "os_version": result.get("operatingSystem", {}).get("version")
        }
    )
```

### 4. Nested Logging

Key JamfApi methods also support Context for nested logging:

- `get_serial_for_user()`
- `get_computer_inventory()`
- `get_computer_history()`
- `get_compliance_status()`
- `search_computers()`

## Example Usage

### Client Code
```python
from fastmcp import Context

# In your MCP client
async def handle_tool_call(tool_name: str, arguments: dict, ctx: Context):
    # Context is automatically provided by the MCP framework
    result = await call_tool(tool_name, arguments, ctx=ctx)
    return result
```

### Server Logging Output
When a client calls `get_computer_inventory`, they'll receive logs like:

```
[DEBUG] Starting inventory retrieval for serial ABC123
[INFO] Fetching computer inventory for ABC123
[DEBUG] Looking up user by email: user@example.com (in nested API call)
[INFO] Successfully retrieved inventory for ABC123
```

## Testing

A mock Context implementation is provided for testing:

```python
from tests.fixtures.mock_context import MockContext

ctx = MockContext()
result = await some_tool(param="value", ctx=ctx)

# Verify logs
assert len(ctx.info_logs) == 2
assert "Success" in ctx.info_logs[0][0]
```

## Backward Compatibility

All Context parameters are optional. Tools work without Context:

```python
# Works without context
result = await get_computer_inventory(serial="ABC123")

# Works with context for logging
result = await get_computer_inventory(serial="ABC123", ctx=ctx)
```

## Benefits

1. **Better Debugging**: Detailed execution traces help diagnose issues
2. **Progress Visibility**: Users see what the tool is doing in real-time
3. **Structured Data**: Extra parameters enable rich, queryable logs
4. **Error Context**: Errors include relevant IDs and context
5. **No Breaking Changes**: Fully backward compatible
