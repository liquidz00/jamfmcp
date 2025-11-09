# Computer Health Tools

These tools provide comprehensive health analysis and diagnostics for computers managed by Jamf Pro.

:::{note}
**About JSON Response Schemas**

The JSON examples throughout this document show the structure of data that JamfMCP returns. When using these tools through an AI assistant, you won't see raw JSON - the AI will interpret and present this information in a natural, conversational format.
:::

## Available Tools

(get_health_scorecard)=
### Getting Health Scorecards

Generate a comprehensive health scorecard with security compliance analysis.

**Tool:** `get_health_scorecard`

Generate a comprehensive health scorecard for a computer.

**Parameters:**
- `serial` (str, required): Computer serial number
- `email_address` (str, optional): User email for additional context

**Returns:**
```python
{
    "overall_score": 85.5,  # 0-100
    "grade": "B",          # A, B, C, D, F
    "status": "GOOD",      # EXCELLENT, GOOD, FAIR, POOR, CRITICAL
    "security_score": {
        "score": 90.0,
        "factors": ["FileVault enabled", "SIP enabled"],
        "recommendations": ["Enable Firewall"]
    },
    "system_health_score": { /* similar structure */ },
    "compliance_score": { /* similar structure */ },
    "maintenance_score": { /* similar structure */ },
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

(get_basic_diagnostics)=
### Get Basic Diagnostics

Get basic diagnostic information without full health analysis.

**Tool:** `get_basic_diagnostics`

Parse computer inventory and extract key diagnostic information.

**Parameters:**
- `serial` (str, required): Computer serial number

**Returns:**
```python
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

## Health Scoring Algorithm

:::{note}
Functionality to configure custom category weights is actively being worked on, allowing end users to be able to set these options based on company needs.
:::

The health analyzer evaluates computers across four weighted categories:

### Category Weights

| Category | Weight | Focus Areas |
|----------|--------|-------------|
| **Security** | 35% | FileVault, Gatekeeper, SIP, Firewall, CVEs |
| **System Health** | 25% | Storage, battery, uptime, hardware |
| **Compliance** | 25% | Check-in frequency, policy status |
| **Maintenance** | 15% | OS updates, app updates, certificates |

### Score Calculation

1. **Individual Scores**: Each category scored 0-100
2. **Weighted Average**: Categories combined by weight
3. **Grade Assignment**:
   - A: 90-100 (Excellent)
   - B: 80-89 (Good)
   - C: 70-79 (Fair)
   - D: 60-69 (Poor)
   - F: 0-59 (Critical)

### Security Scoring Details

Security score factors:
- **FileVault Status** (25 points)
- **SIP Status** (20 points)
- **Gatekeeper Status** (15 points)
- **Firewall Status** (15 points)
- **CVE Assessment** (25 points)

CVE scoring:
- No CVEs: 100%
- Non-exploited CVEs: -5% each
- Actively exploited CVEs: -15% each

## Usage Examples

### Basic Health Check
> "Check the health of computer with serial ABC123"

### Bulk Analysis
> "Generate health scorecards for all computers in the Engineering department"

### CVE Focus
> "Which computers in our fleet have actively exploited CVEs?"

### Compliance Audit
> "Show me all non-compliant computers with their specific issues"

## Best Practices

1. **Regular Monitoring**: Run health checks weekly or monthly
2. **Focus on Failures**: Prioritize F and D grades
3. **Track Trends**: Monitor score changes over time
4. **Act on CVEs**: Address actively exploited CVEs immediately
5. **Automate Reports**: Set up regular health report generation

## Related Tools

- [`get_computer_inventory`](#get_computer_inventory) - Detailed computer data
- [`get_computer_history`](#get_computer_history) - Historical logs
- [`search_computers`](#search_computers) - Find computers
- [`get_policies`](#get_policies) - Review policies
- [`get_compliance_status`](#get_compliance_status) - Compliance details

:::{seealso}
- [Health Analyzer API Reference](../api-reference/health-analyzer)
- [Jamf Pro Computer Inventory](https://developer.jamf.com/jamf-pro/reference/get_v2-computers-inventory)
:::
