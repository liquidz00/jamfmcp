"""
Computer inventory test data fixtures.

This module provides diverse computer inventory test data with various
hardware configurations, operating systems, and health states.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

faker = Faker()


def create_healthy_computer() -> dict[str, Any]:
    """
    Create a computer with excellent health metrics.

    :return: Healthy computer inventory data
    :rtype: dict[str, Any]
    """
    now = datetime.now(timezone.utc)
    return {
        "id": "1001",
        "udid": faker.uuid4().upper(),
        "general": {
            "name": "Healthy-MacBook-Pro",
            "lastIpAddress": "192.168.1.100",
            "lastReportedIp": "203.0.113.45",
            "jamfBinaryVersion": "10.45.0-t1679335982",
            "platform": "Mac",
            "barcode1": None,
            "barcode2": None,
            "assetTag": "HEALTHY-001",
            "remoteManagement": {"managed": True, "managementUsername": "jamfadmin"},
            "supervised": True,
            "mdmCapable": {"capable": True, "capableUsers": ["jamfadmin"]},
            "reportDate": now.isoformat(),
            "lastContactTime": now.isoformat(),
            "lastCloudBackupDate": (now - timedelta(days=1)).isoformat(),
            "lastEnrolledDate": (now - timedelta(days=90)).isoformat(),
            "mdmProfileExpiration": (now + timedelta(days=300)).isoformat(),
            "initialEntryDate": (now - timedelta(days=365)).date().isoformat(),
            "distributionPoint": None,
            "enrollmentMethod": {
                "id": "1",
                "objectName": "User Initiated Enrollment",
                "objectType": "ENROLLMENT",
            },
            "site": {"id": "-1", "name": "None"},
            "itunesStoreAccountActive": True,
            "enrolledViaAutomatedDeviceEnrollment": True,
            "userApprovedMdm": True,
            "declarativeDeviceManagementEnabled": True,
            "extensionAttributes": [],
            "managementId": faker.uuid4(),
        },
        "hardware": {
            "make": "Apple",
            "model": "MacBook Pro (16-inch, 2023)",
            "modelIdentifier": "Mac15,7",
            "serialNumber": "HEALTHY12345",
            "processorSpeedMhz": 3500,
            "processorCount": 1,
            "coreCount": 12,
            "processorType": "Apple M3 Pro",
            "processorArchitecture": "arm64",
            "busSpeedMhz": 0,
            "cacheSizeKilobytes": 0,
            "networkAdapterType": "Wi-Fi",
            "macAddress": faker.mac_address(),
            "altNetworkAdapterType": "Ethernet",
            "altMacAddress": faker.mac_address(),
            "totalRamMegabytes": 32768,
            "openRamSlots": 0,
            "batteryCapacityPercent": 95,
            "smcVersion": "1.0.0",
            "nicSpeed": "1000",
            "opticalDrive": None,
            "bootRom": "10151.1.1",
            "bleCapable": True,
            "supportsIosAppInstalls": True,
            "appleSilicon": True,
            "extensionAttributes": [],
        },
        "operatingSystem": {
            "name": "macOS",
            "version": "14.2.1",
            "build": "23C71",
            "supplementalBuildVersion": None,
            "rapidSecurityResponse": None,
            "activeDirectoryStatus": "Not Bound",
            "fileVault2Status": "VALID",
            "fileVault2RecoveryKeyValidated": True,
            "fileVault2RecoveryKeyValidatedDate": (now - timedelta(days=30)).isoformat(),
            "softwareUpdateDeviceId": faker.uuid4(),
            "extensionAttributes": [],
        },
        "userAndLocation": {
            "username": "john.doe",
            "realname": "John Doe",
            "email": "john.doe@example.com",
            "position": "Senior Developer",
            "phone": "+1-555-0123",
            "departmentId": "5",
            "buildingId": "1",
            "room": "Room 301",
            "extensionAttributes": [],
        },
        "security": {
            "sipStatus": "ENABLED",
            "gatekeeperStatus": "ENABLED",
            "xprotectVersion": "2169",
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
            "bootDriveAvailableSpaceBytes": 750000000000,  # 750 GB free
            "disks": [
                {
                    "id": "1",
                    "device": "disk0",
                    "model": "APPLE SSD AP1024Z",
                    "revision": "1161.80.",
                    "serialNumber": "HEALTHY_DISK_001",
                    "size": 1000000000000,  # 1 TB
                    "type": "INTERNAL",
                    "partitions": [
                        {
                            "name": "Macintosh HD",
                            "sizeMegabytes": 953674,
                            "availableMegabytes": 715530,  # 75% free
                            "partitionType": "APFS",
                            "percentUsed": 25,
                            "fileVault2State": "VALID",
                            "fileVault2ProgressPercent": 100,
                            "lvmManaged": False,
                        }
                    ],
                }
            ],
        },
    }


def create_unhealthy_computer() -> dict[str, Any]:
    """
    Create a computer with poor health metrics.

    :return: Unhealthy computer inventory data
    :rtype: dict[str, Any]
    """
    now = datetime.now(timezone.utc)
    return {
        "id": "1002",
        "udid": faker.uuid4().upper(),
        "general": {
            "name": "Problematic-MacBook-Air",
            "lastIpAddress": "192.168.1.101",
            "lastReportedIp": "203.0.113.46",
            "jamfBinaryVersion": "10.38.0-t1679335982",  # Outdated
            "platform": "Mac",
            "barcode1": None,
            "barcode2": None,
            "assetTag": "PROBLEM-001",
            "remoteManagement": {
                "managed": False,  # Not managed
                "managementUsername": None,
            },
            "supervised": False,  # Not supervised
            "mdmCapable": {"capable": True, "capableUsers": []},
            "reportDate": (now - timedelta(days=45)).isoformat(),  # Old report
            "lastContactTime": (now - timedelta(days=45)).isoformat(),  # No recent contact
            "lastCloudBackupDate": (now - timedelta(days=180)).isoformat(),  # Very old backup
            "lastEnrolledDate": (now - timedelta(days=400)).isoformat(),
            "mdmProfileExpiration": (now + timedelta(days=30)).isoformat(),  # Expiring soon
            "initialEntryDate": (now - timedelta(days=500)).date().isoformat(),
            "distributionPoint": None,
            "enrollmentMethod": {
                "id": "1",
                "objectName": "User Initiated Enrollment",
                "objectType": "ENROLLMENT",
            },
            "site": {"id": "-1", "name": "None"},
            "itunesStoreAccountActive": False,
            "enrolledViaAutomatedDeviceEnrollment": False,
            "userApprovedMdm": False,  # Not approved
            "declarativeDeviceManagementEnabled": False,
            "extensionAttributes": [],
            "managementId": faker.uuid4(),
        },
        "hardware": {
            "make": "Apple",
            "model": "MacBook Air (13-inch, 2020)",
            "modelIdentifier": "MacBookAir10,1",
            "serialNumber": "PROBLEM12345",
            "processorSpeedMhz": 1100,
            "processorCount": 1,
            "coreCount": 4,
            "processorType": "Intel Core i3",
            "processorArchitecture": "x86_64",
            "busSpeedMhz": 0,
            "cacheSizeKilobytes": 0,
            "networkAdapterType": "Wi-Fi",
            "macAddress": faker.mac_address(),
            "altNetworkAdapterType": None,
            "altMacAddress": None,
            "totalRamMegabytes": 8192,  # Only 8 GB RAM
            "openRamSlots": 0,
            "batteryCapacityPercent": 45,  # Poor battery
            "smcVersion": "1.0.0",
            "nicSpeed": "100",
            "opticalDrive": None,
            "bootRom": "1731.40.139.0.0",
            "bleCapable": True,
            "supportsIosAppInstalls": False,
            "appleSilicon": False,
            "extensionAttributes": [],
        },
        "operatingSystem": {
            "name": "macOS",
            "version": "12.6.1",  # Outdated OS
            "build": "21G217",
            "supplementalBuildVersion": None,
            "rapidSecurityResponse": None,
            "activeDirectoryStatus": "Not Bound",
            "fileVault2Status": "NOT_ENCRYPTED",  # Not encrypted
            "fileVault2RecoveryKeyValidated": False,
            "fileVault2RecoveryKeyValidatedDate": None,
            "softwareUpdateDeviceId": faker.uuid4(),
            "extensionAttributes": [],
        },
        "userAndLocation": {
            "username": "temp.user",
            "realname": "Temporary User",
            "email": "temp@example.com",
            "position": "Intern",
            "phone": "+1-555-9999",
            "departmentId": "1",
            "buildingId": "2",
            "room": "Shared Space",
            "extensionAttributes": [],
        },
        "security": {
            "sipStatus": "DISABLED",  # SIP disabled
            "gatekeeperStatus": "DISABLED",  # Gatekeeper disabled
            "xprotectVersion": "2130",  # Outdated
            "autoLoginDisabled": False,  # Auto-login enabled
            "remoteDesktopEnabled": True,  # Remote desktop enabled
            "activationLockEnabled": False,
            "recoveryLockEnabled": False,
            "firewallEnabled": False,  # Firewall disabled
            "secureBootLevel": "NONE",
            "externalBootLevel": "ALLOWED",
            "bootstrapTokenAllowed": False,
            "bootstrapTokenEscrowedStatus": "NOT_ESCROWED",
            "bootstrapTokenRequiredForSoftwareUpdate": False,
            "bootstrapTokenRequiredForKernelExtensionApproval": False,
        },
        "storage": {
            "bootDriveAvailableSpaceBytes": 10000000000,  # Only 10 GB free
            "disks": [
                {
                    "id": "1",
                    "device": "disk0",
                    "model": "APPLE SSD AP0256Q",
                    "revision": "1161.80.",
                    "serialNumber": "PROBLEM_DISK_001",
                    "size": 250000000000,  # 250 GB
                    "type": "INTERNAL",
                    "partitions": [
                        {
                            "name": "Macintosh HD",
                            "sizeMegabytes": 238418,
                            "availableMegabytes": 9536,  # Only 4% free
                            "partitionType": "APFS",
                            "percentUsed": 96,  # Almost full
                            "fileVault2State": "NOT_ENCRYPTED",
                            "fileVault2ProgressPercent": 0,
                            "lvmManaged": False,
                        }
                    ],
                }
            ],
        },
    }


def create_moderate_health_computer() -> dict[str, Any]:
    """
    Create a computer with moderate health metrics.

    :return: Moderate health computer inventory data
    :rtype: dict[str, Any]
    """
    now = datetime.now(timezone.utc)
    return {
        "id": "1003",
        "udid": faker.uuid4().upper(),
        "general": {
            "name": "Average-MacBook-Pro",
            "lastIpAddress": "192.168.1.102",
            "lastReportedIp": "203.0.113.47",
            "jamfBinaryVersion": "10.44.0-t1679335982",  # Recent but not latest
            "platform": "Mac",
            "barcode1": None,
            "barcode2": None,
            "assetTag": "AVERAGE-001",
            "remoteManagement": {"managed": True, "managementUsername": "jamfadmin"},
            "supervised": True,
            "mdmCapable": {"capable": True, "capableUsers": ["jamfadmin"]},
            "reportDate": (now - timedelta(days=7)).isoformat(),  # Week old
            "lastContactTime": (now - timedelta(days=7)).isoformat(),
            "lastCloudBackupDate": (now - timedelta(days=30)).isoformat(),  # Month old backup
            "lastEnrolledDate": (now - timedelta(days=180)).isoformat(),
            "mdmProfileExpiration": (now + timedelta(days=180)).isoformat(),
            "initialEntryDate": (now - timedelta(days=730)).date().isoformat(),
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
            "model": "MacBook Pro (13-inch, 2022)",
            "modelIdentifier": "Mac14,7",
            "serialNumber": "AVERAGE12345",
            "processorSpeedMhz": 3200,
            "processorCount": 1,
            "coreCount": 8,
            "processorType": "Apple M2",
            "processorArchitecture": "arm64",
            "busSpeedMhz": 0,
            "cacheSizeKilobytes": 0,
            "networkAdapterType": "Wi-Fi",
            "macAddress": faker.mac_address(),
            "altNetworkAdapterType": "Ethernet",
            "altMacAddress": faker.mac_address(),
            "totalRamMegabytes": 16384,  # 16 GB RAM
            "openRamSlots": 0,
            "batteryCapacityPercent": 75,  # Decent battery
            "smcVersion": "1.0.0",
            "nicSpeed": "1000",
            "opticalDrive": None,
            "bootRom": "8422.141.2",
            "bleCapable": True,
            "supportsIosAppInstalls": True,
            "appleSilicon": True,
            "extensionAttributes": [],
        },
        "operatingSystem": {
            "name": "macOS",
            "version": "13.6.3",  # One major version behind
            "build": "22G436",
            "supplementalBuildVersion": None,
            "rapidSecurityResponse": None,
            "activeDirectoryStatus": "Not Bound",
            "fileVault2Status": "VALID",
            "fileVault2RecoveryKeyValidated": True,
            "fileVault2RecoveryKeyValidatedDate": (now - timedelta(days=90)).isoformat(),
            "softwareUpdateDeviceId": faker.uuid4(),
            "extensionAttributes": [],
        },
        "userAndLocation": {
            "username": "jane.smith",
            "realname": "Jane Smith",
            "email": "jane.smith@example.com",
            "position": "Product Manager",
            "phone": "+1-555-0456",
            "departmentId": "3",
            "buildingId": "1",
            "room": "Room 205",
            "extensionAttributes": [],
        },
        "security": {
            "sipStatus": "ENABLED",
            "gatekeeperStatus": "ENABLED",
            "xprotectVersion": "2166",  # Slightly outdated
            "autoLoginDisabled": True,
            "remoteDesktopEnabled": False,
            "activationLockEnabled": True,
            "recoveryLockEnabled": False,
            "firewallEnabled": True,
            "secureBootLevel": "MEDIUM",  # Not full security
            "externalBootLevel": "DISALLOWED",
            "bootstrapTokenAllowed": True,
            "bootstrapTokenEscrowedStatus": "ESCROWED",
            "bootstrapTokenRequiredForSoftwareUpdate": True,
            "bootstrapTokenRequiredForKernelExtensionApproval": True,
        },
        "storage": {
            "bootDriveAvailableSpaceBytes": 250000000000,  # 250 GB free
            "disks": [
                {
                    "id": "1",
                    "device": "disk0",
                    "model": "APPLE SSD AP0512Z",
                    "revision": "1161.80.",
                    "serialNumber": "AVERAGE_DISK_001",
                    "size": 500000000000,  # 500 GB
                    "type": "INTERNAL",
                    "partitions": [
                        {
                            "name": "Macintosh HD",
                            "sizeMegabytes": 476837,
                            "availableMegabytes": 238418,  # 50% free
                            "partitionType": "APFS",
                            "percentUsed": 50,
                            "fileVault2State": "VALID",
                            "fileVault2ProgressPercent": 100,
                            "lvmManaged": False,
                        }
                    ],
                }
            ],
        },
    }


def create_intel_computer() -> dict[str, Any]:
    """
    Create an Intel-based computer.

    :return: Intel computer inventory data
    :rtype: dict[str, Any]
    """
    base = create_moderate_health_computer()
    base["id"] = "1004"
    base["general"]["name"] = "Intel-MacBook-Pro"
    base["hardware"].update(
        {
            "model": "MacBook Pro (16-inch, 2019)",
            "modelIdentifier": "MacBookPro16,1",
            "serialNumber": "INTEL12345",
            "processorType": "Intel Core i9",
            "processorArchitecture": "x86_64",
            "processorSpeedMhz": 2300,
            "coreCount": 8,
            "appleSilicon": False,
            "supportsIosAppInstalls": False,
        }
    )
    return base


def create_ios_computer() -> dict[str, Any]:
    """
    Create a computer that supports iOS apps.

    :return: iOS-compatible computer inventory data
    :rtype: dict[str, Any]
    """
    base = create_healthy_computer()
    base["id"] = "1005"
    base["general"]["name"] = "iOS-Compatible-Mac"
    base["hardware"]["supportsIosAppInstalls"] = True
    return base


def create_computer_variations() -> list[dict[str, Any]]:
    """
    Create a list of computers with various configurations.

    :return: List of computer inventory data
    :rtype: list[dict[str, Any]]
    """
    return [
        create_healthy_computer(),
        create_unhealthy_computer(),
        create_moderate_health_computer(),
        create_intel_computer(),
        create_ios_computer(),
    ]


def create_computer_with_custom_attributes(
    computer_id: str = "1006", serial_number: str = "CUSTOM12345", **kwargs: Any
) -> dict[str, Any]:
    """
    Create a computer with custom attributes.

    :param computer_id: Computer ID
    :type computer_id: str
    :param serial_number: Serial number
    :type serial_number: str
    :param kwargs: Additional attributes to override
    :type kwargs: Any
    :return: Computer inventory data
    :rtype: dict[str, Any]
    """
    base = create_healthy_computer()
    base["id"] = computer_id
    base["hardware"]["serialNumber"] = serial_number

    # Apply custom attributes
    for key, value in kwargs.items():
        if "." in key:
            # Handle nested attributes like "general.name"
            parts = key.split(".")
            current = base
            for part in parts[:-1]:
                current = current[part]
            current[parts[-1]] = value
        else:
            base[key] = value

    return base
