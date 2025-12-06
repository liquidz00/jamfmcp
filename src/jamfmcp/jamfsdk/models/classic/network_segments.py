from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {}


class ClassicNetworkSegmentItem(BaseModel):
    """
    Represents a network_segment record returned by the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.list_network_segments` operation.
    """

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    name: str | None = None
    starting_address: str | None = None
    ending_address: str | None = None


class ClassicNetworkSegment(ClassicApiModel):
    """
    Represents a network_segment record returned by the
    :meth:`~jamfsdk.clients.classic_api.ClassicApi.get_network_segment_by_id` operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "network_segment"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {
        "name",
        "starting_address",
        "ending_address",
        "distribution_server",
        "distribution_point",
        "url",
        "swu_server",
        "building",
        "department",
        "override_buildings",
        "override_departments",
    }

    id: int | None = None
    name: str | None = None
    starting_address: str | None = None
    ending_address: str | None = None
    distribution_server: str | None = None
    distribution_point: str | None = None
    url: str | None = None
    swu_server: str | None = None
    building: str | None = None
    department: str | None = None
    override_buildings: bool | None = None
    override_departments: bool | None = None
