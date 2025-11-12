"""
Jamf Pro MCP Server.

FastMCP server providing tools for interacting with Jamf Pro API.

## Parameter Handling
Many tools accept ID parameters (computer_id, policy_id, etc.) as strings rather than
integers to ensure compatibility across MCP clients. These parameters are converted to
integers internally before API calls. This pattern accommodates clients that serialize
numeric inputs as strings during JSON schema validation.

When calling these tools:
- Accept: "12345" or 12345
- Both formats work identically
"""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import Context, FastMCP

from jamfmcp.api import JamfApi
from jamfmcp.auth import JamfAuth
from jamfmcp.health_analyzer import HealthAnalyzer
from jamfmcp.jamfsdk.clients.pro_api.pagination import FilterField

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastMCP):
    """Initialize resources on startup, cleanup on shutdown."""
    auth = JamfAuth()
    jamf_api = JamfApi(auth)
    app.jamf_api = jamf_api

    yield


# Create server and configurations
mcp = FastMCP(name="Jamf Pro MCP", lifespan=lifespan)


@mcp.tool
async def get_computer_inventory(
    serial: str, sections: list[str] | None = None, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed computer inventory information by serial number.

    :param serial: The serial number of the computer
    :type serial: str
    :param sections: Optional list of inventory sections to retrieve (defaults to ALL).
    :type sections: list[str] | None, optional
    :return: Dictionary containing computer inventory data including hardware details,
            OS information, installed applications, user/location data, and more
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Starting inventory retrieval for serial {serial}")
        await ctx.info(
            f"Fetching computer inventory for {serial}",
            extra={"serial": serial, "sections": sections or ["ALL"]},
        )

    try:
        result = await mcp.jamf_api.get_computer_inventory(
            serial=serial, sections=sections, ctx=ctx
        )

        if ctx:
            await ctx.info(
                f"Successfully retrieved inventory for {serial}",
                extra={
                    "serial": serial,
                    "computer_id": result.get("id"),
                    "os_version": result.get("operatingSystem", {}).get("version"),
                },
            )

        return result
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve inventory for {serial}: {str(e)}",
                extra={"serial": serial, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting inventory for serial {serial}: {str(e)}")
        return {
            "error": "Failed to retrieve inventory",
            "message": str(e),
            "serial": serial,
        }


@mcp.tool
async def get_computer_history(
    computer_id: int | str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get computer history including policy logs, management commands, and user activity.

    Note: computer_id should be the JSS ID of the computer. The computer_id can be retrieved from
    ``get_computer_inventory`` results.

    :param computer_id: The JSS ID of the computer
    :type computer_id: int | str
    :return: Dictionary containing computer history data
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching computer history for ID {computer_id}")

    try:
        computer_id_int = int(computer_id)

        if ctx:
            await ctx.info(
                f"Retrieving history for computer {computer_id_int}",
                extra={"computer_id": computer_id_int},
            )

        result = await mcp.jamf_api.get_computer_history(computer_id_int, ctx=ctx)

        if ctx:
            await ctx.info(
                f"Successfully retrieved history for computer {computer_id_int}",
                extra={
                    "computer_id": computer_id_int,
                    "policy_count": len(result.get("policies_completed", []))
                    if isinstance(result, dict)
                    else 0,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid computer_id format: {computer_id}",
                extra={"computer_id": computer_id, "expected": "integer"},
            )

        logger.error(f"Invalid computer_id format: {computer_id}")
        return {
            "error": "Invalid computer_id",
            "message": f"computer_id must be a valid integer, got: {computer_id} (type: {type(computer_id)})",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve history for computer {computer_id}: {str(e)}",
                extra={"computer_id": computer_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting history for computer {computer_id}: {str(e)}")
        return {
            "error": "Failed to retrieve history",
            "message": str(e),
            "computer_id": computer_id,
        }


@mcp.tool
async def search_computers(
    identifier: str | None = None,
    page_size: str | None = "100",
    sections: list[str] | None = None,
    ctx: Context | None = None,
) -> list[dict[str, Any]]:
    """
    Search for computers by name or serial number.

    :param identifier: Computer name or serial number to search for
    :type identifier: str | None
    :param page_size: Number of results per page (default: 100)
    :type page_size: str | None
    :param sections: Optional list of inventory sections to retrieve
    :type sections: list[str] | None
    :return: List of computers matching the search criteria
    :rtype: list[dict[str, Any]]
    """
    page_size_int = int(page_size)

    if ctx:
        await ctx.debug(f"Searching for computers with identifier: {identifier}")
        await ctx.info(
            f"Searching computers{' for ' + identifier if identifier else ''}",
            extra={"identifier": identifier, "page_size": page_size_int, "sections": sections},
        )

    filter_expression = None
    if identifier:
        filter_expression = FilterField("general.name").eq(identifier) | FilterField(
            "hardware.SerialNumber"
        ).eq(identifier)

    try:
        results = await mcp.jamf_api.search_computers(
            filter_expression=filter_expression, page_size=page_size_int, sections=sections, ctx=ctx
        )

        if ctx:
            await ctx.info(
                f"Found {len(results)} computers{' matching ' + identifier if identifier else ''}",
                extra={"count": len(results), "identifier": identifier},
            )

        return results
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Computer search failed: {str(e)}",
                extra={"identifier": identifier, "error_type": type(e).__name__},
            )
        raise


@mcp.tool
async def get_health_scorecard(
    serial: str, email_address: str | None = None, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Generate comprehensive health scorecard for a computer.

    :param serial: Computer serial number
    :type serial: str
    :param email_address: Optional email address to lookup serial number
    :type email_address: str | None
    :return: Health scorecard with overall score, grades, and recommendations
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Starting health scorecard generation for serial {serial}")
        if email_address:
            await ctx.info(
                f"Looking up serial number for email {email_address}",
                extra={"email_address": email_address},
            )

    try:
        try:
            if email_address:
                serial = await mcp.jamf_api.get_serial_for_user(email_address, ctx=ctx)
                if ctx:
                    await ctx.info(
                        f"Found serial {serial} for user {email_address}",
                        extra={"email_address": email_address, "serial": serial},
                    )
        except Exception as e:
            if ctx:
                await ctx.error(
                    f"Failed to find serial for user {email_address}: {str(e)}",
                    extra={"email_address": email_address, "error_type": type(e).__name__},
                )
            return {
                "error": "No serial found",
                "message": f"Serial was not found for user {email_address}: {e}",
            }

        if ctx:
            await ctx.info(
                f"Fetching inventory and history for health analysis", extra={"serial": serial}
            )

        computer_inventory = await mcp.jamf_api.get_computer_inventory(
            serial=serial, sections=["ALL"], ctx=ctx
        )

        if "error" in computer_inventory:
            if ctx:
                await ctx.error(
                    f"Failed to get inventory for health analysis",
                    extra={"serial": serial, "error": computer_inventory.get("error")},
                )
            return computer_inventory

        computer_id = computer_inventory.get("id")
        if not computer_id:
            if ctx:
                await ctx.error("Computer ID not found in inventory data", extra={"serial": serial})
            return {
                "error": "Received invalid data",
                "message": "Computer ID not found in inventory data",
                "serial": serial,
            }

        computer_history = await mcp.jamf_api.get_computer_history(int(computer_id), ctx=ctx)

        if ctx:
            await ctx.info("Loading SOFA feed for vulnerability analysis")

        logger.info(f"Loading SOFA feed for health scorecard analysis for serial {serial}")
        sofa_feed = await HealthAnalyzer.load_sofa_feed()
        if sofa_feed is None:
            if ctx:
                await ctx.warning(
                    "SOFA feed unavailable, using fallback security analysis",
                    extra={"serial": serial},
                )
            logger.warning(
                "Failed to load SOFA feed - health scorecard will use fallback security analysis"
            )

        analyzer = HealthAnalyzer(
            computer_history=computer_history,
            computer_inventory=computer_inventory,
            sofa_feed=sofa_feed,
        )

        scorecard = analyzer.generate_health_scorecard()

        if ctx:
            await ctx.info(
                f"Health scorecard generated successfully",
                extra={
                    "serial": serial,
                    "overall_score": scorecard.overall_score,
                    "grade": scorecard.grade.value,
                    "status": scorecard.status.value,
                    "critical_issues_count": len(scorecard.critical_issues),
                },
            )

        return scorecard.model_dump()
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Health analysis failed for serial {serial}: {str(e)}",
                extra={"serial": serial, "error_type": type(e).__name__},
            )

        logger.error(f"Error generating health scorecard for serial {serial}: {str(e)}")
        return {"error": "Health analysis failed", "message": str(e), "serial": serial}


@mcp.tool
async def get_basic_diagnostics(serial: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get basic diagnostic information for a computer.

    :param serial: Computer serial number
    :type serial: str
    :return: Dictionary containing diagnostic information including hardware, OS, and security status
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Starting basic diagnostics for serial {serial}")
        await ctx.info(f"Retrieving diagnostic information for {serial}", extra={"serial": serial})

    try:
        # Get computer inventory
        computer_inventory = await mcp.jamf_api.get_computer_inventory(
            serial=serial, sections=["ALL"], ctx=ctx
        )

        if "error" in computer_inventory:
            if ctx:
                await ctx.error(
                    f"Failed to get inventory for diagnostics",
                    extra={"serial": serial, "error": computer_inventory.get("error")},
                )
            return computer_inventory

        # Use HealthAnalyzer to parse diagnostics
        analyzer = HealthAnalyzer({})  # Empty history, just using parse_diags method
        diagnostics = analyzer.parse_diags(computer_inventory)

        if ctx:
            await ctx.info(
                f"Diagnostics retrieved successfully",
                extra={
                    "serial": serial,
                    "os_version": diagnostics.get("os_version"),
                    "last_check_in": diagnostics.get("last_check_in"),
                },
            )

        return diagnostics

    except Exception as e:
        if ctx:
            await ctx.error(
                f"Diagnostics failed for serial {serial}: {str(e)}",
                extra={"serial": serial, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting diagnostics for serial {serial}: {str(e)}")
        return {"error": "Diagnostics failed", "message": str(e), "serial": serial}


@mcp.tool
async def get_cves(
    serial: str, include_descriptions: bool = False, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get CVE vulnerability analysis for a computer.

    :param serial: Computer serial number
    :type serial: str
    :param include_descriptions: Include detailed CVE descriptions
    :type include_descriptions: bool
    :return: CVE analysis with vulnerability counts and risk assessment
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Starting CVE vulnerability analysis for serial {serial}")
        await ctx.info(
            f"Analyzing CVE vulnerabilities for {serial}",
            extra={"serial": serial, "include_descriptions": include_descriptions},
        )

    try:
        # Get computer inventory
        computer_inventory = await mcp.jamf_api.get_computer_inventory(
            serial=serial, sections=["ALL"], ctx=ctx
        )

        if "error" in computer_inventory:
            if ctx:
                await ctx.error(
                    f"Failed to get inventory for CVE analysis",
                    extra={"serial": serial, "error": computer_inventory.get("error")},
                )
            return computer_inventory

        computer_id = computer_inventory.get("id")
        if not computer_id:
            if ctx:
                await ctx.error("Computer ID not found in inventory data", extra={"serial": serial})
            return {
                "error": "Invalid Data",
                "message": "Computer ID not found in inventory data",
                "serial": serial,
            }

        # Get computer history for HealthAnalyzer
        computer_history = await mcp.jamf_api.get_computer_history(int(computer_id), ctx=ctx)

        # Load SOFA feed for CVE analysis
        if ctx:
            await ctx.info("Loading SOFA feed for vulnerability data")

        logger.info(f"Loading SOFA feed for CVE analysis for serial {serial}")
        sofa_feed = await HealthAnalyzer.load_sofa_feed()

        if sofa_feed is None:
            if ctx:
                await ctx.error(
                    "Unable to load SOFA feed for CVE analysis", extra={"serial": serial}
                )
            logger.warning("Failed to load SOFA feed for CVE analysis")
            return {
                "error": "SOFA Feed Error",
                "message": "Unable to retrieve security vulnerability data from SOFA feed",
                "serial": serial,
            }

        # Create HealthAnalyzer instance with SOFA feed support
        analyzer = HealthAnalyzer(
            computer_history=computer_history,
            computer_inventory=computer_inventory,
            sofa_feed=sofa_feed,
        )

        # Get CVE analysis
        cve_analysis = analyzer.get_cve_analysis(include_detailed_cves=include_descriptions)

        if cve_analysis is None:
            if ctx:
                await ctx.error("Unable to analyze CVEs for this system", extra={"serial": serial})
            return {
                "error": "Analysis Error",
                "message": "Unable to analyze CVEs for this system",
                "serial": serial,
            }

        # Add serial number to result
        cve_analysis["serial"] = serial

        total_cves = cve_analysis.get("total_cves_affecting", 0)
        actively_exploited = cve_analysis.get("actively_exploited_cves_count", 0)

        if ctx:
            await ctx.info(
                f"CVE analysis complete",
                extra={
                    "serial": serial,
                    "total_cves": total_cves,
                    "actively_exploited_cves": actively_exploited,
                    "critical_cves": cve_analysis.get("critical_cves_count", 0),
                    "high_cves": cve_analysis.get("high_cves_count", 0),
                },
            )

        logger.info(
            f"CVE analysis complete for serial {serial}: "
            f"{total_cves} total CVEs, "
            f"{actively_exploited} actively exploited"
        )

        return cve_analysis

    except Exception as e:
        if ctx:
            await ctx.error(
                f"CVE analysis failed for serial {serial}: {str(e)}",
                extra={"serial": serial, "error_type": type(e).__name__},
            )

        logger.error(f"Error analyzing CVEs for serial {serial}: {e}")
        return {"error": "CVE analysis failed", "message": str(e), "serial": serial}


@mcp.tool
async def get_compliance_status(
    computer_id: str | int, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get compliance status for a computer.

    :param computer_id: The JSS ID of the computer
    :type computer_id: str | int
    :return: Compliance status information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching compliance status for computer {computer_id}")

    try:
        computer_id_int = int(computer_id)

        if ctx:
            await ctx.info(
                f"Retrieving compliance status for computer {computer_id_int}",
                extra={"computer_id": computer_id_int},
            )

        result = await mcp.jamf_api.get_compliance_status(computer_id_int, ctx=ctx)

        if ctx:
            await ctx.info(
                f"Successfully retrieved compliance status",
                extra={
                    "computer_id": computer_id_int,
                    "compliance_state": result.get("complianceState")
                    if isinstance(result, dict)
                    else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid computer_id format: {computer_id}",
                extra={"computer_id": computer_id, "expected": "integer"},
            )

        logger.error(f"Invalid computer_id format: {computer_id}")
        return {
            "error": "Invalid computer_id",
            "message": f"computer_id must be a valid integer, got: {computer_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve compliance status for computer {computer_id}: {str(e)}",
                extra={"computer_id": computer_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting compliance status for computer {computer_id}: {e}")
        return {
            "error": "Failed to retrieve compliance status",
            "message": str(e),
            "computer_id": computer_id,
        }


@mcp.tool
async def get_jcds_files(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of files in Jamf Cloud Distribution Service.

    :return: Dictionary containing files list and count
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching JCDS files list")
        await ctx.info("Retrieving Jamf Cloud Distribution Service files")

    try:
        files = await mcp.jamf_api.get_jcds_files()

        if ctx:
            await ctx.info(f"Retrieved {len(files)} JCDS files", extra={"file_count": len(files)})

        return {"files": files, "count": len(files)}
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve JCDS files: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting JCDS files: {e}")
        return {"error": "Failed to retrieve JCDS files", "message": str(e)}


@mcp.tool
async def get_policies(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all policies.

    :return: List of policies with basic information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all policies")
        await ctx.info("Retrieving policies list")

    try:
        policies = await mcp.jamf_api.get_policies()

        if ctx:
            await ctx.info(
                f"Retrieved {len(policies)} policies", extra={"policy_count": len(policies)}
            )

        return policies
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve policies: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting policies: {e}")
        return [{"error": "Failed to retrieve policies", "message": str(e)}]


@mcp.tool
async def get_policy_details(policy_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific policy.

    :param policy_id: The policy ID
    :type policy_id: str
    :return: Detailed policy information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for policy {policy_id}")

    try:
        policy_id_int = int(policy_id)

        if ctx:
            await ctx.info(
                f"Retrieving policy details for ID {policy_id_int}",
                extra={"policy_id": policy_id_int},
            )

        result = await mcp.jamf_api.get_policy_details(policy_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved policy details",
                extra={
                    "policy_id": policy_id_int,
                    "policy_name": result.get("general", {}).get("name")
                    if isinstance(result, dict)
                    else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid policy_id format: {policy_id}",
                extra={"policy_id": policy_id, "expected": "integer"},
            )

        logger.error(f"Invalid policy_id format: {policy_id}")
        return {
            "error": "Invalid policy_id",
            "message": f"policy_id must be a valid integer, got: {policy_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve policy details for ID {policy_id}: {str(e)}",
                extra={"policy_id": policy_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting policy details for ID {policy_id}: {e}")
        return {
            "error": "Failed to retrieve policy details",
            "message": str(e),
            "policy_id": policy_id,
        }


@mcp.tool
async def get_configuration_profiles(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all configuration profiles.

    :return: List of configuration profiles
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all configuration profiles")
        await ctx.info("Retrieving configuration profiles list")

    try:
        profiles = await mcp.jamf_api.get_configuration_profiles()

        if ctx:
            await ctx.info(
                f"Retrieved {len(profiles)} configuration profiles",
                extra={"profile_count": len(profiles)},
            )

        return profiles
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve configuration profiles: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting configuration profiles: {e}")
        return [{"error": "Failed to retrieve configuration profiles", "message": str(e)}]


@mcp.tool
async def get_profile_details(profile_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific configuration profile.

    :param profile_id: The profile ID
    :type profile_id: str
    :return: Detailed profile information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for profile {profile_id}")

    try:
        profile_id_int = int(profile_id)

        if ctx:
            await ctx.info(
                f"Retrieving configuration profile details for ID {profile_id_int}",
                extra={"profile_id": profile_id_int},
            )

        result = await mcp.jamf_api.get_profile_details(profile_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved profile details",
                extra={
                    "profile_id": profile_id_int,
                    "profile_name": result.get("general", {}).get("name")
                    if isinstance(result, dict)
                    else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid profile_id format: {profile_id}",
                extra={"profile_id": profile_id, "expected": "integer"},
            )

        logger.error(f"Invalid profile_id format: {profile_id}")
        return {
            "error": "Invalid profile_id",
            "message": f"profile_id must be a valid integer, got: {profile_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve profile details for ID {profile_id}: {str(e)}",
                extra={"profile_id": profile_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting profile details for ID {profile_id}: {e}")
        return {
            "error": "Failed to retrieve profile details",
            "message": str(e),
            "profile_id": profile_id,
        }


@mcp.tool
async def get_extension_attributes(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all extension attributes.

    :return: List of extension attributes
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all extension attributes")
        await ctx.info("Retrieving extension attributes list")

    try:
        attributes = await mcp.jamf_api.get_extension_attributes()

        if ctx:
            await ctx.info(
                f"Retrieved {len(attributes)} extension attributes",
                extra={"attribute_count": len(attributes)},
            )

        return attributes
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve extension attributes: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting extension attributes: {e}")
        return [{"error": "Failed to retrieve extension attributes", "message": str(e)}]


@mcp.tool
async def get_smart_groups(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all smart computer groups.

    :return: List of smart groups
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all smart computer groups")
        await ctx.info("Retrieving smart groups list")

    try:
        groups = await mcp.jamf_api.get_smart_groups()

        if ctx:
            await ctx.info(
                f"Retrieved {len(groups)} smart groups", extra={"group_count": len(groups)}
            )

        return groups
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve smart groups: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting smart groups: {e}")
        return [{"error": "Failed to retrieve smart groups", "message": str(e)}]


@mcp.tool
async def get_group_details(group_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific smart group.

    :param group_id: The smart group ID
    :type group_id: str
    :return: Detailed group information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for smart group {group_id}")

    try:
        group_id_int = int(group_id)

        if ctx:
            await ctx.info(
                f"Retrieving smart group details for ID {group_id_int}",
                extra={"group_id": group_id_int},
            )

        result = await mcp.jamf_api.get_group_details(group_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved group details",
                extra={
                    "group_id": group_id_int,
                    "group_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid group_id format: {group_id}",
                extra={"group_id": group_id, "expected": "integer"},
            )

        logger.error(f"Invalid group_id format: {group_id}")
        return {
            "error": "Invalid group_id",
            "message": f"group_id must be a valid integer, got: {group_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve group details for ID {group_id}: {str(e)}",
                extra={"group_id": group_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting group details for ID {group_id}: {e}")
        return {
            "error": "Failed to retrieve group details",
            "message": str(e),
            "group_id": group_id,
        }


@mcp.tool
async def get_scripts(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all scripts.

    :return: List of scripts
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all scripts")
        await ctx.info("Retrieving scripts list")

    try:
        scripts = await mcp.jamf_api.get_scripts()

        if ctx:
            await ctx.info(
                f"Retrieved {len(scripts)} scripts", extra={"script_count": len(scripts)}
            )

        return scripts
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve scripts: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting scripts: {e}")
        return [{"error": "Failed to retrieve scripts", "message": str(e)}]


@mcp.tool
async def get_script_details(script_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific script.

    :param script_id: The script ID
    :type script_id: str
    :return: Detailed script information including content
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for script {script_id}")

    try:
        script_id_int = int(script_id)

        if ctx:
            await ctx.info(
                f"Retrieving script details for ID {script_id_int}",
                extra={"script_id": script_id_int},
            )

        result = await mcp.jamf_api.get_script_details(script_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved script details",
                extra={
                    "script_id": script_id_int,
                    "script_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid script_id format: {script_id}",
                extra={"script_id": script_id, "expected": "integer"},
            )

        logger.error(f"Invalid script_id format: {script_id}")
        return {
            "error": "Invalid script_id",
            "message": f"script_id must be a valid integer, got: {script_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve script details for ID {script_id}: {str(e)}",
                extra={"script_id": script_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting script details for ID {script_id}: {e}")
        return {
            "error": "Failed to retrieve script details",
            "message": str(e),
            "script_id": script_id,
        }


@mcp.tool
async def get_packages(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all packages.

    :return: List of packages
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all packages")
        await ctx.info("Retrieving packages list")

    try:
        packages = await mcp.jamf_api.get_packages()

        if ctx:
            await ctx.info(
                f"Retrieved {len(packages)} packages", extra={"package_count": len(packages)}
            )

        return packages
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve packages: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting packages: {e}")
        return [{"error": "Failed to retrieve packages", "message": str(e)}]


@mcp.tool
async def get_package_details(package_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific package.

    :param package_id: The package ID
    :type package_id: str
    :return: Detailed package information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for package {package_id}")

    try:
        package_id_int = int(package_id)

        if ctx:
            await ctx.info(
                f"Retrieving package details for ID {package_id_int}",
                extra={"package_id": package_id_int},
            )

        result = await mcp.jamf_api.get_package_details(package_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved package details",
                extra={
                    "package_id": package_id_int,
                    "package_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid package_id format: {package_id}",
                extra={"package_id": package_id, "expected": "integer"},
            )

        logger.error(f"Invalid package_id format: {package_id}")
        return {
            "error": "Invalid package_id",
            "message": f"package_id must be a valid integer, got: {package_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve package details for ID {package_id}: {str(e)}",
                extra={"package_id": package_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting package details for ID {package_id}: {e}")
        return {
            "error": "Failed to retrieve package details",
            "message": str(e),
            "package_id": package_id,
        }


@mcp.tool
async def get_users(ctx: Context | None = None) -> dict[str, Any]:
    """
    Get list of all Jamf Pro users.

    :return: List of users
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug("Fetching all Jamf Pro users")
        await ctx.info("Retrieving users list")

    try:
        users = await mcp.jamf_api.get_users()

        if ctx:
            await ctx.info(f"Retrieved {len(users)} users", extra={"user_count": len(users)})

        return users
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve users: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting users: {e}")
        return [{"error": "Failed to retrieve users", "message": str(e)}]


@mcp.tool
async def get_user_details(user_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific user.

    :param user_id: The user ID
    :type user_id: str
    :return: Detailed user information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for user {user_id}")

    try:
        user_id_int = int(user_id)

        if ctx:
            await ctx.info(
                f"Retrieving user details for ID {user_id_int}", extra={"user_id": user_id_int}
            )

        result = await mcp.jamf_api.get_user_details(user_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved user details",
                extra={
                    "user_id": user_id_int,
                    "username": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid user_id format: {user_id}",
                extra={"user_id": user_id, "expected": "integer"},
            )

        logger.error(f"Invalid user_id format: {user_id}")
        return {
            "error": "Invalid user_id",
            "message": f"user_id must be a valid integer, got: {user_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve user details for ID {user_id}: {str(e)}",
                extra={"user_id": user_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting user details for ID {user_id}: {e}")
        return {
            "error": "Failed to retrieve user details",
            "message": str(e),
            "user_id": user_id,
        }


@mcp.tool
async def get_user_group_details(group_id: int | str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific user group.

    :param group_id: The user group ID
    :type group_id: int | str
    :return: Detailed user group information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for user group {group_id}")

    try:
        group_id_int = int(group_id)

        if ctx:
            await ctx.info(
                f"Retrieving user group details for ID {group_id_int}",
                extra={"group_id": group_id_int},
            )

        result = await mcp.jamf_api.get_user_group_details(group_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved user group details",
                extra={
                    "group_id": group_id_int,
                    "group_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid group_id format: {group_id}",
                extra={"group_id": group_id, "expected": "integer"},
            )

        logger.error(f"Invalid group_id format: {group_id}")
        return {
            "error": "Invalid group_id",
            "message": f"group_id must be a valid integer, got: {group_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve user group details for ID {group_id}: {str(e)}",
                extra={"group_id": group_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting user group details for ID {group_id}: {e}")
        return {
            "error": "Failed to retrieve user group details",
            "message": str(e),
            "group_id": group_id,
        }


@mcp.tool
async def get_buildings(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all buildings.

    :return: List of buildings
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all buildings")
        await ctx.info("Retrieving buildings list")

    try:
        buildings = await mcp.jamf_api.get_buildings()

        if ctx:
            await ctx.info(
                f"Retrieved {len(buildings)} buildings", extra={"building_count": len(buildings)}
            )

        return buildings
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve buildings: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error retrieving buildings: {str(e)}")
        return [{"error": "Failed to retrieve buildings", "message": str(e)}]


@mcp.tool
async def get_building_details(
    building_id: int | str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about a specific building.

    :param building_id: The building ID
    :type building_id: int | str
    :return: Detailed building information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for building {building_id}")

    try:
        building_id_int = int(building_id)

        if ctx:
            await ctx.info(
                f"Retrieving building details for ID {building_id_int}",
                extra={"building_id": building_id_int},
            )

        result = await mcp.jamf_api.get_building_details(building_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved building details",
                extra={
                    "building_id": building_id_int,
                    "building_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid building_id format: {building_id}",
                extra={"building_id": building_id, "expected": "integer"},
            )

        logger.error(f"Invalid building_id format: {building_id}")
        return {
            "error": "Invalid building_id",
            "message": f"building_id must be a valid integer, got: {building_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve building details for ID {building_id}: {str(e)}",
                extra={"building_id": building_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting building details for ID {building_id}: {e}")
        return {
            "error": "Failed to retrieve building details",
            "message": str(e),
            "building_id": building_id,
        }


@mcp.tool
async def get_departments(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all departments.

    :return: List of departments
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all departments")
        await ctx.info("Retrieving departments list")

    try:
        departments = await mcp.jamf_api.get_departments()

        if ctx:
            await ctx.info(
                f"Retrieved {len(departments)} departments",
                extra={"department_count": len(departments)},
            )

        return departments
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve departments: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting departments: {str(e)}")
        return [{"error": "Failed to retrieve departments", "message": str(e)}]


@mcp.tool
async def get_department_details(
    department_id: int | str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about a specific department.

    :param department_id: The department ID
    :type department_id: int | str
    :return: Detailed department information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for department {department_id}")

    try:
        department_id_int = int(department_id)

        if ctx:
            await ctx.info(
                f"Retrieving department details for ID {department_id_int}",
                extra={"department_id": department_id_int},
            )

        result = await mcp.jamf_api.get_department_details(department_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved department details",
                extra={
                    "department_id": department_id_int,
                    "department_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid department_id format: {department_id}",
                extra={"department_id": department_id, "expected": "integer"},
            )

        logger.error(f"Invalid department_id format: {department_id}")
        return {
            "error": "Invalid department_id",
            "message": f"department_id must be a valid integer, got: {department_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve department details for ID {department_id}: {str(e)}",
                extra={"department_id": department_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting department details for ID {department_id}: {e}")
        return {
            "error": "Failed to retrieve department details",
            "message": str(e),
            "department_id": department_id,
        }


@mcp.tool
async def get_network_segments(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all network segments.

    :return: List of network segments
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all network segments")
        await ctx.info("Retrieving network segments list")

    try:
        segments = await mcp.jamf_api.get_network_segments()

        if ctx:
            await ctx.info(
                f"Retrieved {len(segments)} network segments",
                extra={"segment_count": len(segments)},
            )

        return segments
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve network segments: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting network segments: {e}")
        return [{"error": "Failed to retrieve network segments", "message": str(e)}]


@mcp.tool
async def get_network_segment_details(
    segment_id: str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about a specific network segment.

    :param segment_id: The network segment ID
    :type segment_id: str
    :return: Detailed network segment information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for network segment {segment_id}")

    try:
        segment_id_int = int(segment_id)

        if ctx:
            await ctx.info(
                f"Retrieving network segment details for ID {segment_id_int}",
                extra={"segment_id": segment_id_int},
            )

        result = await mcp.jamf_api.get_network_segment_details(segment_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved network segment details",
                extra={
                    "segment_id": segment_id_int,
                    "segment_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid segment_id format: {segment_id}",
                extra={"segment_id": segment_id, "expected": "integer"},
            )

        logger.error(f"Invalid segment_id format: {segment_id}")
        return {
            "error": "Invalid segment_id",
            "message": f"segment_id must be a valid integer, got: {segment_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve network segment details for ID {segment_id}: {str(e)}",
                extra={"segment_id": segment_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting network segment details for ID {segment_id}: {e}")
        return {
            "error": "Failed to retrieve network segment details",
            "message": str(e),
            "segment_id": segment_id,
        }


@mcp.tool
async def get_patch_software_titles(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all patch software titles.

    :return: List of patch software titles
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all patch software titles")
        await ctx.info("Retrieving patch software titles list")

    try:
        titles = await mcp.jamf_api.get_patch_software_titles()

        if ctx:
            await ctx.info(
                f"Retrieved {len(titles)} patch software titles", extra={"title_count": len(titles)}
            )

        return titles
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve patch software titles: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting patch software titles: {e}")
        return [{"error": "Failed to retrieve patch software titles", "message": str(e)}]


@mcp.tool
async def get_patch_software_title_details(
    title_id: str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about a specific patch software title.

    :param title_id: The patch software title ID
    :type title_id: str
    :return: Detailed patch software title information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for patch software title {title_id}")

    try:
        title_id_int = int(title_id)

        if ctx:
            await ctx.info(
                f"Retrieving patch software title details for ID {title_id_int}",
                extra={"title_id": title_id_int},
            )

        result = await mcp.jamf_api.get_patch_software_title_details(title_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved patch software title details",
                extra={
                    "title_id": title_id_int,
                    "title_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid title_id format: {title_id}",
                extra={"title_id": title_id, "expected": "integer"},
            )

        logger.error(f"Invalid title_id format: {title_id}")
        return {
            "error": "Invalid title_id",
            "message": f"title_id must be a valid integer, got: {title_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve patch software title details for ID {title_id}: {str(e)}",
                extra={"title_id": title_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting patch software title details for ID {title_id}: {e}")
        return {
            "error": "Failed to retrieve patch software title details",
            "message": str(e),
            "title_id": title_id,
        }


@mcp.tool
async def get_patch_policies(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all patch policies.

    :return: List of patch policies
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all patch policies")
        await ctx.info("Retrieving patch policies list")

    try:
        policies = await mcp.jamf_api.get_patch_policies()

        if ctx:
            await ctx.info(
                f"Retrieved {len(policies)} patch policies", extra={"policy_count": len(policies)}
            )

        return policies
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve patch policies: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting patch policies: {e}")
        return [{"error": "Failed to retrieve patch policies", "message": str(e)}]


@mcp.tool
async def get_categories(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all categories.

    :return: List of categories
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all categories")
        await ctx.info("Retrieving categories list")

    try:
        categories = await mcp.jamf_api.get_categories()

        if ctx:
            await ctx.info(
                f"Retrieved {len(categories)} categories", extra={"category_count": len(categories)}
            )

        return categories
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve categories: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting categories: {e}")
        return [{"error": "Failed to retrieve categories", "message": str(e)}]


@mcp.tool
async def get_category_details(category_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific category.

    :param category_id: The category ID
    :type category_id: str
    :return: Detailed category information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for category {category_id}")

    try:
        category_id_int = int(category_id)

        if ctx:
            await ctx.info(
                f"Retrieving category details for ID {category_id_int}",
                extra={"category_id": category_id_int},
            )

        result = await mcp.jamf_api.get_category_details(category_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved category details",
                extra={
                    "category_id": category_id_int,
                    "category_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid category_id format: {category_id}",
                extra={"category_id": category_id, "expected": "integer"},
            )

        logger.error(f"Invalid category_id format: {category_id}")
        return {
            "error": "Invalid category_id",
            "message": f"category_id must be a valid integer, got: {category_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve category details for ID {category_id}: {str(e)}",
                extra={"category_id": category_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting category details for ID {category_id}: {e}")
        return {
            "error": "Failed to retrieve category details",
            "message": str(e),
            "category_id": category_id,
        }


@mcp.tool
async def get_sites(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all sites.

    :return: List of sites
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all sites")
        await ctx.info("Retrieving sites list")

    try:
        sites = await mcp.jamf_api.get_sites()

        if ctx:
            await ctx.info(f"Retrieved {len(sites)} sites", extra={"site_count": len(sites)})

        return sites
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve sites: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting sites: {e}")
        return [{"error": "Failed to retrieve sites", "message": str(e)}]


@mcp.tool
async def get_site_details(site_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific site.

    :param site_id: The site ID
    :type site_id: str
    :return: Detailed site information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for site {site_id}")

    try:
        site_id_int = int(site_id)

        if ctx:
            await ctx.info(
                f"Retrieving site details for ID {site_id_int}", extra={"site_id": site_id_int}
            )

        result = await mcp.jamf_api.get_site_details(site_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved site details",
                extra={
                    "site_id": site_id_int,
                    "site_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid site_id format: {site_id}",
                extra={"site_id": site_id, "expected": "integer"},
            )

        logger.error(f"Invalid site_id format: {site_id}")
        return {
            "error": "Invalid site_id",
            "message": f"site_id must be a valid integer, got: {site_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve site details for ID {site_id}: {str(e)}",
                extra={"site_id": site_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting site details for ID {site_id}: {e}")
        return {
            "error": "Failed to retrieve site details",
            "message": str(e),
            "site_id": site_id,
        }


@mcp.tool
async def get_advanced_computer_searches(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all advanced computer searches.

    :return: List of advanced computer searches
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all advanced computer searches")
        await ctx.info("Retrieving advanced computer searches list")

    try:
        searches = await mcp.jamf_api.get_advanced_computer_searches()

        if ctx:
            await ctx.info(
                f"Retrieved {len(searches)} advanced computer searches",
                extra={"search_count": len(searches)},
            )

        return searches
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve advanced computer searches: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting advanced computer searches: {e}")
        return [
            {
                "error": "Failed to retrieve advanced computer searches",
                "message": str(e),
            }
        ]


@mcp.tool
async def get_advanced_computer_search_details(
    search_id: str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about a specific advanced computer search.

    :param search_id: The advanced computer search ID
    :type search_id: str
    :return: Detailed search information including results
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for advanced computer search {search_id}")

    try:
        search_id_int = int(search_id)

        if ctx:
            await ctx.info(
                f"Retrieving advanced computer search details for ID {search_id_int}",
                extra={"search_id": search_id_int},
            )

        result = await mcp.jamf_api.get_advanced_computer_search_details(search_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved advanced computer search details",
                extra={
                    "search_id": search_id_int,
                    "search_name": result.get("name") if isinstance(result, dict) else None,
                    "result_count": len(result.get("computers", []))
                    if isinstance(result, dict)
                    else 0,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid search_id format: {search_id}",
                extra={"search_id": search_id, "expected": "integer"},
            )

        logger.error(f"Invalid search_id format: {search_id}")
        return {
            "error": "Invalid search_id",
            "message": f"search_id must be a valid integer, got: {search_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve advanced computer search details for ID {search_id}: {str(e)}",
                extra={"search_id": search_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting advanced computer search details for ID {search_id}: {e}")
        return {
            "error": "Failed to retrieve advanced computer search details",
            "message": str(e),
            "search_id": search_id,
        }


@mcp.tool
async def get_restricted_software(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all restricted software.

    :return: List of restricted software
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all restricted software")
        await ctx.info("Retrieving restricted software list")

    try:
        software = await mcp.jamf_api.get_restricted_software()

        if ctx:
            await ctx.info(
                f"Retrieved {len(software)} restricted software items",
                extra={"software_count": len(software)},
            )

        return software
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve restricted software: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting restricted software: {e}")
        return [{"error": "Failed to retrieve restricted software", "message": str(e)}]


@mcp.tool
async def get_restricted_software_details(
    software_id: str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about specific restricted software.

    :param software_id: The restricted software ID
    :type software_id: str
    :return: Detailed restricted software information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for restricted software {software_id}")

    try:
        software_id_int = int(software_id)

        if ctx:
            await ctx.info(
                f"Retrieving restricted software details for ID {software_id_int}",
                extra={"software_id": software_id_int},
            )

        result = await mcp.jamf_api.get_restricted_software_details(software_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved restricted software details",
                extra={
                    "software_id": software_id_int,
                    "software_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid software_id format: {software_id}",
                extra={"software_id": software_id, "expected": "integer"},
            )

        logger.error(f"Invalid software_id format: {software_id}")
        return {
            "error": "Invalid software_id",
            "message": f"software_id must be a valid integer, got: {software_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve restricted software details for ID {software_id}: {str(e)}",
                extra={"software_id": software_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting restricted software details for ID {software_id}: {e}")
        return {
            "error": "Failed to retrieve restricted software details",
            "message": str(e),
            "software_id": software_id,
        }


@mcp.tool
async def get_licensed_software(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all licensed software.

    :return: List of licensed software
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all licensed software")
        await ctx.info("Retrieving licensed software list")

    try:
        software = await mcp.jamf_api.get_licensed_software()

        if ctx:
            await ctx.info(
                f"Retrieved {len(software)} licensed software items",
                extra={"software_count": len(software)},
            )

        return software
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve licensed software: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting licensed software: {e}")
        return [{"error": "Failed to retrieve licensed software", "message": str(e)}]


@mcp.tool
async def get_licensed_software_details(
    software_id: str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about specific licensed software.

    :param software_id: The licensed software ID
    :type software_id: str
    :return: Detailed licensed software information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for licensed software {software_id}")

    try:
        software_id_int = int(software_id)

        if ctx:
            await ctx.info(
                f"Retrieving licensed software details for ID {software_id_int}",
                extra={"software_id": software_id_int},
            )

        result = await mcp.jamf_api.get_licensed_software_details(software_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved licensed software details",
                extra={
                    "software_id": software_id_int,
                    "software_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid software_id format: {software_id}",
                extra={"software_id": software_id, "expected": "integer"},
            )

        logger.error(f"Invalid software_id format: {software_id}")
        return {
            "error": "Invalid software_id",
            "message": f"software_id must be a valid integer, got: {software_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve licensed software details for ID {software_id}: {str(e)}",
                extra={"software_id": software_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting licensed software details for ID {software_id}: {e}")
        return {
            "error": "Failed to retrieve licensed software details",
            "message": str(e),
            "software_id": software_id,
        }


@mcp.tool
async def get_ldap_servers(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all LDAP servers.

    :return: List of LDAP servers
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all LDAP servers")
        await ctx.info("Retrieving LDAP servers list")

    try:
        servers = await mcp.jamf_api.get_ldap_servers()

        if ctx:
            await ctx.info(
                f"Retrieved {len(servers)} LDAP servers", extra={"server_count": len(servers)}
            )

        return servers
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve LDAP servers: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting LDAP servers: {e}")
        return [{"error": "Failed to retrieve LDAP servers", "message": str(e)}]


@mcp.tool
async def get_ldap_server_details(server_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific LDAP server.

    :param server_id: The LDAP server ID
    :type server_id: str
    :return: Detailed LDAP server information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for LDAP server {server_id}")

    try:
        server_id_int = int(server_id)

        if ctx:
            await ctx.info(
                f"Retrieving LDAP server details for ID {server_id_int}",
                extra={"server_id": server_id_int},
            )

        result = await mcp.jamf_api.get_ldap_server_details(server_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved LDAP server details",
                extra={
                    "server_id": server_id_int,
                    "server_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid server_id format: {server_id}",
                extra={"server_id": server_id, "expected": "integer"},
            )

        logger.error(f"Invalid server_id format: {server_id}")
        return {
            "error": "Invalid server_id",
            "message": f"server_id must be a valid integer, got: {server_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve LDAP server details for ID {server_id}: {str(e)}",
                extra={"server_id": server_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting LDAP server details for ID {server_id}: {e}")
        return {
            "error": "Failed to retrieve LDAP server details",
            "message": str(e),
            "server_id": server_id,
        }


@mcp.tool
async def get_directory_bindings(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all directory bindings.

    :return: List of directory bindings
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all directory bindings")
        await ctx.info("Retrieving directory bindings list")

    try:
        bindings = await mcp.jamf_api.get_directory_bindings()

        if ctx:
            await ctx.info(
                f"Retrieved {len(bindings)} directory bindings",
                extra={"binding_count": len(bindings)},
            )

        return bindings
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve directory bindings: {str(e)}",
                extra={"error_type": type(e).__name__},
            )

        logger.error(f"Error getting directory bindings: {e}")
        return [{"error": "Failed to retrieve directory bindings", "message": str(e)}]


@mcp.tool
async def get_directory_binding_details(
    binding_id: str, ctx: Context | None = None
) -> dict[str, Any]:
    """
    Get detailed information about a specific directory binding.

    :param binding_id: The directory binding ID
    :type binding_id: str
    :return: Detailed directory binding information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for directory binding {binding_id}")

    try:
        binding_id_int = int(binding_id)

        if ctx:
            await ctx.info(
                f"Retrieving directory binding details for ID {binding_id_int}",
                extra={"binding_id": binding_id_int},
            )

        result = await mcp.jamf_api.get_directory_binding_details(binding_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved directory binding details",
                extra={
                    "binding_id": binding_id_int,
                    "binding_name": result.get("name") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid binding_id format: {binding_id}",
                extra={"binding_id": binding_id, "expected": "integer"},
            )

        logger.error(f"Invalid binding_id format: {binding_id}")
        return {
            "error": "Invalid binding_id",
            "message": f"binding_id must be a valid integer, got: {binding_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve directory binding details for ID {binding_id}: {str(e)}",
                extra={"binding_id": binding_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting directory binding details for ID {binding_id}: {e}")
        return {
            "error": "Failed to retrieve directory binding details",
            "message": str(e),
            "binding_id": binding_id,
        }


@mcp.tool
async def get_webhooks(ctx: Context | None = None) -> list[dict[str, Any]]:
    """
    Get list of all webhooks.

    :return: List of webhooks
    :rtype: list[dict[str, Any]]
    """
    if ctx:
        await ctx.debug("Fetching all webhooks")
        await ctx.info("Retrieving webhooks list")

    try:
        webhooks = await mcp.jamf_api.get_webhooks()

        if ctx:
            await ctx.info(
                f"Retrieved {len(webhooks)} webhooks", extra={"webhook_count": len(webhooks)}
            )

        return webhooks
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve webhooks: {str(e)}", extra={"error_type": type(e).__name__}
            )

        logger.error(f"Error getting webhooks: {e}")
        return [{"error": "Failed to retrieve webhooks", "message": str(e)}]


@mcp.tool
async def get_webhook_details(webhook_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get detailed information about a specific webhook.

    :param webhook_id: The webhook ID
    :type webhook_id: str
    :return: Detailed webhook information
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching details for webhook {webhook_id}")

    try:
        webhook_id_int = int(webhook_id)

        if ctx:
            await ctx.info(
                f"Retrieving webhook details for ID {webhook_id_int}",
                extra={"webhook_id": webhook_id_int},
            )

        result = await mcp.jamf_api.get_webhook_details(webhook_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved webhook details",
                extra={
                    "webhook_id": webhook_id_int,
                    "webhook_name": result.get("name") if isinstance(result, dict) else None,
                    "webhook_url": result.get("url") if isinstance(result, dict) else None,
                },
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid webhook_id format: {webhook_id}",
                extra={"webhook_id": webhook_id, "expected": "integer"},
            )

        logger.error(f"Invalid webhook_id format: {webhook_id}")
        return {
            "error": "Invalid webhook_id",
            "message": f"webhook_id must be a valid integer, got: {webhook_id}",
        }
    except Exception as e:
        if ctx:
            await ctx.error(
                f"Failed to retrieve webhook details for ID {webhook_id}: {str(e)}",
                extra={"webhook_id": webhook_id, "error_type": type(e).__name__},
            )

        logger.error(f"Error getting webhook details for ID {webhook_id}: {e}")
        return {
            "error": "Failed to retrieve webhook details",
            "message": str(e),
            "webhook_id": webhook_id,
        }


@mcp.tool
async def get_device_lock_pin(computer_id: str, ctx: Context | None = None) -> dict[str, Any]:
    """
    Get device lock PIN for a computer.

    :param computer_id: The JSS ID of the computer
    :type computer_id: str
    :return: Device lock PIN information or error if device not locked
    :rtype: dict[str, Any]
    """
    if ctx:
        await ctx.debug(f"Fetching device lock PIN for computer {computer_id}")

    try:
        computer_id_int = int(computer_id)

        if ctx:
            await ctx.info(
                f"Retrieving device lock PIN for computer {computer_id_int}",
                extra={"computer_id": computer_id_int},
            )

        result = await mcp.jamf_api.get_device_lock_pin(computer_id_int)

        if ctx:
            await ctx.info(
                f"Successfully retrieved device lock PIN", extra={"computer_id": computer_id_int}
            )

        return result
    except ValueError:
        if ctx:
            await ctx.error(
                f"Invalid computer_id format: {computer_id}",
                extra={"computer_id": computer_id, "expected": "integer"},
            )

        logger.error(f"Invalid computer_id format: {computer_id}")
        return {
            "error": "Invalid computer_id",
            "message": f"computer_id must be a valid integer, got: {computer_id}",
        }
    except Exception as e:
        error_message = str(e)

        # Check if it's a 404 (device not locked) or 403 (no permission)
        if "404" in error_message:
            if ctx:
                await ctx.warning(
                    f"Device {computer_id} is not locked or has no recovery PIN",
                    extra={"computer_id": computer_id, "status": "not_locked"},
                )

            return {
                "error": "Device not locked",
                "message": "This device is not currently locked or does not have a recovery PIN available",
                "computer_id": computer_id,
            }
        elif "403" in error_message:
            if ctx:
                await ctx.error(
                    f"Permission denied for viewing device lock PIN",
                    extra={"computer_id": computer_id, "error_code": "403"},
                )

            return {
                "error": "Permission denied",
                "message": "You do not have permission to view device lock PINs",
                "computer_id": computer_id,
            }
        else:
            if ctx:
                await ctx.error(
                    f"Failed to retrieve device lock PIN for computer {computer_id}: {error_message}",
                    extra={"computer_id": computer_id, "error_type": type(e).__name__},
                )

            logger.error(f"Error getting device lock PIN for computer {computer_id}: {e}")
            return {
                "error": "Failed to retrieve device lock PIN",
                "message": error_message,
                "computer_id": computer_id,
            }


@mcp.tool
async def ping(ctx: Context | None = None) -> dict[str, str]:
    """
    Simple ping test to verify the MCP server is responding.

    :return: Dictionary containing a simple ping response
    """
    if ctx:
        await ctx.debug("Ping request received")
        await ctx.info("MCP server is responding")

    return {"message": "pong", "status": "ok"}


def main():
    """Entry point for MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
