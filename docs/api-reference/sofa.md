# SOFA Module

The `jamfmcp.sofa` module provides integration with the macadmins SOFA (Simple Organized Feed for Apple Software Updates) for CVE tracking and OS version currency analysis.

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

## Data Structure Examples

### SOFA Feed Structure

```python
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

### Parsed OSVersionInfo

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

## CVE Scoring Algorithm

The module uses CVE data to calculate security impact:

```python
def calculate_cve_score(affecting_cves: set, exploited_cves: set) -> float:
    """Calculate security score based on CVEs."""
    score = 100.0

    # Non-exploited CVEs: -5% each
    non_exploited = affecting_cves - exploited_cves
    score -= len(non_exploited) * 5

    # Actively exploited CVEs: -15% each
    score -= len(exploited_cves) * 15

    return max(0.0, score)
```

## Version Comparison

The module includes helper functions for version comparison:

```python
def _version_is_newer(v1_parts: list[int], v2_parts: list[int]) -> bool:
    """Check if v1 is newer than v2."""
    for i in range(max(len(v1_parts), len(v2_parts))):
        v1_part = v1_parts[i] if i < len(v1_parts) else 0
        v2_part = v2_parts[i] if i < len(v2_parts) else 0

        if v1_part > v2_part:
            return True
        elif v1_part < v2_part:
            return False

    return False
```

## Error Handling

The module handles various error conditions:

```python
try:
    feed_data = await get_sofa_feed()
except httpx.HTTPError as e:
    logger.error(f"Failed to fetch SOFA feed: {e}")
    # Use cached data or fail gracefully

try:
    sofa_feed = parse_sofa_feed(feed_data)
except ValueError as e:
    logger.error(f"Failed to parse SOFA feed: {e}")
    # Handle malformed feed data

try:
    cves = get_cves_for_version(sofa_feed, version, os_family)
except ValueError as e:
    logger.error(f"OS family not found: {e}")
    # Handle unknown OS versions
```

## Performance Considerations

### Feed Caching

```python
import asyncio
from datetime import datetime, timedelta

class SOFAFeedCache:
    def __init__(self, ttl_hours: int = 6):
        self.feed = None
        self.last_update = None
        self.ttl = timedelta(hours=ttl_hours)

    async def get_feed(self) -> SOFAFeed:
        now = datetime.now()
        if (not self.feed or not self.last_update or
            now - self.last_update > self.ttl):
            # Refresh cache
            feed_data = await get_sofa_feed()
            self.feed = parse_sofa_feed(feed_data)
            self.last_update = now

        return self.feed
```

### Batch CVE Analysis

```python
async def analyze_fleet_cves(computers: list[dict]) -> dict:
    """Analyze CVEs for entire fleet efficiently."""
    # Fetch feed once
    feed_data = await get_sofa_feed()
    sofa_feed = parse_sofa_feed(feed_data)

    results = {}
    for computer in computers:
        version = computer["os_version"]
        os_family = get_os_family(version)

        try:
            affecting, exploited = get_cves_for_version(
                sofa_feed, version, os_family
            )
            results[computer["serial"]] = {
                "affecting": affecting,
                "exploited": exploited
            }
        except ValueError:
            # Handle unknown OS
            results[computer["serial"]] = {
                "error": "Unknown OS version"
            }

    return results
```

## Constants

```python
# SOFA feed URL
SOFA_FEED_URL = "https://sofafeed.macadmins.io/v1/macos_data_feed.json"

# Common timeout for HTTP requests
HTTP_TIMEOUT = 30.0
```

:::{seealso}
- [macadmins SOFA](https://sofa.macadmins.io/)
- [CVE Database](https://cve.mitre.org/)
- [Apple Security Updates](https://support.apple.com/en-us/HT201222)
- [Health Analyzer Module](health-analyzer)
:::
