# Inventory Management Tools

These tools provide comprehensive computer inventory retrieval and search capabilities.

:::{note}
**About Response Examples**

The JSON structures shown in this documentation represent the data format returned by JamfMCP. When using these tools through an AI assistant, this data will be interpreted and presented conversationally based on your request.
:::

## Available Tools

(get_computer_inventory)=
### Getting Computer Inventory

Retrieve detailed computer inventory information by serial number.

**Tool:** `get_computer_inventory`

Get detailed computer inventory information by serial number.

**Parameters:**
- `serial` (str, required): Computer serial number
- `sections` (list[str], optional): Specific inventory sections to retrieve

**Available Sections:**
- `GENERAL` - Basic computer information
- `DISK_ENCRYPTION` - FileVault status
- `PURCHASING` - Purchase and warranty info
- `APPLICATIONS` - Installed applications
- `STORAGE` - Disk usage details
- `USER_AND_LOCATION` - Assignment information
- `CONFIGURATION_PROFILES` - Installed profiles
- `PRINTERS` - Configured printers
- `SERVICES` - Running services
- `HARDWARE` - Hardware specifications
- `LOCAL_USER_ACCOUNTS` - Local accounts
- `CERTIFICATES` - Installed certificates
- `ATTACHMENTS` - File attachments
- `PLUGINS` - Browser plugins
- `PACKAGE_RECEIPTS` - Installed packages
- `FONTS` - Installed fonts
- `SECURITY` - Security settings
- `OPERATING_SYSTEM` - OS details
- `LICENSED_SOFTWARE` - License information
- `IBEACONS` - iBeacon configuration
- `SOFTWARE_UPDATES` - Available updates
- `EXTENSION_ATTRIBUTES` - Custom attributes
- `CONTENT_CACHING` - Content cache status
- `GROUP_MEMBERSHIPS` - Group assignments
- `ALL` - All sections (default)

**Returns:**
```python
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
    }],
    // ... additional sections based on request
}
```

(get_computer_history)=
### Getting Computer History

Retrieve computer history including policy logs, commands, and user activity.

**Tool:** `get_computer_history`

Get computer history including policy logs, management commands, and user activity.

**Parameters:**
- `computer_id` (int | str, required): Computer JSS ID

**Returns:**
```python
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
    "app_store_history": [{
        "app": "Keynote",
        "version": "13.2",
        "deployed": "2024-01-10T14:00:00Z"
    }],
    "screen_sharing_logs": [],
    "remote_desktop_logs": [],
    "computer_usage_logs": [{
        "event": "Login",
        "username": "john.doe",
        "date": "2024-01-15T08:30:00Z"
    }]
}
```

(search_computers)=
### Searching for Computers

Search for computers by name or serial number.

**Tool:** `search_computers`

Search for computers using various criteria.

**Parameters:**
- `identifier` (str, optional): Search term for name or serial
- `page_size` (str, optional): Results per page (default: "100")
- `sections` (list[str], optional): Inventory sections to include

**Returns:**
```python
[
    {
        "id": 123,
        "name": "John's MacBook Pro",
        "serial_number": "ABC123456",
        "udid": "12345678-1234-1234-1234-123456789012",
        "model": "MacBook Pro",
        "os_version": "14.2.1",
        "last_check_in": "2024-01-15T10:30:00Z",
        "managed": True,
        "supervised": False
    },
    {
        "id": 124,
        "name": "Jane's MacBook Air",
        "serial_number": "XYZ789012",
        // ... similar structure
    }
]
```

## Cache Considerations

- Inventory data is not cached by JamfMCP
- Jamf Pro updates inventory on device check-in
- Consider check-in frequency when analyzing data
- Use `last_check_in` to assess data freshness

## Related Tools

- [`get_health_scorecard`](#get_health_scorecard) - Analyze computer health
- [`get_basic_diagnostics`](#get_basic_diagnostics) - Quick diagnostics
- [`get_policies`](#get_policies) - View assigned policies
- [`get_configuration_profiles`](#get_configuration_profiles) - Check profiles
- [`get_user_details`](#get_user_details) - User information

:::{seealso}
- [Jamf Pro Computer Inventory API](https://developer.jamf.com/jamf-pro/reference/get_v1-computers-inventory)
- [Jamf Pro API Documentation](https://developer.jamf.com/jamf-pro/docs)
- [Computer History API](https://developer.jamf.com/jamf-pro/reference/get_v1-computers-inventory-detail-id)
:::
