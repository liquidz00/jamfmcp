from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES: dict = {}


class ClassicPackageItem(BaseModel):
    """
    Represents a package record returned by the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.list_packages` operation.
    """

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None


class ClassicPackage(ClassicApiModel):
    """
    Represents a package returned by the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.get_package_by_id` operation.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, ``category``, ``filename``, ``info``, ``notes``, ``priority``,
    ``reboot_required``, ``os_requirements``, and ``install_if_reported_available``. To bypass this
    behavior export the model using :meth:`~jamfsdk.models.classic.ClassicApiModel.xml` before
    pasting to the API operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "package"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {
        "name",
        "category",
        "filename",
        "info",
        "notes",
        "priority",
        "reboot_required",
        "os_requirements",
        "install_if_reported_available",
    }

    id: int | None = None
    name: str | None = None
    category: str | None = None
    filename: str | None = None
    info: str | None = None
    notes: str | None = None
    priority: int | None = None
    reboot_required: bool | None = None
    fill_user_template: bool | None = None
    fill_existing_users: bool | None = None
    allow_uninstalled: bool | None = None
    os_requirements: str | None = None
    required_processor: str | None = None
    hash_type: str | None = None
    hash_value: str | None = None
    switch_with_package: str | None = None
    install_if_reported_available: bool | None = None
    reinstall_option: str | None = None
    triggering_files: dict | str | None = None
    send_notification: bool | None = None
