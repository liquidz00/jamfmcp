(health_analyzer_module)=
# Health Analyzer Module

:::{rst-class} lead
Comprehensive health analysis for computers managed by Jamf Pro.
:::

(grading_and_scoring_models)=
## Grading and Scoring

Basic Python [enumeration](https://docs.python.org/3.13/library/enum.html#enum.Enum) classes for health grade and health status.

### Health Grade

```{eval-rst}
.. autoclass:: jamfmcp.health_analyzer.HealthGrade
   :members:
   :undoc-members:
   :show-inheritance:
```

### Health Status

```{eval-rst}
.. autoclass:: jamfmcp.health_analyzer.HealthStatus
   :members:
   :undoc-members:
   :show-inheritance:
```

## Health Analyzer Data Models

Pydantic data model configurations for Health Analyzer functionality.

### Health Score

Individual category score with details.

```{eval-rst}
.. autoclass:: jamfmcp.health_analyzer.HealthScore
   :members:
   :undoc-members:
   :show-inheritance:
```

### Health Scorecard

The complete health assessment result.

```{eval-rst}
.. autoclass:: jamfmcp.health_analyzer.HealthScorecard
   :members:
   :undoc-members:
   :show-inheritance:
```

## Core Classes

### HealthAnalyzer

The main analyzer class that processes computer data and generates health scorecards.

```{eval-rst}
.. autoclass:: jamfmcp.health_analyzer.HealthAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: generate_health_scorecard
   .. automethod:: parse_diags
```

## Helper Functions

```{eval-rst}
.. autofunction:: jamfmcp.health_analyzer.fmt_tmz
```

## Health Scoring System

### Category Weights

The analyzer evaluates computers across four weighted categories:

```python
CATEGORY_WEIGHTS = {
    "security": 0.35,      # 35% - Security is critical
    "system_health": 0.25, # 25% - System performance and hardware
    "compliance": 0.25,    # 25% - Policy and management compliance
    "maintenance": 0.15,   # 15% - Regular maintenance and updates
}
```

### Security Score Components

| Component | Weight | Description |
|-----------|--------|-------------|
| FileVault | 25% | Disk encryption status |
| SIP | 20% | System Integrity Protection |
| Gatekeeper | 15% | App security verification |
| Firewall | 15% | Network protection |
| CVEs | 25% | Known vulnerabilities |

### System Health Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Storage | 30% | Available disk space |
| Battery | 25% | Battery health (laptops) |
| Uptime | 20% | System stability |
| Hardware | 25% | Component status |

### Compliance Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Check-in | 40% | Recent communication |
| Policies | 30% | Policy execution status |
| Profiles | 30% | Configuration compliance |

### Maintenance Components

| Component | Weight | Description |
|-----------|--------|-------------|
| OS Updates | 50% | Operating system currency |
| App Updates | 30% | Application versions |
| Certificates | 20% | Certificate validity |

## Recommendation Engine

The analyzer generates actionable recommendations based on findings:

### Security Recommendations
- Enable FileVault encryption
- Enable System Integrity Protection
- Turn on Firewall
- Update to patch CVEs

### System Health Recommendations
- Free up disk space
- Replace aging battery
- Restart to clear uptime
- Address hardware issues

### Compliance Recommendations
- Configure regular check-ins
- Fix failing policies
- Deploy missing profiles

### Maintenance Recommendations
- Install OS updates
- Update applications
- Renew certificates
