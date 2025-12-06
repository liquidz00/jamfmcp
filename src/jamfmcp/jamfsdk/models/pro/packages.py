from pydantic import ConfigDict

from .. import BaseModel


class Package(BaseModel):
    """Represents a full package record."""

    model_config = ConfigDict(extra="allow")

    id: str | None
    packageName: str
    fileName: str
    categoryId: str
    info: str | None
    notes: str | None
    priority: int
    osRequirements: str | None
    fillUserTemplate: bool
    indexed: bool
    fillExistingUsers: bool
    swu: bool
    rebootRequired: bool
    selfHealNotify: bool
    selfHealingAction: str | None
    osInstall: bool
    serialNumber: str | None
    parentPackageId: str | None
    basePath: str | None
    suppressUpdates: bool
    cloudTransferStatus: str
    ignoreConflicts: bool
    suppressFromDock: bool
    suppressEula: bool
    suppressRegistration: bool
    installLanguage: str | None
    md5: str | None
    sha256: str | None
    hashType: str | None
    hashValue: str | None
    size: str | None
    osInstallerVersion: str | None
    manifest: str | None
    manifestFileName: str | None
    format: str | None
