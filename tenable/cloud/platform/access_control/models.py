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
    elif value is None:
        return []
    return value


StrList = Annotated[
    list[str], BeforeValidator(destringify_list), WrapSerializer(stringify_list)
]

BoolInt = Annotated[bool, PlainSerializer(lambda v: int(v))]
ACActions = Literal["CanScan", "CanView", "CanEdit", "CanUse"]


class AllowedIPAddresses(BaseModel):
    """
    Access Control :: API Allowed IPs
    """

    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)
    ipv4: Annotated[StrList, Field(alias="allowed_ipv4_addresses")]
    ipv6: Annotated[StrList, Field(alias="allowed_ipv6_addresses")]


class AccessControlGroupBase(BaseModel):
    """
    fpermiss    Access Control :: User Group Base Model
    """

    name: str
    uuid: UUID
    id: int
    immutable: bool = False
    user_count: int | None = None
    container_uuid: UUID


class AccessControlGroup(AccessControlGroupBase):
    """
    Access Control :: User Group Base Model
    """

    permissions: int


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

    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)
    uuid: UUID
    id: int
    type: str
    username: str
    last_login_attempt: datetime | None = None
    last_apikey_access: datetime | None = None
    last_login: Annotated[datetime | None, Field(alias="lastlogin")] = None
    login_fail_count: int
    login_fail_total: int
    lockout: bool
    two_factor: AccessControlTwoFactor | None = None
    group_uuids: list[UUID]
    preferences: dict[str, Any]
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

    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)
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

    groups: list[AccessControlGroupBase]


class AccessControlPermObj(BaseModel):
    """
    Access Control :: Permissions Object
    """

    name: str | None = None
    type: Literal["Tag", "AllAssets"]
    uuid: UUID | None = None


class AccessControlSubject(BaseModel):
    """
    Access Control :: Permissions Subject
    """

    name: str | None = None
    type: Literal["User", "UserGroup", "AllUsers"]
    uuid: UUID | None = None


class AccessControlPermissionBase(BaseModel):
    """
    Access Control :: Permissions Base Object
    """

    name: str
    actions: list[ACActions]
    objects: list[AccessControlPermObj]
    subjects: list[AccessControlSubject]


class AccessControlPermission(AccessControlPermissionBase):
    """
    Access Control :: Permissions Object
    """

    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)
    uuid: Annotated[UUID, Field(alias="permission_uuid")]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class ListPermissions(BaseModel):
    """
    Access Control :: Permissions Object List Response
    """

    permissions: list[AccessControlPermission]


class UserGroupPermissions(BaseModel):
    """
    Access Control :: User Group Permissions
    """

    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True)
    granted: Annotated[
        list[AccessControlPermission], Field(alias="permissions_granted")
    ]
    available: Annotated[
        list[AccessControlPermission], Field(alias="permissions_available")
    ]
