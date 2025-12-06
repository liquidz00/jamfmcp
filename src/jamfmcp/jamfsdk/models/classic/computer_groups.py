from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel, ClassicSite
from .criteria import ClassicCriterion

_XML_ARRAY_ITEM_NAMES = {
    "criteria": "criterion",
    "computers": "computer",
    "computer_additions": "computer",
    "computer_deletions": "computer",
}


# class ClassicComputerGroupsItem(BaseModel, extra=Extra.allow):
#     """Represents a computer group record returned by the
#     :meth:`~jamfsdk.clients.classic_api.ClassicApi.list_computer_groups` operation.
#     """
#
#     id: int
#     name: str
#     is_smart: bool


class ClassicComputerGroupMember(BaseModel):
    """
    ComputerGroup nested model: computer_group.computers,
    computer_group.computer_additions, computer_group.computer_deletions
    """

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    mac_address: str | None = None
    alt_mac_address: str | None = None
    serial_number: str | None = None


class ClassicComputerGroup(ClassicApiModel):
    """
    Represents a computer group record returned by the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.list_computer_groups` and
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.get_computer_group_by_id`
    operations.

    When returned by ``list_computer_groups`` only ``id``, ``name`` and ``is_smart`` will
    be populated.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, ``is_smart``, ``site``, and ``criteria``. To bypass this behavior
    export the model using
    :meth:`~jamfsdk.models.classic.ClassicApiModel.xml` before pasting to the API
    operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "computer_group"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name", "is_smart", "site", "criteria"}

    id: int | None = None
    name: str | None = None
    is_smart: bool | None = None
    site: ClassicSite | None = None
    criteria: list[ClassicCriterion] | None = None
    computers: list[ClassicComputerGroupMember] | None = None


class ClassicComputerGroupMembershipUpdate(ClassicApiModel):
    """
    Represents a computer group membership update. This model is generated as a part of the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.update_static_computer_group_membership_by_id`
    operation.
    """

    _xml_root_name = "computer_group"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES

    computer_additions: list[ClassicComputerGroupMember] | None = None
    computer_deletions: list[ClassicComputerGroupMember] | None = None
