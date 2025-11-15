# Utility Tools

:::{rst-class} lead
Additional utility and management tools for JCDS files, webhooks, LDAP integration, and system utilities.
:::

## File Management

(get_jcds_files)=
### Get JCDS Files

List all files stored in Jamf Cloud Distribution Service (JCDS).

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
    "id": "abc123def456",
    "name": "Company_Logo.png",
    "size": 45678,
    "md5": "d41d8cd98f00b204e9800998ecf8427e",
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "region": "us-east-1",
    "created": "2024-01-10T10:00:00Z",
    "modified": "2024-01-10T10:00:00Z"
  },
  {
    "id": "xyz789ghi012",
    "name": "Self_Service_Banner.jpg",
    "size": 123456,
    "md5": "5d41402abc4b2a76b9719d911017c592",
    "region": "us-east-1",
    "created": "2024-01-05T14:30:00Z"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all files in JCDS
:::

:::{ai-prompt}
Show me all images stored in Jamf Cloud Distribution Service
:::

:::{ai-prompt}
Get all JCDS files with their sizes and checksums
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Packages
:link: get_packages
:link-type: ref

Package files in Jamf Pro
::::

::::{grid-item-card} Get Scripts
:link: get_scripts
:link-type: ref

Script files in Jamf Pro
::::
:::::

---

## Webhook Management

(get_webhooks)=
### Get Webhooks

List all configured webhooks.

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
    "name": "Slack Notifications",
    "enabled": true,
    "url": "https://hooks.slack.com/services/...",
    "content_type": "application/json",
    "event": "ComputerAdded",
    "connection_timeout": 5000,
    "read_timeout": 5000
  },
  {
    "id": 2,
    "name": "ServiceNow Integration",
    "enabled": true,
    "url": "https://instance.service-now.com/api/...",
    "event": "ComputerCheckIn",
    "authentication_type": "Basic",
    "username": "jamf_integration"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all webhooks
:::

:::{ai-prompt}
Show me all enabled webhooks
:::

:::{ai-prompt}
Get webhooks configured for Slack notifications
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Webhook Details
:link: get_webhook_details
:link-type: ref

Detailed webhook configuration
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Webhook triggers from policies
::::
:::::

---

(get_webhook_details)=
### Get Webhook Details

Get detailed information about a specific webhook.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `webhook_id`
    - str | int
    - **Yes**
    - Webhook ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Slack Notifications",
  "enabled": true,
  "url": "https://hooks.slack.com/services/...",
  "content_type": "application/json",
  "event": "ComputerAdded",
  "connection_timeout": 5000,
  "read_timeout": 5000,
  "authentication_type": "None",
  "username": "",
  "enable_display_fields_for_group_object": false,
  "smart_group": {
    "id": -1,
    "name": "None"
  },
  "display_fields": [
    {
      "name": "general",
      "inventory_display": {
        "id": "general"
      }
    },
    {
      "name": "hardware",
      "inventory_display": {
        "id": "hardware"
      }
    }
  ]
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for webhook ID 1
:::

:::{ai-prompt}
Show me the configuration for webhook 5
:::

:::{ai-prompt}
What events trigger webhook ID 10?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Webhooks
:link: get_webhooks
:link-type: ref

List all webhooks
::::

::::{grid-item-card} Get Smart Groups
:link: get_smart_groups
:link-type: ref

Groups used in webhooks
::::
:::::

---

## Directory Services

(get_ldap_servers)=
### Get LDAP Servers

List all configured LDAP servers.

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
    "name": "Corporate Active Directory",
    "hostname": "ldap.company.com",
    "port": 389,
    "use_ssl": true,
    "authentication_type": "Simple",
    "account": "CN=JamfLDAP,OU=ServiceAccounts,DC=company,DC=com",
    "use_wildcards": true,
    "connection_timeout": 15,
    "search_timeout": 60,
    "referral_response": "Follow"
  },
  {
    "id": 2,
    "name": "Azure AD",
    "hostname": "ldaps.company.com",
    "port": 636,
    "use_ssl": true
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all LDAP servers
:::

:::{ai-prompt}
Show me Active Directory configurations
:::

:::{ai-prompt}
Get all LDAP servers using SSL
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get LDAP Server Details
:link: get_ldap_server_details
:link-type: ref

Detailed LDAP configuration
::::

::::{grid-item-card} Get Users
:link: get_users
:link-type: ref

LDAP-synced users
::::
:::::

---

(get_ldap_server_details)=
### Get LDAP Server Details

Get detailed information about a specific LDAP server.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `server_id`
    - str | int
    - **Yes**
    - LDAP server ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Corporate Active Directory",
  "hostname": "ldap.company.com",
  "port": 389,
  "use_ssl": true,
  "authentication_type": "Simple",
  "account": "CN=JamfLDAP,OU=ServiceAccounts,DC=company,DC=com",
  "use_wildcards": true,
  "connection_timeout": 15,
  "search_timeout": 60,
  "referral_response": "Follow",
  "mappings": {
    "user_mappings": {
      "user_id": "sAMAccountName",
      "username": "sAMAccountName",
      "real_name": "displayName",
      "email_address": "mail",
      "department": "department",
      "building": "physicalDeliveryOfficeName",
      "room": "roomNumber",
      "telephone": "telephoneNumber",
      "position": "title"
    },
    "user_group_mappings": {
      "object_classes": "group",
      "search_base": "DC=company,DC=com",
      "search_scope": "All Subtrees",
      "group_id": "cn",
      "group_name": "cn"
    }
  },
  "connection": {
    "open_close_timeout": 15,
    "search_timeout": 60,
    "use_referrals": true,
    "test_successful": true,
    "test_date": "2024-01-15T10:00:00Z"
  }
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for LDAP server ID 1
:::

:::{ai-prompt}
Show me the user mappings for LDAP server 2
:::

:::{ai-prompt}
Check if LDAP server 1 connection test was successful
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get LDAP Servers
:link: get_ldap_servers
:link-type: ref

List all LDAP servers
::::

::::{grid-item-card} Get Directory Bindings
:link: get_directory_bindings
:link-type: ref

Directory binding configurations
::::
:::::

---

(get_directory_bindings)=
### Get Directory Bindings

List all directory binding configurations.

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
    "name": "Active Directory Binding",
    "priority": 1,
    "domain": "COMPANY.COM",
    "username": "jamfbind",
    "computer_ou": "CN=Computers,DC=company,DC=com",
    "type": "Active Directory"
  },
  {
    "id": 2,
    "name": "OpenDirectory Binding",
    "priority": 2,
    "server": "od.company.com",
    "type": "Open Directory"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all directory bindings
:::

:::{ai-prompt}
Show me Active Directory bindings
:::

:::{ai-prompt}
Get directory binding priorities
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Directory Binding Details
:link: get_directory_binding_details
:link-type: ref

Detailed binding configuration
::::

::::{grid-item-card} Get LDAP Servers
:link: get_ldap_servers
:link-type: ref

LDAP server configurations
::::
:::::

---

(get_directory_binding_details)=
### Get Directory Binding Details

Get detailed information about a specific directory binding.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `binding_id`
    - str | int
    - **Yes**
    - Directory binding ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Active Directory Binding",
  "priority": 1,
  "domain": "COMPANY.COM",
  "username": "jamfbind",
  "computer_ou": "CN=Computers,DC=company,DC=com",
  "type": "Active Directory",
  "open_close_timeout": 15,
  "mapping": {
    "uid": "sAMAccountName",
    "user_gid": "primaryGroupID",
    "gid": "primaryGroupID",
    "preferred_domain_controller": "",
    "preferred_domain_controller_port": 389
  },
  "cache": {
    "cache_last_user": true,
    "require_confirmation": false,
    "local_home": false,
    "use_unc_path": true,
    "mount_style": "SMB",
    "default_shell": "/bin/bash"
  },
  "administrative": {
    "preferred_domain_controller": "",
    "allowed_groups": "Domain Admins,Enterprise Admins",
    "authentication_from_any_domain": true,
    "packet_signing": "Allow",
    "packet_encryption": "Allow",
    "password_interval": 14,
    "restrict_ddns": false,
    "namespace": "Domain"
  }
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for directory binding ID 1
:::

:::{ai-prompt}
Show me the cache settings for binding 2
:::

:::{ai-prompt}
What is the computer OU for Active Directory binding?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Directory Bindings
:link: get_directory_bindings
:link-type: ref

List all bindings
::::

::::{grid-item-card} Get LDAP Server Details
:link: get_ldap_server_details
:link-type: ref

LDAP server details
::::
:::::

---

## Advanced Search

(get_advanced_computer_searches)=
### Get Advanced Computer Searches

List all advanced computer searches.

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
    "name": "Computers with Low Disk Space",
    "criteria": [
      {
        "name": "Available MB",
        "priority": 0,
        "and_or": "and",
        "search_type": "less than",
        "value": "10240"
      }
    ],
    "display_fields": ["Computer Name", "Available MB", "Last Check-in"],
    "site": {
      "id": -1,
      "name": "None"
    }
  },
  {
    "id": 2,
    "name": "Non-Compliant Computers",
    "criteria": [
      {
        "name": "FileVault 2 Status",
        "priority": 0,
        "and_or": "and",
        "search_type": "is not",
        "value": "Enabled"
      }
    ]
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all advanced computer searches
:::

:::{ai-prompt}
Show me saved searches for compliance
:::

:::{ai-prompt}
Get all advanced searches with their criteria
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Advanced Computer Search Details
:link: get_advanced_computer_search_details
:link-type: ref

Search results and details
::::

::::{grid-item-card} Search Computers
:link: search_computers
:link-type: ref

Direct computer search
::::
:::::

---

(get_advanced_computer_search_details)=
### Get Advanced Computer Search Details

Get details about a specific advanced computer search.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `search_id`
    - str | int
    - **Yes**
    - Advanced search ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "Computers with Low Disk Space",
  "view_as": "Standard Web Page",
  "sort_1": "Available MB",
  "sort_2": "",
  "sort_3": "",
  "criteria": [
    {
      "name": "Available MB",
      "priority": 0,
      "and_or": "and",
      "search_type": "less than",
      "value": "10240",
      "opening_paren": false,
      "closing_paren": false
    }
  ],
  "display_fields": [
    "Computer Name",
    "Available MB",
    "Last Check-in",
    "Username",
    "Operating System"
  ],
  "computers": [
    {
      "id": 123,
      "name": "John-MacBook-Pro",
      "udid": "12345678-1234-1234-1234-123456789012",
      "Computer_Name": "John-MacBook-Pro",
      "Available_MB": "5234",
      "Last_Check_in": "2024-01-15 10:30:00",
      "Username": "john.doe",
      "Operating_System": "14.2.1"
    }
  ],
  "site": {
    "id": -1,
    "name": "None"
  }
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get results for advanced search ID 1
:::

:::{ai-prompt}
Show me computers matching search 5
:::

:::{ai-prompt}
What are the criteria for advanced search ID 10?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Advanced Computer Searches
:link: get_advanced_computer_searches
:link-type: ref

List all searches
::::

::::{grid-item-card} Get Smart Groups
:link: get_smart_groups
:link-type: ref

Smart computer groups
::::
:::::

---

## Computer Groups

(get_smart_groups)=
### Get Smart Groups

List all smart computer groups.

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
    "name": "All Managed Computers",
    "is_smart": true,
    "criteria": [
      {
        "name": "Managed",
        "priority": 0,
        "and_or": "and",
        "search_type": "is",
        "value": "Managed"
      }
    ],
    "site": {
      "id": -1,
      "name": "None"
    }
  },
  {
    "id": 2,
    "name": "macOS 14 Computers",
    "is_smart": true,
    "criteria": [
      {
        "name": "Operating System Version",
        "priority": 0,
        "and_or": "and",
        "search_type": "like",
        "value": "14."
      }
    ]
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all smart computer groups
:::

:::{ai-prompt}
Show me groups based on OS version
:::

:::{ai-prompt}
Get all smart groups with their criteria
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Group Details
:link: get_group_details
:link-type: ref

Group members and details
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Policies scoped to groups
::::
:::::

---

(get_group_details)=
### Get Smart Group Details

Get detailed information about a computer group.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `group_id`
    - str
    - **Yes**
    - Computer group ID
:::

:::{dropdown} Example Response

```json
{
  "id": 1,
  "name": "All Managed Computers",
  "is_smart": true,
  "criteria": [
    {
      "name": "Managed",
      "priority": 0,
      "and_or": "and",
      "search_type": "is",
      "value": "Managed",
      "opening_paren": false,
      "closing_paren": false
    }
  ],
  "site": {
    "id": -1,
    "name": "None"
  },
  "computers": [
    {
      "id": 123,
      "name": "John-MacBook-Pro",
      "serial_number": "ABC123456",
      "mac_address": "00:11:22:33:44:55"
    }
  ],
  "computer_count": 245
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for smart group ID 1
:::

:::{ai-prompt}
Show me all computers in group 5
:::

:::{ai-prompt}
How many computers are in the macOS 14 group?
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Smart Groups
:link: get_smart_groups
:link-type: ref

List all smart groups
::::

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Computer group memberships
::::
:::::

---

(get_extension_attributes)=
### Get Extension Attributes

List all computer extension attributes.

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
    "name": "Battery Cycle Count",
    "enabled": true,
    "description": "Returns the battery cycle count",
    "data_type": "Integer",
    "input_type": "Script",
    "inventory_display": "Hardware"
  },
  {
    "id": 2,
    "name": "Time Machine Status",
    "enabled": true,
    "description": "Checks if Time Machine is configured",
    "data_type": "String",
    "input_type": "Script",
    "inventory_display": "Operating System"
  }
]
```
:::

#### Usage Examples

:::{ai-prompt}
List all extension attributes
:::

:::{ai-prompt}
Show me enabled extension attributes
:::

:::{ai-prompt}
Get all script-based extension attributes
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Extension attribute values
::::

::::{grid-item-card} Get Scripts
:link: get_scripts
:link-type: ref

Scripts used in attributes
::::
:::::

---

## System Utilities

(ping)=
### Ping

Simple ping test to verify MCP server connectivity.

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
{
  "message": "pong",
  "status": "ok"
}
```
:::

#### Usage Examples

:::{ai-prompt}
Ping the MCP server
:::

:::{ai-prompt}
Test server connectivity
:::

:::{ai-prompt}
Verify the MCP server is responding
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Health Scorecard
:link: get_health_scorecard
:link-type: ref

Full system health check
::::

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Verify data retrieval
::::
:::::

---

## Best Practices

### Webhook Security
1. **Use HTTPS**: Always use HTTPS endpoints
2. **Authentication**: Configure authentication
3. **Timeout Settings**: Set appropriate timeouts
4. **Error Handling**: Monitor webhook failures
5. **Payload Size**: Be aware of size limits

### LDAP Configuration
1. **Use SSL/TLS**: Always encrypt LDAP traffic
2. **Service Accounts**: Use dedicated accounts
3. **Search Optimization**: Configure search bases
4. **Connection Testing**: Regularly test connections
5. **Timeout Values**: Set reasonable timeouts

### Advanced Searches
1. **Performance**: Avoid overly complex criteria
2. **Naming Convention**: Use descriptive names
3. **Regular Review**: Audit saved searches
4. **Display Fields**: Only include needed fields
5. **Site Scoping**: Use sites to limit scope

### Extension Attributes
1. **Script Efficiency**: Optimize script performance
2. **Error Handling**: Handle script failures gracefully
3. **Data Types**: Use appropriate data types
4. **Documentation**: Document attribute purpose
5. **Regular Audits**: Review for unused attributes

:::{seealso}
- [Jamf Pro Webhooks](https://docs.jamf.com/jamf-pro/documentation/Webhooks.html)
- [LDAP Integration](https://docs.jamf.com/jamf-pro/documentation/Integrating_with_LDAP_Directory_Services.html)
- [Advanced Computer Searches](https://docs.jamf.com/jamf-pro/documentation/Advanced_Computer_Searches.html)
- [Extension Attributes](https://docs.jamf.com/jamf-pro/documentation/Computer_Extension_Attributes.html)
:::
