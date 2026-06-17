from typing import Annotated, Any, Literal

from pydantic import BaseModel as PydanticBaseModel
from pydantic import (
    BeforeValidator,
    ConfigDict,
    PlainSerializer,
    SerializerFunctionWrapHandler,
    WrapSerializer,
)

PERMISSIONS = (
    (0, "no_access"),
    (16, "can_use"),
    (32, "can_execute"),
    (64, "can_edit"),
    (128, "owner"),
)
ROLES = (
    (0, "read-only"),
    (16, "basic"),
    (24, "scan_operator"),
    (32, "standard"),
    (40, "scan_manager"),
    (64, "administrator"),
    (128, "site_administrator"),
)


def ser_perm_str_to_int(value: str, handler: SerializerFunctionWrapHandler) -> int:
    """Converts the string annotation of a permission to it's integer id"""
    value = handler(value)
    for id, name in PERMISSIONS:
        if value == name:
            return id
    raise ValueError(f"{value} is not a valid permission label")


def val_perm_int_to_str(value: Any) -> Any:
    """Attempts to convert the string annotation of a permission to it's label"""
    if isinstance(value, int):
        for id, name in PERMISSIONS:
            if value == id:
                return name
        raise ValueError(f"{value} is not a valid permission id")
    return value


def ser_role_str_to_int(value: str, handler: SerializerFunctionWrapHandler) -> int:
    """Converts the string annotation of a permission to it's integer id"""
    value = handler(value)
    for id, name in ROLES:
        if value == name:
            return id
    raise ValueError(f"{value} is not a valid role label")


def val_role_int_to_str(value: Any) -> Any:
    """Attempts to convert the string annotation of a permission to it's label"""
    if isinstance(value, int):
        for id, name in ROLES:
            if value == id:
                return name
        raise ValueError(f"{value} is not a valid role id")
    return value


def val_str_to_list(value: Any) -> Any:
    """Attempts to convert a comma-separated string into a list of strings"""
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v != ""]
    elif value is None:
        return []
    return value


def ser_list_to_str(value: list[str], handler: SerializerFunctionWrapHandler) -> str:
    """Attempts to convert a list into a comma-separated string"""
    return ",".join(handler(value))


Permission = Annotated[
    Literal["no_access", "can_use", "can_execute", "can_edit", "owner"],
    BeforeValidator(val_perm_int_to_str),
    WrapSerializer(ser_perm_str_to_int),
]
""" Annotated Permission field to handle id/label conversions """

Role = Annotated[
    Literal[
        "read-only",
        "basic",
        "scan_operator",
        "standard",
        "scan_manager",
        "administrator",
        "site_administrator",
    ],
    BeforeValidator(val_role_int_to_str),
    WrapSerializer(ser_role_str_to_int),
]
""" Annotated Role field to handle id/label conversions """

StrList = Annotated[
    list[str], BeforeValidator(val_str_to_list), WrapSerializer(ser_list_to_str)
]
""" Handles conversion between a string to a list and back """

BoolInt = Annotated[bool, PlainSerializer(lambda v: int(v))]
""" Handles conversions between a boolean and integer """


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)
