# Server Module

The `jamfmcp.server` module contains the FastMCP server implementation with all available MCP tools.

## Available Tools

The server exposes 49 tools organized into categories. These tools are decorated with `@mcp.tool` which transforms them into MCP-compatible tools. For detailed documentation of each tool, see the user guides.

### Tool Categories

#### Computer Health Tools (4 tools)
- `get_health_scorecard` - Generate comprehensive health scorecards
- `get_basic_diagnostics` - Get basic diagnostic information
- `get_cves` - Analyze CVE vulnerabilities
- `get_compliance_status` - Check compliance status

📖 See [Computer Health Tools](../user-guide/computer-health) for detailed documentation.

#### Inventory Management Tools (3 tools)
- `get_computer_inventory` - Get detailed computer inventory
- `get_computer_history` - Get computer history
- `search_computers` - Search for computers

📖 See [Inventory Management Tools](../user-guide/inventory) for detailed documentation.

#### Policy & Configuration Tools (11 tools)
- `get_policies` - List all policies
- `get_policy_details` - Get policy details
- `get_configuration_profiles` - List configuration profiles
- `get_profile_details` - Get profile details
- `get_scripts` - List scripts
- `get_script_details` - Get script details
- `get_packages` - List packages
- `get_package_details` - Get package details
- `get_patch_software_titles` - List patch software titles
- `get_patch_software_title_details` - Get patch title details
- `get_patch_policies` - List patch policies

📖 See [Policy & Configuration Tools](../user-guide/policies) for detailed documentation.

#### Security & Compliance Tools (5 tools)
- `get_restricted_software` - List restricted software
- `get_restricted_software_details` - Get restricted software details
- `get_licensed_software` - List licensed software
- `get_licensed_software_details` - Get licensed software details
- `get_device_lock_pin` - Get device lock PIN

📖 See [Security & Compliance Tools](../user-guide/security) for detailed documentation.

#### Organization Management Tools (13 tools)
- `get_buildings` - List buildings
- `get_building_details` - Get building details
- `get_departments` - List departments
- `get_department_details` - Get department details
- `get_users` - List users
- `get_user_details` - Get user details
- `get_user_group_details` - Get user group details
- `get_sites` - List sites
- `get_site_details` - Get site details
- `get_categories` - List categories
- `get_category_details` - Get category details
- `get_network_segments` - List network segments
- `get_network_segment_details` - Get network segment details

📖 See [Organization Tools](../user-guide/organization) for detailed documentation.

#### Utility Tools (13 tools)
- `get_jcds_files` - List JCDS files
- `get_webhooks` - List webhooks
- `get_webhook_details` - Get webhook details
- `get_ldap_servers` - List LDAP servers
- `get_ldap_server_details` - Get LDAP server details
- `get_directory_bindings` - List directory bindings
- `get_directory_binding_details` - Get directory binding details
- `get_advanced_computer_searches` - List advanced searches
- `get_advanced_computer_search_details` - Get search details
- `get_smart_groups` - List smart groups
- `get_group_details` - Get group details
- `get_extension_attributes` - List extension attributes
- `ping` - Ping the server

📖 See [Utility Tools](../user-guide/utility) for detailed documentation.

## Logging

The module uses Python's standard logging:

```python
import logging

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## Running the Server

The server can be run directly:

```python
if __name__ == "__main__":
    mcp.run()
```

Or through FastMCP:

```bash
fastmcp run src/jamfmcp/server.py:mcp
```

## Environment Variables

The server uses environment variables for configuration:

- `JAMF_URL` - Jamf Pro server URL
- `JAMF_CLIENT_ID` - Client ID for OAuth
- `JAMF_CLIENT_SECRET` - Client secret for OAuth

## Performance Considerations

- Tools use async/await for non-blocking operations
- API calls are rate-limited by Jamf Pro
- Large result sets are paginated automatically
- Caching is handled at the API client level

## Testing

Tools can be tested individually:

```python
import asyncio
from jamfmcp.server import get_health_scorecard

async def test():
    result = await get_health_scorecard(serial="ABC123")
    print(result)

asyncio.run(test())
```
