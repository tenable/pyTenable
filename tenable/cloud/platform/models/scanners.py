from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import PlainSerializer

from tenable.cloud._common import APIModel, BaseModel, BoolInt

BoolStr = Annotated[bool, PlainSerializer(lambda v: str(v).lower())]
""" Handles conversion between a boolean and a lowercase "true"/"false" string """

ScannerStatus = Literal["on", "off"]
ScannerScanAction = Literal["stop", "pause", "resume"]
ScannerDirectiveType = Literal["restart", "settings"]
ScannerDirectiveSetting = Literal[
    "backend_log_level", "auto_update", "auto_update_delay"
]
ScannerDirectiveTaskStatus = Literal[
    "pending", "running", "completed", "failed", "canceled"
]


class ScannerGroupRef(BaseModel):
    name: str | None = None
    uuid: str | None = None


class ScannerRemoteSettingValue(BaseModel):
    value: str


class ScannerRemoteSetting(BaseModel):
    name: str
    setting: str
    type: str
    description: str | None = None
    backend_reload: bool | None = None
    status: str | None = None
    value: str | None = None
    default: str | None = None
    allowable_values: list[ScannerRemoteSettingValue] | None = None
    min: int | None = None


class Scanner(APIModel):
    __api_path__ = "/scanners/{model.id}"
    __api_save_request_model_kwargs__ = {"include": ["name"]}
    __api_save_method__ = "PUT"

    id: int
    uuid: str | None = None
    name: str | None = None
    type: str | None = None
    group: bool = False
    pool: bool = False
    status: ScannerStatus | None = None
    platform: str | None = None
    distro: str | None = None
    engine_version: str | None = None
    hostname: str | None = None
    ip_addresses: list[str] | None = None
    key: str | None = None
    linked: int | None = None
    loaded_plugin_set: str | None = None
    registration_code: str | None = None
    license: dict[str, Any] | None = None
    network_name: str | None = None
    num_scans: int | None = None
    scan_count: int | None = None
    owner: str | None = None
    owner_id: int | None = None
    owner_name: str | None = None
    owner_uuid: UUID | None = None
    shared: int | None = None
    source: str | None = None
    creation_date: datetime | None = None
    last_connect: datetime | None = None
    last_modification_date: datetime | None = None
    timestamp: datetime | None = None
    ui_build: str | None = None
    ui_version: str | None = None
    user_permissions: int | None = None
    remote_uuid: str | None = None
    supports_remote_logs: bool | None = None
    supports_webapp: bool | None = None
    supports_remote_settings: bool | None = None
    aws_update_interval: int | None = None
    profile_uuid: str | None = None
    profile_name: str | None = None
    remote_settings: list[ScannerRemoteSetting] | None = None
    groups: list[ScannerGroupRef] | None = None


class ScannerListResponse(BaseModel):
    scanners: list[Scanner]


class ScannerUpdate(BaseModel):
    name: str | None = None
    force_plugin_update: BoolInt | None = None
    force_ui_update: BoolInt | None = None
    finish_update: BoolInt | None = None
    registration_code: str | None = None
    aws_update_interval: int | None = None


class ScannerUpdateResult(BaseModel):
    owner_uuid: UUID | None = None
    created: datetime | None = None
    modified: datetime | None = None
    container_uuid: UUID | None = None
    uuid: str | None = None
    id: int | None = None
    name: str | None = None
    network_name: str | None = None
    default_permissions: int | None = None
    shared: int | None = None
    user_permissions: int | None = None
    key: str | None = None
    status: ScannerStatus | None = None
    profile_uuid: str | None = None
    profile_name: str | None = None
    type: str | None = None
    distributed: bool | None = None
    remote_uuid: str | None = None
    linked: int | None = None
    last_connect: datetime | None = None
    max_tasks: int | None = None
    max_targets: int | None = None
    task_max_targets: int | None = None
    platform: str | None = None
    distro: str | None = None
    ui_version: str | None = None
    ui_build: str | None = None
    engine_version: str | None = None
    loaded_plugin_set: str | None = None
    ip_addresses: list[str] | None = None
    hostname: str | None = None
    group: bool = False
    pool: bool = False
    supports_remote_logs: bool | None = None
    supports_remote_settings: bool | None = None
    supports_webapp: bool | None = None
    settings_pending: bool | None = None
    restart_pending: bool | None = None
    network_id: UUID | None = None
    created_in_seconds: datetime | None = None
    modified_in_seconds: datetime | None = None
    groups: list[ScannerGroupRef] | None = None
    remote_settings: list[dict[str, Any]] | None = None
    settings: dict[str, Any] | None = None
    system: bool | None = None
    scanner_scanner: bool | None = None
    system_group_scanner: bool | None = None
    pvs: bool | None = None
    given_nessus_updates: bool | None = None
    industrial_security: bool | None = None
    webapp: bool | None = None
    lce: bool | None = None
    aws: bool | None = None
    system_scanner_scanner: bool | None = None
    cloud_group: bool | None = None
    active_directory: bool | None = None
    can_factory_reset: bool | None = None
    system_webapp_scanner: bool | None = None


class ScannerAWSTarget(BaseModel):
    scanner_id: int | None = None
    instance_id: str | None = None
    private_ip: str | None = None
    public_ip: str | None = None
    state: str | None = None
    zone: str | None = None
    type: str | None = None
    name: str | None = None


class ScannerAWSTargetListResponse(BaseModel):
    targets: list[ScannerAWSTarget]


class ScannerScan(BaseModel):
    scanner_uuid: str | None = None
    name: str | None = None
    status: str | None = None
    id: str | None = None
    scan_id: int | None = None
    user: str | None = None
    user_uuid: UUID | None = None
    last_modification_date: datetime | None = None
    start_time: datetime | None = None
    remote: bool | None = None
    network_id: UUID | None = None


class ScannerScanListResponse(BaseModel):
    scans: list[ScannerScan]


class ScannerKeyResponse(BaseModel):
    key: str


class ScannerLinkUpdate(BaseModel):
    link: BoolInt


class ScannerScanControl(BaseModel):
    action: ScannerScanAction


class ScannerConcurrentUpdate(BaseModel):
    enabled: bool | None = None
    max_concurrent_update: int | None = None


class ScannerConfig(APIModel):
    __api_path__ = "/scanners/config"
    __api_save_method__ = "PUT"

    concurrent_update: ScannerConcurrentUpdate | None = None


class ScannerTaskStatus(BaseModel):
    container_uuid: UUID | None = None
    type: str | None = None
    id: UUID | None = None
    status: str | None = None
    created: datetime | None = None
    modified: datetime | None = None
    expiration: datetime | None = None


class ScannerDirectiveSettingItem(BaseModel):
    setting: ScannerDirectiveSetting
    value: str | int


class ScannerDirectiveOptions(BaseModel):
    hard: bool | None = None
    idle: bool | None = None
    settings: list[ScannerDirectiveSettingItem] | None = None


class ScannerDirective(BaseModel):
    type: ScannerDirectiveType
    options: ScannerDirectiveOptions | None = None


class ScannerBulkDirective(BaseModel):
    all_scanners: BoolStr | None = None
    scanners: list[str] | None = None
    directive: ScannerDirective


class ScannerDirectiveTask(BaseModel):
    container_uuid: UUID | None = None
    uuid: UUID | None = None
    sensor_uuid: UUID | None = None
    owner_uuid: UUID | None = None
    type: str | None = None
    status: ScannerDirectiveTaskStatus | None = None
    created: datetime | None = None
    modified: datetime | None = None
    results_blob_size: int | None = None
    options: dict[str, Any] | None = None
    ttl: int | None = None
    id: UUID | None = None
