from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import Field

from tenable.cloud._common import BaseModel

ServerStatusValue = Literal[
    "loading",
    "ready",
    "corrupt-db",
    "feed-expired",
    "eval-expired",
    "locked",
    "register",
    "register-locked",
    "download-failed",
    "feed-error",
]


class ServerStatus(BaseModel):
    status: ServerStatusValue
    code: int


class ServerUpdate(BaseModel):
    href: str | None = None
    new_version: int | None = None
    restart: int | None = None


class ServerProperties(BaseModel):
    capabilities: dict[str, Any] | None = None
    enterprise: bool | None = None
    expiration: datetime | None = None
    idle_timeout: int | None = None
    license: dict[str, Any] | None = None
    loaded_plugin_set: str | None = None
    login_banner: bool | None = None
    nessus_type: str | None = None
    nessus_ui_version: str | None = None
    notifications: list[str] | None = None
    plugin_set: str | None = None
    scanner_boottime: datetime | None = None
    server_version: str | None = None
    server_uuid: str | None = None
    update: ServerUpdate | None = None
    analytics: dict[str, Any] | None = None
    limit_enabled: Annotated[bool | None, Field(alias="limitEnabled")] = None
    msp: bool | None = None
    server_build: str | None = None
    force_ui_reload: bool | None = None
    nessus_ui_build: str | None = None
    container_db_version: str | None = None
