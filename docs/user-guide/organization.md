# Organization Tools

:::{rst-class} lead
Tools for accessing organizational data including buildings, departments, users, groups, and sites.
:::

## Buildings & Locations

(get_buildings)=
### Get Buildings

List all buildings configured in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
List all buildings in our organization
:::

:::{ai-prompt}
Show me all office locations
:::

:::{ai-prompt}
Get addresses for all buildings
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Building Details
:link: get_building_details
:link-type: ref

Detailed building information
::::

::::{grid-item-card} Get Departments
:link: get_departments
:link-type: ref

Department assignments
::::
:::::

---

(get_building_details)=
### Get Building Details

Get detailed information about a specific building.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `building_id`
    - int | str
    - **Yes**
    - Building ID
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
Get details for building ID 1
:::

:::{ai-prompt}
Show me how many computers are assigned to building 5
:::

:::{ai-prompt}
Get the full address for building ID 10
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Buildings
:link: get_buildings
:link-type: ref

List all buildings
::::

::::{grid-item-card} Search Computers
:link: search_computers
:link-type: ref

Find computers by building
::::
:::::

---

## Departments

(get_departments)=
### Get Departments

List all departments configured in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
List all departments in the organization
:::

:::{ai-prompt}
Show me all departments and when they were created
:::

:::{ai-prompt}
Get department names and IDs
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Department Details
:link: get_department_details
:link-type: ref

Detailed department information
::::

::::{grid-item-card} Get Users
:link: get_users
:link-type: ref

Users by department
::::
:::::

---

(get_department_details)=
### Get Department Details

Get detailed information about a specific department.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `department_id`
    - int | str
    - **Yes**
    - Department ID
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
Get details for department ID 1
:::

:::{ai-prompt}
How many computers are assigned to department 5?
:::

:::{ai-prompt}
Show me user count for Engineering department
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Departments
:link: get_departments
:link-type: ref

List all departments
::::

::::{grid-item-card} Search Computers
:link: search_computers
:link-type: ref

Find computers by department
::::
:::::

---

## Users & Groups

(get_users)=
### Get Users

List all users in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
[
  {
    "id": 1,
    "username": "john.doe",
    "full_name": "John Doe",
    "email": "john.doe@company.com",
    "phone_number": "555-1234",
    "position": "Senior Engineer",
    "enable_custom_photo_url": false,
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
:::

#### Usage Examples

:::{ai-prompt}
List all users in Jamf Pro
:::

:::{ai-prompt}
Show me all users with their email addresses
:::

:::{ai-prompt}
Get all users and their positions
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get User Details
:link: get_user_details
:link-type: ref

Detailed user information
::::

::::{grid-item-card} Get User Group Details
:link: get_user_group_details
:link-type: ref

User group memberships
::::
:::::

---

(get_user_details)=
### Get User Details

Get detailed information about a specific user.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `user_id`
    - str
    - **Yes**
    - User ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "username": "john.doe",
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "email_address": "john.doe@company.com",
  "phone_number": "555-1234",
  "position": "Senior Engineer",
  "enable_custom_photo_url": false,
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
:::

#### Usage Examples

:::{ai-prompt}
Get details for user ID 1
:::

:::{ai-prompt}
Show me which computers are assigned to user john.doe
:::

:::{ai-prompt}
Get employee ID for user 100
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Users
:link: get_users
:link-type: ref

List all users
::::

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Computer assignments
::::
:::::

---

(get_user_group_details)=
### Get User Group Details

Get detailed information about a user group.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `group_id`
    - int | str
    - **Yes**
    - User group ID
:::

:::{dropdown} Example Response

```json
{
  "id": 10,
  "name": "Engineering Team",
  "is_smart": true,
  "is_notify_on_change": false,
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
:::

#### Usage Examples

:::{ai-prompt}
Get details for user group ID 10
:::

:::{ai-prompt}
Show me all members of the Engineering Team group
:::

:::{ai-prompt}
What are the criteria for user group 5?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Users
:link: get_users
:link-type: ref

List all users
::::

::::{grid-item-card} Get Smart Groups
:link: get_smart_groups
:link-type: ref

Computer groups
::::
:::::

---

## Sites

(get_sites)=
### Get Sites

List all sites configured in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
List all sites in Jamf Pro
:::

:::{ai-prompt}
Show me all configured sites
:::

:::{ai-prompt}
Get site names and IDs
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Site Details
:link: get_site_details
:link-type: ref

Detailed site information
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Site-specific policies
::::
:::::

---

(get_site_details)=
### Get Site Details

Get detailed information about a specific site.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `site_id`
    - str | int
    - **Yes**
    - Site ID
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
Get details for site ID 1
:::

:::{ai-prompt}
How many computers are assigned to site 2?
:::

:::{ai-prompt}
Show me all objects assigned to the West Coast site
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Sites
:link: get_sites
:link-type: ref

List all sites
::::

::::{grid-item-card} Get Configuration Profiles
:link: get_configuration_profiles
:link-type: ref

Site-specific profiles
::::
:::::

---

(get_categories)=
### Get Categories

List all categories used for organizing items.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
List all categories
:::

:::{ai-prompt}
Show me categories sorted by priority
:::

:::{ai-prompt}
Get all category names and IDs
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Category Details
:link: get_category_details
:link-type: ref

Category usage information
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Policies by category
::::
:::::

---

(get_category_details)=
### Get Category Details

Get detailed information about a specific category.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `category_id`
    - str | int
    - **Yes**
    - Category ID
:::

:::{dropdown} Example Response

```json
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
:::

#### Usage Examples

:::{ai-prompt}
Get details for category ID 2
:::

:::{ai-prompt}
How many policies use category 5?
:::

:::{ai-prompt}
Show me usage statistics for the Security category
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Categories
:link: get_categories
:link-type: ref

List all categories
::::

::::{grid-item-card} Get Scripts
:link: get_scripts
:link-type: ref

Scripts by category
::::
:::::

---

## Network Segments

(get_network_segments)=
### Get Network Segments

List all network segments configured in Jamf Pro.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   -
    -
    -
    - No parameters required
:::

:::{dropdown} Example Response

```json
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
    "override_buildings": false,
    "override_departments": false
  },
  {
    "id": 2,
    "name": "Guest WiFi",
    "starting_address": "192.168.1.0",
    "ending_address": "192.168.1.255"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all network segments
:::

:::{ai-prompt}
Show me IP ranges for all network segments
:::

:::{ai-prompt}
Get network segments by building
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Network Segment Details
:link: get_network_segment_details
:link-type: ref

Detailed segment information
::::

::::{grid-item-card} Get Buildings
:link: get_buildings
:link-type: ref

Building associations
::::
:::::

---

(get_network_segment_details)=
### Get Network Segment Details

Get detailed information about a specific network segment.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `segment_id`
    - str | int
    - **Yes**
    - Network segment ID
:::

:::{dropdown} Example Response

```json
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
  "override_buildings": false,
  "override_departments": false,
  "assigned_computers": 245
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for network segment ID 1
:::

:::{ai-prompt}
How many computers are on network segment 5?
:::

:::{ai-prompt}
Show me the IP range for the Corporate LAN segment
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Network Segments
:link: get_network_segments
:link-type: ref

List all segments
::::

::::{grid-item-card} Get Building Details
:link: get_building_details
:link-type: ref

Building information
::::
:::::

---

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

:::{seealso}
- [Jamf Pro Buildings API](https://developer.jamf.com/jamf-pro/reference/get_v1-buildings)
- [Jamf Pro Departments API](https://developer.jamf.com/jamf-pro/reference/get_v1-departments)
- [Jamf Pro Users API](https://developer.jamf.com/jamf-pro/reference/get_v1-users)
- [Jamf Pro Sites Documentation](https://docs.jamf.com/jamf-pro/documentation/Sites.html)
:::
