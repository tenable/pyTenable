from typing import Literal
from uuid import UUID

from tenable.cloud._common import BaseModel, Permission

ObjectType = Literal["agent-group", "policy", "scan", "scanner"]


class ACL(BaseModel):
    type: Literal["default", "user", "group"]
    id: int | None = None
    uuid: UUID | None = None
    name: str | None = None
    display_name: str | None = None
    permissions: Permission
    owner: int | None = None


class ACLRequest(BaseModel):
    type: Literal["default", "user", "group"]
    id: int | None = None
    permissions: Permission


class PermissionsListResponse(BaseModel):
    acls: list[ACL]


class PermissionsUpdate(BaseModel):
    acls: list[ACLRequest]
