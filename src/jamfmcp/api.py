import logging
from typing import Any

import httpx

from .auth import JamfAuth
from .jamfsdk import JamfProClient
from .jamfsdk.clients.pro_api.pagination import FilterField

logger = logging.getLogger(__name__)


class JamfApi:
    """
    API client for interacting with Jamf Pro services.

    This class provides methods to interact with Jamf Pro API endpoints including
    computer inventory, user management, policies, configuration profiles, and more.
    All methods are async and use the JamfProClient for authenticated requests.
    """

    def __init__(self, auth: JamfAuth) -> None:
        """
        Initialize the JamfApi client with authentication.

        :param auth: JamfAuth instance for authentication
        :type auth: JamfAuth
        """
        self.auth = auth
        self.server = auth.server
        self.credentials = auth.get_credentials_provider()

    async def get_serial_for_user(self, email_address: str) -> str | None:
        """
        Retrieve the serial number of a computer assigned to a user by email address.

        :param email_address: The email address of the user
        :type email_address: str
        :return: The serial number (name) of the first assigned computer, or None if not found
        :rtype: str | None
        :raises ValueError: If email address is invalid or user not found
        :raises ConnectionError: If API request fails
        """
        try:
            async with JamfProClient(self.server, self.credentials) as client:
                resp = await client.classic_api_request("get", f"users/email/{email_address}")
                response = await client.parse_json_response(resp)

                # Check if users list exists and is not empty
                users = response.get("users", [])
                if not users:
                    logger.warning("No user found with email address: %s", email_address)
                    raise ValueError(f"No user found with email address: {email_address}")

                jss_user = users[0]
                links = jss_user.get("links", [])

                # Search for assigned computers
                for link in links:
                    computers = link.get("computer")
                    if computers:  # list of dict
                        for c in computers:
                            serial = c.get("name")
                            if serial:
                                logger.info("Found serial %s for user %s", serial, email_address)
                                return serial

                # No computers found for user
                logger.warning("No assigned computers found for user: %s", email_address)
                return None

        except (httpx.HTTPError, ConnectionError, TimeoutError) as e:
            logger.error(
                "Connection error retrieving serial for email %s: %s",
                email_address,
                str(e),
            )
            raise ConnectionError(f"Failed to connect to Jamf Pro: {str(e)}") from e
        except (ValueError, KeyError, AttributeError) as e:
            logger.error("Data processing error for email %s: %s", email_address, str(e))
            raise ValueError(f"Error processing user data for {email_address}: {str(e)}") from e

    async def get_computer_inventory(
        self,
        serial: str | None = None,
        computer_id: int | None = None,
        sections: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Get detailed computer inventory information.

        :param serial: The serial number of the computer
        :type serial: str | None
        :param computer_id: The JSS ID of the computer
        :type computer_id: int | None
        :param sections: Optional list of inventory sections to retrieve
        :type sections: list[str] | None
        :return: Dictionary containing computer inventory data
        :rtype: dict[str, Any]
        :raises ValueError: If neither serial nor computer_id is provided, or if computer not found
        :raises ConnectionError: If API request fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            if serial:
                computers = await client.pro_api.get_computer_inventory_v1(
                    sections=sections or ["ALL"],
                    filter_expression=FilterField("hardware.serialNumber").eq(serial),
                    return_generator=False,
                )
                if not computers:
                    raise ValueError(f"No computer found with serial number: {serial}")
                return computers[0].model_dump()
            elif computer_id:
                computer_resp = await client.pro_api_request(
                    "get", f"v1/computers-inventory-detail/{computer_id}"
                )
                return await client.parse_json_response(computer_resp)
            else:
                raise ValueError("Either serial or computer_id must be provided")

    async def get_computer_history(self, computer_id: str | int) -> dict[str, Any]:
        """
        Get computer history including policy logs and management commands.

        :param computer_id: The JSS ID of the computer
        :type computer_id: str | int
        :return: Dictionary containing computer history data or error information
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails (handled and returned as error dict)
        :raises ValueError: If data processing fails (handled and returned as error dict)
        """
        try:
            async with JamfProClient(self.server, self.credentials) as client:
                history = await client.classic_api_request(
                    "get", f"computerhistory/id/{computer_id}"
                )
                response = await client.parse_json_response(history)
                return response.get("computer_history", {})

        except (httpx.HTTPError, ConnectionError, TimeoutError) as e:
            logger.error(
                "Connection error getting computer history for computer_id %s: %s",
                computer_id,
                str(e),
            )
            return {
                "error": "Connection Error",
                "message": f"Failed to connect to Jamf Pro: {str(e)}",
                "computer_id": computer_id,
            }
        except (ValueError, KeyError, AttributeError) as e:
            logger.error("Data processing error for computer_id %s: %s", computer_id, str(e))
            return {
                "error": "Data Error",
                "message": f"Error processing response data: {str(e)}",
                "computer_id": computer_id,
            }

    async def get_compliance_status(self, computer_id: str | int) -> dict[str, Any]:
        """
        Get compliance status for a computer.

        :param computer_id: The JSS ID of the computer
        :type computer_id: str | int
        :return: Dictionary containing compliance status information or error information
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails (handled and returned as error dict)
        :raises ValueError: If data processing fails (handled and returned as error dict)
        """
        try:
            async with JamfProClient(self.server, self.credentials) as client:
                status = await client.pro_api_request(
                    "get",
                    f"v1/conditional-access/device-compliance-information/computer/{computer_id}",
                )
                return await client.parse_json_response(status)

        except (httpx.HTTPError, ConnectionError, TimeoutError) as e:
            logger.error(
                "Connection error getting compliance for computer_id %s: %s",
                computer_id,
                str(e),
            )
            return {
                "error": "Connection Error",
                "message": f"Failed to connect to Jamf Pro: {str(e)}",
                "computer_id": computer_id,
            }
        except (ValueError, KeyError, AttributeError) as e:
            logger.error(
                "Data processing error for compliance computer_id %s: %s",
                computer_id,
                str(e),
            )
            return {
                "error": "Data Processing Error",
                "message": f"Error processing compliance data: {str(e)}",
                "computer_id": computer_id,
            }

    async def search_computers(
        self,
        filter_expression: FilterField | Any | None = None,
        page_size: int = 100,
        sections: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for computers with optional filtering.

        :param filter_expression: Filter expression for the search
        :type filter_expression: FilterField | Any | None
        :param page_size: Number of results per page
        :type page_size: int
        :param sections: List of sections to retrieve
        :type sections: list[str] | None
        :return: List of computer inventory data
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            computers = await client.pro_api.get_computer_inventory_v1(
                sections=sections or ["GENERAL"],
                filter_expression=filter_expression,
                page_size=page_size,
                return_generator=False,
            )
            return [computer.model_dump() for computer in computers]

    async def get_jcds_files(self) -> list[dict[str, Any]]:
        """
        Get list of files in Jamf Cloud Distribution Service.

        :return: List of JCDS file information
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            files = await client.pro_api.get_jcds_files_v1()
            return [file.model_dump() for file in files]

    async def get_policies(self) -> list[dict[str, Any]]:
        """
        Get list of all policies.

        :return: List of policy information
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "policies")
            data = await client.parse_json_response(response)
            return data.get("policies", [])

    async def get_policy_details(self, policy_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific policy.

        :param policy_id: ID of the policy
        :type policy_id: int
        :return: Policy details
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """

        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"policies/id/{policy_id}")
            data = await client.parse_json_response(response)
            return data.get("policy", {})

    async def get_configuration_profiles(self) -> list[dict[str, Any]]:
        """
        Get list of all configuration profiles.

        :return: List of configuration profile information
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """

        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "osxconfigurationprofiles")
            data = await client.parse_json_response(response)
            return data.get("os_x_configuration_profiles", [])

    async def get_profile_details(self, profile_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific configuration profile.

        :param profile_id: ID of the configuration profile
        :type profile_id: int
        :return: Profile details
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """

        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request(
                "get", f"osxconfigurationprofiles/id/{profile_id}"
            )
            data = await client.parse_json_response(response)
            return data.get("os_x_configuration_profile", {})

    async def get_extension_attributes(self) -> list[dict[str, Any]]:
        """
        Get list of all computer extension attributes.

        :return: List of extension attribute information
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """

        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "computerextensionattributes")
            data = await client.parse_json_response(response)
            return data.get("computer_extension_attributes", [])

    async def get_smart_groups(self) -> list[dict[str, Any]]:
        """
        Get list of all smart computer groups.

        :return: List of smart group information
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """

        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "computergroups")
            data = await client.parse_json_response(response)
            return data.get("computer_groups", [])

    async def get_group_details(self, group_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific computer group.

        :param group_id: ID of the computer group
        :type group_id: int
        :return: Group details
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """

        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"computergroups/id/{group_id}")
            data = await client.parse_json_response(response)
            return data.get("computer_group", {})

    async def get_scripts(self) -> list[dict[str, Any]]:
        """
        Get list of all scripts.

        :return: List of script information including names, IDs, and basic details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "scripts")
            data = await client.parse_json_response(response)
            return data.get("scripts", [])

    async def get_script_details(self, script_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific script including script contents.

        :param script_id: ID of the script
        :type script_id: int
        :return: Script details including script contents, parameters, and metadata
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"scripts/id/{script_id}")
            data = await client.parse_json_response(response)
            return data.get("script", {})

    async def get_packages(self) -> list[dict[str, Any]]:
        """
        Get list of all packages.

        :return: List of package information including names, IDs, categories, and basic details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.pro_api.get_packages_v1()
            return [p.model_dump() for p in response]

    async def get_package_details(self, package_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific package.

        :param package_id: ID of the package
        :type package_id: int
        :return: Package details including deployment settings, requirements, and metadata
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"packages/id/{package_id}")
            data = await client.parse_json_response(response)
            return data.get("package", {})

    async def get_users(self) -> list[dict[str, Any]]:
        """
        Get list of all users.

        :return: List of user information including names, IDs, email addresses, and basic details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "users")
            data = await client.parse_json_response(response)
            return data.get("users", [])

    async def get_user_details(self, user_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific user.

        :param user_id: ID of the user
        :type user_id: int
        :return: User details including contact info, groups, device assignments, and settings
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"users/id/{user_id}")
            data = await client.parse_json_response(response)
            return data.get("user", {})

    async def get_user_groups(self) -> list[dict[str, Any]]:
        """
        Get list of all user groups.

        :return: List of user group information including names, IDs, and membership details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "usergroups")
            data = await client.parse_json_response(response)
            return data.get("user_groups", [])

    async def get_user_group_details(self, group_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific user group.

        :param group_id: ID of the user group
        :type group_id: int
        :return: User group details including membership, criteria, and settings
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"usergroups/id/{group_id}")
            data = await client.parse_json_response(response)
            return data.get("user_group", {})

    async def get_buildings(self) -> list[dict[str, Any]]:
        """
        Get list of all buildings.

        :return: List of building information including names, IDs, and location details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "buildings")
            data = await client.parse_json_response(response)
            return data.get("buildings", [])

    async def get_building_details(self, building_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific building.

        :param building_id: ID of the building
        :type building_id: int
        :return: Building details including location, contact info, and assignments
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"buildings/id/{building_id}")
            data = await client.parse_json_response(response)
            return data.get("building", {})

    async def get_departments(self) -> list[dict[str, Any]]:
        """
        Get list of all departments.

        :return: List of department information including names, IDs, and organizational details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "departments")
            data = await client.parse_json_response(response)
            return data.get("departments", [])

    async def get_department_details(self, department_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific department.

        :param department_id: ID of the department
        :type department_id: int
        :return: Department details including members and organizational structure
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"departments/id/{department_id}")
            data = await client.parse_json_response(response)
            return data.get("department", {})

    async def get_network_segments(self) -> list[dict[str, Any]]:
        """
        Get list of all network segments.

        :return: List of network segment information including names, IDs, and network details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "networksegments")
            data = await client.parse_json_response(response)
            return data.get("network_segments", [])

    async def get_network_segment_details(self, segment_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific network segment.

        :param segment_id: ID of the network segment
        :type segment_id: int
        :return: Network segment details including IP ranges, settings, and assignments
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"networksegments/id/{segment_id}")
            data = await client.parse_json_response(response)
            return data.get("network_segment", {})

    async def get_patch_software_titles(self) -> list[dict[str, Any]]:
        """
        Get list of all patch software titles.

        :return: List of patch software title information including names, IDs, and versions
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.pro_api_request("get", "v2/patch-software-title-configurations")
            return await client.parse_json_response(response)

    async def get_patch_software_title_details(self, title_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific patch software title.

        :param title_id: ID of the patch software title
        :type title_id: int
        :return: Patch software title details including versions, policies, and update status
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request(
                "get", f"v2/patch-software-title-configurations/{title_id}"
            )
            return await client.parse_json_response(response)

    async def get_patch_policies(self) -> list[dict[str, Any]]:
        """
        Get list of all patch policies.

        :return: List of patch policy information including names, IDs, and target software
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.pro_api_request("get", "v2/patch-policies")
            data = await client.parse_json_response(response)
            return data.get("results", [])

    async def get_categories(self) -> list[dict[str, Any]]:
        """
        Get list of all categories.

        :return: List of category information including names, IDs, and organizational details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "categories")
            data = await client.parse_json_response(response)
            return data.get("categories", [])

    async def get_category_details(self, category_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific category.

        :param category_id: ID of the category
        :type category_id: int
        :return: Category details including associated items and organizational structure
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"categories/id/{category_id}")
            data = await client.parse_json_response(response)
            return data.get("category", {})

    async def get_sites(self) -> list[dict[str, Any]]:
        """
        Get list of all sites.

        :return: List of site information including names, IDs, and multi-site details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "sites")
            data = await client.parse_json_response(response)
            return data.get("sites", [])

    async def get_site_details(self, site_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific site.

        :param site_id: ID of the site
        :type site_id: int
        :return: Site details including location, configuration, and administrative settings
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"sites/id/{site_id}")
            data = await client.parse_json_response(response)
            return data.get("site", {})

    async def get_advanced_computer_searches(self) -> list[dict[str, Any]]:
        """
        Get list of all advanced computer searches.

        :return: List of advanced search information including names, IDs, and criteria
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "advancedcomputersearches")
            data = await client.parse_json_response(response)
            return data.get("advanced_computer_searches", [])

    async def get_advanced_computer_search_details(self, search_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific advanced computer search.

        :param search_id: ID of the advanced computer search
        :type search_id: int
        :return: Search details including criteria, results, and configuration
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request(
                "get", f"advancedcomputersearches/id/{search_id}"
            )
            data = await client.parse_json_response(response)
            return data.get("advanced_computer_search", {})

    async def get_restricted_software(self) -> list[dict[str, Any]]:
        """
        Get list of all restricted software.

        :return: List of restricted software information including names, IDs, and restriction details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "restrictedsoftware")
            data = await client.parse_json_response(response)
            return data.get("restricted_software", [])

    async def get_restricted_software_details(self, software_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific restricted software item.

        :param software_id: ID of the restricted software
        :type software_id: int
        :return: Restricted software details including restriction criteria and settings
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request(
                "get", f"restrictedsoftware/id/{software_id}"
            )
            data = await client.parse_json_response(response)
            return data.get("restricted_software", {})

    async def get_licensed_software(self) -> list[dict[str, Any]]:
        """
        Get list of all licensed software.

        :return: List of licensed software information including names, IDs, and license details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "licensedsoftware")
            data = await client.parse_json_response(response)
            return data.get("licensed_software", [])

    async def get_licensed_software_details(self, software_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific licensed software item.

        :param software_id: ID of the licensed software
        :type software_id: int
        :return: Licensed software details including license information and usage tracking
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"licensedsoftware/id/{software_id}")
            data = await client.parse_json_response(response)
            return data.get("licensed_software", {})

    async def get_ldap_servers(self) -> list[dict[str, Any]]:
        """
        Get list of all LDAP servers configured in Jamf Pro.

        :return: List of LDAP server information including server names, IDs, and connection details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "ldapservers")
            data = await client.parse_json_response(response)
            return data.get("ldap_servers", [])

    async def get_ldap_server_details(self, server_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific LDAP server.

        :param server_id: ID of the LDAP server
        :type server_id: int
        :return: LDAP server details including connection settings, search bases, and authentication
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"ldapservers/id/{server_id}")
            data = await client.parse_json_response(response)
            return data.get("ldap_server", {})

    async def get_directory_bindings(self) -> list[dict[str, Any]]:
        """
        Get list of all directory bindings configured in Jamf Pro.

        :return: List of directory binding information including binding names, IDs, and domain details
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "directorybindings")
            data = await client.parse_json_response(response)
            return data.get("directory_bindings", [])

    async def get_directory_binding_details(self, binding_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific directory binding.

        :param binding_id: ID of the directory binding
        :type binding_id: int
        :return: Directory binding details including domain settings, authentication, and user mapping
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"directorybindings/id/{binding_id}")
            data = await client.parse_json_response(response)
            return data.get("directory_binding", {})

    async def get_webhooks(self) -> list[dict[str, Any]]:
        """
        Get list of all webhooks configured in Jamf Pro.

        :return: List of webhook information including names, IDs, URLs, and event types
        :rtype: list[dict[str, Any]]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", "webhooks")
            data = await client.parse_json_response(response)
            return data.get("webhooks", [])

    async def get_webhook_details(self, webhook_id: int) -> dict[str, Any]:
        """
        Get detailed information about a specific webhook.

        :param webhook_id: ID of the webhook
        :type webhook_id: int
        :return: Webhook details including URL, events, authentication, and configuration
        :rtype: dict[str, Any]
        :raises ConnectionError: If API request fails
        :raises ValueError: If data processing fails
        """
        async with JamfProClient(self.server, self.credentials) as client:
            response = await client.classic_api_request("get", f"webhooks/id/{webhook_id}")
            data = await client.parse_json_response(response)
            return data.get("webhook", {})
