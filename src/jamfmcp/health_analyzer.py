"""
Computer Health Analysis Module for Jamf Pro Data.

This module provides health scoring for computers managed by Jamf Pro,
analyzing security compliance, system health, policy adherence, and maintenance status.

Includes device diagnostic parsing functionality.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timezone
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError

from jamfmcp.jamfsdk.models.pro.computers import (
    Computer,
    ComputerExtensionAttribute,
    ComputerUserAndLocation,
)
from jamfmcp.sofa import (
    SOFAFeed,
    get_cves_for_version,
    get_sofa_feed,
    get_version_currency_info,
    parse_sofa_feed,
)

logger = logging.getLogger(__name__)


class HealthGrade(str, Enum):
    """Health grade enumeration."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class HealthStatus(str, Enum):
    """Health status enumeration."""

    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    CRITICAL = "Critical"


def fmt_tmz(time_input: str | datetime) -> str:
    """
    Format timestamp string or datetime object to human-readable format.

    Converts ISO 8601 timestamp string with timezone information or datetime object to a
    formatted string in "Month DD YYYY HH:MM AM/PM" format.

    :param time_input: ISO 8601 timestamp string with timezone or datetime object
    :type time_input: str | datetime
    :return: Formatted timestamp string
    :rtype: str
    """
    if not time_input:
        return "Unknown"

    # If it's already a datetime object, format it directly
    if isinstance(time_input, datetime):
        return time_input.strftime("%b %d %Y %I:%M %p")

    time_str = str(time_input)

    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ]

    for fmt in formats:
        try:
            normalized_time_str = (
                time_str.replace("Z", "+00:00") if time_str.endswith("Z") else time_str
            )
            date_obj = datetime.strptime(normalized_time_str, fmt)
            return date_obj.strftime("%b %d %Y %I:%M %p")
        except (ValueError, TypeError):
            continue

    logger.warning(f"Failed to parse timestamp: {time_str}")
    return time_str


class HealthScore(BaseModel):
    """Individual health metric score with details."""

    category: str = Field(..., description="The health category being scored")
    score: float = Field(..., ge=0, le=100, description="Score from 0-100")
    max_score: float = Field(..., ge=0, le=100, description="Maximum possible score")
    weight: float = Field(..., ge=0, le=1, description="Weight in overall calculation")
    factors: list[str] = Field(default_factory=list, description="Factors affecting this score")
    recommendations: list[str] = Field(
        default_factory=list, description="Improvement recommendations"
    )


class HealthScorecard(BaseModel):
    """Complete computer health scorecard."""

    overall_score: float = Field(..., ge=0, le=100, description="Overall health percentage")
    grade: HealthGrade = Field(..., description="Letter grade (A, B, C, D, F)")
    status: HealthStatus = Field(..., description="Health status description")

    security_score: HealthScore
    system_health_score: HealthScore
    compliance_score: HealthScore
    maintenance_score: HealthScore

    device_info: dict[str, Any] = Field(default_factory=dict)
    assessment_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))  # noqa

    critical_issues: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class HealthAnalyzer:
    """
    Analyzes computer health from Jamf Pro diagnostic data.

    This class processes comprehensive diagnostic information from Jamf Pro
    to generate detailed health scorecards with actionable recommendations.

    :param diagnostic_data: Parsed diagnostic data from Jamf Pro
    :type diagnostic_data: dict[str, Any]
    :param computer_history: Computer history data containing usage and policy logs
    :type computer_history: dict[str, Any] | None
    :param computer_inventory: Full computer inventory data
    :type computer_inventory: dict[str, Any] | None

    Example:
        >>> analyzer = HealthAnalyzer(diag_data, history_data, inventory_data)
        >>> scorecard = analyzer.generate_health_scorecard()
        >>> print(f"Overall Health: {scorecard.overall_score}%")
    """

    # Scoring weights
    CATEGORY_WEIGHTS = {
        "security": 0.35,  # 35% - Security is critical
        "system_health": 0.25,  # 25% - System performance and hardware
        "compliance": 0.25,  # 25% - Policy and management compliance
        "maintenance": 0.15,  # 15% - Regular maintenance and updates
    }

    # Time threshold (hours)
    RECENT_CHECKIN_THRESHOLD = 24
    RECENT_ACTIVITY_THRESHOLD = 72
    ACCEPTABLE_UPTIME_MAX = 336  # 2 weeks

    def __init__(
        self,
        diagnostic_data: dict[str, Any] | None = None,
        computer_history: dict[str, Any] | None = None,
        computer_inventory: dict[str, Any] | None = None,
        sofa_feed: SOFAFeed | None = None,
    ) -> None:
        """
        Initialize the health analyzer with optional diagnostic data and SOFA feed.

        If diagnostic_data is not provided but computer_inventory is available,
        the diagnostic data will be automatically parsed from the inventory.

        :param diagnostic_data: Parsed diagnostic data from Jamf Pro (optional)
        :type diagnostic_data: dict[str, Any] | None
        :param computer_history: Computer history data containing usage and policy logs
        :type computer_history: dict[str, Any] | None
        :param computer_inventory: Full computer inventory data
        :type computer_inventory: dict[str, Any] | None
        :param sofa_feed: SOFA feed for CVE and OS currency analysis (optional)
        :type sofa_feed: SOFAFeed | None
        """
        self.computer_history = computer_history or {}
        self.computer_inventory = computer_inventory or {}
        self.sofa_feed = sofa_feed

        # Parse JSON if needed
        if isinstance(computer_history, str):
            self.computer_history = json.loads(computer_history)
        if isinstance(computer_inventory, str):
            self.computer_inventory = json.loads(computer_inventory)

        if diagnostic_data is not None:
            # Use provided data
            if isinstance(diagnostic_data, str):
                self.diagnostic_data = json.loads(diagnostic_data)
            else:
                self.diagnostic_data = diagnostic_data
        elif self.computer_inventory:
            # Auto-parse diagnostic data from computer inventory
            self.diagnostic_data = self.parse_diags(self.computer_inventory)
        else:
            self.diagnostic_data = {}

        # Cache parsed computer for efficiency
        self._computer_model: Computer | None = None

    def _get_computer_model(self) -> Computer | None:
        """
        Get the parsed Computer model, caching it for efficiency.

        :return: Computer model if available
        :rtype: Computer | None
        """
        if self._computer_model is None and self.computer_inventory:
            try:
                self._computer_model = Computer.model_validate(self.computer_inventory)
            except (ValidationError, ValueError, TypeError) as e:
                # Keep as None if parsing fails
                logger.warning(f"Failed to parse computer inventory: {str(e)}")
                pass
        return self._computer_model

    def _apply_security_check(
        self,
        condition_failed: bool,
        points_penalty: int,
        factor_message: str,
        recommendation: str,
    ) -> tuple[int, str, str]:
        """
        Apply a security check and return penalty details if condition failed.

        :param condition_failed: Whether the security condition failed
        :type condition_failed: bool
        :param points_penalty: Points to deduct if condition failed
        :type points_penalty: int
        :param factor_message: Message to add to factors if condition failed
        :type factor_message: str
        :param recommendation: Recommendation to add if condition failed
        :type recommendation: str
        :return: tuple of (points_lost, factor, recommendation) - empty strings if condition passed
        :rtype: tuple[int, str, str]
        """
        if condition_failed:
            return points_penalty, factor_message, recommendation
        return 0, "", ""

    def _create_health_score(
        self,
        category: str,
        score: float,
        factors: list[str],
        recommendations: list[str],
    ) -> HealthScore:
        """
        Create a HealthScore object with proper formatting and validation.

        :param category: Health category name
        :type category: str
        :param score: Calculated score (will be clamped to 0-100)
        :type score: float
        :param factors: list of factors affecting the score
        :type factors: list[str]
        :param recommendations: list of recommendations for improvement
        :type recommendations: list[str]
        :return: Formatted HealthScore object
        :rtype: HealthScore
        """
        return HealthScore(
            category=category,
            score=max(0, score),
            max_score=100.0,
            weight=self.CATEGORY_WEIGHTS.get(category.lower().replace(" ", "_"), 0.0),
            factors=factors,
            recommendations=recommendations,
        )

    def _aggregate_check_results(
        self, checks: list[tuple[int, list[str], list[str]]]
    ) -> tuple[float, list[str], list[str]]:
        """
        Aggregate results from multiple security/health checks.

        :param checks: list of check results as (points_lost, factors, recommendations) tuples
        :type checks: list[tuple[int, list[str], list[str]]]
        :return: tuple of (total_score, all_factors, all_recommendations)
        :rtype: tuple[float, list[str], list[str]]
        """
        total_points_lost = 0
        all_factors = []
        all_recommendations = []

        for points_lost, factors, recommendations in checks:
            total_points_lost += points_lost
            all_factors.extend(factors)
            all_recommendations.extend(recommendations)

        final_score = 100.0 - total_points_lost
        return max(0, final_score), all_factors, all_recommendations

    def _safe_get_diagnostic_value(self, key: str, default: str = "Unknown") -> str:
        """
        Safely get a value from diagnostic data with fallback.

        :param key: Key to retrieve from diagnostic data
        :type key: str
        :param default: Default value if key is missing or empty
        :type default: str
        :return: Retrieved value or default
        :rtype: str
        """
        value = self.diagnostic_data.get(key, default)
        return value if value and str(value).strip() else default

    def _safe_get_inventory_value(self, *keys: str, default: Any = None) -> Any:
        """
        Safely navigate nested inventory data using a sequence of keys.

        :param keys: Sequence of keys to navigate nested data
        :type keys: str
        :param default: Default value if navigation fails
        :type default: Any
        :return: Retrieved value or default
        :rtype: Any
        """
        current = self.computer_inventory

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    @staticmethod
    async def load_sofa_feed() -> SOFAFeed | None:
        """
        Load the latest SOFA feed data for CVE and OS analysis.

        :return: Parsed SOFA feed or None if loading fails
        :rtype: SOFAFeed | None
        """
        try:
            raw_feed = await get_sofa_feed()
            return parse_sofa_feed(raw_feed)
        except (httpx.HTTPStatusError, ValueError, TypeError) as e:
            logger.warning(f"Failed to load SOFA feed: {str(e)}")
            return None

    def _get_os_family_from_version(self, os_version: str) -> str | None:
        """
        Determine the OS family from version string for SOFA lookup.

        :param os_version: OS version string (e.g., "15.1.0", "14.6.1", "10.15.7")
        :type os_version: str
        :return: OS family for SOFA lookup (e.g., "Sequoia 15", "Sonoma 14") or None
        :rtype: str | None
        """
        if not os_version or os_version == "Unknown":
            return None

        try:
            major_version = int(os_version.split(".")[0])
            os_family_map = {
                26: "Tahoe 26",
                15: "Sequoia 15",
                14: "Sonoma 14",
                13: "Ventura 13",
                12: "Monterey 12",
                11: "Big Sur 11",
                10: "Catalina 10",
            }

            if major_version == 10:
                try:
                    minor_version = int(os_version.split(".")[1])
                    legacy_mapping = {
                        15: "Catalina 10",
                        14: "Mojave 10",
                        13: "High Sierra 10",
                        12: "Sierra 10",
                    }
                    return legacy_mapping.get(minor_version, f"macOS 10.{minor_version}")
                except (ValueError, IndexError):
                    return "macOS 10"

            return os_family_map.get(major_version)

        except (ValueError, IndexError):
            logger.warning(f"Failed to parse OS version: {os_version}")
            return None

    def _check_cve_vulnerabilities(self) -> tuple[int, list[str], list[str]]:
        """
        Check for CVE vulnerabilities using SOFA feed data.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        if not self.sofa_feed:
            return 0, [], []

        os_version = self._safe_get_diagnostic_value("OS Version")
        if os_version == "Unknown":
            return 0, [], []

        os_family = self._get_os_family_from_version(os_version)
        if not os_family:
            return 0, [], []

        try:
            affecting_cves, exploited_cves = get_cves_for_version(
                self.sofa_feed, os_version, os_family
            )

            points_lost = 0
            factors = []
            recommendations = []

            # Severe penalty for actively exploited CVEs
            if exploited_cves:
                points_lost += len(exploited_cves) * 15  # 15 points lost per exploited CVE
                factors.append(f"Actively exploited CVEs: {len(exploited_cves)}")
                recommendations.append(
                    "CRITICAL: Update OS immediately - actively exploited vulnerabilities detected"
                )

            # Moderate penalty for other CVEs
            non_exploited_cves = affecting_cves - exploited_cves
            if non_exploited_cves:
                cve_penalty = min(len(non_exploited_cves) * 2, 25)
                points_lost += cve_penalty
                factors.append(f"Known CVEs affecting this version: {len(affecting_cves)}")

                if len(affecting_cves) > 20:
                    recommendations.append(
                        "HIGH: Multiple security vulnerabilities - schedule OS update soon"
                    )
                elif len(affecting_cves) > 5:
                    recommendations.append(
                        "MEDIUM: Security vulnerabilities detected - update when convenient"
                    )

            return points_lost, factors, recommendations

        except (ValueError, KeyError, AttributeError) as e:
            logger.warning(f"Failed to analyze CVEs for {os_version}: {str(e)}")
            return 0, [], []

    def _check_os_currency(self) -> tuple[int, list[str], list[str]]:
        """
        Check OS version currency using SOFA feed data when available.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        os_version = self._safe_get_diagnostic_value("OS Version")
        if os_version == "Unknown":
            return 5, ["OS Version: Unknown"], ["Unable to determine OS version"]

        if self.sofa_feed:
            os_family = self._get_os_family_from_version(os_version)
            if os_family:
                try:
                    currency_info = get_version_currency_info(self.sofa_feed, os_version, os_family)

                    # Convert to health penalty
                    currency_score = currency_info["currency_score"]
                    points_lost = max(0, 100 - currency_score) // 4

                    factors = [
                        f"OS Version: {os_version} (Latest: {currency_info['latest_version']})"
                    ]

                    if currency_info["versions_behind"] > 0:
                        factors.append(f"Versions behind: {currency_info['versions_behind']}")

                    if currency_info["security_updates_missed"] > 0:
                        factors.append(
                            f"Security updates missed: {currency_info['security_updates_missed']}"
                        )

                    recommendations = [currency_info["recommendation"]]

                    return points_lost, factors, recommendations
                except (ValueError, KeyError, AttributeError) as e:
                    logger.warning(f"Failed to get currency info for {os_version}: {str(e)}")

        # Fallback if SOFA feed not available
        if self._is_os_outdated(os_version):
            return (
                25,
                [f"OS Version: {os_version} (outdated)"],
                ["Update to latest macOS version"],
            )

        return 0, [], []

    def get_cve_analysis(self, include_detailed_cves: bool = False) -> dict[str, Any] | None:
        """
        Analyze CVE vulnerabilities affecting the current OS version.

        :param include_detailed_cves: Include detailed CVE information in the analysis
        :type include_detailed_cves: bool
        :return: CVE analysis dictionary with vulnerability counts and risk assessment, or None if analysis unavailable
        :rtype: dict[str, Any] | None
        """
        if not self.sofa_feed:
            return None

        os_version = self._safe_get_diagnostic_value("OS Version")
        if os_version == "Unknown":
            return None

        os_family = self._get_os_family_from_version(os_version)
        if not os_family:
            return None

        try:
            affecting_cves, exploited_cves = get_cves_for_version(
                self.sofa_feed, os_version, os_family
            )
            currency_info = get_version_currency_info(self.sofa_feed, os_version, os_family)
            risk_assessment = self._assess_detailed_cve_risk(
                len(affecting_cves), len(exploited_cves)
            )

            analysis_result = {
                "os_version": os_version,
                "os_family": os_family,
                "total_cves_affecting": len(affecting_cves),
                "actively_exploited_cves_count": len(exploited_cves),
                "actively_exploited_cves": sorted(list(exploited_cves)),  # noqa: C414
                "affecting_cves_list": sorted(list(affecting_cves)),  # noqa: C414
                "currency_info": currency_info,
                "risk_assessment": risk_assessment,
                "risk_level": risk_assessment["risk_level"],  # Keep for backward compatibility
            }

            # Add detailed CVE information if requested
            if include_detailed_cves:
                analysis_result["detailed_cves"] = self._build_detailed_cve_info(
                    affecting_cves, exploited_cves, os_family
                )

            return analysis_result

        except (ValueError, KeyError, AttributeError) as e:
            logger.warning(f"Failed to generate CVE analysis for {os_version}: {str(e)}")
            return None

    def _assess_cve_risk_level(self, total_cves: int, exploited_cves: int) -> str:
        """
        Assess risk level based on CVE counts.

        :param total_cves: Total number of affecting CVEs
        :type total_cves: int
        :param exploited_cves: Number of actively exploited CVEs
        :type exploited_cves: int
        :return: Risk level assessment
        :rtype: str
        """
        if exploited_cves > 0:
            return "CRITICAL"
        elif total_cves > 20:
            return "HIGH"
        elif total_cves > 5:
            return "MEDIUM"
        elif total_cves > 0:
            return "LOW"
        else:
            return "MINIMAL"

    def _assess_detailed_cve_risk(
        self, total_cves: int, actively_exploited_count: int
    ) -> dict[str, Any]:
        """
        Assess detailed risk level based on CVE counts and exploitation status.

        :param total_cves: Total number of CVEs affecting the system
        :type total_cves: int
        :param actively_exploited_count: Number of actively exploited CVEs
        :type actively_exploited_count: int
        :return: Detailed risk assessment dictionary with level and recommendations
        :rtype: dict[str, Any]
        """
        # Determine risk level based on CVE metrics
        if actively_exploited_count > 0:
            risk_level = "CRITICAL"
            recommendation = (
                "Immediate update required - actively exploited vulnerabilities present"
            )
            priority = 1
        elif total_cves >= 10:
            risk_level = "HIGH"
            recommendation = "High priority update - multiple security vulnerabilities present"
            priority = 2
        elif total_cves >= 5:
            risk_level = "MEDIUM"
            recommendation = "Medium priority update - several security vulnerabilities present"
            priority = 3
        elif total_cves >= 1:
            risk_level = "LOW"
            recommendation = "Low priority update - minor security vulnerabilities present"
            priority = 4
        else:
            risk_level = "MINIMAL"
            recommendation = (
                "System appears current - no known vulnerabilities affecting this version"
            )
            priority = 5

        # Calculate risk score (0-100, where 100 is highest risk)
        risk_score = min(100, (actively_exploited_count * 40) + (total_cves * 3))

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "priority": priority,
            "recommendation": recommendation,
            "metrics": {
                "total_cves": total_cves,
                "actively_exploited": actively_exploited_count,
            },
        }

    def _build_detailed_cve_info(
        self, affecting_cves: set, actively_exploited_cves: set, os_family: str
    ) -> list[dict[str, Any]]:
        """
        Build detailed CVE information including descriptions and links.

        :param affecting_cves: Set of CVE IDs affecting the OS version
        :type affecting_cves: set
        :param actively_exploited_cves: Set of actively exploited CVE IDs
        :type actively_exploited_cves: set
        :param os_family: OS family name
        :type os_family: str
        :return: list of detailed CVE information dictionaries
        :rtype: list[dict[str, Any]]
        """
        detailed_cves = []

        if os_family not in self.sofa_feed.os_versions:
            return detailed_cves

        os_info = self.sofa_feed.os_versions[os_family]

        # Build CVE details from security releases
        for release in os_info.security_releases:
            for cve_id, _ in release.cves.items():
                if cve_id in affecting_cves:
                    # Generate NIST NVD link for CVE
                    nvd_link = f"https://nvd.nist.gov/vuln/detail/{cve_id}"

                    detailed_cves.append(
                        {
                            "cve_id": cve_id,
                            "actively_exploited": cve_id in actively_exploited_cves,
                            "fixed_in_version": release.product_version,
                            "release_date": release.release_date,
                            "update_name": release.update_name,
                            "nvd_link": nvd_link,
                        }
                    )

        # Sort by actively exploited first, then by CVE ID
        detailed_cves.sort(key=lambda x: (not x["actively_exploited"], x["cve_id"]))

        return detailed_cves

    def _check_gatekeeper_security(self) -> tuple[int, list[str], list[str]]:
        """
        Check Gatekeeper security status.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        gatekeeper = self.diagnostic_data.get("Gatekeeper", "").lower()
        points_lost, factor, recommendation = self._apply_security_check(
            condition_failed=gatekeeper != "app_store_and_identified_developers",
            points_penalty=20,
            factor_message=f"Gatekeeper: {gatekeeper}",
            recommendation="Enable Gatekeeper to protect against malicious software",
        )

        factors = [factor] if factor else []
        recommendations = [recommendation] if recommendation else []
        return points_lost, factors, recommendations

    def _check_sip_status(self) -> tuple[int, list[str], list[str]]:
        """
        Check System Integrity Protection (SIP) status.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        sip_status = self.diagnostic_data.get("SIP Status", "").lower()
        points_lost, factor, recommendation = self._apply_security_check(
            condition_failed=sip_status != "enabled",
            points_penalty=25,
            factor_message=f"SIP Status: {sip_status}",
            recommendation="System Integrity Protection should be enabled",
        )

        factors = [factor] if factor else []
        recommendations = [recommendation] if recommendation else []
        return points_lost, factors, recommendations

    def _check_xprotect_status(self) -> tuple[int, list[str], list[str]]:
        """
        Check XProtect malware protection status.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        xprotect = self.diagnostic_data.get("XProtect Version", "")
        condition_failed = not xprotect or xprotect.lower() in [
            "unknown",
            "not available",
        ]
        points_lost, factor, recommendation = self._apply_security_check(
            condition_failed=condition_failed,
            points_penalty=15,
            factor_message="XProtect: Not available",
            recommendation="Ensure XProtect malware definitions are current",
        )

        factors = [factor] if factor else []
        recommendations = [recommendation] if recommendation else []
        return points_lost, factors, recommendations

    def _check_certificate_compliance(self) -> tuple[int, list[str], list[str]]:
        """
        Check security certificate compliance.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        okta_cert = self.diagnostic_data.get("Okta SCEP Cert Present", False)
        condition_failed = not okta_cert or (
            isinstance(okta_cert, str) and okta_cert.lower() != "true"
        )
        points_lost, factor, recommendation = self._apply_security_check(
            condition_failed=condition_failed,
            points_penalty=20,
            factor_message="SCEP Certificate: Missing",
            recommendation="Install required security certificates",
        )

        factors = [factor] if factor else []
        recommendations = [recommendation] if recommendation else []
        return points_lost, factors, recommendations

    def _check_filevault_encryption(self) -> tuple[int, list[str], list[str]]:
        """
        Check FileVault disk encryption status with comprehensive analysis.

        Handles Jamf Pro reporting nuances where fileVault2Enabled can be False
        despite the drive being encrypted as expected.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        factors = []
        recommendations = []
        points_lost = 0

        if not self.computer_inventory:
            return points_lost, factors, recommendations

        disk_encryption = self.computer_inventory.get("diskEncryption", {})

        # Gather all FileVault indicators for comprehensive analysis
        filevault_enabled = disk_encryption.get("fileVault2Enabled", False)
        boot_details = disk_encryption.get("bootPartitionEncryptionDetails", {})
        partition_state = boot_details.get("partitionFileVault2State", "")
        enabled_users = disk_encryption.get("fileVault2EnabledUserNames", [])
        recovery_key_status = disk_encryption.get("individualRecoveryKeyValidityStatus", "")

        # Determine actual encryption state based on all indicators
        # Due to Jamf Pro reporting nuances, fileVault2Enabled can be False even when encrypted
        encryption_indicators = {
            "partition_encrypted": partition_state == "ENCRYPTED",
            "users_enabled": bool(enabled_users),
            "recovery_key_valid": recovery_key_status == "VALID",
        }

        # Count positive encryption indicators
        positive_indicators = sum(encryption_indicators.values())

        # Determine FileVault status and apply appropriate scoring
        if not filevault_enabled and positive_indicators == 0:
            # All indicators suggest FileVault is truly disabled - highest penalty
            points_lost = 40  # Increased penalty as FileVault is critical security control
            factors.append("FileVault: Completely disabled")
            recommendations.append("CRITICAL: Enable FileVault disk encryption immediately")

        elif not filevault_enabled and positive_indicators < 3:
            # Mixed indicators suggest partial or problematic configuration
            points_lost = 25
            issues = []
            if not encryption_indicators["partition_encrypted"]:
                issues.append("partition not encrypted")
            if not encryption_indicators["users_enabled"]:
                issues.append("no enabled users")
            if not encryption_indicators["recovery_key_valid"]:
                issues.append("invalid recovery key")

            factors.append(f"FileVault: Partially configured ({', '.join(issues)})")
            recommendations.append("Review and complete FileVault configuration")

        elif not filevault_enabled and positive_indicators == 3:
            # Jamf reporting issue: fileVault2Enabled is False but all other indicators suggest encryption is working
            points_lost = 5  # Minor deduction for reporting inconsistency
            factors.append("FileVault: Encrypted but reporting inconsistency detected")
            recommendations.append("Verify FileVault status reporting in Jamf Pro")

        else:
            # fileVault2Enabled is True - check for configuration issues
            filevault_issues = []

            if partition_state != "ENCRYPTED":
                filevault_issues.append("Boot partition not encrypted")

            if not enabled_users:
                filevault_issues.append("No users enabled for FileVault")

            if recovery_key_status != "VALID":
                filevault_issues.append("Invalid recovery key")

            # Deduct points for FileVault configuration issues
            if filevault_issues:
                points_lost = min(
                    15, len(filevault_issues) * 5
                )  # Max 15 points deduction for config issues
                factors.append(f"FileVault configuration issues: {', '.join(filevault_issues)}")
                recommendations.append("Review and fix FileVault configuration")

        return points_lost, factors, recommendations

    def _calculate_security_score(self) -> HealthScore:
        """
        Calculate security-related health score.

        Evaluates:
        - Gatekeeper status
        - System Integrity Protection (SIP)
        - XProtect version
        - FileVault encryption
        - Certificate compliance

        :return: HealthScore object with security assessment
        :rtype: HealthScore
        """
        # Run all security checks using the extracted methods
        security_checks = [
            self._check_gatekeeper_security(),
            self._check_sip_status(),
            self._check_xprotect_status(),
            self._check_certificate_compliance(),
            self._check_filevault_encryption(),
            self._check_cve_vulnerabilities(),  # Enhanced with SOFA data
        ]

        # Aggregate results using helper utility
        final_score, all_factors, all_recommendations = self._aggregate_check_results(
            security_checks
        )

        return self._create_health_score("Security", final_score, all_factors, all_recommendations)

    def _check_battery_health(self) -> tuple[int, list[str], list[str]]:
        """
        Check battery health status.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        battery_health = self._safe_get_diagnostic_value("Battery Health")

        if battery_health == "Unknown":
            return 0, [], []

        if "poor" in battery_health.lower():
            return (
                25,
                [f"Battery Health: {battery_health}"],
                ["Consider battery replacement"],
            )
        elif "fair" in battery_health.lower():
            return (
                10,
                [f"Battery Health: {battery_health}"],
                ["Monitor battery health closely"],
            )

        return 0, [], []

    def _check_device_connectivity(self) -> tuple[int, list[str], list[str]]:
        """
        Check device connectivity based on last check-in time.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        last_checkin = self._safe_get_diagnostic_value("Last Check In")

        if last_checkin == "Unknown":
            return (
                15,
                ["Last Check In: Unknown"],
                ["Verify device connectivity to Jamf Pro"],
            )

        checkin_score = self._score_time_recency(last_checkin, self.RECENT_CHECKIN_THRESHOLD)

        if checkin_score < 0.8:  # Less than 80% means issues
            points_lost = int(30 * (1 - checkin_score))
            factors = [f"Last Check In: {last_checkin}"]

            if checkin_score < 0.5:
                recommendations = ["Device not checking in regularly - investigate connectivity"]
            else:
                recommendations = ["Check device connectivity to Jamf Pro"]

            return points_lost, factors, recommendations

        return 0, [], []

    def _check_system_uptime(self) -> tuple[int, list[str], list[str]]:
        """
        Check system uptime for excessive values.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        uptime = self._safe_get_diagnostic_value("Uptime")

        if uptime == "Unknown":
            return 0, [], []

        uptime_hours = self._parse_uptime_hours(uptime)

        if uptime_hours > self.ACCEPTABLE_UPTIME_MAX:
            return (
                20,
                [f"Uptime: {uptime} (excessive)"],
                ["Restart device regularly to apply updates and clear memory"],
            )
        elif uptime_hours > self.ACCEPTABLE_UPTIME_MAX / 2:
            return 10, [f"Uptime: {uptime} (high)"], ["Consider restarting device soon"]

        return 0, [], []

    def _check_os_currency(self) -> tuple[int, list[str], list[str]]:
        """
        Check OS version currency.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        os_version = self._safe_get_diagnostic_value("OS Version")

        if os_version == "Unknown":
            return 5, ["OS Version: Unknown"], ["Unable to determine OS version"]

        if self._is_os_outdated(os_version):
            return (
                25,
                [f"OS Version: {os_version} (outdated)"],
                ["Update to latest macOS version"],
            )

        return 0, [], []

    def _calculate_system_health_score(self) -> HealthScore:
        """
        Calculate system health score.

        Evaluates:
        - Battery health
        - Last check-in time
        - System uptime
        - OS version currency
        - Hardware status

        :return: HealthScore object with system health assessment
        :rtype: HealthScore
        """
        # Run all system health checks using extracted methods
        system_checks = [
            self._check_battery_health(),
            self._check_device_connectivity(),
            self._check_system_uptime(),
            self._check_os_currency(),  # Enhanced with SOFA data when available
        ]

        # Aggregate results using helper utility
        final_score, all_factors, all_recommendations = self._aggregate_check_results(system_checks)

        return self._create_health_score(
            "System Health", final_score, all_factors, all_recommendations
        )

    def _check_policy_compliance(self) -> tuple[int, list[str], list[str]]:
        """
        Check policy execution success rate.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        if not self.computer_history:
            return 0, [], []

        policy_logs = self.computer_history.get("policy_logs", [])
        if not policy_logs:
            return 0, [], []

        # Calculate success rate for last 10 policies
        recent_policies = [
            p
            for p in policy_logs[-10:]  # Last 10 policies
            if p.get("status", "").lower() == "completed"
        ]
        success_rate = len(recent_policies) / min(len(policy_logs), 10)

        if success_rate < 0.8:
            points_lost = int(40 * (1 - success_rate))
            factors = [f"Policy Success Rate: {success_rate:.1%}"]
            recommendations = ["Investigate failed policy executions"]
            return points_lost, factors, recommendations

        return 0, [], []

    def _check_command_compliance(self) -> tuple[int, list[str], list[str]]:
        """
        Check management command success rate and pending commands.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        if not self.computer_history:
            return 0, [], []

        commands_data = self.computer_history.get("commands", {})
        if not commands_data or not isinstance(commands_data, dict):
            return 0, [], []

        completed_commands = commands_data.get("completed", [])
        pending_commands = commands_data.get("pending", [])
        failed_commands = commands_data.get("failed", [])

        points_lost = 0
        factors = []
        recommendations = []

        # Check command success rate
        total_commands = len(completed_commands) + len(failed_commands)
        if total_commands > 0:
            command_success_rate = len(completed_commands) / total_commands

            if command_success_rate < 0.8:
                points_lost += int(30 * (1 - command_success_rate))
                factors.append(
                    f"Command Success Rate: {command_success_rate:.1%} ({len(completed_commands)}/{total_commands})"
                )
                recommendations.append("Review failed management commands")

        # Check for excessive pending commands
        if len(pending_commands) > 5:
            points_lost += 10
            factors.append(f"High number of pending commands: {len(pending_commands)}")
            recommendations.append("Monitor pending commands for potential issues")

        return points_lost, factors, recommendations

    def _check_profile_compliance(self) -> tuple[int, list[str], list[str]]:
        """
        Check certificate and configuration profile compliance.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        if not self.computer_inventory:
            return (
                10,
                ["No inventory data available"],
                ["Ensure device inventory is current"],
            )

        points_lost = 0
        factors = []
        recommendations = []

        # Check for required certificates
        certificates = self._safe_get_inventory_value("certificates", default=[])
        if len(certificates) < 2:  # Expect at least some certificates
            points_lost += 15
            factors.append("Insufficient certificates installed")
            recommendations.append("Ensure required certificates are deployed")

        # Check for configuration profiles
        profiles = self._safe_get_inventory_value("configurationProfiles", default=[])
        if len(profiles) < 1:  # Expect at least some configuration profiles
            points_lost += 15
            factors.append("No configuration profiles found")
            recommendations.append("Deploy required configuration profiles")

        return points_lost, factors, recommendations

    def _calculate_compliance_score(self) -> HealthScore:
        """
        Calculate policy compliance score.

        Evaluates:
        - Recent policy execution success
        - Management framework compliance
        - Configuration profile status
        - Required application presence

        :return: HealthScore object with compliance assessment
        :rtype: HealthScore
        """
        if not self.computer_history:
            return self._create_health_score(
                "Compliance",
                75.0,  # Neutral score if no history available
                ["No computer history available"],
                ["Ensure computer history is properly recorded in Jamf Pro"],
            )

        # Run all compliance checks using extracted methods
        compliance_checks = [
            self._check_policy_compliance(),
            self._check_command_compliance(),
            self._check_profile_compliance(),
        ]

        # Aggregate results using helper utility
        final_score, all_factors, all_recommendations = self._aggregate_check_results(
            compliance_checks
        )

        return self._create_health_score(
            "Compliance", final_score, all_factors, all_recommendations
        )

    def _check_user_activity(self) -> tuple[int, list[str], list[str]]:
        """
        Check recent user activity and login patterns.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        if not self.computer_history:
            return (
                5,
                ["No user activity history available"],
                ["Monitor device usage patterns"],
            )

        usage_logs = self.computer_history.get("computer_usage_logs", [])
        if not usage_logs:
            return 5, ["No user login records found"], ["Verify user activity logging"]

        last_login = usage_logs[0] if usage_logs else {}
        last_login_time = last_login.get("date_time", "")

        if not last_login_time:
            return 10, ["No recent user login data"], ["Check user activity monitoring"]

        activity_score = self._score_time_recency(last_login_time, self.RECENT_ACTIVITY_THRESHOLD)
        if activity_score < 0.7:
            points_lost = int(30 * (1 - activity_score))
            factors = [f"Last User Login: {last_login_time}"]
            recommendations = ["Device appears unused - verify if still needed"]
            return points_lost, factors, recommendations

        return 0, [], []

    def _check_inventory_currency(self) -> tuple[int, list[str], list[str]]:
        """
        Check inventory update recency.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        last_inventory = self._safe_get_diagnostic_value("Last Inventory Update")

        if last_inventory == "Unknown":
            return (
                15,
                ["Last Inventory Update: Unknown"],
                ["Ensure inventory collection is enabled"],
            )

        inventory_score = self._score_time_recency(last_inventory, 48)  # 2 days
        if inventory_score < 0.8:
            points_lost = int(40 * (1 - inventory_score))
            factors = [f"Last Inventory Update: {last_inventory}"]
            recommendations = ["Ensure regular inventory updates are occurring"]
            return points_lost, factors, recommendations

        return 0, [], []

    def _check_application_management(self) -> tuple[int, list[str], list[str]]:
        """
        Check application management and deployment activity.

        :return: tuple of (points_lost, factors, recommendations)
        :rtype: tuple[int, list[str], list[str]]
        """
        if not self.computer_history:
            return 0, [], []

        commands_data = self.computer_history.get("commands", {})
        if not commands_data or not isinstance(commands_data, dict):
            return 0, [], []

        completed_commands = commands_data.get("completed", [])

        # Look for application installation commands
        app_installs = [
            cmd for cmd in completed_commands if "install" in cmd.get("name", "").lower()
        ]

        # Check for recent application management
        recent_app_activity = any(
            self._is_recent_timestamp(cmd.get("completed_epoch", 0), 168)  # 1 week
            for cmd in app_installs[-5:]  # Last 5 app operations
        )

        if not recent_app_activity and len(app_installs) == 0:
            return (
                15,
                ["No recent application management"],
                ["Verify application deployment processes"],
            )

        return 0, [], []

    def _calculate_maintenance_score(self) -> HealthScore:
        """
        Calculate maintenance and update score.

        Evaluates:
        - Recent user activity
        - Application updates
        - Inventory updates
        - System maintenance patterns

        :return: HealthScore object with maintenance assessment
        :rtype: HealthScore
        """
        # Run all maintenance checks using extracted methods
        maintenance_checks = [
            self._check_user_activity(),
            self._check_inventory_currency(),
            self._check_application_management(),
        ]

        # Aggregate results using helper utility
        final_score, all_factors, all_recommendations = self._aggregate_check_results(
            maintenance_checks
        )

        return self._create_health_score(
            "Maintenance", final_score, all_factors, all_recommendations
        )

    def _score_time_recency(self, time_str: str, threshold_hours: float) -> float:
        """
        Score how recent a timestamp is (1.0 = very recent, 0.0 = very old).

        :param time_str: Time string to evaluate
        :type time_str: str
        :param threshold_hours: Hours threshold for scoring
        :type threshold_hours: float
        :return: Score between 0.0 and 1.0
        :rtype: float
        """
        try:
            # Handle "Yesterday at X" format
            if "yesterday" in time_str.lower():
                hours_ago = 24  # Approximate
            elif "today" in time_str.lower():
                hours_ago = 1  # Approximate
            else:
                # Try to parse actual timestamps
                # This is a simplified parser - in production you'd want more robust parsing
                hours_ago = threshold_hours + 1  # Default to threshold + 1

            if hours_ago <= threshold_hours:
                return 1.0 - (hours_ago / threshold_hours) * 0.5
            else:
                decay_factor = min(hours_ago / threshold_hours, 10)  # Cap decay
                return max(0.0, 1.0 - (decay_factor - 1) * 0.2)

        except (ValueError, AttributeError, TypeError) as e:
            logger.debug(f"Failed to parse time string '{time_str}': {str(e)}")
            return 0.5  # Neutral score if parsing fails

    def _parse_uptime_hours(self, uptime_str: str) -> float:
        """
        Parse uptime string to hours.

        :param uptime_str: Uptime string (e.g., "5 days, 3 hours")
        :type uptime_str: str
        :return: Total uptime in hours
        :rtype: float
        """
        try:
            hours = 0.0
            uptime_lower = uptime_str.lower()

            # Parse days
            if "day" in uptime_lower:
                days_part = uptime_lower.split("day")[0].strip().split()[-1]
                hours += float(days_part) * 24

            # Parse hours
            if "hour" in uptime_lower:
                if "day" in uptime_lower:
                    # Get hours after days - handle "days" plural
                    after_days = (
                        uptime_lower.split("days")[1]
                        if "days" in uptime_lower
                        else uptime_lower.split("day")[1]
                    )
                    parts = after_days.split("hour")[0].strip()
                    # Remove common separators and extract number
                    parts_clean = parts.replace(",", "").strip()
                    # Find the number in the parts
                    import re

                    hour_match = re.search(r"(\d+)", parts_clean)
                    if hour_match:
                        hours += float(hour_match.group(1))
                else:
                    hours_part = uptime_lower.split("hour")[0].strip().split()[-1]
                    hours += float(hours_part)

            return hours
        except (ValueError, AttributeError, TypeError) as e:
            logger.debug(f"Failed to parse uptime string '{uptime_str}': {str(e)}")
            return 0.0  # Default if parsing fails

    def _is_os_outdated(self, os_version: str) -> bool:
        """
        Check if OS version appears outdated using fallback logic when SOFA feed unavailable.

        This provides a reasonable assessment when SOFA feed is not available,
        based on current macOS support lifecycle and security considerations.

        :param os_version: OS version string
        :type os_version: str
        :return: True if version appears outdated
        :rtype: bool
        """
        try:
            # Extract version components
            version_parts = os_version.split(".")
            if len(version_parts) >= 1:
                major = int(version_parts[0])
                minor = int(version_parts[1]) if len(version_parts) >= 2 else 0

                # Current year assessment (update as needed)
                # As of 2024/2025, consider versions that are significantly behind current support

                # Very old macOS versions (unsupported)
                if major < 11:  # Big Sur and older
                    return True

                # Older supported versions that are multiple major releases behind
                elif major < 13:  # Monterey and older when Sequoia+ are current
                    return True

                # Recent versions - be more conservative and only flag if very behind on patches
                elif major == 13 and minor < 6:  # Ventura but significantly behind on patches
                    return True
                elif major == 14 and minor < 4:  # Sonoma but significantly behind on patches
                    return True
                elif major == 15 and minor < 0:  # Sequoia but behind on patches
                    return True

            return False
        except (ValueError, IndexError, AttributeError) as e:
            logger.debug(f"Failed to parse OS version '{os_version}': {str(e)}")
            return False  # Don't penalize if we can't parse

    def _is_recent_timestamp(self, epoch_timestamp: int, hours_threshold: float) -> bool:
        """
        Check if epoch timestamp is within hours threshold.

        :param epoch_timestamp: Unix timestamp in milliseconds
        :type epoch_timestamp: int
        :param hours_threshold: Hours threshold
        :type hours_threshold: float
        :return: True if timestamp is recent
        :rtype: bool
        """
        try:
            if epoch_timestamp <= 0:
                return False

            # Convert milliseconds to seconds
            timestamp_seconds = epoch_timestamp / 1000
            event_time = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)  # noqa
            now = datetime.now(timezone.utc)  # noqa

            hours_ago = (now - event_time).total_seconds() / 3600
            return hours_ago <= hours_threshold
        except (ValueError, OverflowError, OSError) as e:
            logger.debug(f"Failed to parse timestamp {epoch_timestamp}: {str(e)}")
            return False

    def _calculate_overall_score(
        self,
        security: HealthScore,
        system_health: HealthScore,
        compliance: HealthScore,
        maintenance: HealthScore,
    ) -> float:
        """
        Calculate weighted overall health score.

        :param security: Security health score
        :type security: HealthScore
        :param system_health: System health score
        :type system_health: HealthScore
        :param compliance: Compliance score
        :type compliance: HealthScore
        :param maintenance: Maintenance score
        :type maintenance: HealthScore
        :return: Weighted overall score (0-100)
        :rtype: float
        """
        weighted_score = (
            security.score * security.weight
            + system_health.score * system_health.weight
            + compliance.score * compliance.weight
            + maintenance.score * maintenance.weight
        )

        return round(weighted_score, 1)

    def _get_health_grade(self, score: float) -> HealthGrade:
        """
        Convert numeric score to letter grade.

        :param score: Numeric score (0-100)
        :type score: float
        :return: Letter grade (A, B, C, D, F)
        :rtype: HealthGrade
        """
        if score >= 90:
            return HealthGrade.A
        elif score >= 80:
            return HealthGrade.B
        elif score >= 70:
            return HealthGrade.C
        elif score >= 60:
            return HealthGrade.D
        else:
            return HealthGrade.F

    def _get_health_status(self, score: float) -> HealthStatus:
        """
        Get health status description.

        :param score: Numeric score (0-100)
        :type score: float
        :return: Health status description
        :rtype: HealthStatus
        """
        if score >= 90:
            return HealthStatus.EXCELLENT
        elif score >= 80:
            return HealthStatus.GOOD
        elif score >= 70:
            return HealthStatus.FAIR
        elif score >= 60:
            return HealthStatus.POOR
        else:
            return HealthStatus.CRITICAL

    def generate_health_scorecard(self) -> HealthScorecard:
        """
        Generate comprehensive health scorecard.

        Analyzes all health categories and produces a detailed scorecard
        with overall health percentage, individual category scores, and
        actionable recommendations.

        :return: Complete HealthScorecard with scores and recommendations
        :rtype: HealthScorecard
        """
        # Calculate individual category scores
        security = self._calculate_security_score()
        system_health = self._calculate_system_health_score()
        compliance = self._calculate_compliance_score()
        maintenance = self._calculate_maintenance_score()

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            security, system_health, compliance, maintenance
        )

        # Gather critical issues (scores below 60)
        critical_issues = []
        if security.score < 60:
            critical_issues.append("Critical security vulnerabilities detected")
        if system_health.score < 60:
            critical_issues.append("System health issues require attention")
        if compliance.score < 60:
            critical_issues.append("Policy compliance failures detected")
        if maintenance.score < 60:
            critical_issues.append("Maintenance and update issues detected")

        # Gather top recommendations
        all_recommendations = (
            security.recommendations
            + system_health.recommendations
            + compliance.recommendations
            + maintenance.recommendations
        )
        top_recommendations = all_recommendations[:5]  # Top 5 recommendations

        # Extract device info
        device_info = {
            "name": self.diagnostic_data.get("Name", "Unknown"),
            "serial_number": self.diagnostic_data.get("Serial Number", "Unknown"),
            "os_version": self.diagnostic_data.get("OS Version", "Unknown"),
            "last_checkin": self.diagnostic_data.get("Last Check In", "Unknown"),
            "assigned_to": self.diagnostic_data.get("Assigned To", "Unassigned"),
        }

        return HealthScorecard(
            overall_score=overall_score,
            grade=self._get_health_grade(overall_score),
            status=self._get_health_status(overall_score),
            security_score=security,
            system_health_score=system_health,
            compliance_score=compliance,
            maintenance_score=maintenance,
            device_info=device_info,
            critical_issues=critical_issues,
            recommendations=top_recommendations,
        )

    # =============================================================================
    # Device Diagnostic Parsing Methods (formerly from Parser class)
    # =============================================================================

    def _extract_general_info(self, computer: Computer) -> dict[str, str]:
        """
        Extract general device information from Computer model.

        :param computer: Computer model containing device information
        :type computer: Computer
        :return: dictionary of general device information
        :rtype: dict[str, str]
        """
        general = computer.general
        hardware = computer.hardware

        return {
            "Name": general.name if general and general.name else "Unknown",
            "Serial Number": (
                hardware.serialNumber if hardware and hardware.serialNumber else "Unknown"
            ),
            "Last Check In": (
                fmt_tmz(general.lastContactTime)
                if general and general.lastContactTime
                else "Unknown"
            ),
            "Last Inventory Update": (
                fmt_tmz(general.reportDate) if general and general.reportDate else "Unknown"
            ),
            "Last Reported IP": (
                general.lastReportedIp if general and general.lastReportedIp else "Unknown"
            ),
        }

    def _extract_hardware_info(self, computer: Computer) -> dict[str, str]:
        """
        Extract hardware information from Computer model.

        :param computer: Computer model containing hardware information
        :type computer: Computer
        :return: dictionary of hardware information
        :rtype: dict[str, str]
        """
        hardware = computer.hardware

        return {
            "Processor Type": (
                hardware.processorType if hardware and hardware.processorType else "Unknown"
            ),
            "Battery Health": (
                hardware.batteryHealth if hardware and hardware.batteryHealth else "Unknown"
            ),
        }

    def _extract_os_security_info(self, computer: Computer) -> dict[str, str]:
        """
        Extract operating system and security information from Computer model.

        :param computer: Computer model containing OS and security information
        :type computer: Computer
        :return: dictionary of OS and security information
        :rtype: dict[str, str]
        """
        security = computer.security
        operating_system = computer.operatingSystem

        return {
            "OS Version": (
                operating_system.version
                if operating_system and operating_system.version
                else "Unknown"
            ),
            "Gatekeeper": (
                security.gatekeeperStatus.value
                if security and security.gatekeeperStatus
                else "Unknown"
            ),
            "XProtect Version": (
                security.xprotectVersion if security and security.xprotectVersion else "Unknown"
            ),
            "SIP Status": (
                security.sipStatus.value if security and security.sipStatus else "Unknown"
            ),
        }

    def _extract_user_assignment_info(self, computer: Computer) -> dict[str, str]:
        """
        Extract user assignment information from Computer model.

        :param computer: Computer model containing user assignment information
        :type computer: Computer
        :return: dictionary of user assignment information
        :rtype: dict[str, str]
        """
        user_info = self._enrich_user_location(computer.userAndLocation)

        return {
            "Assigned To": user_info.get("realname", "Unknown"),
            "Email": user_info.get("email", "Unknown"),
            "Department": f"{user_info.get('departmentName', 'Unknown')} ({user_info.get('departmentId', 'Unknown')})",
        }

    def _normalize_payload_enums(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Normalize enum values in the payload to match expected jamfsdk format.

        Converts lowercase enum values to uppercase as expected by the Computer model.

        :param payload: Raw payload from Jamf API
        :type payload: dict[str, Any]
        :return: Normalized payload with corrected enum values
        :rtype: dict[str, Any]
        """
        normalized = payload.copy()

        # Normalize security enum values
        if "security" in normalized and isinstance(normalized["security"], dict):
            security = normalized["security"]

            # Map sipStatus values to expected enum values
            if "sipStatus" in security and isinstance(security["sipStatus"], str):
                sip_mapping = {
                    "enabled": "ENABLED",
                    "disabled": "DISABLED",
                    "not_collected": "NOT_COLLECTED",
                    "not_available": "NOT_AVAILABLE",
                }
                sip_value = security["sipStatus"].lower()
                if sip_value in sip_mapping:
                    security["sipStatus"] = sip_mapping[sip_value]

            # Map gatekeeperStatus values to expected enum values
            if "gatekeeperStatus" in security and isinstance(security["gatekeeperStatus"], str):
                gatekeeper_mapping = {
                    "app_store_and_identified_developers": "APP_STORE_AND_IDENTIFIED_DEVELOPERS",
                    "app_store": "APP_STORE",
                    "disabled": "DISABLED",
                    "not_collected": "NOT_COLLECTED",
                }
                gatekeeper_value = security["gatekeeperStatus"].lower()
                if gatekeeper_value in gatekeeper_mapping:
                    security["gatekeeperStatus"] = gatekeeper_mapping[gatekeeper_value]

        return normalized

    def parse_diags(self, payload: dict[str, Any]) -> dict[str, str]:
        """
        Parse comprehensive device diagnostics information from Jamf Pro payload.

        Leverages the Computer model for structured data parsing and validation.
        Compiles a complete diagnostic report including general device information,
        hardware details, security status, user assignment, and security tool status.

        :param payload: The Jamf API response payload containing device information
        :type payload: dict[str, Any]
        :return: Complete device diagnostics dictionary with formatted values
        :rtype: dict[str, str]
        :raises Exception: If payload parsing fails with detailed error information
        """
        try:
            # Normalize enum values to match expected format
            normalized_payload = self._normalize_payload_enums(payload)

            # Parse the payload into a structured Computer model for type safety and validation
            computer = Computer.model_validate(normalized_payload)

            # Extract extension attributes efficiently
            eas = self._extract_extension_attributes(computer.extensionAttributes or [])

            # Extract information using focused helper methods
            general_info = self._extract_general_info(computer)
            hardware_info = self._extract_hardware_info(computer)
            os_security_info = self._extract_os_security_info(computer)
            user_assignment_info = self._extract_user_assignment_info(computer)

            # Parse Falcon data using structured models
            falcon_dict = self._parse_falcon_from_computer(computer)

            # Combine all diagnostic information
            diag_data = {
                **general_info,
                **hardware_info,
                **os_security_info,
                **user_assignment_info,
                "Uptime": eas.get("Uptime", "Unknown"),
            }

            return {**diag_data, **falcon_dict}

        except (ValidationError, ValueError, KeyError, AttributeError) as e:
            # Add detailed error information for debugging
            logger.error(
                "Error in parse_diags processing: %s. Payload keys: %s",
                str(e),
                list(payload.keys()) if payload else "None",
            )
            raise ValueError(
                f"Error in parse_diags processing: {str(e)}. "
                f"Payload keys: {list(payload.keys()) if payload else 'None'}"
            ) from e

    def _extract_extension_attributes(
        self, extension_attributes: list[ComputerExtensionAttribute]
    ) -> dict[str, str]:
        """
        Extract and format extension attributes from Computer model.

        :param extension_attributes: list of ComputerExtensionAttribute objects
        :type extension_attributes: list[ComputerExtensionAttribute]
        :return: dictionary mapping extension attribute names to values
        :rtype: dict[str, str]
        """
        result = {}
        for ea in extension_attributes:
            if ea and ea.name and ea.values and len(ea.values) > 0:
                result[ea.name] = ea.values[0]
        return result

    def _enrich_user_location(
        self, user_location: ComputerUserAndLocation | None
    ) -> dict[str, Any]:
        """
        Enrich user location information with department name.

        :param user_location: ComputerUserAndLocation object
        :type user_location: ComputerUserAndLocation | None
        :return: User assignment information with department name resolved
        :rtype: dict[str, Any]
        """
        if not user_location or not user_location.realname:
            return {
                "realname": "Unassigned",
                "email": "Unassigned",
                "departmentId": "Unassigned",
                "departmentName": "Unassigned",
            }

        return {
            "realname": user_location.realname,
            "email": user_location.email,
            "departmentId": user_location.departmentId,
        }

    def _parse_falcon_from_computer(self, computer: Computer) -> dict[str, str]:
        """
        Parse CrowdStrike Falcon sensor information from Computer model.

        :param computer: Computer object containing all device information
        :type computer: Computer
        :return: dictionary containing Falcon sensor details and status
        :rtype: dict[str, str]
        """
        falcon_dict = {}

        # Check for Falcon application in applications list
        if computer.applications:
            for app in computer.applications:
                if app and app.name == "Falcon.app":
                    falcon_dict["Installed"] = True
                    falcon_dict["Version"] = app.version or "Unknown"
                    break

        # Check for Falcon service in services list
        if computer.services:
            falcon_service_running = any(
                service and service.name and "com.crowdstrike.falcon.Agent" in service.name
                for service in computer.services
            )
            falcon_dict["Falcon Service Status"] = (
                "Running" if falcon_service_running else "Not loaded"
            )

        # Extract Falcon health information from extension attributes
        if computer.extensionAttributes:
            for ea in computer.extensionAttributes:
                if ea and ea.name == "Crowdstrike Falcon Sensor Status" and ea.values:
                    falcon_health = ea.values[0]
                    if falcon_health:
                        lines = falcon_health.split("\\n")
                        for line in lines:
                            if ": " in line:
                                key, value = line.split(": ", 1)
                                falcon_dict[key.strip()] = value.strip()
                    break

        return falcon_dict
