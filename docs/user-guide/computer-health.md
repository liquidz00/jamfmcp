# Computer Health

:::{rst-class} lead
Tools for comprehensive health analysis and diagnostics of computers managed by Jamf Pro.
:::

(get_health_scorecard)=
## Get Health Scorecard

Generate a comprehensive health scorecard with security compliance analysis for a computer.

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
    - The serial number of the computer to retrieve
*   - `email_address`
    - str
    - No
    - User email instead of serial number
:::

:::{dropdown} Example Response

```json
{
  "overall_score": 85.5,
  "grade": "B",
  "status": "GOOD",
  "security_score": {
    "score": 90.0,
    "factors": ["FileVault enabled", "SIP enabled"],
    "recommendations": ["Enable Firewall"]
  },
  "system_health_score": {
    "score": 82.0,
    "factors": ["Storage adequate", "Battery healthy"],
    "recommendations": []
  },
  "compliance_score": {
    "score": 88.0,
    "factors": ["Regular check-ins", "Policies up-to-date"],
    "recommendations": []
  },
  "maintenance_score": {
    "score": 79.0,
    "factors": ["OS current", "Apps updated"],
    "recommendations": ["Update to latest macOS version"]
  },
  "device_info": {
    "serial": "ABC123",
    "model": "MacBook Pro",
    "os_version": "14.2.1"
  },
  "recommendations": [
    "Update to latest macOS version",
    "Enable automatic updates"
  ]
}
```
:::

### Usage Examples

:::{ai-prompt}
Check the health of computer with serial ABC123
:::

:::{ai-prompt}
Generate a health scorecard for the computer assigned to john.doe@company.com
:::

:::{ai-prompt}
Show me the security compliance status for serial number ABC123
:::

### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Computer Inventory
:link: get_computer_inventory
:link-type: ref

Retrieve detailed hardware and software information
::::

::::{grid-item-card} Get CVEs
:link: get_cves
:link-type: ref

Check for CVE vulnerabilities affecting the system
::::
:::::

---

(get_basic_diagnostics)=
## Get Basic Diagnostics

Extract key diagnostic information from computer inventory without full health analysis.

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
    - The serial number of the computer to retrieve
:::

:::{dropdown} Example Response

```json
{
  "computer_name": "John's MacBook Pro",
  "serial_number": "ABC123456",
  "model": "MacBook Pro (16-inch, 2023)",
  "os_version": "macOS 14.2.1",
  "last_check_in": "2024-01-15T10:30:00Z",
  "ip_address": "10.0.1.50",
  "mac_address": "00:11:22:33:44:55",
  "storage": {
    "total_gb": 512,
    "available_gb": 256,
    "used_percent": 50
  },
  "memory": {
    "total_gb": 32
  },
  "battery": {
    "cycle_count": 45,
    "condition": "Normal"
  },
  "security": {
    "filevault": "Enabled",
    "sip": "Enabled",
    "gatekeeper": "Enabled"
  }
}
```
:::

### Usage Examples

:::{ai-prompt}
Get basic diagnostics for computer with serial ABC123
:::

:::{ai-prompt}
Show me the system info for serial number XYZ789
:::

### Related Tools

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} Get Health Scorecard
:link: get_health_scorecard
:link-type: ref

Full health analysis with scoring and recommendations
::::

::::{grid-item-card} Get Computer History
:link: get_computer_history
:link-type: ref

View historical logs and policy execution
::::
:::::

---

## Health Scoring Algorithm

:::{note}
Functionality to configure custom category weights is actively being worked on, allowing organizations to adjust scoring based on their priorities.
:::

The health analyzer evaluates computers across four weighted categories:

### Scoring Categories

:::::{grid} 2 2 2 2
:gutter: 2

::::{grid-item-card} {fas}`shield-alt` Security (35%)

- FileVault encryption
- System Integrity Protection
- Gatekeeper status
- Firewall configuration
- CVE vulnerabilities
::::

::::{grid-item-card} {fas}`heartbeat` System Health (25%)

- Storage capacity
- Battery health
- System uptime
- Hardware status
::::

::::{grid-item-card} {fas}`check-circle` Compliance (25%)

- Check-in frequency
- Policy execution
- Profile installation
- Management status
::::

::::{grid-item-card} {fas}`wrench` Maintenance (15%)

- OS updates
- App updates
- Certificate validity
- Extension attributes
::::
:::::

### Grade Scale

| Grade | Score Range | Status | Action Required |
|-------|------------|--------|-----------------|
| **A** | 90-100 | Excellent | Routine monitoring |
| **B** | 80-89 | Good | Minor improvements |
| **C** | 70-79 | Fair | Attention needed |
| **D** | 60-69 | Poor | Immediate action |
| **F** | 0-59 | Critical | Urgent remediation |

## Best Practices

:::::{grid} 1 1 2 2
:gutter: 2

::::{grid-item-card} {fas}`calendar-check` Regular Monitoring
Run health checks weekly or monthly to track trends and catch issues early.
::::

::::{grid-item-card} {fas}`exclamation-triangle` Priority Focus
Address F and D grades immediately, focusing on security issues first.
::::

::::{grid-item-card} {fas}`chart-line` Trend Analysis
Monitor score changes over time to identify patterns and recurring issues.
::::

::::{grid-item-card} {fas}`bolt` CVE Response
Address actively exploited CVEs within 48 hours of detection.
::::
:::::

## Common Use Cases

### Compliance Reporting

:::{ai-prompt}
Generate health scorecards for all computers in the Engineering department
:::

### Security Auditing

:::{ai-prompt}
Find all computers with health scores below 70 and list their critical issues
:::

### Proactive Maintenance

:::{ai-prompt}
Show me computers that haven't checked in for 7 days with their last known health status
:::

:::{seealso}
- [Health Analyzer API Reference](../api-reference/health-analyzer)
- [Jamf Pro Computer Inventory](https://developer.jamf.com/jamf-pro/reference/get_v2-computers-inventory)
- [macadmins SOFA Feed](https://sofa.macadmins.io/)
:::
