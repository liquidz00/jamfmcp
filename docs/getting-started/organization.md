# Organization Tools

These tools provide access to organizational data including buildings, departments, users, groups, and sites.

:::{note}
**About JSON Response Schemas**

The JSON examples throughout this document show the structure of data that JamfMCP returns. When using these tools through an AI assistant, you won't see raw JSON - the AI will interpret and present this information in a natural, conversational format.
:::

## Buildings & Locations

### get_buildings

List all buildings configured in Jamf Pro.

**Tool:** `get_buildings`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Headquarters",
        "street_address1": "123 Main Street",
        "street_address2": "Suite 100",
        "city": "San Francisco",
        "state_province": "CA",
        "zip_postal_code": "94105",
        "country": "United States"
    },
    {
        "id": 2,
        "name": "East Coast Office",
        "street_address1": "456 Broadway",
        "city": "New York",
        "state_province": "NY",
        "zip_postal_code": "10013",
        "country": "United States"
    }
]
```

### get_building_details

Get detailed information about a specific building.

**Tool:** `get_building_details`

**Parameters:**
- `building_id` (int | str, required): Building ID

**Returns:**
```python
{
    "id": 1,
    "name": "Headquarters",
    "street_address1": "123 Main Street",
    "street_address2": "Suite 100",
    "city": "San Francisco",
    "state_province": "CA",
    "zip_postal_code": "94105",
    "country": "United States",
    "assigned_computers": 245,
    "assigned_users": 198,
    "assigned_devices": 312
}
```

## Departments

### get_departments

List all departments configured in Jamf Pro.

**Tool:** `get_departments`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Engineering",
        "created_date": "2023-01-15T00:00:00Z",
        "updated_date": "2024-01-10T00:00:00Z"
    },
    {
        "id": 2,
        "name": "Sales",
        "created_date": "2023-01-15T00:00:00Z",
        "updated_date": "2023-12-01T00:00:00Z"
    },
    {
        "id": 3,
        "name": "Human Resources",
        "created_date": "2023-01-15T00:00:00Z",
        "updated_date": "2023-06-15T00:00:00Z"
    }
]
```

### get_department_details

Get detailed information about a specific department.

**Tool:** `get_department_details`

**Parameters:**
- `department_id` (int | str, required): Department ID

**Returns:**
```python
{
    "id": 1,
    "name": "Engineering",
    "created_date": "2023-01-15T00:00:00Z",
    "updated_date": "2024-01-10T00:00:00Z",
    "assigned_computers": 87,
    "assigned_users": 92,
    "assigned_devices": 156
}
```

## Users & Groups

(get_users)=
### get_users

List all users in Jamf Pro.

**Tool:** `get_users`

**Returns:**
```python
[
    {
        "id": 1,
        "username": "john.doe",
        "full_name": "John Doe",
        "email": "john.doe@company.com",
        "phone_number": "555-1234",
        "position": "Senior Engineer",
        "enable_custom_photo_url": False,
        "custom_photo_url": "",
        "ldap_server": {
            "id": 1,
            "name": "Corporate AD"
        },
        "extension_attributes": []
    },
    {
        "id": 2,
        "username": "jane.smith",
        "full_name": "Jane Smith",
        "email": "jane.smith@company.com",
        "phone_number": "555-5678",
        "position": "Sales Manager"
    }
]
```
(get_user_details)=
### get_user_details

Get detailed information about a specific user.

**Tool:** `get_user_details`

**Parameters:**
- `user_id` (str, required): User ID

**Returns:**
```python
{
    "id": 1,
    "username": "john.doe",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "email_address": "john.doe@company.com",
    "phone_number": "555-1234",
    "position": "Senior Engineer",
    "enable_custom_photo_url": False,
    "custom_photo_url": "",
    "ldap_server": {
        "id": 1,
        "name": "Corporate AD"
    },
    "extension_attributes": [
        {
            "id": 1,
            "name": "Employee ID",
            "type": "String",
            "value": "EMP12345"
        }
    ],
    "sites": [],
    "managed_computers": [
        {
            "id": 123,
            "name": "John's MacBook Pro",
            "serial_number": "ABC123456"
        }
    ],
    "managed_mobile_devices": []
}
```

### get_user_group_details

Get detailed information about a user group.

**Tool:** `get_user_group_details`

**Parameters:**
- `group_id` (int | str, required): User group ID

**Returns:**
```python
{
    "id": 10,
    "name": "Engineering Team",
    "is_smart": True,
    "is_notify_on_change": False,
    "site": {
        "id": -1,
        "name": "None"
    },
    "criteria": [
        {
            "name": "Department",
            "priority": 0,
            "and_or": "and",
            "search_type": "is",
            "value": "Engineering"
        }
    ],
    "users": [
        {
            "id": 1,
            "username": "john.doe",
            "full_name": "John Doe",
            "email": "john.doe@company.com"
        }
    ],
    "user_count": 92
}
```

## Sites

### get_sites

List all sites configured in Jamf Pro.

**Tool:** `get_sites`

**Returns:**
```python
[
    {
        "id": -1,
        "name": "None"
    },
    {
        "id": 1,
        "name": "West Coast",
        "created_date": "2023-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "name": "East Coast",
        "created_date": "2023-01-01T00:00:00Z"
    }
]
```

### get_site_details

Get detailed information about a specific site.

**Tool:** `get_site_details`

**Parameters:**
- `site_id` (str | int, required): Site ID

**Returns:**
```python
{
    "id": 1,
    "name": "West Coast",
    "created_date": "2023-01-01T00:00:00Z",
    "updated_date": "2024-01-15T00:00:00Z",
    "assigned_objects": {
        "computers": 156,
        "mobile_devices": 203,
        "configuration_profiles": 25,
        "policies": 48,
        "users": 198
    }
}
```

## Categories

(get_categories)=
### get_categories

List all categories used for organizing items.

**Tool:** `get_categories`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Productivity",
        "priority": 9
    },
    {
        "id": 2,
        "name": "Security",
        "priority": 10
    },
    {
        "id": 3,
        "name": "Utilities",
        "priority": 5
    }
]
```

### get_category_details

Get detailed information about a specific category.

**Tool:** `get_category_details`

**Parameters:**
- `category_id` (str | int, required): Category ID

**Returns:**
```python
{
    "id": 2,
    "name": "Security",
    "priority": 10,
    "usage": {
        "policies": 15,
        "packages": 8,
        "scripts": 12,
        "printers": 0,
        "computer_extension_attributes": 3,
        "mobile_device_extension_attributes": 2
    }
}
```

## Network Segments

### get_network_segments

List all network segments configured in Jamf Pro.

**Tool:** `get_network_segments`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Corporate LAN",
        "starting_address": "10.0.0.0",
        "ending_address": "10.0.255.255",
        "distribution_server": "",
        "distribution_point": "",
        "url": "",
        "swu_server": "",
        "building": "Headquarters",
        "department": "",
        "override_buildings": False,
        "override_departments": False
    },
    {
        "id": 2,
        "name": "Guest WiFi",
        "starting_address": "192.168.1.0",
        "ending_address": "192.168.1.255"
    }
]
```

### get_network_segment_details

Get detailed information about a specific network segment.

**Tool:** `get_network_segment_details`

**Parameters:**
- `segment_id` (str | int, required): Network segment ID

**Returns:**
```python
{
    "id": 1,
    "name": "Corporate LAN",
    "starting_address": "10.0.0.0",
    "ending_address": "10.0.255.255",
    "distribution_server": "",
    "distribution_point": "Main DP",
    "url": "https://dp.company.com",
    "swu_server": "",
    "building": {
        "id": 1,
        "name": "Headquarters"
    },
    "department": {
        "id": -1,
        "name": "None"
    },
    "override_buildings": False,
    "override_departments": False,
    "assigned_computers": 245
}
```

## Common Use Cases

### Organizational Overview
```python
# Get organizational structure
buildings = await get_buildings()
departments = await get_departments()
sites = await get_sites()

print(f"Organization has:")
print(f"- {len(buildings)} buildings")
print(f"- {len(departments)} departments")
print(f"- {len(sites)} sites")

# Department breakdown
for dept in departments:
    details = await get_department_details(department_id=dept["id"])
    print(f"{dept['name']}: {details['assigned_computers']} computers")
```

### User Management Audit
```python
# Analyze user assignments
users = await get_users()

# Check for users without email
no_email = [u for u in users if not u.get("email")]
print(f"Users without email: {len(no_email)}")

# Find users with multiple computers
for user in users[:10]:  # Sample
    details = await get_user_details(user_id=str(user["id"]))
    computer_count = len(details.get("managed_computers", []))
    if computer_count > 1:
        print(f"{user['full_name']}: {computer_count} computers")
```

### Network Segment Analysis
```python
# Review network segments
segments = await get_network_segments()

for segment in segments:
    details = await get_network_segment_details(segment_id=segment["id"])
    print(f"{segment['name']}: {segment['starting_address']} - {segment['ending_address']}")
    print(f"  Assigned computers: {details.get('assigned_computers', 0)}")
    if segment.get("building"):
        print(f"  Building: {segment['building']}")
```

### Site-Based Reporting
```python
# Analyze site distribution
sites = await get_sites()

for site in sites:
    if site["id"] != -1:  # Skip "None" site
        details = await get_site_details(site_id=site["id"])
        objects = details["assigned_objects"]
        print(f"\n{site['name']}:")
        print(f"  Computers: {objects['computers']}")
        print(f"  Policies: {objects['policies']}")
        print(f"  Profiles: {objects['configuration_profiles']}")
```

### Category Usage
```python
# Review category utilization
categories = await get_categories()

# Sort by priority
sorted_cats = sorted(categories, key=lambda x: x["priority"], reverse=True)

for cat in sorted_cats:
    details = await get_category_details(category_id=cat["id"])
    usage = details["usage"]
    total_usage = sum(usage.values())
    print(f"{cat['name']} (Priority {cat['priority']}): {total_usage} items")
```

## Best Practices

### Building Management
1. **Consistent Naming**: Use clear, consistent building names
2. **Complete Addresses**: Include full address for mapping
3. **Regular Updates**: Keep location info current
4. **Assignment Accuracy**: Ensure computers assigned correctly

### Department Organization
1. **Clear Structure**: Mirror actual org structure
2. **Avoid Duplicates**: Prevent similar department names
3. **Regular Audits**: Review assignments periodically
4. **Update Processes**: Have process for org changes

### User Management
1. **Data Completeness**: Ensure all users have email/phone
2. **LDAP Integration**: Leverage directory services
3. **Extension Attributes**: Use for additional user data
4. **Access Reviews**: Regular audit of user assignments

### Network Segmentation
1. **IP Range Accuracy**: Ensure ranges don't overlap
2. **Building Association**: Link segments to locations
3. **Distribution Points**: Configure for each segment
4. **Documentation**: Document segment purposes

## Integration Examples

### With Computer Inventory
```python
# Get computers by building
building = await get_building_details(building_id=1)
computers = await search_computers()

building_computers = [
    c for c in computers
    if c.get("building") == building["name"]
]
```

### With User Groups
```python
# Analyze department user groups
departments = await get_departments()

for dept in departments:
    # Find matching user group
    group_name = f"{dept['name']} Team"
    # Would need to get all groups and filter
    # This is a conceptual example
```

### With Policies
```python
# Check site-specific policies
sites = await get_sites()
policies = await get_policies()

for site in sites:
    if site["id"] != -1:
        site_policies = [
            p for p in policies
            if p.get("site", {}).get("id") == site["id"]
        ]
        print(f"{site['name']}: {len(site_policies)} policies")
```

## Related Tools

- [`get_computer_inventory`](#get_computer_inventory) - Computer assignments
- [`search_computers`](#search_computers) - Find by location
- [`get_policies`](#get_policies) - Site-specific policies
- [`get_smart_groups`](#get_smart_groups) - Department groups
- [`get_ldap_servers`](#get_ldap_servers) - User directory integration

:::{seealso}
- [Jamf Pro Buildings API](https://developer.jamf.com/jamf-pro/reference/get_v1-buildings)
- [Jamf Pro Departments API](https://developer.jamf.com/jamf-pro/reference/get_v1-departments)
- [Jamf Pro Users API](https://developer.jamf.com/jamf-pro/reference/get_v1-users)
- [Jamf Pro Sites Documentation](https://docs.jamf.com/jamf-pro/documentation/Sites.html)
:::
