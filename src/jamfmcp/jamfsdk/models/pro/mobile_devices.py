from datetime import datetime
from enum import Enum

from pydantic import ConfigDict

from .. import BaseModel


class MobileDeviceType(str, Enum):
    """Not in use: the value of this attribute can be an undocumented state."""

    iOS = "iOS"
    tvOS = "tvOS"


class MobileDeviceExtensionAttributeType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DATE = "DATE"


class MobileDeviceExtensionAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    type: MobileDeviceExtensionAttributeType | None = None
    value: list[str] | None = None
    extensionAttributeCollectionAllowed: bool | None = None
    inventoryDisplay: str | None = None


class MobileDeviceHardware(BaseModel):
    model_config = ConfigDict(extra="allow")

    capacityMb: int | None = None
    availableSpaceMb: int | None = None
    usedSpacePercentage: int | None = None
    batteryLevel: int | None = None
    serialNumber: str | None = None
    wifiMacAddress: str | None = None
    bluetoothMacAddress: str | None = None
    modemFirmwareVersion: str | None = None
    model: str | None = None
    modelIdentifier: str | None = None
    modelNumber: str | None = None
    bluetoothLowEnergyCapable: bool | None = None
    deviceId: str | None = None
    extensionAttributes: list[MobileDeviceExtensionAttribute] | None = None


class MobileDeviceUserAndLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    username: str | None = None
    realName: str | None = None
    emailAddress: str | None = None
    position: str | None = None
    phoneNumber: str | None = None
    departmentId: str | None = None
    buildingId: str | None = None
    room: str | None = None
    building: str | None = None
    department: str | None = None
    extensionAttributes: list[MobileDeviceExtensionAttribute] | None = None


class MobileDevicePurchasing(BaseModel):
    model_config = ConfigDict(extra="allow")

    purchased: bool | None = None
    leased: bool | None = None
    poNumber: str | None = None
    vendor: str | None = None
    appleCareId: str | None = None
    purchasePrice: str | None = None
    purchasingAccount: str | None = None
    poDate: datetime | None = None
    warrantyExpiresDate: datetime | None = None
    leaseExpiresDate: datetime | None = None
    lifeExpectancy: int | None = None
    purchasingContact: str | None = None
    extensionAttributes: list[MobileDeviceExtensionAttribute] | None = None


class MobileDeviceApplication(BaseModel):
    model_config = ConfigDict(extra="allow")

    identifier: str | None = None
    name: str | None = None
    version: str | None = None
    shortVersion: str | None = None
    managementStatus: str | None = None
    validationStatus: bool | None = None
    bundleSize: str | None = None
    dynamicSize: str | None = None


class MobileDeviceCertificate(BaseModel):
    model_config = ConfigDict(extra="allow")

    commonName: str | None = None
    identity: bool | None = None
    expirationDate: datetime | None = None


class MobileDeviceProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    displayName: str | None = None
    version: str | None = None
    uuid: str | None = None
    identifier: str | None = None
    removable: bool | None = None
    lastInstalled: datetime | None = None


class MobileDeviceUserProfile(MobileDeviceProfile):
    """Extends :class:`~jamfsdk.models.pro.mobile_devices.MobileDeviceProfile`."""

    model_config = ConfigDict(extra="allow")

    username: str | None = None


class MobileDeviceOwnershipType(str, Enum):
    Institutional = "Institutional"
    PersonalDeviceProfile = "PersonalDeviceProfile"
    UserEnrollment = "UserEnrollment"
    AccountDrivenUserEnrollment = "AccountDrivenUserEnrollment"
    AccountDrivenDeviceEnrollment = "AccountDrivenDeviceEnrollment"


class MobileDeviceEnrollmentMethodPrestage(BaseModel):
    model_config = ConfigDict(extra="allow")

    mobileDevicePrestageId: str | None = None
    profileName: str | None = None


class MobileDeviceGeneral(BaseModel):
    model_config = ConfigDict(extra="allow")

    udid: str | None = None
    displayName: str | None = None
    assetTag: str | None = None
    siteId: str | None = None
    lastInventoryUpdateDate: datetime | None = None
    osVersion: str | None = None
    osRapidSecurityResponse: str | None = None
    osBuild: str | None = None
    osSupplementalBuildVersion: str | None = None
    softwareUpdateDeviceId: str | None = None
    ipAddress: str | None = None
    managed: bool | None = None
    supervised: bool | None = None
    deviceOwnershipType: MobileDeviceOwnershipType | None = None
    enrollmentMethodPrestage: MobileDeviceEnrollmentMethodPrestage | None = None
    enrollmentSessionTokenValid: bool | None = None
    lastEnrolledDate: datetime | None = None
    mdmProfileExpirationDate: datetime | None = None
    timeZone: str | None = None
    declarativeDeviceManagementEnabled: bool | None = None
    extensionAttributes: list[MobileDeviceExtensionAttribute] | None = None
    airPlayPassword: str | None = None
    locales: str | None = None
    languages: str | None = None


class MobileDeviceSecurityLostModeLocation(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    lastLocationUpdate: datetime | None = None
    lostModeLocationHorizontalAccuracyMeters: int | None = None
    lostModeLocationVerticalAccuracyMeters: int | None = None
    lostModeLocationAltitudeMeters: int | None = None
    lostModeLocationSpeedMetersPerSecond: int | None = None
    lostModeLocationCourseDegrees: int | None = None
    lostModeLocationTimestamp: str | None = None


class MobileDeviceSecurity(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    dataProtected: bool | None = None
    blockLevelEncryptionCapable: bool | None = None
    fileLevelEncryptionCapable: bool | None = None
    passcodePresent: bool | None = None
    passcodeCompliant: bool | None = None
    passcodeCompliantWithProfile: bool | None = None
    hardwareEncryption: int | None = None
    activationLockEnabled: bool | None = None
    jailBreakDetected: bool | None = None
    passcodeLockGracePeriodEnforcedSeconds: int | None = None
    personalDeviceProfileCurrent: bool | None = None
    lostModeEnabled: bool | None = None
    lostModePersistent: bool | None = None
    lostModeMessage: str | None = None
    lostModePhoneNumber: str | None = None
    lostModeFootnote: str | None = None
    lostModeLocation: MobileDeviceSecurityLostModeLocation | None = None


class MobileDeviceEbook(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    author: str | None = None
    title: str | None = None
    version: str | None = None
    kind: str | None = None
    managementState: str | None = None


class MobileDeviceNetwork(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    cellularTechnology: str | None = None
    voiceRoamingEnabled: bool | None = None
    imei: str | None = None
    iccid: str | None = None
    meid: str | None = None
    eid: str | None = None
    carrierSettingsVersion: str | None = None
    currentCarrierNetwork: str | None = None
    currentMobileCountryCode: str | None = None
    currentMobileNetworkCode: str | None = None
    homeCarrierNetwork: str | None = None
    homeMobileCountryCode: str | None = None
    homeMobileNetworkCode: str | None = None
    dataRoamingEnabled: bool | None = None
    roaming: bool | None = None
    personalHotspotEnabled: bool | None = None
    phoneNumber: str | None = None


class MobileDeviceServiceSubscription(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    carrierSettingsVersion: str | None = None
    currentCarrierNetwork: str | None = None
    currentMobileCountryCode: str | None = None
    currentMobileNetworkCode: str | None = None
    subscriberCarrierNetwork: str | None = None
    eid: str | None = None
    iccid: str | None = None
    imei: str | None = None
    dataPreferred: bool | None = None
    roaming: bool | None = None
    voicePreferred: bool | None = None
    label: str | None = None
    labelId: str | None = None
    meid: str | None = None
    phoneNumber: str | None = None
    slot: str | None = None


class ProvisioningProfile(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    displayName: str | None = None
    uuid: str | None = None
    expirationDate: datetime | None = None


class SharedUser(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    managedAppleId: str | None = None
    loggedIn: bool | None = None
    dataToSync: bool | None = None


class MobileDevice(BaseModel):
    """Represents a full mobile device inventory record."""

    model_config = ConfigDict(extra="allow")

    mobileDeviceId: str | None = None
    deviceType: str | None = None
    hardware: MobileDeviceHardware | None = None
    userAndLocation: MobileDeviceUserAndLocation | None = None
    purchasing: MobileDevicePurchasing | None = None
    applications: list[MobileDeviceApplication] | None = None
    certificates: list[MobileDeviceCertificate] | None = None
    profiles: list[MobileDeviceProfile] | None = None
    userProfiles: list[MobileDeviceUserProfile] | None = None
    extensionAttributes: list[MobileDeviceExtensionAttribute] | None = None
    general: MobileDeviceGeneral | None = None
    security: MobileDeviceSecurity | None = None
    ebooks: list[MobileDeviceEbook] | None = None
    network: MobileDeviceNetwork | None = None
    serviceSubscriptions: list[MobileDeviceServiceSubscription] | None = None
    provisioningProfiles: list[ProvisioningProfile] | None = None
    sharedUsers: list[SharedUser] | None = None
