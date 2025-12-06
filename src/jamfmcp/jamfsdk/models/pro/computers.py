from datetime import date, datetime  # date in models: 2019-01-01
from enum import Enum

from pydantic import ConfigDict, Field

from .. import BaseModel
from . import V1Site

# Computer Extension Attribute Models


class ComputerExtensionAttributeDataType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DATE_TIME = "DATE_TIME"


class ComputerExtensionAttributeInputType(str, Enum):
    TEXT = "TEXT"
    POPUP = "POPUP"
    SCRIPT = "SCRIPT"
    LDAP = "LDAP"


class ComputerExtensionAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")

    definitionId: str | None = None
    name: str | None = None
    description: str | None = None
    enabled: bool | None = None
    multiValue: bool | None = None
    values: list[str] | None = None
    dataType: ComputerExtensionAttributeDataType | None = None
    options: list[str] | None = None
    inputType: ComputerExtensionAttributeInputType | None = None


# Computer General Models


class ComputerRemoteManagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    managed: bool | None = None
    managementUsername: str | None = None
    managementPassword: str | None = None


class ComputerMdmCapability(BaseModel):
    model_config = ConfigDict(extra="allow")

    capable: bool | None = None
    capableUsers: list[str] | None = None


class EnrollmentMethod(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    objectName: str | None = None
    objectType: str | None = None


class ComputerGeneral(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    lastIpAddress: str | None = None
    lastReportedIp: str | None = None
    jamfBinaryVersion: str | None = None
    platform: str | None = None
    barcode1: str | None = None
    barcode2: str | None = None
    assetTag: str | None = None
    remoteManagement: ComputerRemoteManagement | None = Field(
        default_factory=ComputerRemoteManagement
    )
    supervised: bool | None = None
    mdmCapable: ComputerMdmCapability | None = None
    reportDate: datetime | None = None
    lastContactTime: datetime | None = None
    lastCloudBackupDate: datetime | None = None
    lastEnrolledDate: datetime | None = None
    mdmProfileExpiration: datetime | None = None
    initialEntryDate: date | None = None  # 2018-10-31
    distributionPoint: str | None = None
    enrollmentMethod: EnrollmentMethod | None = None
    site: V1Site | None = Field(default_factory=V1Site)
    itunesStoreAccountActive: bool | None = None
    enrolledViaAutomatedDeviceEnrollment: bool | None = None
    userApprovedMdm: bool | None = None
    declarativeDeviceManagementEnabled: bool | None = None
    extensionAttributes: list[ComputerExtensionAttribute] | None = None
    managementId: str | None = None


# Computer Disk Encryption Models


class ComputerPartitionFileVault2State(str, Enum):
    UNKNOWN = "UNKNOWN"
    UNENCRYPTED = "UNENCRYPTED"
    INELIGIBLE = "INELIGIBLE"
    DECRYPTED = "DECRYPTED"
    DECRYPTING = "DECRYPTING"
    ENCRYPTED = "ENCRYPTED"
    ENCRYPTING = "ENCRYPTING"
    RESTART_NEEDED = "RESTART_NEEDED"
    OPTIMIZING = "OPTIMIZING"
    DECRYPTING_PAUSED = "DECRYPTING_PAUSED"
    ENCRYPTING_PAUSED = "ENCRYPTING_PAUSED"


class IndividualRecoveryKeyValidityStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ComputerPartitionEncryption(BaseModel):
    model_config = ConfigDict(extra="allow")

    partitionName: str | None = None
    partitionFileVault2State: ComputerPartitionFileVault2State | None = None
    partitionFileVault2Percent: int | None = None


class ComputerDiskEncryption(BaseModel):
    model_config = ConfigDict(extra="allow")

    bootPartitionEncryptionDetails: ComputerPartitionEncryption | None = None
    individualRecoveryKeyValidityStatus: IndividualRecoveryKeyValidityStatus | None = None
    institutionalRecoveryKeyPresent: bool | None = None
    diskEncryptionConfigurationName: str | None = None
    fileVault2EnabledUserNames: list[str] | None = None
    fileVault2EligibilityMessage: str | None = None


# Computer Purchase Model


class ComputerPurchase(BaseModel):
    model_config = ConfigDict(extra="allow")

    leased: bool | None = None
    purchased: bool | None = None
    poNumber: str | None = None
    poDate: date | None = None
    vendor: str | None = None
    warrantyDate: date | None = None
    appleCareId: str | None = None
    leaseDate: date | None = None
    purchasePrice: str | None = None
    lifeExpectancy: int | None = None
    purchasingAccount: str | None = None
    purchasingContact: str | None = None
    extensionAttributes: list[ComputerExtensionAttribute] | None = None


# Computer Application Model


class ComputerApplication(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    path: str | None = None
    version: str | None = None
    macAppStore: bool | None = None
    sizeMegabytes: int | None = None
    bundleId: str | None = None
    updateAvailable: bool | None = None
    externalVersionId: str | None = None


# Computer Storage Models


class PartitionType(str, Enum):
    BOOT = "BOOT"
    RECOVERY = "RECOVERY"
    OTHER = "OTHER"


class ComputerPartition(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    sizeMegabytes: int | None = None
    availableMegabytes: int | None = None
    partitionType: PartitionType | None = None
    percentUsed: int | None = None
    fileVault2State: ComputerPartitionFileVault2State | None = None
    fileVault2ProgressPercent: int | None = None
    lvmManaged: bool | None = None


class ComputerDisk(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    device: str | None = None
    model: str | None = None
    revision: str | None = None
    serialNumber: str | None = None
    sizeMegabytes: int | None = None
    smartStatus: str | None = None
    type: str | None = None
    partitions: list[ComputerPartition] | None = None


class ComputerStorage(BaseModel):
    model_config = ConfigDict(extra="allow")

    bootDriveAvailableSpaceMegabytes: int | None = None
    disks: list[ComputerDisk] | None = None


# Computer User and Location Model


class ComputerUserAndLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    username: str | None = None
    realname: str | None = None
    email: str | None = None
    position: str | None = None
    phone: str | None = None
    departmentId: str | None = None
    buildingId: str | None = None
    room: str | None = None
    extensionAttributes: list[ComputerExtensionAttribute] | None = None


# Computer Configuration Profile Model


class ComputerConfigurationProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    username: str | None = None
    lastInstalled: datetime | None = None
    removable: bool | None = None
    displayName: str | None = None
    profileIdentifier: str | None = None


# Computer Printer Model


class ComputerPrinter(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    type: str | None = None
    uri: str | None = None
    location: str | None = None


# Computer Service Model


class ComputerService(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None


# Computer Hardware Models


class ComputerHardware(BaseModel):
    model_config = ConfigDict(extra="allow")

    make: str | None = None
    model: str | None = None
    modelIdentifier: str | None = None
    serialNumber: str | None = None
    processorSpeedMhz: int | None = None
    processorCount: int | None = None
    coreCount: int | None = None
    processorType: str | None = None
    processorArchitecture: str | None = None
    busSpeedMhz: int | None = None
    cacheSizeKilobytes: int | None = None
    networkAdapterType: str | None = None
    macAddress: str | None = None
    altNetworkAdapterType: str | None = None
    altMacAddress: str | None = None
    totalRamMegabytes: int | None = None
    openRamSlots: int | None = None
    batteryCapacityPercent: int | None = None
    smcVersion: str | None = None
    nicSpeed: str | None = None
    opticalDrive: str | None = None
    bootRom: str | None = None
    bleCapable: bool | None = None
    supportsIosAppInstalls: bool | None = None
    appleSilicon: bool | None = None
    extensionAttributes: list[ComputerExtensionAttribute] | None = None


# Computer Local User Account Models


class UserAccountType(str, Enum):
    LOCAL = "LOCAL"
    MOBILE = "MOBILE"
    UNKNOWN = "UNKNOWN"


class AzureActiveDirectoryId(str, Enum):
    ACTIVATED = "ACTIVATED"
    DEACTIVATED = "DEACTIVATED"
    UNRESPONSIVE = "UNRESPONSIVE"
    UNKNOWN = "UNKNOWN"


class ComputerLocalUserAccount(BaseModel):
    model_config = ConfigDict(extra="allow")

    uid: str | None = None
    username: str | None = None
    fullName: str | None = None
    admin: bool | None = None
    homeDirectory: str | None = None
    homeDirectorySizeMb: int | None = None
    fileVault2Enabled: bool | None = None
    userAccountType: UserAccountType | None = None
    passwordMinLength: int | None = None
    passwordMaxAge: int | None = None
    passwordMinComplexCharacters: int | None = None
    passwordHistoryDepth: int | None = None
    passwordRequireAlphanumeric: bool | None = None
    computerAzureActiveDirectoryId: str | None = None
    userAzureActiveDirectoryId: str | None = None
    azureActiveDirectoryId: AzureActiveDirectoryId | None = None


# Computer Certificate Models


class LifecycleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CertificateStatus(str, Enum):
    EXPIRING = "EXPIRING"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    PENDING_REVOKE = "PENDING_REVOKE"
    ISSUED = "ISSUED"


class ComputerCertificate(BaseModel):
    model_config = ConfigDict(extra="allow")

    commonName: str | None = None
    identity: bool | None = None
    expirationDate: datetime | None = None
    username: str | None = None
    lifecycleStatus: LifecycleStatus | None = None
    certificateStatus: CertificateStatus | None = None
    subjectName: str | None = None
    serialNumber: str | None = None
    sha1Fingerprint: str | None = None
    issuedDate: str | None = None


# Computer Attachment Model


class ComputerAttachment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    fileType: str | None = None
    sizeBytes: int | None = None


# Computer Plugin Model


class ComputerPlugin(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    version: str | None = None
    path: str | None = None


# Computer Package Receipt Model


class ComputerPackageReceipts(BaseModel):
    model_config = ConfigDict(extra="allow")

    installedByJamfPro: list[str] | None = None
    installedByInstallerSwu: list[str] | None = None
    cached: list[str] | None = None


# Computer Font Model


class ComputerFont(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    version: str | None = None
    path: str | None = None


# Computer Security Models


class SipStatus(str, Enum):
    NOT_COLLECTED = "NOT_COLLECTED"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class GatekeeperStatus(str, Enum):
    NOT_COLLECTED = "NOT_COLLECTED"
    DISABLED = "DISABLED"
    APP_STORE_AND_IDENTIFIED_DEVELOPERS = "APP_STORE_AND_IDENTIFIED_DEVELOPERS"
    APP_STORE = "APP_STORE"


class SecureBootLevel(str, Enum):
    NO_SECURITY = "NO_SECURITY"
    MEDIUM_SECURITY = "MEDIUM_SECURITY"
    FULL_SECURITY = "FULL_SECURITY"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    UNKNOWN = "UNKNOWN"


class ExternalBootLevel(str, Enum):
    ALLOW_BOOTING_FROM_EXTERNAL_MEDIA = "ALLOW_BOOTING_FROM_EXTERNAL_MEDIA"
    DISALLOW_BOOTING_FROM_EXTERNAL_MEDIA = "DISALLOW_BOOTING_FROM_EXTERNAL_MEDIA"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    UNKNOWN = "UNKNOWN"


class ComputerSecurity(BaseModel):
    model_config = ConfigDict(extra="allow")

    sipStatus: SipStatus | None = None
    gatekeeperStatus: GatekeeperStatus | None = None
    xprotectVersion: str | None = None
    autoLoginDisabled: bool | None = None
    remoteDesktopEnabled: bool | None = None
    activationLockEnabled: bool | None = None
    recoveryLockEnabled: bool | None = None
    firewallEnabled: bool | None = None
    secureBootLevel: SecureBootLevel | None = None
    externalBootLevel: ExternalBootLevel | None = None
    bootstrapTokenAllowed: bool | None = None


# Computer Operating System Models


class FileVault2Status(str, Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_ENCRYPTED = "NOT_ENCRYPTED"
    BOOT_ENCRYPTED = "BOOT_ENCRYPTED"
    SOME_ENCRYPTED = "SOME_ENCRYPTED"
    ALL_ENCRYPTED = "ALL_ENCRYPTED"


class ComputerOperatingSystem(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    version: str | None = None
    build: str | None = None
    activeDirectoryStatus: str | None = None
    fileVault2Status: FileVault2Status | None = None
    softwareUpdateDeviceId: str | None = None
    extensionAttributes: list[ComputerExtensionAttribute] | None = None


# Computer Licensed Software Model


class ComputerLicensedSoftware(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None


# Computer iBeacon Model


class ComputeriBeacon(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None


# Computer Software Update Model


class ComputerSoftwareUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    version: str | None = None
    packageName: str | None = None


# Computer Content Caching Models


class ComputerContentCachingParentAlert(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentAlertId: str | None = None
    addresses: list[str] | None = None
    className: str | None = None
    postDate: datetime | None = None


class ComputerContentCachingParentCapabilities(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentCapabilitiesId: str | None = None
    imports: bool | None = None
    namespaces: bool | None = None
    personalContent: bool | None = None
    queryParameters: bool | None = None
    sharedContent: bool | None = None
    prioritization: bool | None = None


class ComputerContentCachingParentLocalNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentLocalNetworkId: str | None = None
    speed: int | None = None
    wired: bool | None = None


class ComputerContentCachingParentDetails(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentDetailsId: str | None = None
    acPower: bool | None = None
    cacheSizeBytes: int | None = None
    capabilities: ComputerContentCachingParentCapabilities | None = None
    portable: bool | None = None
    localNetwork: list[ComputerContentCachingParentLocalNetwork] | None = None


class ComputerContentCachingParent(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentId: str | None = None
    address: str | None = None
    alerts: ComputerContentCachingParentAlert | None = None
    details: ComputerContentCachingParentDetails | None = None
    guid: str | None = None
    healthy: bool | None = None
    port: int | None = None
    version: str | None = None


class ComputerContentCachingAlert(BaseModel):
    model_config = ConfigDict(extra="allow")

    cacheBytesLimit: int | None = None
    className: str | None = None
    pathPreventingAccess: str | None = None
    postDate: datetime | None = None
    reservedVolumeBytes: int | None = None
    resource: str | None = None


class ComputerContentCachingCacheDetail(BaseModel):
    model_config = ConfigDict(extra="allow")

    computerContentCachingCacheDetailsId: str | None = None
    categoryName: str | None = None
    diskSpaceBytesUsed: int | None = None


class ComputerContentCachingDataMigrationErrorUserInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    key: str | None = None
    value: str | None = None


class ComputerContentCachingDataMigrationError(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: int | None = None
    domain: str | None = None
    userInfo: list[ComputerContentCachingDataMigrationErrorUserInfo] | None = None


class ComputerContentCachingRegistrationStatus(str, Enum):
    CONTENT_CACHING_FAILED = "CONTENT_CACHING_FAILED"
    CONTENT_CACHING_PENDING = "CONTENT_CACHING_PENDING"
    CONTENT_CACHING_SUCCEEDED = "CONTENT_CACHING_SUCCEEDED"


class ComputerContentCachingTetheratorStatus(str, Enum):
    CONTENT_CACHING_UNKNOWN = "CONTENT_CACHING_UNKNOWN"
    CONTENT_CACHING_DISABLED = "CONTENT_CACHING_DISABLED"
    CONTENT_CACHING_ENABLED = "CONTENT_CACHING_ENABLED"


class ComputerContentCaching(BaseModel):
    model_config = ConfigDict(extra="allow")

    computerContentCachingInformationId: str | None = None
    parents: list[ComputerContentCachingParent] | None = None
    alerts: list[ComputerContentCachingAlert] | None = None
    activated: bool | None = None
    active: bool | None = None
    actualCacheBytesUsed: int | None = None
    cacheDetails: list[ComputerContentCachingCacheDetail] | None = None
    cacheBytesFree: int | None = None
    cacheBytesLimit: int | None = None
    cacheStatus: str | None = None
    cacheBytesUsed: int | None = None
    dataMigrationCompleted: bool | None = None
    dataMigrationProgressPercentage: int | None = None
    dataMigrationError: ComputerContentCachingDataMigrationError | None = None
    maxCachePressureLast1HourPercentage: int | None = None
    personalCacheBytesFree: int | None = None
    personalCacheBytesLimit: int | None = None
    personalCacheBytesUsed: int | None = None
    port: int | None = None
    publicAddress: str | None = None
    registrationError: str | None = None
    registrationResponseCode: int | None = None
    registrationStarted: datetime | None = None
    registrationStatus: ComputerContentCachingRegistrationStatus | None = None
    restrictedMedia: bool | None = None
    serverGuid: str | None = None
    startupStatus: str | None = None
    tetheratorStatus: ComputerContentCachingTetheratorStatus | None = None
    totalBytesAreSince: datetime | None = None
    totalBytesDropped: int | None = None
    totalBytesImported: int | None = None
    totalBytesReturnedToChildren: int | None = None
    totalBytesReturnedToClients: int | None = None
    totalBytesReturnedToPeers: int | None = None
    totalBytesStoredFromOrigin: int | None = None
    totalBytesStoredFromParents: int | None = None
    totalBytesStoredFromPeers: int | None = None


# Computer Group Membership Model


class ComputerGroupMembership(BaseModel):
    model_config = ConfigDict(extra="allow")

    groupId: str | None = None
    groupName: str | None = None
    smartGroup: bool | None = None


# Computer Inventory Model


class Computer(BaseModel):
    """Represents a full computer inventory record."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    udid: str | None = None
    general: ComputerGeneral | None = Field(default_factory=ComputerGeneral)
    diskEncryption: ComputerDiskEncryption | None = None
    purchasing: ComputerPurchase | None = None
    applications: list[ComputerApplication] | None = None
    storage: ComputerStorage | None = None
    userAndLocation: ComputerUserAndLocation | None = Field(default_factory=ComputerUserAndLocation)
    configurationProfiles: list[ComputerConfigurationProfile] | None = None
    printers: list[ComputerPrinter] | None = None
    services: list[ComputerService] | None = None
    hardware: ComputerHardware | None = None
    localUserAccounts: list[ComputerLocalUserAccount] | None = None
    certificates: list[ComputerCertificate] | None = None
    attachments: list[ComputerAttachment] | None = None
    plugins: list[ComputerPlugin] | None = None
    packageReceipts: ComputerPackageReceipts | None = None
    fonts: list[ComputerFont] | None = None
    security: ComputerSecurity | None = None
    operatingSystem: ComputerOperatingSystem | None = None
    licensedSoftware: list[ComputerLicensedSoftware] | None = None
    ibeacons: list[ComputeriBeacon] | None = None
    softwareUpdates: list[ComputerSoftwareUpdate] | None = None
    extensionAttributes: list[ComputerExtensionAttribute] | None = None
    contentCaching: ComputerContentCaching | None = None
    groupMemberships: list[ComputerGroupMembership] | None = None
