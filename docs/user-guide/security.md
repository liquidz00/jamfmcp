# Security & Compliance

:::{rst-class} lead
Tools providing security analysis, compliance checking, and vulnerability management capabilities.
:::

## Security Analysis

(get_cves)=
### Get CVEs

Analyze CVE vulnerabilities affecting a computer using the macadmins SOFA feed.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `serial`
    - str
    - **Yes**
    - Computer serial number
*   - `include_descriptions`
    - bool
    - No
    - Include CVE descriptions (default: false)
:::

:::{dropdown} Example Response

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
  "recommendations": [
    "CRITICAL: Update to macOS 14.2.1 immediately",
    "3 actively exploited vulnerabilities affect this system",
    "Security update available since 2024-01-01"
  ]
}
```
:::

#### Usage Examples

:::{ai-prompt}
Check for CVE vulnerabilities on computer with serial ABC123
:::

:::{ai-prompt}
Show me all actively exploited CVEs affecting serial XYZ789 with descriptions
:::

:::{ai-prompt}
Scan computer ABC123 for security vulnerabilities
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Health Scorecard
:link: get_health_scorecard
:link-type: ref

Includes CVE analysis in security scoring
::::

::::{grid-item-card} Get Compliance Status
:link: get_compliance_status
:link-type: ref

Check overall security compliance
::::
:::::

---

(get_compliance_status)=
### Get Compliance Status

Check computer compliance with organizational policies.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `computer_id`
    - str | int
    - **Yes**
    - Computer JSS ID
:::

:::{dropdown} Example Response

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
:::

#### Usage Examples

:::{ai-prompt}
Check compliance status for computer ID 123
:::

:::{ai-prompt}
Show me compliance issues for computer 456
:::

:::{ai-prompt}
Get the compliance score and critical issues for computer ID 789
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Health Scorecard
:link: get_health_scorecard
:link-type: ref

Overall health including compliance
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

View policy configurations
::::
:::::

---

## Software Restrictions

(get_restricted_software)=
### Get Restricted Software

List all restricted software configurations.

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
:::

#### Usage Examples

:::{ai-prompt}
Show me all restricted software configurations
:::

:::{ai-prompt}
List software that is blocked on company computers
:::

:::{ai-prompt}
Get all restricted software rules and their enforcement actions
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Restricted Software Details
:link: get_restricted_software_details
:link-type: ref

Detailed configuration for specific software
::::

::::{grid-item-card} Get Policies
:link: get_policies
:link-type: ref

Related restriction policies
::::
:::::

---

(get_restricted_software_details)=
### Get Restricted Software Details

Get details about a specific restricted software configuration.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `software_id`
    - str | int
    - **Yes**
    - Restricted software ID
:::

:::{dropdown} Example Response

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
:::

#### Usage Examples

:::{ai-prompt}
Get details for restricted software ID 1
:::

:::{ai-prompt}
Show me the scope and exclusions for restricted software 5
:::

:::{ai-prompt}
Check if BitTorrent restriction applies to all computers
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Restricted Software
:link: get_restricted_software
:link-type: ref

List all restricted software
::::

::::{grid-item-card} Get Smart Groups
:link: get_smart_groups
:link-type: ref

Groups used in scope/exclusions
::::
:::::

---

## License Management

(get_licensed_software)=
### Get Licensed Software

List all licensed software configurations.

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
:::

#### Usage Examples

:::{ai-prompt}
Show me all licensed software and their usage
:::

:::{ai-prompt}
List software licenses with less than 10% availability
:::

:::{ai-prompt}
Get license counts for all managed software
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Licensed Software Details
:link: get_licensed_software_details
:link-type: ref

Detailed license information
::::

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Check installed software
::::
:::::

---

(get_licensed_software_details)=
### Get Licensed Software Details

Get details about specific licensed software.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `software_id`
    - str | int
    - **Yes**
    - Licensed software ID
:::

:::{dropdown} Example Response

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
  ]
}
```
:::

#### Usage Examples

:::{ai-prompt}
Get details for licensed software ID 1
:::

:::{ai-prompt}
Show me which computers have Adobe Creative Cloud installed
:::

:::{ai-prompt}
Check the license expiration date for software ID 5
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Licensed Software
:link: get_licensed_software
:link-type: ref

List all licensed software
::::

::::{grid-item-card} Get Users
:link: get_users
:link-type: ref

User assignments for per-user licenses
::::
:::::

---

## Device Security

(get_device_lock_pin)=
### Get Device Lock PIN

Retrieve the device lock PIN for a lost or stolen computer.

:::{list-table}
:widths: auto
:align: left
:header-rows: 1

*   - Parameter
    - Type
    - Required
    - Description
*   - `computer_id`
    - str
    - **Yes**
    - Computer JSS ID
:::

:::{dropdown} Example Response

```json
{
  "computer_id": "123",
  "device_lock_pin": "123456",
  "pin_set_date": "2024-01-15T10:00:00Z",
  "pin_expires": "2024-01-22T10:00:00Z",
  "status": "active"
}
```
:::

:::{warning}
**Security Notice**: Device lock PINs are sensitive information. Ensure proper authorization before retrieving and handle with appropriate security measures.
:::

#### Usage Examples

:::{ai-prompt}
Get the device lock PIN for computer ID 123
:::

:::{ai-prompt}
Retrieve the lost device PIN for computer 456
:::

:::{ai-prompt}
Show me the lock code for stolen computer ID 789
:::

#### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Device identification details
::::

::::{grid-item-card} Get Computer History
:link: get_computer_history
:link-type: ref

Device management history
::::
:::::

---

## Common Use Cases

### CVE Vulnerability Scan

:::{ai-prompt}
Scan all computers for actively exploited CVEs and summarize the vulnerable systems
:::

:::{ai-prompt}
Which computers in our fleet have known security vulnerabilities that are being actively exploited?
:::

:::{ai-prompt}
Generate a report of all computers affected by CVEs, prioritizing those with active exploits
:::

### Compliance Audit

:::{ai-prompt}
Check compliance status for all computers in the Finance department
:::

:::{ai-prompt}
Find all non-compliant computers and list their critical issues
:::

:::{ai-prompt}
Generate a compliance report showing computers with scores below 80%
:::

### License Usage Report

:::{ai-prompt}
Show me all software licenses that have less than 10% availability remaining
:::

:::{ai-prompt}
Generate a license usage report highlighting critical shortages
:::

:::{ai-prompt}
Which software licenses are expiring in the next 30 days?
:::

### Restricted Software Monitoring

:::{ai-prompt}
Show me all restricted software configurations that kill processes and delete executables
:::

:::{ai-prompt}
Which restricted software rules have the highest impact on users?
:::

:::{ai-prompt}
List all software restrictions and the computer groups they affect
:::

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

:::{seealso}
- [macadmins SOFA Feed](https://sofa.macadmins.io/)
- [Jamf Pro Compliance](https://docs.jamf.com/jamf-pro/documentation/Compliance.html)
- [Restricted Software](https://docs.jamf.com/jamf-pro/documentation/Restricted_Software.html)
- [Licensed Software](https://docs.jamf.com/jamf-pro/documentation/Licensed_Software.html)
:::
