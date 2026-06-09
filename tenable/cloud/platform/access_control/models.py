from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    WrapSerializer,
)


def stringify_list(value, handler) -> str:
    if isinstance(value, list):
        return ",".join(value)
    return str(value)


def destringify_list(value) -> Any:
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v != ""]


StrList = Annotated[
    list[str], BeforeValidator(destringify_list), WrapSerializer(stringify_list)
]

BoolInt = Annotated[bool, PlainSerializer(lambda v: int(v))]
ACActions = Literal["CanScan", "CanView", "CanEdit", "CanUse"]


class AllowedIPAddresses(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)
    ipv4: Annotated[StrList, Field(alias="allowed_ipv4_addresses")]
    ipv6: Annotated[StrList, Field(alias="allowed_ipv6_addresses")]


class AccessControlGroup(BaseModel):
    """
    Access Control :: User Groups
    """

    permissions: int
    name: str
    uuid: UUID
    id: int
    user_count: int | None = None


class AccessControlTwoFactor(BaseModel):
    """
    Access Control :: User Two-Factor Sub-Object
    """

    sms_phone: str
    sms_enabled: BoolInt
    email_enabled: BoolInt


class AccessControlUserBase(BaseModel):
    """
    Access Control :: User Base Object
    """

    permissions: int
    name: str
    email: str
    enabled: bool


class AccessControlUserCreate(AccessControlUserBase):
    """
    Access Control :: User Creation Payload
    """

    username: str
    password: str
    permissions: int | None = None
    name: str | None = None
    email: str | None = None


class AccessControlUser(AccessControlUserBase):
    """
    Access Control :: User Response Object
    """

    model_config = ConfigDict(serialize_by_alias=True)
    uuid: UUID
    id: int
    type: str
    username: str
    last_login_attempt: datetime
    last_login: Annotated[datetime, Field(alias="lastLogin")]
    login__count: datetime
    login_fail_total: int
    undeletable: bool = False
    lockout: bool
    two_factor: AccessControlTwoFactor
    container_uuid: UUID


class AccessControlUserAuthorizations(BaseModel):
    """
    Access Control :: User Access Authorizations
    """

    account_uuid: UUID
    user_uuid: UUID
    api_permitted: bool
    password_permitted: bool
    saml_permitted: bool


class AccessControlUserAuthorizationsUpdate(BaseModel):
    """
    Access Control User Access Authorization Update Payload
    """

    api_permitted: bool
    password_permitted: bool
    saml_permitted: bool
    mfa_enrollment_required: bool


class AccessControlApiKeys(BaseModel):
    """
    Access Control :: API Key Assignment Response
    """

    model_config = ConfigDict(serialize_by_alias=True)
    access_key: Annotated[str, Field(alias="accessKey")]
    secret_key: Annotated[str, Field(alias="secretKey")]


class ListUsersResponse(BaseModel):
    """
    Access Control :: Users List Response
    """

    users: list[AccessControlUser]


class ListGroupsResponse(BaseModel):
    """
    Access Control :: Groups List Response
    """

    groups: list[AccessControlGroup]


class AccessControlPermObj(BaseModel):
    name: str | None = None
    type: Literal["Tag", "AllAssets"]
    uuid: UUID | None = None


class AccessControlSubject(BaseModel):
    name: str | None = None
    type: Literal["User", "UserGroup", "AllUsers"]
    uuid: UUID | None = None


class AccessControlPermissionBase(BaseModel):
    name: str
    actions: list[ACActions]
    objects: list[AccessControlPermObj]
    subjects: list[AccessControlSubject]


class AccessControlPermission(AccessControlPermissionBase):
    model_config = ConfigDict(serialize_by_alias=True)
    uuid: Annotated[UUID, Field(alias="permission_uuid")]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class ListPermissions(BaseModel):
    permissions: list[AccessControlPermission]


class UserGroupPermissions(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)
    granted: Annotated[
        list[AccessControlPermission], Field(alias="permissions_granted")
    ]
    available: Annotated[
        list[AccessControlPermission], Field(alias="permissions_available")
    ]
