# Inventory Management

:::{rst-class} lead
Tools for comprehensive computer inventory retrieval and search capabilities in Jamf Pro.
:::

(get_computer_inventory)=
## Get Computer Inventory

Retrieve detailed computer inventory information by serial number.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `serial_number`
    - str
    - **Yes**
    - The serial number of the computer to retrieve
:::

:::{dropdown} Example Response

```json
{
  "general": {
    "id": 123,
    "name": "John's MacBook Pro",
    "serial_number": "ABC123456",
    "udid": "12345678-1234-1234-1234-123456789012",
    "model": "MacBook Pro (16-inch, 2023)",
    "model_identifier": "Mac15,6",
    "last_check_in": "2024-01-15T10:30:00Z"
  },
  "hardware": {
    "make": "Apple",
    "model": "MacBook Pro",
    "processor": "Apple M3 Max",
    "processor_speed_mhz": 3500,
    "total_ram_mb": 32768,
    "battery_capacity": 95
  },
  "operating_system": {
    "name": "macOS",
    "version": "14.2.1",
    "build": "23C71"
  },
  "storage": {
    "disks": [{
      "device": "disk1s1",
      "model": "Apple SSD",
      "size_mb": 524288,
      "available_mb": 262144,
      "percentage_used": 50
    }]
  },
  "applications": [{
    "name": "Google Chrome",
    "version": "120.0.6099.129",
    "bundle_id": "com.google.Chrome"
  }]
}
```
:::

### Usage Examples

:::{ai-prompt}
Get the full inventory for computer with serial number ABC123
:::

:::{ai-prompt}
Show me hardware and storage details for serial XYZ789
:::

:::{ai-prompt}
Retrieve application inventory for computer ABC123
:::

### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Computer History
:link: get_computer_history
:link-type: ref

View policy logs and management history
::::

::::{grid-item-card} Search Computers
:link: search_computers
:link-type: ref

Find computers by various criteria
::::
:::::

---

(get_computer_history)=
## Get Computer History

Retrieve computer history including policy logs, management commands, and user activity.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `computer_id`
    - int | str
    - **Yes**
    - Computer JSS ID
:::


:::{dropdown} Example Response

```json
{
  "computer_id": 123,
  "general": {
    "name": "John's MacBook Pro",
    "serial_number": "ABC123456"
  },
  "policy_logs": [{
    "policy_id": 45,
    "policy_name": "Install Chrome",
    "status": "Completed",
    "date_completed": "2024-01-15T09:00:00Z",
    "username": "john.doe"
  }],
  "commands": [{
    "command": "Update Inventory",
    "status": "Completed",
    "issued": "2024-01-15T08:00:00Z",
    "completed": "2024-01-15T08:01:00Z"
  }],
  "user_location_history": [{
    "username": "john.doe",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "department": "Engineering",
    "building": "HQ",
    "date_assigned": "2023-06-01T00:00:00Z"
  }],
  "computer_usage_logs": [{
    "event": "Login",
    "username": "john.doe",
    "date": "2024-01-15T08:30:00Z"
  }]
}
```
:::

### Usage Examples

:::{ai-prompt}
Show me the policy execution history for computer ID 123
:::

:::{ai-prompt}
Get all management commands sent to computer 456 in the last month
:::

:::{ai-prompt}
Display user assignment history for computer ID 789
:::

### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Current inventory and configuration details
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

View all available policies
::::
:::::

---

(search_computers)=
## Search Computers

Search for computers using various criteria including name, serial number, or other attributes.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `identifier`
    - str
    - No
    - Search term (name or serial)
*   - `page_size`
    - str
    - No
    - Results per page (defaults to 100)
*   - `sections`
    - list[str]
    - No
    - Inventory sections to include
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 123,
    "name": "John's MacBook Pro",
    "serial_number": "ABC123456",
    "udid": "12345678-1234-1234-1234-123456789012",
    "model": "MacBook Pro",
    "os_version": "14.2.1",
    "last_check_in": "2024-01-15T10:30:00Z",
    "managed": true,
    "supervised": false
  },
  {
    "id": 124,
    "name": "Jane's MacBook Air",
    "serial_number": "XYZ789012",
    "model": "MacBook Air",
    "os_version": "14.2.1",
    "last_check_in": "2024-01-15T09:15:00Z",
    "managed": true,
    "supervised": true
  }
]
```
:::

### Usage Examples

:::{ai-prompt}
Find all computers with "MacBook Pro" in their name
:::

:::{ai-prompt}
Search for computers that haven't checked in for 30 days
:::

:::{ai-prompt}
List all computers in the inventory with their basic details
:::

### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Detailed information for specific computers
::::

::::{grid-item-card} Get Smart Groups
:link: get_smart_groups
:link-type: ref

Pre-configured computer groups
::::
:::::

---

## Inventory Sections Reference

:::{dropdown} Available Inventory Sections
:open:

| Section | Description | Key Data |
|---------|-------------|----------|
| **GENERAL** | Basic computer information | Name, serial, model, UDID |
| **DISK_ENCRYPTION** | FileVault status | Encryption state, recovery key |
| **PURCHASING** | Purchase and warranty info | PO number, warranty expiration |
| **APPLICATIONS** | Installed applications | App names, versions, bundle IDs |
| **STORAGE** | Disk usage details | Capacity, available space |
| **USER_AND_LOCATION** | Assignment information | User, department, building |
| **CONFIGURATION_PROFILES** | Installed profiles | Profile names, payloads |
| **HARDWARE** | Hardware specifications | CPU, RAM, battery |
| **SECURITY** | Security settings | SIP, Gatekeeper, Firewall |
| **OPERATING_SYSTEM** | OS details | Version, build, kernel |
| **EXTENSION_ATTRIBUTES** | Custom attributes | Organization-specific data |
| **GROUP_MEMBERSHIPS** | Group assignments | Smart and static groups |
:::

## Best Practices

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} {fas}`database` Data Freshness
Check `last_check_in` timestamps to assess data currency before making decisions.
::::

::::{grid-item-card} {fas}`filter` Selective Retrieval
Request only needed inventory sections to improve performance and reduce data transfer.
::::

::::{grid-item-card} {fas}`sync` Cache Awareness
Remember that Jamf Pro updates inventory on device check-in, not in real-time.
::::

::::{grid-item-card} {fas}`search` Smart Searching
Use specific identifiers when possible rather than broad searches for better performance.
::::
:::::

## Common Use Cases

### Hardware Audit

:::{ai-prompt}
Get hardware specifications for all computers with less than 16GB of RAM
:::

### Software Compliance

:::{ai-prompt}
Find all computers with Chrome installed and show their version numbers
:::

### User Assignment Tracking

:::{ai-prompt}
Show me all computers assigned to the Engineering department with their users
:::

:::{seealso}
- [Jamf Pro Computer Inventory API](https://developer.jamf.com/jamf-pro/docerence/get_v1-computers-inventory)
- [Jamf Pro API Documentation](https://developer.jamf.com/jamf-pro/docs)
- [Computer History API](https://developer.jamf.com/jamf-pro/docerence/get_v1-computers-inventory-detail-id)
:::
