"""
SOFA Feed Processing Module.

This module provides functionatliy to retrieve and parse the SOFA (Software Update for Apple)
macOS data feed for security vulnerability analysis and OS version currency assessment.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Tuple

import httpx
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

# Feed URL
SOFA_FEED_URL = "https://sofafeed.macadmins.io/v1/macos_data_feed.json"


class CVEInfo(BaseModel):
    """
    CVE information with exploitation status.

    :param cve_id: CVE identifier
    :type cve_id: str
    :param actively_exploited: Whether the CVE is actively exploited
    :type actively_exploited: bool
    """

    cve_id: str = Field(..., description="CVE identifier (e.g., CVE-2024-12345)")
    actively_exploited: bool = Field(..., description="Whether CVE is actively exploited")


class SecurityRelease(BaseModel):
    """
    Security release information.

    :param update_name: Name of the security update
    :type update_name: str
    :param product_version: Product version number
    :type product_version: str
    :param release_date: Release date in ISO format
    :type release_date: str
    :param cves: Dictionary of CVE IDs to exploitation status
    :type cves: Dict[str, bool]
    :param actively_exploited_cves: List of actively exploited CVE IDs
    :type actively_exploited_cves: List[str]
    :param unique_cves_count: Number of unique CVEs addressed
    :type unique_cves_count: int
    :param days_since_previous: Days since previous release
    :type days_since_previous: Optional[int]
    """

    update_name: str
    product_version: str
    release_date: str
    cves: Dict[str, bool] = Field(default_factory=Dict)
    actively_exploited_cves: List[str] = Field(default_factory=List)
    unique_cves_count: int = 0
    days_since_previous: Optional[int] = None


class OSVersionInfo(BaseModel):
    """
    Operating system version information.

    :param os_version: OS version name (e.g., "Sequoia 15")
    :type os_version: str
    :param latest_version: Latest available product version
    :type latest_version: str
    :param latest_build: Latest build number
    :type latest_build: str
    :param latest_release_date: Latest release date
    :type latest_release_date: str
    :param security_releases: List of security releases for this OS version
    :type security_releases: List[SecurityRelease]
    :param all_cves: Set of all CVEs affecting this OS version
    :type all_cves: Set[str]
    :param actively_exploited_cves: Set of actively exploited CVEs
    :type actively_exploited_cves: Set[str]
    """

    os_version: str
    latest_version: str
    latest_build: str
    latest_release_date: str
    security_releases: List[SecurityRelease] = Field(default_factory=List)
    all_cves: set[str] = Field(default_factory=set)
    actively_exploited_cves: set[str] = Field(default_factory=set)


class SOFAFeed(BaseModel):
    """
    Complete SOFA feed data structure.

    :param update_hash: Feed update hash
    :type update_hash: str
    :param os_versions: Dictionary of OS versions to their information
    :type os_versions: Dict[str, OSVersionInfo]
    :param last_updated: When the feed was last processed
    :type last_updated: datetime
    """

    update_hash: str
    os_versions: Dict[str, OSVersionInfo] = Field(default_factory=Dict)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))


async def get_sofa_feed() -> Dict[str, Any]:
    """
    Retrieve the SOFA macOS data feed from the official endpoint.

    :return: Raw SOFA feed data as dictionary
    :rtype: Dict[str, Any]
    :raises aiohttp.ClientError: If there's an error fetching the feed
    :raises ValueError: If the response is not valid JSON
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(SOFA_FEED_URL, headers={"accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            logger.info(
                "Successfully retrieved SOFA feed with %d OS versions",
                len(data.get("OSVersions", [])),
            )
            return data
    except httpx.HTTPError as e:
        logger.error(f"Failed to retrieve SOFA feed: {str(e)}")
        raise
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f"Unexpected error retrieving SOFA feed: {str(e)}")
        raise ValueError(f"Failed to parse SOFA feed response: {str(e)}") from e


def parse_sofa_feed(feed_data: Dict[str, Any]) -> SOFAFeed:
    """
    Parse raw SOFA feed data into structured models.

    :param feed_data: Raw SOFA feed data from API
    :type feed_data: Dict[str, Any]
    :return: Parsed and structured SOFA feed
    :rtype: SOFAFeed
    :raises ValueError: If feed data is invalid or missing required fields
    """
    try:
        update_hash = feed_data.get("UpdateHash", "")
        os_versions_data = feed_data.get("OSVersions", [])

        os_versions = {}

        for os_data in os_versions_data:
            os_version_name = os_data.get("OSVersion", "")
            if not os_version_name:
                continue

            # Parse latest version info
            latest = os_data.get("Latest", {})
            latest_version = latest.get("ProductVersion", "")
            latest_build = latest.get("Build", "")
            latest_release_date = latest.get("ReleaseDate", "")

            security_releases = []
            all_cves = set()
            actively_exploited_cves = set()

            for release_data in os_data.get("SecurityReleases", []):
                release = SecurityRelease(
                    update_name=release_data.get("UpdateName", ""),
                    product_version=release_data.get("ProductVersion", ""),
                    release_date=release_data.get("ReleaseDate", ""),
                    cves=release_data.get("CVEs", {}),
                    actively_exploited_cves=release_data.get("ActivelyExploitedCVEs", []),
                    unique_cves_count=release_data.get("UniqueCVEsCount", 0),
                    days_since_previous=release_data.get("DaysSincePreviousRelease"),
                )
                security_releases.append(release)

                all_cves.update(release.cves.keys())
                actively_exploited_cves.update(release.actively_exploited_cves)

            os_version_info = OSVersionInfo(
                os_version=os_version_name,
                latest_version=latest_version,
                latest_build=latest_build,
                latest_release_date=latest_release_date,
                security_releases=security_releases,
                all_cves=all_cves,
                actively_exploited_cves=actively_exploited_cves,
            )

            os_versions[os_version_name] = os_version_info

        return SOFAFeed(update_hash=update_hash, os_versions=os_versions)
    except (ValidationError, ValueError, KeyError, AttributeError) as e:
        logger.error(f"Error parsing SOFA feed: {str(e)}")
        raise ValueError(f"Failed to parse SOFA feed: {str(e)}") from e


def get_cves_for_version(
    sofa_feed: SOFAFeed, current_version: str, os_family: str = "Tahoe 26"
) -> Tuple[set[str], set[str]]:
    """
    Get CVEs that affect a specific OS version.

    Identifies which CVEs affect the current version by looking at security releases
    that came after the current version was released.

    :param sofa_feed: Parsed SOFA feed data
    :type sofa_feed: SOFAFeed
    :param current_version: Current OS version (e.g., "15.1.0")
    :type current_version: str
    :param os_family: OS family to check (e.g., "Sequoia 15")
    :type os_family: str
    :return: Tuple of (all_affecting_cves, actively_exploited_cves)
    :rtype: Tuple[Set[str], Set[str]]
    :raises ValueError: If OS family not found in feed
    """
    if os_family not in sofa_feed.os_versions:
        raise ValueError(f"OS family '{os_family}' not found in SOFA feed")

    os_info = sofa_feed.os_versions[os_family]
    affecting_cves = set()
    exploited_cves = set()

    try:
        current_parts = [int(x) for x in current_version.split(".")]

        for release in os_info.security_releases:
            try:
                release_parts = [int(x) for x in release.product_version.split(".")]

                if _version_is_newer(release_parts, current_parts):
                    affecting_cves.update(release.cves.keys())
                    exploited_cves.update(release.actively_exploited_cves)

            except (ValueError, AttributeError):
                # Skip releases where version parsing fails
                continue

    except (ValueError, AttributeError):
        logger.warning(f"Failed to parse current version: {current_version}")
        # Return all CVEs if unable to parse version
        affecting_cves = os_info.all_cves
        exploited_cves = os_info.actively_exploited_cves

    return affecting_cves, exploited_cves


def get_version_currency_info(
    sofa_feed: SOFAFeed, current_version: str, os_family: str = "Tahoe 26"
) -> Dict[str, Any]:
    """
    Determine how current/behind an OS version is compared to latest.

    :param sofa_feed: Parsed SOFA feed data
    :type sofa_feed: SOFAFeed
    :param current_version: Current OS version (e.g., "15.1.0")
    :type current_version: str
    :param os_family: OS family to check (e.g., "Sequoia 15")
    :type os_family: str
    :return: Dictionary with currency information and scoring metrics
    :rtype: Dict[str, Any]
    :raises ValueError: If OS family not found in feed
    """
    if os_family not in sofa_feed.os_versions:
        raise ValueError(f"OS family '{os_family}' not found in SOFA feed")

    os_info = sofa_feed.os_versions[os_family]
    latest_version = os_info.latest_version

    is_current = current_version == latest_version
    versions_behind = 0
    security_updates_missed = 0
    days_behind = 0

    try:
        current_parts = [int(x) for x in current_version.split(".")]
        latest_parts = [int(x) for x in latest_version.split(".")]

        for release in os_info.security_releases:
            try:
                release_parts = [int(x) for x in release.product_version.split(".")]

                if _version_is_newer(release_parts, current_parts) and not _version_is_newer(
                    release_parts, latest_parts
                ):
                    security_updates_missed += 1
                    if release.days_since_previous:
                        days_behind += release.days_since_previous

            except (ValueError, AttributeError):
                continue

        versions_behind = _calculate_version_distance(current_parts, latest_parts)

    except (ValueError, AttributeError):
        logger.warning("Failed to parse versions for currency calculation")

    # Calculate scoring (0-100, 100 is current)
    currency_score = 100
    if not is_current:
        currency_score -= min(versions_behind * 10, 50)  # Max 50 for version distance
        currency_score -= min(security_updates_missed * 5, 30)
        currency_score -= min(days_behind // 30, 20)

    return {
        "is_current": is_current,
        "current_version": current_version,
        "latest_version": latest_version,
        "versions_behind": versions_behind,
        "security_updates_missed": security_updates_missed,
        "days_behind": days_behind,
        "currency_score": max(0, currency_score),  # Don't go below 0
        "recommendation": _get_currency_recommendation(
            is_current, versions_behind, security_updates_missed
        ),
    }


def _version_is_newer(version_a: List[int], version_b: List[int]) -> bool:
    """
    Compare two version number lists to determine if A is newer than B.

    :param version_a: Version A as list of integers
    :type version_a: List[int]
    :param version_b: Version B as list of integers
    :type version_b: List[int]
    :return: True if version A is newer than version B
    :rtype: bool
    """
    max_len = max(len(version_a), len(version_b))
    a_padded = version_a + [0] * (max_len - len(version_a))
    b_padded = version_b + [0] * (max_len - len(version_b))

    return a_padded > b_padded


def _calculate_version_distance(current: List[int], latest: List[int]) -> int:
    """
    Calculate the 'distance' between two versions.

    :param current: Current version as list of integers
    :type current: List[int]
    :param latest: Latest version as list of integers
    :type latest: List[int]
    :return: Version distance (higher = further behind)
    :rtype: int
    """
    if not _version_is_newer(latest, current):
        return 0

    max_len = max(len(current), len(latest))
    current_padded = current + [0] * (max_len - len(current))
    latest_padded = latest + [0] * (max_len - len(latest))

    distance = 0
    for i, (current_part, latest_part) in enumerate(
        zip(current_padded, latest_padded, strict=False)
    ):
        if latest_part > current_part:
            # Weight earlier positions more heavily (major > minor > patch)
            weight = max_len - i
            distance += (latest_part - current_part) * weight

    return distance


def _get_currency_recommendation(
    is_current: bool, versions_behind: int, updates_missed: int
) -> str:
    if is_current:
        return "OS is current - no action needed"
    elif updates_missed >= 3:
        return "CRITICAL: Multiple security updates missed - update immediately"
    elif versions_behind >= 3:
        return "HIGH: Multiple versions behind - schedule update soon"
    elif updates_missed >= 1:
        return "MEDIUM: Security updates available - update when convenient"
    else:
        return "LOW: Minor version update available"
