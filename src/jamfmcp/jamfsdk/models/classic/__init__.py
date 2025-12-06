from datetime import datetime
from typing import Any, Iterable

import dicttoxml
from pydantic import ConfigDict

from .. import BaseModel


def convert_datetime_to_jamf_iso(dt: datetime) -> str:
    """
    Classic API deviates from the published Jamf API Style Guide:
    https://developer.jamf.com/developer-guide/docs/api-style-guide#date--time-format
    """
    if not dt.tzinfo:
        raise ValueError("Datetime object must have timezone information")

    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + dt.strftime("%z")


def remove_fields(data: Any, values_to_remove: Iterable = None):
    """
    For use with the .xml() method of the `ClassicApiModel`.

    When constructing resources using models and some default sub-models are instantiated
    for ease of developer use. Upon export to XML, any empty objects and arrays are removed
    to prevent overwriting existing data in the API.
    """
    if not values_to_remove:
        values_to_remove = [{}, []]

    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if v in values_to_remove:
                continue
            elif isinstance(v, dict):
                v = remove_fields(v, values_to_remove)
            elif isinstance(v, list):
                new_v = []
                for i in v:
                    print("Array item: ", i)
                    if new_i := remove_fields(i, values_to_remove):
                        new_v.append(new_i)
                v = new_v

            new_data[k] = v
        return new_data

    elif data not in values_to_remove:
        return data


class ClassicApiModel(BaseModel):
    """The base model used for Classic API models."""

    model_config = ConfigDict(extra="allow", json_encoders={datetime: convert_datetime_to_jamf_iso})

    _xml_root_name: str
    _xml_array_item_names: dict[str, str]
    _xml_write_fields: set[str] | None = None

    def xml(self, exclude_none: bool = True, exclude_read_only: bool = False) -> str:
        """
        Generate a Jamf Pro XML representation of the model.

        :param exclude_none: Any field with a value of ``None`` is not included.
        :type exclude_none: bool

        :param exclude_read_only: If write field names are set, only include those.
        :type exclude_read_only: bool

        :return: XML string
        :rtype: str
        """
        data = remove_fields(
            self.model_dump(
                include=self._xml_write_fields if exclude_read_only else None,
                exclude_none=exclude_none,
            )
        )

        return dicttoxml.dicttoxml(
            data,
            custom_root=self._xml_root_name,
            attr_type=False,
            item_func=self._xml_array_item_names.get,
            return_bytes=False,
        )


class ClassicDeviceLocation(BaseModel):
    """Device user assignment information."""

    model_config = ConfigDict(extra="allow")

    username: str | None = None
    realname: str | None = None
    real_name: str | None = None
    email_address: str | None = None
    position: str | None = None
    phone: str | None = None
    phone_number: str | None = None
    department: str | None = None
    building: str | None = None
    room: str | None = None


class ClassicDevicePurchasing(BaseModel):
    """Device purchase information (normally populated by GSX)."""

    model_config = ConfigDict(extra="allow")

    is_purchased: bool | None = None
    is_leased: bool | None = None
    po_number: str | None = None
    vendor: str | None = None
    applecare_id: str | None = None
    purchase_price: str | None = None
    purchasing_account: str | None = None
    po_date: str | None = None
    po_date_epoch: int | None = None
    po_date_utc: str | None = None
    warranty_expires: str | None = None
    warranty_expires_epoch: int | None = None
    warranty_expires_utc: str | None = None
    lease_expires: str | None = None
    lease_expires_epoch: int | None = None
    lease_expires_utc: str | None = None
    life_expectancy: int | None = None
    purchasing_contact: str | None = None
    os_applecare_id: str | None = None
    os_maintenance_expires: str | None = None
    attachments: list | None = None  # Deprecated?


class ClassicSite(BaseModel):
    """Site assignment information."""

    id: int | None = None
    name: str | None = None
