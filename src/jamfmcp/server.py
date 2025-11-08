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
from typing import Any

from fastmcp import FastMCP

from .api import JamfApi
from .auth import JamfAuth
from .health_analyzer import HealthAnalyzer
from .jamfsdk.clients.pro_api.pagination import FilterField

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize auth and api client
auth = JamfAuth()
jamf_api = JamfApi(auth)

# Create server and configurations
mcp = FastMCP(name="Jamf Pro MCP")


@mcp.tool
async def get_computer_inventory(serial: str, sections: list[str] | None = None) -> dict[str, Any]:
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
    try:
        return await jamf_api.get_computer_inventory(serial=serial, sections=sections)
    except Exception as e:
        logger.error(f"Error getting inventory for serial {serial}: {str(e)}")
        return {
            "error": "Failed to retrieve inventory",
            "message": str(e),
            "serial": serial,
        }


@mcp.tool
async def get_computer_history(computer_id: int | str) -> dict[str, Any]:
    """
    Get computer history including policy logs, management commands, and user activity.

    Note: computer_id should be the JSS ID of the computer. The computer_id can be retrieved from
    ``get_computer_inventory`` results.

    :param computer_id: The JSS ID of the computer
    :type computer_id: int | str
    :return: Dictionary containing computer history data
    :rtype: dict[str, Any]
    """
    try:
        computer_id_int = int(computer_id)
        return await jamf_api.get_computer_history(computer_id_int)
    except ValueError:
        logger.error(f"Invalid computer_id format: {computer_id}")
        return {
            "error": "Invalid computer_id",
            "message": f"computer_id must be a valid integer, got: {computer_id} (type: {type(computer_id)})",
        }
    except Exception as e:
        logger.error(f"Error getting history for computer {computer_id}: {str(e)}")
        return {
            "error": "Failed to retrieve history",
            "message": str(e),
            "computer_id": computer_id,
        }


@mcp.tool
async def search_computers(
    identifier: str | None = None, page_size: str | None = "100", sections: list[str] | None = None
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

    filter_expression = None
    if identifier:
        filter_expression = FilterField("general.name").eq(identifier) | FilterField(
            "hardware.SerialNumber"
        ).eq(identifier)

    return await jamf_api.search_computers(
        filter_expression=filter_expression, page_size=page_size_int, sections=sections
    )


@mcp.tool
async def get_health_scorecard(serial: str, email_address: str | None = None) -> dict[str, Any]:
    """
    Generate comprehensive health scorecard for a computer.

    :param serial: Computer serial number
    :type serial: str
    :param email_address: Optional email address to lookup serial number
    :type email_address: str | None
    :return: Health scorecard with overall score, grades, and recommendations
    :rtype: dict[str, Any]
    """
    try:
        try:
            if email_address:
                serial = await jamf_api.get_serial_for_user(email_address)
        except Exception as e:
            return {
                "error": "No serial found",
                "message": f"Serial was not found for user {email_address}: {e}",
            }

        computer_inventory = await jamf_api.get_computer_inventory(serial=serial, sections=["ALL"])

        if "error" in computer_inventory:
            return computer_inventory

        computer_id = computer_inventory.get("id")
        if not computer_id:
            return {
                "error": "Received invalid data",
                "message": "Computer ID not found in inventory data",
                "serial": serial,
            }

        computer_history = await jamf_api.get_computer_history(int(computer_id))
        logger.info(f"Loading SOFA feed for health scorecard analysis for serial {serial}")
        sofa_feed = HealthAnalyzer.load_sofa_feed()
        if sofa_feed is None:
            logger.warning(
                "Failed to load SOFA feed - health scorecard will use fallback security analysis"
            )

        analyzer = HealthAnalyzer(
            computer_history=computer_history,
            computer_inventory=computer_inventory,
            sofa_feed=sofa_feed,
        )

        scorecard = analyzer.generate_health_scorecard()
        return scorecard.model_dump()
    except Exception as e:
        logger.error(f"Error generating health scorecard for serial {serial}: {str(e)}")
        return {"error": "Health analysis failed", "message": str(e), "serial": serial}


@mcp.tool
async def get_basic_diagnostics(serial: str) -> dict[str, Any]:
    """
    Get basic diagnostic information for a computer.

    :param serial: Computer serial number
    :type serial: str
    :return: Dictionary containing diagnostic information including hardware, OS, and security status
    :rtype: dict[str, Any]
    """
    try:
        # Get computer inventory
        computer_inventory = await jamf_api.get_computer_inventory(serial=serial, sections=["ALL"])

        if "error" in computer_inventory:
            return computer_inventory

        # Use HealthAnalyzer to parse diagnostics
        analyzer = HealthAnalyzer({})  # Empty history, just using parse_diags method
        return analyzer.parse_diags(computer_inventory)

    except Exception as e:
        logger.error(f"Error getting diagnostics for serial {serial}: {str(e)}")
        return {"error": "Diagnostics failed", "message": str(e), "serial": serial}


@mcp.tool
async def get_cves(serial: str, include_descriptions: bool = False) -> dict[str, Any]:
    """
    Get CVE vulnerability analysis for a computer.

    :param serial: Computer serial number
    :type serial: str
    :param include_descriptions: Include detailed CVE descriptions
    :type include_descriptions: bool
    :return: CVE analysis with vulnerability counts and risk assessment
    :rtype: dict[str, Any]
    """
    try:
        # Get computer inventory
        computer_inventory = await jamf_api.get_computer_inventory(serial=serial, sections=["ALL"])

        if "error" in computer_inventory:
            return computer_inventory

        computer_id = computer_inventory.get("id")
        if not computer_id:
            return {
                "error": "Invalid Data",
                "message": "Computer ID not found in inventory data",
                "serial": serial,
            }

        # Get computer history for HealthAnalyzer
        computer_history = await jamf_api.get_computer_history(int(computer_id))

        # Load SOFA feed for CVE analysis
        logger.info(f"Loading SOFA feed for CVE analysis for serial {serial}")
        sofa_feed = await HealthAnalyzer.load_sofa_feed()

        if sofa_feed is None:
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
            return {
                "error": "Analysis Error",
                "message": "Unable to analyze CVEs for this system",
                "serial": serial,
            }

        # Add serial number to result
        cve_analysis["serial"] = serial

        logger.info(
            f"CVE analysis complete for serial {serial}: "
            f"{cve_analysis.get('total_cves_affecting', 0)} total CVEs, "
            f"{cve_analysis.get('actively_exploited_cves_count', 0)} actively exploited"
        )

        return cve_analysis

    except Exception as e:
        logger.error(f"Error analyzing CVEs for serial {serial}: {e}")
        return {"error": "CVE analysis failed", "message": str(e), "serial": serial}


@mcp.tool
async def get_compliance_status(computer_id: str | int) -> dict[str, Any]:
    """
    Get compliance status for a computer.

    :param computer_id: The JSS ID of the computer
    :type computer_id: str | int
    :return: Compliance status information
    :rtype: dict[str, Any]
    """
    try:
        computer_id_int = int(computer_id)
        return await jamf_api.get_compliance_status(computer_id_int)
    except ValueError:
        logger.error(f"Invalid computer_id format: {computer_id}")
        return {
            "error": "Invalid computer_id",
            "message": f"computer_id must be a valid integer, got: {computer_id}",
        }
    except Exception as e:
        logger.error(f"Error getting compliance status for computer {computer_id}: {e}")
        return {
            "error": "Failed to retrieve compliance status",
            "message": str(e),
            "computer_id": computer_id,
        }


@mcp.tool
async def get_jcds_files() -> dict[str, Any]:
    """
    Get list of files in Jamf Cloud Distribution Service.

    :return: Dictionary containing files list and count
    :rtype: dict[str, Any]
    """
    try:
        files = await jamf_api.get_jcds_files()
        return {"files": files, "count": len(files)}
    except Exception as e:
        logger.error(f"Error getting JCDS files: {e}")
        return {"error": "Failed to retrieve JCDS files", "message": str(e)}


@mcp.tool
async def get_policies() -> dict[str, Any]:
    """
    Get list of all policies.

    :return: List of policies with basic information
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_policies()
    except Exception as e:
        logger.error(f"Error getting policies: {e}")
        return [{"error": "Failed to retrieve policies", "message": str(e)}]


@mcp.tool
async def get_policy_details(policy_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific policy.

    :param policy_id: The policy ID
    :type policy_id: str
    :return: Detailed policy information
    :rtype: dict[str, Any]
    """
    try:
        policy_id_int = int(policy_id)
        return await jamf_api.get_policy_details(policy_id_int)
    except ValueError:
        logger.error(f"Invalid policy_id format: {policy_id}")
        return {
            "error": "Invalid policy_id",
            "message": f"policy_id must be a valid integer, got: {policy_id}",
        }
    except Exception as e:
        logger.error(f"Error getting policy details for ID {policy_id}: {e}")
        return {
            "error": "Failed to retrieve policy details",
            "message": str(e),
            "policy_id": policy_id,
        }


@mcp.tool
async def get_configuration_profiles() -> dict[str, Any]:
    """
    Get list of all configuration profiles.

    :return: List of configuration profiles
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_configuration_profiles()
    except Exception as e:
        logger.error(f"Error getting configuration profiles: {e}")
        return [{"error": "Failed to retrieve configuration profiles", "message": str(e)}]


@mcp.tool
async def get_profile_details(profile_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific configuration profile.

    :param profile_id: The profile ID
    :type profile_id: str
    :return: Detailed profile information
    :rtype: dict[str, Any]
    """
    try:
        profile_id_int = int(profile_id)
        return await jamf_api.get_profile_details(profile_id_int)
    except ValueError:
        logger.error(f"Invalid profile_id format: {profile_id}")
        return {
            "error": "Invalid profile_id",
            "message": f"profile_id must be a valid integer, got: {profile_id}",
        }
    except Exception as e:
        logger.error(f"Error getting profile details for ID {profile_id}: {e}")
        return {
            "error": "Failed to retrieve profile details",
            "message": str(e),
            "profile_id": profile_id,
        }


@mcp.tool
async def get_extension_attributes() -> dict[str, Any]:
    """
    Get list of all extension attributes.

    :return: List of extension attributes
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_extension_attributes()
    except Exception as e:
        logger.error(f"Error getting extension attributes: {e}")
        return [{"error": "Failed to retrieve extension attributes", "message": str(e)}]


@mcp.tool
async def get_smart_groups() -> dict[str, Any]:
    """
    Get list of all smart computer groups.

    :return: List of smart groups
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_smart_groups()
    except Exception as e:
        logger.error(f"Error getting smart groups: {e}")
        return [{"error": "Failed to retrieve smart groups", "message": str(e)}]


@mcp.tool
async def get_group_details(group_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific smart group.

    :param group_id: The smart group ID
    :type group_id: str
    :return: Detailed group information
    :rtype: dict[str, Any]
    """
    try:
        group_id_int = int(group_id)
        return await jamf_api.get_group_details(group_id_int)
    except ValueError:
        logger.error(f"Invalid group_id format: {group_id}")
        return {
            "error": "Invalid group_id",
            "message": f"group_id must be a valid integer, got: {group_id}",
        }
    except Exception as e:
        logger.error(f"Error getting group details for ID {group_id}: {e}")
        return {
            "error": "Failed to retrieve group details",
            "message": str(e),
            "group_id": group_id,
        }


@mcp.tool
async def get_scripts() -> dict[str, Any]:
    """
    Get list of all scripts.

    :return: List of scripts
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_scripts()
    except Exception as e:
        logger.error(f"Error getting scripts: {e}")
        return [{"error": "Failed to retrieve scripts", "message": str(e)}]


@mcp.tool
async def get_script_details(script_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific script.

    :param script_id: The script ID
    :type script_id: str
    :return: Detailed script information including content
    :rtype: dict[str, Any]
    """
    try:
        script_id_int = int(script_id)
        return await jamf_api.get_script_details(script_id_int)
    except ValueError:
        logger.error(f"Invalid script_id format: {script_id}")
        return {
            "error": "Invalid script_id",
            "message": f"script_id must be a valid integer, got: {script_id}",
        }
    except Exception as e:
        logger.error(f"Error getting script details for ID {script_id}: {e}")
        return {
            "error": "Failed to retrieve script details",
            "message": str(e),
            "script_id": script_id,
        }


@mcp.tool
async def get_packages() -> dict[str, Any]:
    """
    Get list of all packages.

    :return: List of packages
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_packages()
    except Exception as e:
        logger.error(f"Error getting packages: {e}")
        return [{"error": "Failed to retrieve packages", "message": str(e)}]


@mcp.tool
async def get_package_details(package_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific package.

    :param package_id: The package ID
    :type package_id: str
    :return: Detailed package information
    :rtype: dict[str, Any]
    """
    try:
        package_id_int = int(package_id)
        return await jamf_api.get_package_details(package_id_int)
    except ValueError:
        logger.error(f"Invalid package_id format: {package_id}")
        return {
            "error": "Invalid package_id",
            "message": f"package_id must be a valid integer, got: {package_id}",
        }
    except Exception as e:
        logger.error(f"Error getting package details for ID {package_id}: {e}")
        return {
            "error": "Failed to retrieve package details",
            "message": str(e),
            "package_id": package_id,
        }


@mcp.tool
async def get_users() -> dict[str, Any]:
    """
    Get list of all Jamf Pro users.

    :return: List of users
    :rtype: dict[str, Any]
    """
    try:
        return await jamf_api.get_users()
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return [{"error": "Failed to retrieve users", "message": str(e)}]


@mcp.tool
async def get_user_details(user_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific user.

    :param user_id: The user ID
    :type user_id: str
    :return: Detailed user information
    :rtype: dict[str, Any]
    """
    try:
        user_id_int = int(user_id)
        return await jamf_api.get_user_details(user_id_int)
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return {
            "error": "Invalid user_id",
            "message": f"user_id must be a valid integer, got: {user_id}",
        }
    except Exception as e:
        logger.error(f"Error getting user details for ID {user_id}: {e}")
        return {
            "error": "Failed to retrieve user details",
            "message": str(e),
            "user_id": user_id,
        }


@mcp.tool
async def get_user_group_details(group_id: int | str) -> dict[str, Any]:
    """
    Get detailed information about a specific user group.

    :param group_id: The user group ID
    :type group_id: int | str
    :return: Detailed user group information
    :rtype: dict[str, Any]
    """
    try:
        group_id_int = int(group_id)
        return await jamf_api.get_user_group_details(group_id_int)
    except ValueError:
        logger.error(f"Invalid group_id format: {group_id}")
        return {
            "error": "Invalid group_id",
            "message": f"group_id must be a valid integer, got: {group_id}",
        }
    except Exception as e:
        logger.error(f"Error getting user group details for ID {group_id}: {e}")
        return {
            "error": "Failed to retrieve user group details",
            "message": str(e),
            "group_id": group_id,
        }


@mcp.tool
async def get_buildings() -> list[dict[str, Any]]:
    """
    Get list of all buildings.

    :return: List of buildings
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_buildings()
    except Exception as e:
        logger.error(f"Error retrieving buildings: {str(e)}")
        return [{"error": "Failed to retrieve buildings", "message": str(e)}]


@mcp.tool
async def get_building_details(building_id: int | str) -> dict[str, Any]:
    """
    Get detailed information about a specific building.

    :param building_id: The building ID
    :type building_id: int | str
    :return: Detailed building information
    :rtype: dict[str, Any]
    """
    try:
        building_id_int = int(building_id)
        return await jamf_api.get_building_details(building_id_int)
    except ValueError:
        logger.error(f"Invalid building_id format: {building_id}")
        return {
            "error": "Invalid building_id",
            "message": f"building_id must be a valid integer, got: {building_id}",
        }
    except Exception as e:
        logger.error(f"Error getting building details for ID {building_id}: {e}")
        return {
            "error": "Failed to retrieve building details",
            "message": str(e),
            "building_id": building_id,
        }


@mcp.tool
async def get_departments() -> list[dict[str, Any]]:
    """
    Get list of all departments.

    :return: List of departments
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_departments()
    except Exception as e:
        logger.error(f"Error getting departments: {str(e)}")
        return [{"error": "Failed to retrieve departments", "message": str(e)}]


@mcp.tool
async def get_department_details(department_id: int | str) -> dict[str, Any]:
    """
    Get detailed information about a specific department.

    :param department_id: The department ID
    :type department_id: int | str
    :return: Detailed department information
    :rtype: dict[str, Any]
    """
    try:
        department_id_int = int(department_id)
        return await jamf_api.get_department_details(department_id_int)
    except ValueError:
        logger.error(f"Invalid department_id format: {department_id}")
        return {
            "error": "Invalid department_id",
            "message": f"department_id must be a valid integer, got: {department_id}",
        }
    except Exception as e:
        logger.error(f"Error getting department details for ID {department_id}: {e}")
        return {
            "error": "Failed to retrieve department details",
            "message": str(e),
            "department_id": department_id,
        }


@mcp.tool
async def get_network_segments() -> list[dict[str, Any]]:
    """
    Get list of all network segments.

    :return: List of network segments
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_network_segments()
    except Exception as e:
        logger.error(f"Error getting network segments: {e}")
        return [{"error": "Failed to retrieve network segments", "message": str(e)}]


@mcp.tool
async def get_network_segment_details(
    segment_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific network segment.

    :param segment_id: The network segment ID
    :type segment_id: str
    :return: Detailed network segment information
    :rtype: dict[str, Any]
    """
    try:
        segment_id_int = int(segment_id)
        return await jamf_api.get_network_segment_details(segment_id_int)
    except ValueError:
        logger.error(f"Invalid segment_id format: {segment_id}")
        return {
            "error": "Invalid segment_id",
            "message": f"segment_id must be a valid integer, got: {segment_id}",
        }
    except Exception as e:
        logger.error(f"Error getting network segment details for ID {segment_id}: {e}")
        return {
            "error": "Failed to retrieve network segment details",
            "message": str(e),
            "segment_id": segment_id,
        }


@mcp.tool
async def get_patch_software_titles() -> list[dict[str, Any]]:
    """
    Get list of all patch software titles.

    :return: List of patch software titles
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_patch_software_titles()
    except Exception as e:
        logger.error(f"Error getting patch software titles: {e}")
        return [{"error": "Failed to retrieve patch software titles", "message": str(e)}]


@mcp.tool
async def get_patch_software_title_details(
    title_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific patch software title.

    :param title_id: The patch software title ID
    :type title_id: str
    :return: Detailed patch software title information
    :rtype: dict[str, Any]
    """
    try:
        title_id_int = int(title_id)
        return await jamf_api.get_patch_software_title_details(title_id_int)
    except ValueError:
        logger.error(f"Invalid title_id format: {title_id}")
        return {
            "error": "Invalid title_id",
            "message": f"title_id must be a valid integer, got: {title_id}",
        }
    except Exception as e:
        logger.error(f"Error getting patch software title details for ID {title_id}: {e}")
        return {
            "error": "Failed to retrieve patch software title details",
            "message": str(e),
            "title_id": title_id,
        }


@mcp.tool
async def get_patch_policies() -> list[dict[str, Any]]:
    """
    Get list of all patch policies.

    :return: List of patch policies
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_patch_policies()
    except Exception as e:
        logger.error(f"Error getting patch policies: {e}")
        return [{"error": "Failed to retrieve patch policies", "message": str(e)}]


@mcp.tool
async def get_categories() -> list[dict[str, Any]]:
    """
    Get list of all categories.

    :return: List of categories
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_categories()
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return [{"error": "Failed to retrieve categories", "message": str(e)}]


@mcp.tool
async def get_category_details(
    category_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific category.

    :param category_id: The category ID
    :type category_id: str
    :return: Detailed category information
    :rtype: dict[str, Any]
    """
    try:
        category_id_int = int(category_id)
        return await jamf_api.get_category_details(category_id_int)
    except ValueError:
        logger.error(f"Invalid category_id format: {category_id}")
        return {
            "error": "Invalid category_id",
            "message": f"category_id must be a valid integer, got: {category_id}",
        }
    except Exception as e:
        logger.error(f"Error getting category details for ID {category_id}: {e}")
        return {
            "error": "Failed to retrieve category details",
            "message": str(e),
            "category_id": category_id,
        }


@mcp.tool
async def get_sites() -> list[dict[str, Any]]:
    """
    Get list of all sites.

    :return: List of sites
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_sites()
    except Exception as e:
        logger.error(f"Error getting sites: {e}")
        return [{"error": "Failed to retrieve sites", "message": str(e)}]


@mcp.tool
async def get_site_details(
    site_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific site.

    :param site_id: The site ID
    :type site_id: str
    :return: Detailed site information
    :rtype: dict[str, Any]
    """
    try:
        site_id_int = int(site_id)
        return await jamf_api.get_site_details(site_id_int)
    except ValueError:
        logger.error(f"Invalid site_id format: {site_id}")
        return {
            "error": "Invalid site_id",
            "message": f"site_id must be a valid integer, got: {site_id}",
        }
    except Exception as e:
        logger.error(f"Error getting site details for ID {site_id}: {e}")
        return {
            "error": "Failed to retrieve site details",
            "message": str(e),
            "site_id": site_id,
        }


@mcp.tool
async def get_advanced_computer_searches() -> list[dict[str, Any]]:
    """
    Get list of all advanced computer searches.

    :return: List of advanced computer searches
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_advanced_computer_searches()
    except Exception as e:
        logger.error(f"Error getting advanced computer searches: {e}")
        return [
            {
                "error": "Failed to retrieve advanced computer searches",
                "message": str(e),
            }
        ]


@mcp.tool
async def get_advanced_computer_search_details(
    search_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific advanced computer search.

    :param search_id: The advanced computer search ID
    :type search_id: str
    :return: Detailed search information including results
    :rtype: dict[str, Any]
    """
    try:
        search_id_int = int(search_id)
        return await jamf_api.get_advanced_computer_search_details(search_id_int)
    except ValueError:
        logger.error(f"Invalid search_id format: {search_id}")
        return {
            "error": "Invalid search_id",
            "message": f"search_id must be a valid integer, got: {search_id}",
        }
    except Exception as e:
        logger.error(f"Error getting advanced computer search details for ID {search_id}: {e}")
        return {
            "error": "Failed to retrieve advanced computer search details",
            "message": str(e),
            "search_id": search_id,
        }


@mcp.tool
async def get_restricted_software() -> list[dict[str, Any]]:
    """
    Get list of all restricted software.

    :return: List of restricted software
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_restricted_software()
    except Exception as e:
        logger.error(f"Error getting restricted software: {e}")
        return [{"error": "Failed to retrieve restricted software", "message": str(e)}]


@mcp.tool
async def get_restricted_software_details(
    software_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about specific restricted software.

    :param software_id: The restricted software ID
    :type software_id: str
    :return: Detailed restricted software information
    :rtype: dict[str, Any]
    """
    try:
        software_id_int = int(software_id)
        return await jamf_api.get_restricted_software_details(software_id_int)
    except ValueError:
        logger.error(f"Invalid software_id format: {software_id}")
        return {
            "error": "Invalid software_id",
            "message": f"software_id must be a valid integer, got: {software_id}",
        }
    except Exception as e:
        logger.error(f"Error getting restricted software details for ID {software_id}: {e}")
        return {
            "error": "Failed to retrieve restricted software details",
            "message": str(e),
            "software_id": software_id,
        }


@mcp.tool
async def get_licensed_software() -> list[dict[str, Any]]:
    """
    Get list of all licensed software.

    :return: List of licensed software
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_licensed_software()
    except Exception as e:
        logger.error(f"Error getting licensed software: {e}")
        return [{"error": "Failed to retrieve licensed software", "message": str(e)}]


@mcp.tool
async def get_licensed_software_details(
    software_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about specific licensed software.

    :param software_id: The licensed software ID
    :type software_id: str
    :return: Detailed licensed software information
    :rtype: dict[str, Any]
    """
    try:
        software_id_int = int(software_id)
        return await jamf_api.get_licensed_software_details(software_id_int)
    except ValueError:
        logger.error(f"Invalid software_id format: {software_id}")
        return {
            "error": "Invalid software_id",
            "message": f"software_id must be a valid integer, got: {software_id}",
        }
    except Exception as e:
        logger.error(f"Error getting licensed software details for ID {software_id}: {e}")
        return {
            "error": "Failed to retrieve licensed software details",
            "message": str(e),
            "software_id": software_id,
        }


@mcp.tool
async def get_ldap_servers() -> list[dict[str, Any]]:
    """
    Get list of all LDAP servers.

    :return: List of LDAP servers
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_ldap_servers()
    except Exception as e:
        logger.error(f"Error getting LDAP servers: {e}")
        return [{"error": "Failed to retrieve LDAP servers", "message": str(e)}]


@mcp.tool
async def get_ldap_server_details(
    server_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific LDAP server.

    :param server_id: The LDAP server ID
    :type server_id: str
    :return: Detailed LDAP server information
    :rtype: dict[str, Any]
    """
    try:
        server_id_int = int(server_id)
        return await jamf_api.get_ldap_server_details(server_id_int)
    except ValueError:
        logger.error(f"Invalid server_id format: {server_id}")
        return {
            "error": "Invalid server_id",
            "message": f"server_id must be a valid integer, got: {server_id}",
        }
    except Exception as e:
        logger.error(f"Error getting LDAP server details for ID {server_id}: {e}")
        return {
            "error": "Failed to retrieve LDAP server details",
            "message": str(e),
            "server_id": server_id,
        }


@mcp.tool
async def get_directory_bindings() -> list[dict[str, Any]]:
    """
    Get list of all directory bindings.

    :return: List of directory bindings
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_directory_bindings()
    except Exception as e:
        logger.error(f"Error getting directory bindings: {e}")
        return [{"error": "Failed to retrieve directory bindings", "message": str(e)}]


@mcp.tool
async def get_directory_binding_details(
    binding_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific directory binding.

    :param binding_id: The directory binding ID
    :type binding_id: str
    :return: Detailed directory binding information
    :rtype: dict[str, Any]
    """
    try:
        binding_id_int = int(binding_id)
        return await jamf_api.get_directory_binding_details(binding_id_int)
    except ValueError:
        logger.error(f"Invalid binding_id format: {binding_id}")
        return {
            "error": "Invalid binding_id",
            "message": f"binding_id must be a valid integer, got: {binding_id}",
        }
    except Exception as e:
        logger.error(f"Error getting directory binding details for ID {binding_id}: {e}")
        return {
            "error": "Failed to retrieve directory binding details",
            "message": str(e),
            "binding_id": binding_id,
        }


@mcp.tool
async def get_webhooks() -> list[dict[str, Any]]:
    """
    Get list of all webhooks.

    :return: List of webhooks
    :rtype: list[dict[str, Any]]
    """
    try:
        return await jamf_api.get_webhooks()
    except Exception as e:
        logger.error(f"Error getting webhooks: {e}")
        return [{"error": "Failed to retrieve webhooks", "message": str(e)}]


@mcp.tool
async def get_webhook_details(
    webhook_id: str,
) -> dict[str, Any]:
    """
    Get detailed information about a specific webhook.

    :param webhook_id: The webhook ID
    :type webhook_id: str
    :return: Detailed webhook information
    :rtype: dict[str, Any]
    """
    try:
        webhook_id_int = int(webhook_id)
        return await jamf_api.get_webhook_details(webhook_id_int)
    except ValueError:
        logger.error(f"Invalid webhook_id format: {webhook_id}")
        return {
            "error": "Invalid webhook_id",
            "message": f"webhook_id must be a valid integer, got: {webhook_id}",
        }
    except Exception as e:
        logger.error(f"Error getting webhook details for ID {webhook_id}: {e}")
        return {
            "error": "Failed to retrieve webhook details",
            "message": str(e),
            "webhook_id": webhook_id,
        }


@mcp.tool
async def get_device_lock_pin(
    computer_id: str,
) -> dict[str, Any]:
    """
    Get device lock PIN for a computer.

    :param computer_id: The JSS ID of the computer
    :type computer_id: str
    :return: Device lock PIN information or error if device not locked
    :rtype: dict[str, Any]
    """
    try:
        computer_id_int = int(computer_id)
        return await jamf_api.get_device_lock_pin(computer_id_int)
    except ValueError:
        logger.error(f"Invalid computer_id format: {computer_id}")
        return {
            "error": "Invalid computer_id",
            "message": f"computer_id must be a valid integer, got: {computer_id}",
        }
    except Exception as e:
        logger.error(f"Error getting device lock PIN for computer {computer_id}: {e}")
        # Check if it's a 404 (device not locked) or 403 (no permission)
        error_message = str(e)
        if "404" in error_message:
            return {
                "error": "Device not locked",
                "message": "This device is not currently locked or does not have a recovery PIN available",
                "computer_id": computer_id,
            }
        elif "403" in error_message:
            return {
                "error": "Permission denied",
                "message": "You do not have permission to view device lock PINs",
                "computer_id": computer_id,
            }
        else:
            return {
                "error": "Failed to retrieve device lock PIN",
                "message": error_message,
                "computer_id": computer_id,
            }


@mcp.tool
async def ping() -> dict[str, str]:
    """
    Simple ping test to verify the MCP server is responding.

    :return: Dictionary containing a simple ping response
    """
    return {"message": "pong", "status": "ok"}


if __name__ == "__main__":
    mcp.run()
