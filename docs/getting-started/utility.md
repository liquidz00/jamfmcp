# Utility Tools

These tools provide additional utility and management capabilities including JCDS files, webhooks, LDAP integration, and system utilities.

:::{note}
**About JSON Response Schemas**

The JSON examples throughout this document show the structure of data that JamfMCP returns. When using these tools through an AI assistant, you won't see raw JSON - the AI will interpret and present this information in a natural, conversational format.
:::

## File Management

(get_jcds_files)=
### Get all JCDS Files

List all files stored in Jamf Cloud Distribution Service (JCDS).

**Tool:** `get_jcds_files`

**Returns:**
```python
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

## Webhook Management

(get_webhooks)=
### Getting Webhooks

List all configured webhooks.

**Tool:** `get_webhooks`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Slack Notifications",
        "enabled": True,
        "url": "https://hooks.slack.com/services/...",
        "content_type": "application/json",
        "event": "ComputerAdded",
        "connection_timeout": 5000,
        "read_timeout": 5000
    },
    {
        "id": 2,
        "name": "ServiceNow Integration",
        "enabled": True,
        "url": "https://instance.service-now.com/api/...",
        "event": "ComputerCheckIn",
        "authentication_type": "Basic",
        "username": "jamf_integration"
    }
]
```

(get_webhook_details)=
### Getting Webhook Details

Get detailed information about a specific webhook.

**Tool:** `get_webhook_details`

**Parameters:**
- `webhook_id` (str | int, required): Webhook ID

**Returns:**
```python
{
    "id": 1,
    "name": "Slack Notifications",
    "enabled": True,
    "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    "content_type": "application/json",
    "event": "ComputerAdded",
    "connection_timeout": 5000,
    "read_timeout": 5000,
    "authentication_type": "None",
    "username": "",
    "enable_display_fields_for_group_object": False,
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

## Directory Services

(get_ldap_servers)=
### Getting LDAP Servers

List all configured LDAP servers.

**Tool:** `get_ldap_servers`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Corporate Active Directory",
        "hostname": "ldap.company.com",
        "port": 389,
        "use_ssl": True,
        "authentication_type": "Simple",
        "account": "CN=JamfLDAP,OU=ServiceAccounts,DC=company,DC=com",
        "use_wildcards": True,
        "connection_timeout": 15,
        "search_timeout": 60,
        "referral_response": "Follow"
    },
    {
        "id": 2,
        "name": "Azure AD",
        "hostname": "ldaps.company.com",
        "port": 636,
        "use_ssl": True
    }
]
```
(get_ldap_server_details)=
### Getting LDAP Server Details

Get detailed information about a specific LDAP server.

**Tool:** `get_ldap_server_details`

**Parameters:**
- `server_id` (str | int, required): LDAP server ID

**Returns:**
```python
{
    "id": 1,
    "name": "Corporate Active Directory",
    "hostname": "ldap.company.com",
    "port": 389,
    "use_ssl": True,
    "authentication_type": "Simple",
    "account": "CN=JamfLDAP,OU=ServiceAccounts,DC=company,DC=com",
    "use_wildcards": True,
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
        "use_referrals": True,
        "test_successful": True,
        "test_date": "2024-01-15T10:00:00Z"
    }
}
```

(get_directory_bindings)=
### Getting Directory Bindings

List all directory binding configurations.

**Tool:** `get_directory_bindings`

**Returns:**
```python
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

(get_directory_binding_details)=
### Getting Directory Binding Details

Get detailed information about a specific directory binding.

**Tool:** `get_directory_binding_details`

**Parameters:**
- `binding_id` (str | int, required): Directory binding ID

**Returns:**
```python
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
        "cache_last_user": True,
        "require_confirmation": False,
        "local_home": False,
        "use_unc_path": True,
        "mount_style": "SMB",
        "default_shell": "/bin/bash"
    },
    "administrative": {
        "preferred_domain_controller": "",
        "allowed_groups": "Domain Admins,Enterprise Admins",
        "authentication_from_any_domain": True,
        "packet_signing": "Allow",
        "packet_encryption": "Allow",
        "password_interval": 14,
        "restrict_ddns": False,
        "namespace": "Domain"
    }
}
```

## Advanced Search

(get_advanced_computer_searches)=
### Getting Advanced Computer Searches

List all advanced computer searches.

**Tool:** `get_advanced_computer_searches`

**Returns:**
```python
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

(get_advanced_computer_search_details)=
### Getting Advanced Computer Search Details

Get details about a specific advanced computer search.

**Tool:** `get_advanced_computer_search_details`

**Parameters:**
- `search_id` (str | int, required): Advanced search ID

**Returns:**
```python
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
            "opening_paren": False,
            "closing_paren": False
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

## Computer Groups

(get_smart_groups)=
### Getting Smart Groups

List all smart computer groups.

**Tool:** `get_smart_groups`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "All Managed Computers",
        "is_smart": True,
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
        "is_smart": True,
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
(get_group_details)=
### Getting Smart Group Details

Get detailed information about a computer group.

**Tool:** `get_group_details`

**Parameters:**
- `group_id` (str, required): Computer group ID

**Returns:**
```python
{
    "id": 1,
    "name": "All Managed Computers",
    "is_smart": True,
    "criteria": [
        {
            "name": "Managed",
            "priority": 0,
            "and_or": "and",
            "search_type": "is",
            "value": "Managed",
            "opening_paren": False,
            "closing_paren": False
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
        // ... more computers
    ],
    "computer_count": 245
}
```

## Extension Attributes

(get_extension_attributes)=
### Getting Extension Attributes

List all computer extension attributes.

**Tool:** `get_extension_attributes`

**Returns:**
```python
[
    {
        "id": 1,
        "name": "Battery Cycle Count",
        "enabled": True,
        "description": "Returns the battery cycle count",
        "data_type": "Integer",
        "input_type": "Script",
        "inventory_display": "Hardware"
    },
    {
        "id": 2,
        "name": "Time Machine Status",
        "enabled": True,
        "description": "Checks if Time Machine is configured",
        "data_type": "String",
        "input_type": "Script",
        "inventory_display": "Operating System"
    }
]
```

## System Utilities

(ping)=
### Pinging the Server

Simple ping test to verify MCP server connectivity.

**Tool:** `ping`

**Returns:**
```python
{
    "message": "pong",
    "status": "ok"
}
```

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

### Extension Attributes Best Practices
1. **Script Efficiency**: Optimize script performance
2. **Error Handling**: Handle script failures gracefully
3. **Data Types**: Use appropriate data types
4. **Documentation**: Document attribute purpose
5. **Regular Audits**: Review for unused attributes

## Troubleshooting

For help with these issues, see the [Tools Troubleshooting Guide](#utility_tools).

### LDAP Problems
- Test connection from Jamf Pro
- Verify service account permissions
- Check network connectivity
- Review SSL certificate validity
- Enable LDAP debug logging

### Search Performance
- Simplify search criteria
- Index relevant fields
- Use smart groups instead
- Limit display fields
- Consider search scope

## Related Tools

- [`get_computer_inventory`](#get_computer_inventory) - Extension attribute values
- [`get_policies`](#get_policies) - Webhook triggers
- [`get_users`](#get_users) - LDAP user data
- [`search_computers`](#search_computers) - Alternative to advanced search
- [`get_smart_groups`](#get_smart_groups) - Computer grouping

:::{seealso}
- [Jamf Pro Webhooks](https://docs.jamf.com/jamf-pro/documentation/Webhooks.html)
- [LDAP Integration](https://docs.jamf.com/jamf-pro/documentation/Integrating_with_LDAP_Directory_Services.html)
- [Advanced Computer Searches](https://docs.jamf.com/jamf-pro/documentation/Advanced_Computer_Searches.html)
- [Extension Attributes](https://docs.jamf.com/jamf-pro/documentation/Computer_Extension_Attributes.html)
:::
