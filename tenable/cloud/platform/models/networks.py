from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from tenable.cloud._common import APIModel, BaseModel

from .pagination_v1 import PageV1Response, PaginationV1Query


class NetworkCreate(BaseModel):
    name: str
    description: str | None = None
    assets_ttl_days: int | None = None


class Network(APIModel):
    __api_path__ = "/networks/{model.uuid}"
    __api_save_request_model_kwargs__ = {
        "include": ["name", "description", "assets_ttl_days"]
    }

    uuid: UUID
    name: str
    description: str | None = None
    owner_uuid: UUID | None = None
    is_default: bool = False
    created_by: UUID | None = None
    modified_by: UUID | None = None
    assets_ttl_days: int | None = None
    scanner_count: int | None = None
    created_on: Annotated[datetime, Field(alias="created_in_seconds")]
    modified_on: Annotated[datetime, Field(alias="modified_in_seconds")]
    deleted: int | None = None
    deleted_by: UUID | None = None


class NetworkQueryParams(PaginationV1Query):
    sort: str | None = None
    include_deleted: Annotated[bool | None, Field(alias="includeDeleted")] = None


class NetworkListResponse(PageV1Response):
    items: Annotated[list[Network], Field(validation_alias="networks")]


class NetworkAssetCount(BaseModel):
    not_seen: Annotated[int, Field(alias="numAssetsNotSeen")]
    # the OpenAPI schema declares this property as "numAssetstotal", but the
    # documented example (and the real API) use "numAssetsTotal".
    total: Annotated[int, Field(alias="numAssetsTotal")]


class NetworkScanner(BaseModel):
    id: int | None = None
    uuid: UUID | None = None
    name: str | None = None
    type: str | None = None
    group: bool = False
    pool: bool = False
    status: str | None = None
    platform: str | None = None
    distro: str | None = None
    engine_build: str | None = None
    engine_version: str | None = None
    key: str | None = None
    linked: int | None = None
    loaded_plugin_set: str | None = None
    num_scans: int | None = None
    scan_count: int | None = None
    owner: str | None = None
    owner_id: int | None = None
    owner_name: str | None = None
    owner_uuid: UUID | None = None
    report_frequency: int | None = None
    settings: dict | None = None
    source: str | None = None
    creation_date: int | None = None
    last_connect: int | None = None
    last_modification_date: int | None = None
    timestamp: int | None = None
    remote_uuid: str | None = None
    supports_remote_logs: bool | None = None


class NetworkScannerListResponse(BaseModel):
    scanners: list[NetworkScanner]


class NetworkScannerBulkAssign(BaseModel):
    scanner_uuids: list[UUID]
