from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import EmailStr, Field

from tenable.cloud._common import BaseModel, BoolInt, Role, StrList

ACActions = Literal[
    "CanScan",
    "CanView",
    "CanEdit",
    "CanUse",
    "CanViewMssp",
    "CanEditMssp",
    "CanImpersonateAdmin",
    "CanImpersonateScanManager",
    "CanImpersonateScanOperator",
]


class AllowedIPAddresses(BaseModel):
    """
    Access Control :: API Allowed IPs
    """

    ipv4: Annotated[StrList, Field(alias="allowed_ipv4_addresses")]
    ipv6: Annotated[StrList, Field(alias="allowed_ipv6_addresses")]


class AccessControlGroupBase(BaseModel):
    """
    Access Control :: User Group Base Model
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

    role: Annotated[Role, Field(alias="permissions")]
    name: str
    email: EmailStr


class AccessControlUserUpdate(AccessControlUserBase):
    enabled: bool


class AccessControlUserCreate(AccessControlUserBase):
    """
    Access Control :: User Creation Payload
    """

    username: EmailStr
    password: str
    role: Annotated[Role | None, Field(alias="permissions")] = None
    name: str | None = None
    email: EmailStr | None = None


class AccessControlUser(AccessControlUserBase):
    """
    Access Control :: User Response Object
    """

    uuid: UUID
    id: int
    type: str
    username: EmailStr
    enabled: bool
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


class AccessControlUserAuthorizationsBase(BaseModel):
    """
    Access Control :: User Access Authorizations Base Model
    """

    api: Annotated[bool, Field(alias="api_permitted")]
    password: Annotated[bool, Field(alias="password_permitted")]
    saml: Annotated[bool, Field(alias="saml_permitted")]


class AccessControlUserAuthorizations(AccessControlUserAuthorizationsBase):
    """
    Access Control :: User Access Authorizations
    """

    account_uuid: UUID
    user_uuid: UUID


class AccessControlUserAuthorizationsUpdate(AccessControlUserAuthorizationsBase):
    """
    Access Control User Access Authorization Update Payload
    """

    mfa: Annotated[bool | None, Field(alias="mfa_enrollment_required")] = None


class AccessControlApiKeys(BaseModel):
    """
    Access Control :: API Key Assignment Response
    """

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
    type: Literal["Tag", "AllAssets", "AllObjects"]
    uuid: UUID | None = None


class AccessControlSubject(AccessControlPermObj):
    """
    Access Control :: Permissions Subject
    """

    type: Literal["User", "UserGroup", "AllUsers", "AllAdmins"]


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

    uuid: Annotated[UUID, Field(alias="permission_uuid")]
    created_at: datetime | None = None
    created_by: str | None = None
    updated_at: datetime | None = None
    updated_by: str | None = None


class ListPermissions(BaseModel):
    """
    Access Control :: Permissions Object List Response
    """

    permissions: list[AccessControlPermission]


class UserGroupPermissions(BaseModel):
    """
    Access Control :: User Group Permissions
    """

    granted: Annotated[
        list[AccessControlPermission], Field(alias="permissions_granted")
    ]
    available: Annotated[
        list[AccessControlPermission], Field(alias="permissions_available")
    ]
