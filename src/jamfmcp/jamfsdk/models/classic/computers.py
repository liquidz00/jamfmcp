from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from .. import BaseModel
from . import (
    ClassicApiModel,
    ClassicDeviceLocation,
    ClassicDevicePurchasing,
    ClassicSite,
)

_XML_ARRAY_ITEM_NAMES = {
    # Computer
    "certificates": "certificate",
    "extension_attributes": "extension_attribute",
    # Computer.Hardware
    "filevault2_users": "user",
    "storage": "device",
    "partitions": "partition",
    "mapped_printers": "printer",
    # Computer.Software
    "licensed_software": "name",
    "installed_by_casper": "package",
    "installed_by_installer_swu": "package",
    "cached_by_casper": "package",
    "available_software_updates": "name",
    "available_updates": "update",
    "running_services": "name",
    "applications": "application",
    "fonts": "font",
    "plugins": "plugin",
    # Computer.GroupsAccounts
    "computer_group_memberships": "group",
    "local_accounts": "user",
    # Computer.ConfigurationProfiles
    "configuration_profiles": "configuration_profile",
}

# Computer.General Models


class ClassicComputerGeneralRemoteManagement(BaseModel):
    """
    Computer nested model: computer.general.remote_management

    - :class:`str` management_password: This attribute is only used in POST/PUT operations
    - :class:`str` management_password_sha256: This attribute is read-only
    """

    model_config = ConfigDict(extra="allow")

    managed: bool | None = None
    management_username: str | None = None
    management_password: str | None = None
    management_password_sha256: str | None = None


class ClassicComputerGeneralMdmCapableUsers(BaseModel):
    """Computer nested model: computer.general.mdm_capable_users"""

    model_config = ConfigDict(extra="allow")

    mdm_capable_user: str | None = None


class ClassicComputerGeneralManagementStatus(BaseModel):
    """Computer nested model: computer.general.management_status"""

    model_config = ConfigDict(extra="allow")

    enrolled_via_dep: bool | None = None
    user_approved_enrollment: bool | None = None
    user_approved_mdm: bool | None = None


class ClassicComputerGeneral(BaseModel):
    """Computer nested model: computer.general"""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    mac_address: str | None = None
    network_adapter_type: str | None = None
    alt_mac_address: str | None = None
    alt_network_adapter_type: str | None = None
    ip_address: str | None = None
    last_reported_ip: str | None = None
    serial_number: str | None = None
    udid: str | None = None
    jamf_version: str | None = None
    platform: str | None = None
    barcode_1: str | None = None
    barcode_2: str | None = None
    asset_tag: str | None = None
    remote_management: ClassicComputerGeneralRemoteManagement | None = None
    supervised: bool | None = None
    mdm_capable: bool | None = None
    mdm_capable_users: dict | ClassicComputerGeneralMdmCapableUsers | None = None
    management_status: ClassicComputerGeneralManagementStatus | None = None
    report_date: str | None = None
    report_date_epoch: int | None = None
    report_date_utc: datetime | str | None = None
    last_contact_time: str | None = None
    last_contact_time_epoch: int | None = None
    last_contact_time_utc: str | None = None
    initial_entry_date: str | None = None
    initial_entry_date_epoch: int | None = None
    initial_entry_date_utc: datetime | str | None = None
    last_cloud_backup_date_epoch: int | None = None
    last_cloud_backup_date_utc: datetime | str | None = None
    last_enrolled_date_epoch: int | None = None
    last_enrolled_date_utc: datetime | str | None = None
    mdm_profile_expiration_epoch: int | None = None
    mdm_profile_expiration_utc: datetime | str | None = None
    distribution_point: str | None = None
    sus: str | None = None
    site: ClassicSite | None = None
    itunes_store_account_is_active: bool | None = None


# Computer.Hardware Models


class ClassicComputerHardwareStorageDevicePartition(BaseModel):
    """Computer nested model: computer.hardware.storage.partitions"""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    size: int | None = None
    type: str | None = None
    partition_capacity_mb: int | None = None
    percentage_full: int | None = None
    available_mb: int | None = None
    filevault_status: str | None = None
    filevault_percent: int | None = None
    filevault2_status: str | None = None
    filevault2_percent: int | None = None
    boot_drive_available_mb: int | None = None
    lvgUUID: str | None = None
    lvUUID: str | None = None
    pvUUID: str | None = None


class ClassicComputerHardwareStorageDevice(BaseModel):
    """Computer nested model: computer.hardware.storage"""

    model_config = ConfigDict(extra="allow")

    disk: str | None = None
    model: str | None = None
    revision: str | None = None
    serial_number: str | None = None
    size: int | None = None
    drive_capacity_mb: int | None = None
    connection_type: str | None = None
    smart_status: str | None = None
    partitions: list[ClassicComputerHardwareStorageDevicePartition] | None = None


class ClassicComputerHardwareMappedPrinter(BaseModel):
    """Computer nested model: computer.hardware.mapped_printers"""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    uri: str | None = None
    type: str | None = None
    location: str | None = None


class ClassicComputerHardware(ClassicApiModel):
    """Computer nested model: computer.hardware"""

    model_config = ConfigDict(extra="allow", protected_namespaces=())
    # The 'model_identifier' attribute conflicts with Pydantic's protect 'model_' namespace
    # Overriding 'protected_namespaces' for hardware suppresses the warning

    _xml_root_name = "hardware"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES

    make: str | None = None
    model: str | None = None
    model_identifier: str | None = None
    os_name: str | None = None
    os_version: str | None = None
    os_build: str | None = None
    software_update_device_id: str | None = None
    active_directory_status: str | None = None
    service_pack: str | None = None
    processor_type: str | None = None
    is_apple_silicon: bool | None = None
    processor_architecture: str | None = None
    processor_speed: int | None = None
    processor_speed_mhz: int | None = None
    number_processors: int | None = None
    number_cores: int | None = None
    total_ram: int | None = None
    total_ram_mb: int | None = None
    boot_rom: str | None = None
    bus_speed: int | None = None
    bus_speed_mhz: int | None = None
    battery_capacity: int | None = None
    cache_size: int | None = None
    cache_size_kb: int | None = None
    available_ram_slots: int | None = None
    optical_drive: str | None = None
    nic_speed: str | None = None
    smc_version: str | None = None
    ble_capable: bool | None = None
    supports_ios_app_installs: bool | None = None
    sip_status: str | None = None
    gatekeeper_status: str | None = None
    xprotect_version: str | None = None
    institutional_recovery_key: str | None = None
    disk_encryption_configuration: str | None = None
    filevault2_users: list[str] | None = None
    storage: list[ClassicComputerHardwareStorageDevice] | None = None
    mapped_printers: list[ClassicComputerHardwareMappedPrinter] | None = None


# Computer.Certificate Models


class ClassicComputerCertificate(BaseModel):
    """Computer nested model: computer.certificates"""

    model_config = ConfigDict(extra="allow")

    common_name: str | None = None
    identity: bool | None = None
    expires_utc: str | None = None
    expires_epoch: int | None = None
    name: str | None = None


# Computer.Security Models


class ClassicComputerSecurity(BaseModel):
    """Computer nested model: computer.security"""

    model_config = ConfigDict(extra="allow")

    activation_lock: bool | None = None
    recovery_lock_enabled: bool | None = None
    secure_boot_level: str | None = None
    external_boot_level: str | None = None
    firewall_enabled: bool | None = None


# Computer.Software Models


class ClassicComputerSoftwareAvailableUpdate(BaseModel):
    """Computer nested model: computer.software.available_updates"""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    package_name: str | None = None
    version: str | None = None


class ClassicComputerSoftwareItem(BaseModel):
    """
    Computer nested model: computer.software.applications, computer.software.fonts,
    computer.software.plugins
    """

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    path: str | None = None
    version: str | None = None
    bundle_id: str | None = None


class ClassicComputerSoftware(BaseModel):  # Lots of assumptions in this object
    """Computer nested model: computer.software"""

    model_config = ConfigDict(extra="allow")

    unix_executables: list[str] | None = None
    licensed_software: list[str] | None = None
    installed_by_casper: list[str] | None = None
    installed_by_installer_swu: list[str] | None = None
    cached_by_casper: list[str] | None = None
    available_software_updates: list[str] | None = None
    available_updates: list[ClassicComputerSoftwareAvailableUpdate] | dict | None = None
    running_services: list[str] | None = None
    applications: list[ClassicComputerSoftwareItem] | None = None
    fonts: list[ClassicComputerSoftwareItem] | None = None
    plugins: list[ClassicComputerSoftwareItem] | None = None


# Computer.ExtensionAttributes Models


class ClassicComputerExtensionAttribute(BaseModel):
    """Computer nested model: computer.extension_attributes"""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    type: str | None = None
    multi_value: bool | None = None
    value: str | None = None


# Computer GroupsAccounts Models


class ClassicComputerGroupsAccountsLocalAccount(BaseModel):
    """Computer nested model: computer.groups_accounts.local_accounts"""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    realname: str | None = None
    uid: str | None = None
    home: str | None = None
    home_size: str | None = None
    home_size_mb: int | None = None
    administrator: bool | None = None
    filevault_enabled: bool | None = None


class ClassicComputerGroupsAccountsUserInventoriesUser(BaseModel):
    """Computer nested model: computer.groups_accounts.user_inventories.user"""

    model_config = ConfigDict(extra="allow")

    username: str | None = None
    password_history_depth: str | None = None
    password_min_length: str | None = None
    password_max_age: str | None = None
    password_min_complex_characters: str | None = None
    password_require_alphanumeric: str | None = None


class ClassicComputerGroupsAccountsUserInventories(BaseModel):
    """Computer nested model: computer.groups_accounts.user_inventories

    There is a bug with this API resource!

    XML response::

        <user_inventories>
          <disable_automatic_login>true</disable_automatic_login>
          <user>...</user>
          <user>...</user>
        </user_inventories>

    JSON response::

        {
            "user_inventories": {
                "disable_automatic_login": true,
                "user": {...}
            }
        }

    Only one user is represented in a JSON response
    TODO: Accurate data can only be obtained using an XML response
    """

    model_config = ConfigDict(extra="allow")

    disable_automatic_login: bool | None = None
    user: (
        ClassicComputerGroupsAccountsUserInventoriesUser
        | list[ClassicComputerGroupsAccountsUserInventoriesUser]
        | None
    ) = None


class ClassicComputerGroupsAccounts(BaseModel):
    """Computer nested model: computer.groups_accounts"""

    model_config = ConfigDict(extra="allow")

    computer_group_memberships: list[str] | None = None
    local_accounts: list[ClassicComputerGroupsAccountsLocalAccount] | None = None
    user_inventories: ClassicComputerGroupsAccountsUserInventories | None = None


# Computer.ConfigurationProfiles Models


class ClassicComputerConfigurationProfile(BaseModel):
    """Computer nested model: computer.configuration_profiles"""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    uuid: str | None = None
    is_removable: bool | None = None


# Computer Models


class ClassicComputersItem(BaseModel):
    """
    Represents a computer record returned by the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.list_computers` operation.

    Unless the ``basic`` subset has been requested, only ``id`` and ``name`` will be
    populated.
    """

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    managed: bool | None = None
    username: str | None = None
    model: str | None = None
    department: str | None = None
    building: str | None = None
    mac_address: str | None = None
    udid: str | None = None
    serial_number: str | None = None
    report_date_utc: datetime | str | None = None
    report_date_epoch: int | None = None


class ClassicComputer(ClassicApiModel):
    """
    Represents a full computer inventory record.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``general``, ``location``, and ``extension_attributes``. To bypass this
    behavior export the model using
    :meth:`~jamfsdk.models.classic.ClassicApiModel.xml` before pasting to the API
    operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "computer"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"general", "location", "extension_attributes"}

    general: ClassicComputerGeneral | None = Field(default_factory=ClassicComputerGeneral)
    location: ClassicDeviceLocation | None = Field(default_factory=ClassicDeviceLocation)
    purchasing: ClassicDevicePurchasing | None = None
    # Peripherals are a deprecated feature of Jamf Pro
    peripherals: Any | None = None
    hardware: ClassicComputerHardware | None = None
    certificates: list[ClassicComputerCertificate] | None = None
    security: ClassicComputerSecurity | None = None
    software: ClassicComputerSoftware | None = None
    extension_attributes: list[ClassicComputerExtensionAttribute] | None = Field(
        default_factory=list
    )
    groups_accounts: ClassicComputerGroupsAccounts | None = None
    # iPhones in Computer inventory is a deprecated feature of Jamf Pro
    iphones: Any | None = None
    configuration_profiles: list[ClassicComputerConfigurationProfile] | None = None
