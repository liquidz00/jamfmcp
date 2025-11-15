# SOFA Integration

:::{rst-class} lead
Integration with [SOFA](https://sofa.macadmins.io) for CVE tracking and OS version currency analysis.
:::

(sofa_data_models)=
## SOFA Data Models

[Pydantic](https://docs.pydantic.dev/latest/api/base_model/) data models used in conjunction with SOFA functionality.

### CVE Info

CVE information with exploitation status.

```{eval-rst}
.. autoclass:: jamfmcp.sofa.CVEInfo
   :members:
   :undoc-members:
   :show-inheritance:
```

### Security Release

Details about a security release for an OS version.

```{eval-rst}
.. autoclass:: jamfmcp.sofa.SecurityRelease
   :members:
   :undoc-members:
   :show-inheritance:
```

(os_version_info)=
### OSVersion Information

Information about a specific macOS version family.

```{eval-rst}
.. autoclass:: jamfmcp.sofa.OSVersionInfo
   :members:
   :undoc-members:
   :show-inheritance:
```

### SOFA Feed

The complete SOFA feed data structure.

```{eval-rst}
.. autoclass:: jamfmcp.sofa.SOFAFeed
   :members:
   :undoc-members:
   :show-inheritance:
```

## Core Functions

### Feed Retrieval

```{eval-rst}
.. autofunction:: jamfmcp.sofa.get_sofa_feed
```

### Feed Parsing

```{eval-rst}
.. autofunction:: jamfmcp.sofa.parse_sofa_feed
```

### CVE Analysis

```{eval-rst}
.. autofunction:: jamfmcp.sofa.get_cves_for_version
```

### Version Currency

```{eval-rst}
.. autofunction:: jamfmcp.sofa.get_version_currency_info
```

## Feed Conversion

The SOFA module is also responsible for [data feed](https://sofa.macadmins.io/how-it-works) into [Pydantic data models](#sofa_data_models).

### SOFA Feed Structure (example)

```json
{
    "UpdateHash": "abc123def456",
    "OSVersions": [
        {
            "OSVersion": "Sonoma 14",
            "Latest": {
                "ProductVersion": "14.2.1",
                "Build": "23C71",
                "ReleaseDate": "2023-12-19"
            },
            "SecurityReleases": [
                {
                    "UpdateName": "macOS Sonoma 14.2.1",
                    "ProductVersion": "14.2.1",
                    "ReleaseDate": "2023-12-19",
                    "CVEs": {
                        "CVE-2023-42916": {},
                        "CVE-2023-42917": {}
                    },
                    "ActivelyExploitedCVEs": [
                        "CVE-2023-42916",
                        "CVE-2023-42917"
                    ],
                    "UniqueCVEsCount": 2,
                    "DaysSincePreviousRelease": 7
                }
            ]
        }
    ]
}
```

### Parsed Feed

The example used above would be converted into an [`OSVersionInfo`](#os_version_info) object:

```python
OSVersionInfo(
    os_version="Sonoma 14",
    latest_version="14.2.1",
    latest_build="23C71",
    latest_release_date="2023-12-19",
    security_releases=[
        SecurityRelease(
            update_name="macOS Sonoma 14.2.1",
            product_version="14.2.1",
            release_date="2023-12-19",
            cves={"CVE-2023-42916": {}, "CVE-2023-42917": {}},
            actively_exploited_cves=["CVE-2023-42916", "CVE-2023-42917"],
            unique_cves_count=2,
            days_since_previous=7
        )
    ],
    all_cves={"CVE-2023-42916", "CVE-2023-42917"},
    actively_exploited_cves={"CVE-2023-42916", "CVE-2023-42917"}
)
```


:::{seealso}
- [CVE Database](https://cve.mitre.org/)
- [Apple Security Updates](https://support.apple.com/en-us/HT201222)
- [Health Analyzer Module](health-analyzer)
:::
