"""
Mock API response fixtures for jamfmcp testing.

This module provides realistic mock responses based on the Jamf Pro API
OpenAPI schema. All data is fictitious and follows the exact structure
of real API responses.
"""

from datetime import datetime, timezone
from typing import Any

from faker import Faker

faker = Faker()


def create_auth_token_response() -> dict[str, Any]:
    """
    Create a mock auth token response.

    :return: Mock auth token response
    :rtype: dict[str, Any]
    """
    return {"token": faker.sha256(), "expires": "2024-12-31T23:59:59.999Z"}


def create_computer_inventory_response(
    computer_id: str | None = None,
    serial_number: str | None = None,
    sections: list[str] | None = None,
) -> dict[str, Any]:
    """
    Create a mock computer inventory response.

    :param computer_id: Computer ID
    :type computer_id: str | None
    :param serial_number: Serial number
    :type serial_number: str | None
    :param sections: Sections to include
    :type sections: list[str] | None
    :return: Mock computer inventory response
    :rtype: dict[str, Any]
    """
    if not computer_id:
        computer_id = str(faker.random_int(min=1000, max=9999))
    if not serial_number:
        serial_number = f"FAKE{faker.bothify(text='????####')}"

    response = {
        "id": computer_id,
        "udid": faker.uuid4().upper(),
        "general": {
            "name": f"{faker.first_name()}'s MacBook Pro",
            "lastIpAddress": faker.ipv4_private(),
            "lastReportedIp": faker.ipv4_public(),
            "jamfBinaryVersion": "10.45.0-t1679335982",
            "platform": "Mac",
            "barcode1": None,
            "barcode2": None,
            "assetTag": faker.bothify(text="ASSET-####"),
            "remoteManagement": {"managed": True, "managementUsername": "jamfadmin"},
            "supervised": True,
            "mdmCapable": {"capable": True, "capableUsers": ["jamfadmin"]},
            "reportDate": datetime.now(timezone.utc).isoformat(),
            "lastContactTime": datetime.now(timezone.utc).isoformat(),
            "lastCloudBackupDate": datetime.now(timezone.utc).isoformat(),
            "lastEnrolledDate": "2023-01-15T10:30:00Z",
            "mdmProfileExpiration": "2025-01-15T10:30:00Z",
            "initialEntryDate": "2023-01-15",
            "distributionPoint": None,
            "enrollmentMethod": {
                "id": "1",
                "objectName": "User Initiated Enrollment",
                "objectType": "ENROLLMENT",
            },
            "site": {"id": "-1", "name": "None"},
            "itunesStoreAccountActive": True,
            "enrolledViaAutomatedDeviceEnrollment": False,
            "userApprovedMdm": True,
            "declarativeDeviceManagementEnabled": True,
            "extensionAttributes": [],
            "managementId": faker.uuid4(),
        },
        "hardware": {
            "make": "Apple",
            "model": "MacBook Pro (16-inch, 2021)",
            "modelIdentifier": "MacBookPro18,1",
            "serialNumber": serial_number,
            "processorSpeedMhz": 3200,
            "processorCount": 1,
            "coreCount": 10,
            "processorType": "Apple M1 Pro",
            "processorArchitecture": "arm64",
            "busSpeedMhz": 0,
            "cacheSizeKilobytes": 0,
            "networkAdapterType": "Wi-Fi",
            "macAddress": faker.mac_address(),
            "altNetworkAdapterType": "Ethernet",
            "altMacAddress": faker.mac_address(),
            "totalRamMegabytes": 16384,
            "openRamSlots": 0,
            "batteryCapacityPercent": faker.random_int(min=70, max=100),
            "smcVersion": "1.0.0",
            "nicSpeed": "1000",
            "opticalDrive": None,
            "bootRom": "8419.41.10",
            "bleCapable": True,
            "supportsIosAppInstalls": True,
            "appleSilicon": True,
            "extensionAttributes": [],
        },
        "operatingSystem": {
            "name": "macOS",
            "version": "14.1.0",
            "build": "23B74",
            "supplementalBuildVersion": None,
            "rapidSecurityResponse": None,
            "activeDirectoryStatus": "Not Bound",
            "fileVault2Status": "VALID",
            "fileVault2RecoveryKeyValidated": True,
            "fileVault2RecoveryKeyValidatedDate": "2023-06-15T12:00:00Z",
            "softwareUpdateDeviceId": faker.uuid4(),
            "extensionAttributes": [],
        },
        "userAndLocation": {
            "username": faker.user_name(),
            "realname": faker.name(),
            "email": faker.email(),
            "position": faker.job(),
            "phone": faker.phone_number(),
            "departmentId": str(faker.random_int(min=1, max=10)),
            "buildingId": str(faker.random_int(min=1, max=5)),
            "room": faker.bothify(text="Room ###"),
            "extensionAttributes": [],
        },
        "security": {
            "sipStatus": "ENABLED",
            "gatekeeperStatus": "ENABLED",
            "xprotectVersion": "2166",
            "autoLoginDisabled": True,
            "remoteDesktopEnabled": False,
            "activationLockEnabled": True,
            "recoveryLockEnabled": False,
            "firewallEnabled": True,
            "secureBootLevel": "FULL",
            "externalBootLevel": "DISALLOWED",
            "bootstrapTokenAllowed": True,
            "bootstrapTokenEscrowedStatus": "ESCROWED",
            "bootstrapTokenRequiredForSoftwareUpdate": True,
            "bootstrapTokenRequiredForKernelExtensionApproval": True,
        },
        "storage": {
            "bootDriveAvailableSpaceBytes": faker.random_int(min=100000000000, max=500000000000),
            "disks": [
                {
                    "id": "1",
                    "device": "disk0",
                    "model": "APPLE SSD AP0512Q",
                    "revision": "1161.80.",
                    "serialNumber": faker.bothify(text="??########"),
                    "size": 500277790720,
                    "type": "INTERNAL",
                    "partitions": [
                        {
                            "name": "Macintosh HD",
                            "sizeMegabytes": 476837,
                            "availableMegabytes": faker.random_int(min=100000, max=300000),
                            "partitionType": "APFS",
                            "percentUsed": faker.random_int(min=20, max=80),
                            "fileVault2State": "VALID",
                            "fileVault2ProgressPercent": 100,
                            "lvmManaged": False,
                        }
                    ],
                }
            ],
        },
    }

    # Add sections based on request
    if sections and "ALL" not in sections:
        # Filter response to only requested sections
        filtered_response = {"id": response["id"], "udid": response["udid"]}
        section_mapping = {
            "GENERAL": "general",
            "HARDWARE": "hardware",
            "OPERATING_SYSTEM": "operatingSystem",
            "USER_AND_LOCATION": "userAndLocation",
            "SECURITY": "security",
            "STORAGE": "storage",
        }
        for section in sections:
            if section in section_mapping and section_mapping[section] in response:
                filtered_response[section_mapping[section]] = response[section_mapping[section]]
        return filtered_response

    return response


def create_computer_search_results(count: int = 5) -> dict[str, Any]:
    """
    Create mock computer search results.

    :param count: Number of results to generate
    :type count: int
    :return: Mock computer search results
    :rtype: dict[str, Any]
    """
    return {
        "totalCount": count,
        "results": [
            {
                "id": str(faker.random_int(min=1000, max=9999)),
                "location": {
                    "username": faker.user_name(),
                    "realName": faker.name(),
                    "emailAddress": faker.email(),
                    "position": faker.job(),
                    "phoneNumber": faker.phone_number(),
                    "departmentId": str(faker.random_int(min=1, max=10)),
                    "buildingId": str(faker.random_int(min=1, max=5)),
                    "room": faker.bothify(text="Room ###"),
                },
                "name": f"{faker.first_name()}'s MacBook Pro",
                "udid": faker.uuid4().upper(),
                "serialNumber": f"FAKE{faker.bothify(text='????####')}",
                "lastContactDate": datetime.now(timezone.utc).isoformat(),
                "lastReportDate": datetime.now(timezone.utc).isoformat(),
                "lastEnrollmentDate": "2023-01-15T10:30:00Z",
                "operatingSystemVersion": "14.1.0",
                "operatingSystemBuild": "23B74",
                "operatingSystemSupplementalBuildVersion": None,
                "operatingSystemRapidSecurityResponse": None,
                "ipAddress": faker.ipv4_private(),
                "jamfBinaryVersion": "10.45.0-t1679335982",
                "platform": "Mac",
                "isManaged": True,
            }
            for _ in range(count)
        ],
    }


def create_computer_history_response(computer_id: str | None = None) -> dict[str, Any]:
    """
    Create mock computer history response.

    :param computer_id: Computer ID
    :type computer_id: str | None
    :return: Mock computer history response
    :rtype: dict[str, Any]
    """
    if not computer_id:
        computer_id = str(faker.random_int(min=1000, max=9999))

    return {
        "id": computer_id,
        "general": {
            "name": f"{faker.first_name()}'s MacBook Pro",
            "udid": faker.uuid4().upper(),
            "serialNumber": f"FAKE{faker.bothify(text='????####')}",
            "macAddress": faker.mac_address(),
        },
        "computerUsageLogs": [
            {
                "event": "Login",
                "username": faker.user_name(),
                "dateTime": faker.date_time_this_month().isoformat() + "Z",
            }
            for _ in range(faker.random_int(min=5, max=15))
        ],
        "auditLogs": [
            {
                "event": "Inventory Update",
                "username": "jamf",
                "dateTime": faker.date_time_this_week().isoformat() + "Z",
                "note": "Automated inventory collection",
            }
            for _ in range(faker.random_int(min=3, max=8))
        ],
        "policyLogs": [
            {
                "policyId": str(faker.random_int(min=1, max=100)),
                "policyName": f"Policy {faker.word()}",
                "username": faker.user_name(),
                "dateCompleted": faker.date_time_this_month().isoformat() + "Z",
                "status": "Completed",
            }
            for _ in range(faker.random_int(min=10, max=30))
        ],
        "casperRemoteLogs": [],
        "screenSharingLogs": [],
        "casperImagingLogs": [],
        "commands": {
            "completed": [
                {
                    "id": str(faker.random_int(min=1000, max=9999)),
                    "name": "InventoryUpdate",
                    "dateCompleted": faker.date_time_this_week().isoformat() + "Z",
                    "username": "jamf",
                }
                for _ in range(faker.random_int(min=5, max=15))
            ],
            "pending": [],
            "failed": [],
        },
        "userLocationChange": [
            {
                "username": faker.user_name(),
                "realName": faker.name(),
                "email": faker.email(),
                "position": faker.job(),
                "dateTime": faker.date_time_this_year().isoformat() + "Z",
            }
        ],
        "macAppStoreApplications": [
            {
                "name": app,
                "version": f"{faker.random_int(min=1, max=10)}.{faker.random_int(min=0, max=9)}.{faker.random_int(min=0, max=9)}",
                "sizeMegabytes": faker.random_int(min=10, max=500),
                "isFree": faker.boolean(),
                "dateInstalled": faker.date_time_this_year().isoformat() + "Z",
            }
            for app in ["Pages", "Numbers", "Keynote", "Xcode", "Final Cut Pro"]
        ],
    }


def create_policy_response(policy_id: str | None = None) -> dict[str, Any]:
    """
    Create mock policy response.

    :param policy_id: Policy ID
    :type policy_id: str | None
    :return: Mock policy response
    :rtype: dict[str, Any]
    """
    if not policy_id:
        policy_id = str(faker.random_int(min=1, max=1000))

    return {
        "id": policy_id,
        "name": f"Policy {faker.word().title()}",
        "enabled": faker.boolean(chance_of_getting_true=80),
        "trigger": "CHECKIN",
        "frequency": "Once per computer",
        "category": {"id": str(faker.random_int(min=1, max=20)), "name": faker.word().title()},
        "scope": {
            "allComputers": False,
            "computers": [],
            "computerGroups": [
                {"id": str(faker.random_int(min=1, max=50)), "name": f"Group {faker.word()}"}
            ],
        },
        "payloads": {
            "packages": [
                {
                    "id": str(faker.random_int(min=1, max=100)),
                    "name": f"{faker.word()}.pkg",
                    "action": "Install",
                    "fillUserTemplate": False,
                    "fillExistingUsers": False,
                }
            ],
            "scripts": [
                {
                    "id": str(faker.random_int(min=1, max=50)),
                    "name": f"{faker.word()}_script.sh",
                    "priority": "After",
                    "parameter4": "",
                    "parameter5": "",
                    "parameter6": "",
                    "parameter7": "",
                    "parameter8": "",
                    "parameter9": "",
                    "parameter10": "",
                    "parameter11": "",
                }
            ],
        },
    }


def create_configuration_profile_response(profile_id: str | None = None) -> dict[str, Any]:
    """
    Create mock configuration profile response.

    :param profile_id: Profile ID
    :type profile_id: str | None
    :return: Mock configuration profile response
    :rtype: dict[str, Any]
    """
    if not profile_id:
        profile_id = str(faker.random_int(min=1, max=500))

    return {
        "id": profile_id,
        "name": f"Profile {faker.word().title()}",
        "description": faker.sentence(),
        "level": "Computer",
        "distributionMethod": "Install Automatically",
        "userRemovable": False,
        "lastModified": faker.date_time_this_year().isoformat() + "Z",
        "scope": {
            "allComputers": False,
            "allJSSUsers": False,
            "computers": [],
            "computerGroups": [
                {"id": str(faker.random_int(min=1, max=50)), "name": f"Group {faker.word()}"}
            ],
        },
        "payloads": [
            {
                "payloadType": "com.apple.security.firewall",
                "payloadIdentifier": faker.uuid4(),
                "payloadDisplayName": "Firewall Settings",
                "payloadEnabled": True,
            }
        ],
    }


def create_mdm_command_response(command_id: str | None = None) -> dict[str, Any]:
    """
    Create mock MDM command response.

    :param command_id: Command ID
    :type command_id: str | None
    :return: Mock MDM command response
    :rtype: dict[str, Any]
    """
    if not command_id:
        command_id = faker.uuid4()

    return {
        "commandId": command_id,
        "commandType": "InventoryUpdate",
        "commandStatus": "Completed",
        "dateIssued": faker.date_time_this_week().isoformat() + "Z",
        "dateCompleted": faker.date_time_this_week().isoformat() + "Z",
        "deviceId": str(faker.random_int(min=1000, max=9999)),
        "deviceType": "Computer",
    }


def create_device_lock_pin_response() -> dict[str, Any]:
    """
    Create mock device lock PIN response.

    :return: Mock device lock PIN response
    :rtype: dict[str, Any]
    """
    return {"deviceLockPin": faker.bothify(text="######")}


def create_error_response(
    status_code: int = 404, error_message: str | None = None
) -> dict[str, Any]:
    """
    Create mock error response.

    :param status_code: HTTP status code
    :type status_code: int
    :param error_message: Error message
    :type error_message: str | None
    :return: Mock error response
    :rtype: dict[str, Any]
    """
    if not error_message:
        error_messages = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            409: "Conflict",
            500: "Internal Server Error",
        }
        error_message = error_messages.get(status_code, "Unknown Error")

    return {
        "httpStatus": status_code,
        "errors": [{"code": f"ERROR_{status_code}", "description": error_message, "field": None}],
    }


def create_paginated_response(
    results: list[dict[str, Any]],
    page: int = 0,
    page_size: int = 100,
    total_count: int | None = None,
) -> dict[str, Any]:
    """
    Create mock paginated response.

    :param results: List of results
    :type results: list[dict[str, Any]]
    :param page: Page number
    :type page: int
    :param page_size: Page size
    :type page_size: int
    :param total_count: Total count
    :type total_count: int | None
    :return: Mock paginated response
    :rtype: dict[str, Any]
    """
    if total_count is None:
        total_count = len(results)

    return {
        "totalCount": total_count,
        "results": results[page * page_size : (page + 1) * page_size],
    }
