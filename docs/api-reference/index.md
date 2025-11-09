# API Reference

This section provides detailed API documentation for JamfMCP's core classes and modules.

## Core Components

::::{grid} 2
:gutter: 3

:::{grid-item-card} 🏥 Health Analyzer
:link: health-analyzer
:link-type: doc

Computer health analysis and scoring system
:::

:::{grid-item-card} 🔒 SOFA Integration
:link: sofa
:link-type: doc

macOS security vulnerability tracking via SOFA feed
:::
::::

## Module Overview

### jamfmcp.server

The main MCP server module containing all tool implementations:
- 49 MCP tools for Jamf Pro interaction
- Async/await pattern throughout
- Automatic error handling and logging
- Parameter validation and type conversion

### jamfmcp.health_analyzer

Health analysis engine that provides:
- Comprehensive scoring across 4 categories
- CVE vulnerability assessment
- Compliance checking
- Actionable recommendations

### jamfmcp.sofa

Integration with macadmins SOFA feed for:
- CVE tracking and analysis
- OS version currency assessment
- Security patch monitoring
- Exploit detection

### jamfmcp.api

API client layer providing:
- Authenticated requests to Jamf Pro
- Response parsing and validation
- Error handling and retries
- Rate limit management

### jamfmcp.auth

Authentication provider supporting:
- Basic authentication (username/password)
- OAuth client credentials
- Token management and caching
- Automatic token refresh

## Using the API

### Direct Usage

:::{note}
While JamfMCP is designed to be used through MCP clients, you can _hypothetically_ use it directly, although this feature is **not technically supported**.
:::

```python
import asyncio
from jamfmcp.auth import JamfAuth
from jamfmcp.api import JamfApi

async def main():
    # Initialize authentication
    auth = JamfAuth(
        server="your-server.jamfcloud.com",
        auth_type="basic",
        username="api-user",
        password="password"
    )

    # Create API client
    api = JamfApi(auth)

    # Get computer inventory
    inventory = await api.get_computer_inventory(serial="ABC123456")
    print(inventory)

asyncio.run(main())
```

### Health Analysis

```python
from jamfmcp.health_analyzer import HealthAnalyzer

# Create analyzer with diagnostic data
analyzer = HealthAnalyzer(
    diagnostic_data=diag_data,
    computer_history=history_data,
    computer_inventory=inventory_data
)

# Generate health scorecard
scorecard = analyzer.generate_health_scorecard()
print(f"Overall Score: {scorecard.overall_score}")
print(f"Grade: {scorecard.grade}")
```

### SOFA Integration

```python
from jamfmcp.sofa import get_sofa_feed, get_cves_for_version

# Fetch latest SOFA data
feed_data = await get_sofa_feed()
sofa_feed = parse_sofa_feed(feed_data)

# Check CVEs for a specific version
affecting_cves, exploited_cves = get_cves_for_version(
    sofa_feed,
    current_version="14.2.0",
    os_family="Sonoma 14"
)
```

## Architecture

The JamfMCP architecture consists of several interconnected components:

- **MCP Client** → **FastMCP Server**: Client connections via MCP protocol
- **FastMCP Server** → **Tool Functions**: Request routing to appropriate tools
- **Tool Functions** → **JamfApi**: API operations management
- **JamfApi** → **JamfAuth**: Authentication handling
- **JamfApi** → **Jamf Pro API**: External API communication
- **Tool Functions** → **HealthAnalyzer**: Health metrics processing
- **Tool Functions** → **SOFA Integration**: Security analysis
- **SOFA Integration** → **SOFA Feed API**: Vulnerability data retrieval

## Error Handling

All API methods follow consistent error handling patterns:

```python
try:
    result = await api.some_method()
except JamfApiError as e:
    # Handle API-specific errors
    print(f"API Error: {e.message}")
except AuthenticationError as e:
    # Handle auth failures
    print(f"Auth Error: {e.message}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected Error: {e}")
```

## Type Safety

JamfMCP uses type hints throughout for better IDE support and runtime validation:

```python
from typing import Any

async def get_computer_inventory(
    serial: str,
    sections: list[str] | None = None
) -> dict[str, Any]:
    """Type-safe function signature"""
    pass
```

## Async Patterns

All API methods are async for optimal performance:

```python
# Sequential (slower)
inventory1 = await api.get_computer_inventory("ABC123")
inventory2 = await api.get_computer_inventory("XYZ789")

# Parallel (faster)
import asyncio
inventories = await asyncio.gather(
    api.get_computer_inventory("ABC123"),
    api.get_computer_inventory("XYZ789")
)
```

## Next Steps

Explore the detailed API documentation:
- [Server Module](server) - All MCP tools
- [Health Analyzer](health-analyzer) - Health scoring system
- [SOFA Module](sofa) - CVE tracking

:::{seealso}
- [FastMCP API Documentation](https://gofastmcp.com/servers/core-components)
- [Jamf Pro API Reference](https://developer.jamf.com/jamf-pro/reference)
- [Pydantic Documentation](https://docs.pydantic.dev/)
:::

```{toctree}
:caption: Health Analyzation
:hidden:
:maxdepth: 3

health-enums
health-models
health-analyzer
```

```{toctree}
:caption: SOFA Integration
:hidden:
:maxdepth: 3

sofa-models
sofa
```

```{toctree}
:caption: MCP Server module
:hidden:
:maxdepth: 3

server
```
