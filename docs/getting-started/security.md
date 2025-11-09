# Security & Compliance Tools

These tools provide security analysis, compliance checking, and vulnerability management capabilities.

:::{note}
**About JSON Response Schemas**

The JSON examples throughout this document show the structure of data that JamfMCP returns. When using these tools through an AI assistant, you won't see raw JSON - the AI will interpret and present this information in a natural, conversational format.
:::

## Security Analysis

(get_cves)=
### Get CVEs

Analyze CVE vulnerabilities affecting a computer using the macadmins SOFA feed.

**Tool:** `get_cves`

**Parameters:**
- `serial` (str, required): Computer serial number
- `include_descriptions` (bool, optional): Include CVE descriptions (default: false)

**Returns (JSON Schema):**
```json
{
    "serial": "ABC123456",
    "os_version": "14.2.0",
    "os_build": "23C64",
    "cve_summary": {
        "total_cves": 15,
        "actively_exploited": 3,
        "days_since_release": 45,
        "patch_available": true,
        "latest_os_version": "14.2.1"
    },
    "affecting_cves": [
        "CVE-2024-12345",
        "CVE-2024-12346",
        "CVE-2024-12347"
    ],
    "exploited_cves": [
        "CVE-2024-12345"
    ],
    "cve_details": {  // Only if include_descriptions=true
        "CVE-2024-12345": {
            "description": "A memory corruption issue...",
            "severity": "Critical",
            "actively_exploited": true
        }
    },
    "recommendations": [
        "CRITICAL: Update to macOS 14.2.1 immediately",
        "3 actively exploited vulnerabilities affect this system",
        "Security update available since 2024-01-01"
    ]
}
```

(get_compliance_status)=
### Getting Compliance Status

Check computer compliance with organizational policies.

**Tool:** `get_compliance_status`

**Parameters:**
- `computer_id` (str | int, required): Computer JSS ID

**Returns (JSON Schema):**
```json
{
    "computer_id": 123,
    "computer_name": "John's MacBook Pro",
    "compliant": false,
    "compliance_score": 75,
    "issues": [
        {
            "type": "policy_failure",
            "severity": "high",
            "policy_id": 45,
            "policy_name": "Security Settings",
            "last_failure": "2024-01-15T08:00:00Z",
            "failure_count": 3
        },
        {
            "type": "profile_missing",
            "severity": "critical",
            "profile_id": 12,
            "profile_name": "FileVault Configuration",
            "required": true
        },
        {
            "type": "outdated_os",
            "severity": "high",
            "current_version": "14.2.0",
            "required_version": "14.2.1",
            "days_outdated": 15
        }
    ],
    "last_check": "2024-01-15T10:00:00Z",
    "next_check": "2024-01-15T22:00:00Z"
}
```

## Software Restrictions

(get_restricted_software)=
### Getting Restricted Software

List all restricted software configurations.

**Tool:** `get_restricted_software`

**Returns (JSON Schema):**
```json
[
    {
        "id": 1,
        "name": "BitTorrent Clients",
        "process_name": "BitTorrent",
        "match_exact": false,
        "send_notification": true,
        "kill_process": true,
        "delete_executable": false,
        "display_message": "BitTorrent is not allowed on company computers",
        "site": {
            "id": -1,
            "name": "None"
        },
        "scope": {
            "all_computers": true,
            "computer_groups": []
        }
    },
    {
        "id": 2,
        "name": "Limewire",
        "process_name": "Limewire.app",
        "match_exact": true,
        "send_notification": true,
        "kill_process": true,
        "delete_executable": true,
        "display_message": "P2P software is prohibited"
    }
]
```

(get_restricted_software_details)=
### Getting Restricted Software Details

Get details about a specific restricted software configuration.

**Tool:** `get_restricted_software_details`

**Parameters:**
- `software_id` (str | int, required): Restricted software ID

**Returns (JSON Schema):**
```json
{
    "id": 1,
    "name": "BitTorrent Clients",
    "enabled": true,
    "process_name": "BitTorrent",
    "match_exact": false,
    "send_notification": true,
    "kill_process": true,
    "delete_executable": false,
    "display_message": "BitTorrent is not allowed on company computers",
    "site": {
        "id": -1,
        "name": "None"
    },
    "scope": {
        "all_computers": true,
        "computer_groups": [],
        "computers": [],
        "buildings": [],
        "departments": [],
        "exclusions": {
            "computer_groups": [{
                "id": 15,
                "name": "Developer Exceptions"
            }],
            "computers": [],
            "buildings": [],
            "departments": []
        }
    }
}
```

## License Management

(get_licensed_software)=
### Getting Licensed Software

List all licensed software configurations.

**Tool:** `get_licensed_software`

**Returns (JSON Schema):**
```json
[
    {
        "id": 1,
        "name": "Adobe Creative Cloud",
        "publisher": "Adobe Inc.",
        "platform": "Mac",
        "bundle_id": "com.adobe.CreativeCloud",
        "total_licenses": 100,
        "used_licenses": 87,
        "available_licenses": 13,
        "license_type": "Per Device"
    },
    {
        "id": 2,
        "name": "Microsoft Office",
        "publisher": "Microsoft",
        "platform": "Mac",
        "bundle_id": "com.microsoft.office",
        "total_licenses": 500,
        "used_licenses": 423,
        "available_licenses": 77,
        "license_type": "Per User"
    }
]
```

(get_licensed_software_details)=
### Getting Licensed Software Details

Get details about specific licensed software.

**Tool:** `get_licensed_software_details`

**Parameters:**
- `software_id` (str | int, required): Licensed software ID

**Returns (JSON Schema):**
```json
{
    "id": 1,
    "name": "Adobe Creative Cloud",
    "publisher": "Adobe Inc.",
    "platform": "Mac",
    "bundle_id": "com.adobe.CreativeCloud",
    "version": "2024",
    "total_licenses": 100,
    "used_licenses": 87,
    "available_licenses": 13,
    "license_type": "Per Device",
    "purchasing_info": {
        "po_number": "PO-2024-001",
        "vendor": "Adobe Direct",
        "purchase_date": "2024-01-01",
        "purchase_price": "$52,000",
        "license_expires": "2025-01-01"
    },
    "scope": {
        "all_computers": false,
        "computer_groups": [{
            "id": 20,
            "name": "Creative Team"
        }]
    },
    "computers": [
        {
            "id": 123,
            "name": "Designer-Mac-01",
            "serial_number": "ABC123"
        }
        // ... more computers
    ]
}
```

## Device Security

(get_device_lock_pin)=
### Getting Device Lock Pin

Retrieve the device lock PIN for a lost or stolen computer.

**Tool:** `get_device_lock_pin`

**Parameters:**
- `computer_id` (str, required): Computer JSS ID

**Returns (JSON Schema):**
```json
{
    "computer_id": "123",
    "device_lock_pin": "123456",
    "pin_set_date": "2024-01-15T10:00:00Z",
    "pin_expires": "2024-01-22T10:00:00Z",
    "status": "active"
}
```

:::{warning}
**Security Notice**: Device lock PINs are sensitive information. Ensure proper authorization before retrieving and handle with appropriate security measures.
:::

## Common Use Cases

### CVE Vulnerability Scan

**AI Prompt Examples:**

> "Scan all computers for actively exploited CVEs and summarize the vulnerable systems"

> "Which computers in our fleet have known security vulnerabilities that are being actively exploited?"

> "Generate a report of all computers affected by CVEs, prioritizing those with active exploits"

### Compliance Audit

**AI Prompt Examples:**

> "Check compliance status for all computers in the Finance department"

> "Find all non-compliant computers and list their critical issues"

> "Generate a compliance report showing computers with scores below 80%"

### License Usage Report

**AI Prompt Examples:**

> "Show me all software licenses that have less than 10% availability remaining"

> "Generate a license usage report highlighting critical shortages"

> "Which software licenses are expiring in the next 30 days?"

### Restricted Software Monitoring

**AI Prompt Examples:**

> "Show me all restricted software configurations that kill processes and delete executables"

> "Which restricted software rules have the highest impact on users?"

> "List all software restrictions and the computer groups they affect"

## Security Best Practices

### CVE Management
1. **Regular Scans**: Check for CVEs weekly
2. **Prioritize Exploited**: Focus on actively exploited CVEs
3. **Rapid Response**: Update within 48 hours for critical CVEs
4. **Track Compliance**: Monitor update adoption

### Compliance Monitoring
1. **Automated Checks**: Schedule regular compliance scans
2. **Severity Levels**: Address critical issues first
3. **Trend Analysis**: Track compliance scores over time
4. **Exception Handling**: Document approved exceptions

### License Optimization
1. **Usage Tracking**: Monitor license utilization
2. **Expiration Alerts**: Track renewal dates
3. **Reallocation**: Reassign unused licenses
4. **Compliance Audit**: Ensure proper licensing

### Software Restrictions
1. **Clear Policies**: Define what's restricted and why
2. **User Communication**: Inform users of restrictions
3. **Exception Process**: Have a process for exceptions
4. **Regular Review**: Update restricted software list

## Integration Examples

### With Health Scoring

**AI Prompt Example:**

> "Generate a health scorecard for serial ABC123 and include CVE vulnerability analysis in the overall assessment"

### With Inventory

**AI Prompt Example:**

> "Get security and disk encryption settings for computer with serial ABC123"

### With Policies

**AI Prompt Example:**

> "Show me all security policies and highlight any that are disabled"

## Related Tools

- [`get_health_scorecard`](#get_health_scorecard) - Overall security health
- [`get_computer_inventory`](#get_computer_inventory) - Security settings
- [`get_policies`](#get_policies) - Security policies
- [`get_configuration_profiles`](#get_configuration_profiles) - Security profiles
- [`get_patch_policies`](#get_patch_policies) - Security updates

:::{seealso}
- [macadmins SOFA Feed](https://sofa.macadmins.io/)
- [Jamf Pro Compliance](https://docs.jamf.com/jamf-pro/documentation/Compliance.html)
- [Restricted Software](https://docs.jamf.com/jamf-pro/documentation/Restricted_Software.html)
- [Licensed Software](https://docs.jamf.com/jamf-pro/documentation/Licensed_Software.html)
:::
