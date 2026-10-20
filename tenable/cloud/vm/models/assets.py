from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import Field, RootModel, field_validator, model_validator

from tenable.cloud._common import BaseModel, StrList

AcrReason = Literal[
    "Business Critical",
    "In Scope For Compliance",
    "Existing Mitigation Control",
    "Dev only",
    "Key drivers does not match",
    "Other",
]
""" Supported reasons for overriding an asset's ACR """


class AssetSource(BaseModel):
    # The source name is documented as an enum, however organizations can provide
    # custom source names (and the documented examples already include values outside
    # of that enum), so we leave this as a string.
    name: str
    first_seen: datetime | None = None
    last_seen: datetime | None = None


class AssetAcrDriver(BaseModel):
    driver_name: str
    driver_value: list[str] = Field(default_factory=list)


class AssetScanFrequency(BaseModel):
    interval: int | None = None
    frequency: int | None = None
    licensed: bool | None = None


class AssetTag(BaseModel):
    tag_uuid: UUID
    tag_key: str
    tag_value: str
    added_by: UUID | None = None
    added_at: datetime | None = None


class AssetInterface(BaseModel):
    name: str | None = None
    ipv4: list[str] = Field(default_factory=list)
    ipv6: list[str] = Field(default_factory=list)
    fqdn: list[str] = Field(default_factory=list)
    mac_address: list[str] = Field(default_factory=list)
    virtual: bool | None = None
    aliased: bool | None = None


class AssetSummary(BaseModel):
    id: UUID
    has_agent: bool = False
    last_seen: datetime | None = None
    last_scan_target: str | None = None
    sources: list[AssetSource] = Field(default_factory=list)
    acr_score: float | None = None
    acr_drivers: list[AssetAcrDriver] = Field(default_factory=list)
    exposure_score: float | None = None
    scan_frequency: list[AssetScanFrequency] | None = None
    ipv4: list[str] = Field(default_factory=list)
    ipv6: list[str] = Field(default_factory=list)
    fqdn: list[str] = Field(default_factory=list)
    mac_address: list[str] = Field(default_factory=list)
    netbios_name: list[str] = Field(default_factory=list)
    operating_system: list[str] = Field(default_factory=list)
    hostname: list[str] = Field(default_factory=list)
    agent_name: list[str] = Field(default_factory=list)
    aws_ec2_name: list[str] = Field(default_factory=list)
    security_protection_level: int | None = None
    security_protections: list[str] = Field(default_factory=list)
    exposure_confidence_value: int | None = None


class Asset(AssetSummary):
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    terminated_at: datetime | None = None
    deleted_at: datetime | None = None
    first_seen: datetime | None = None
    aes_score_v3: float | None = None
    acr_score_v3: float | None = None
    last_authentication_attempt_date: datetime | None = None
    last_authentication_success_date: datetime | None = None
    last_authenticated_scan_date: datetime | None = None
    last_licensed_scan_date: datetime | None = None
    last_scan_id: UUID | None = None
    last_schedule_id: str | None = None
    tags: list[AssetTag] = Field(default_factory=list)
    network_id: list[UUID] = Field(default_factory=list)
    system_type: list[str] = Field(default_factory=list)
    tenable_uuid: list[str] = Field(default_factory=list)
    bios_uuid: list[str] = Field(default_factory=list)
    aws_ec2_instance_id: list[str] = Field(default_factory=list)
    aws_ec2_instance_ami_id: list[str] = Field(default_factory=list)
    aws_owner_id: list[str] = Field(default_factory=list)
    aws_availability_zone: list[str] = Field(default_factory=list)
    aws_region: list[str] = Field(default_factory=list)
    aws_vpc_id: list[str] = Field(default_factory=list)
    aws_ec2_instance_group_name: list[str] = Field(default_factory=list)
    aws_ec2_instance_state_name: list[str] = Field(default_factory=list)
    aws_ec2_instance_type: list[str] = Field(default_factory=list)
    aws_subnet_id: list[str] = Field(default_factory=list)
    aws_ec2_product_code: list[str] = Field(default_factory=list)
    azure_vm_id: list[str] = Field(default_factory=list)
    azure_resource_id: list[str] = Field(default_factory=list)
    gcp_project_id: list[str] = Field(default_factory=list)
    gcp_zone: list[str] = Field(default_factory=list)
    gcp_instance_id: list[str] = Field(default_factory=list)
    ssh_fingerprint: list[str] = Field(default_factory=list)
    mcafee_epo_guid: list[str] = Field(default_factory=list)
    mcafee_epo_agent_guid: list[str] = Field(default_factory=list)
    qualys_asset_id: list[str] = Field(default_factory=list)
    qualys_host_id: list[str] = Field(default_factory=list)
    servicenow_sysid: list[str] = Field(default_factory=list)
    bigfix_asset_id: list[str] = Field(default_factory=list)
    installed_software: list[str] = Field(default_factory=list)
    interfaces: list[AssetInterface] = Field(default_factory=list)


class AssetListResponse(BaseModel):
    assets: list[AssetSummary]
    total: int | None = None


class AssetAcrIdentifier(BaseModel):
    id: UUID | None = None
    fqdn: list[str] | None = None
    ipv4: list[str] | None = None
    mac_address: list[str] | None = None
    netbios_name: list[str] | None = None

    @model_validator(mode="after")
    def validate_single_identifier(self) -> "AssetAcrIdentifier":
        # The API only allows a single property within each identifier object.
        if len([v for v in self.model_dump().values() if v is not None]) != 1:
            raise ValueError(
                "Each asset identifier must contain exactly one of id, fqdn, ipv4, "
                "mac_address, or netbios_name."
            )
        return self


class AssetAcrUpdate(BaseModel):
    acr_score: Annotated[int, Field(ge=1, le=10)]
    reason: list[AcrReason] | None = None
    note: str | None = None
    asset: Annotated[list[AssetAcrIdentifier], Field(min_length=1)]

    @field_validator("asset", mode="before")
    @classmethod
    def split_identifiers(cls, value: Any) -> Any:
        """
        Splits any identifier objects containing multiple properties into a single
        identifier object per property.  As an asset id is a single value, a list of
        ids is split into an identifier object per id.  Empty properties are dropped.
        """
        if not isinstance(value, list):
            return value
        identifiers = []
        for item in value:
            if not isinstance(item, dict):
                identifiers.append(item)
                continue
            for key, prop in item.items():
                if prop is None or prop == []:
                    continue
                if key == "id" and isinstance(prop, (list, tuple)):
                    identifiers.extend({"id": i} for i in prop)
                else:
                    identifiers.append({key: prop})
        return identifiers


class AssetAcrUpdateRequest(RootModel[list[AssetAcrUpdate]]): ...


class AssetMoveRequest(BaseModel):
    source: UUID
    destination: UUID
    targets: StrList


class AssetQueryFilter(BaseModel):
    field: str
    operator: str
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        if isinstance(data, str):
            parts = data.split(":", 2)
            if len(parts) != 3:
                raise ValueError(f"{data} is not in a valid filter format.")
            data = {"field": parts[0], "operator": parts[1], "value": parts[2]}
        elif isinstance(data, tuple) and len(data) == 3:
            data = {"field": data[0], "operator": data[1], "value": data[2]}
        return data


class AssetDeleteQuery(BaseModel):
    and_: Annotated[list[AssetQueryFilter] | None, Field(alias="and")] = None
    or_: Annotated[list[AssetQueryFilter] | None, Field(alias="or")] = None


class AssetDeleteRequest(BaseModel):
    query: AssetDeleteQuery
    hard_delete: bool | None = None


class BulkJobData(BaseModel):
    asset_count: int


class BulkJobDetails(BaseModel):
    data: BulkJobData


class BulkJobResponse(BaseModel):
    response: BulkJobDetails


class AssetImport(BaseModel):
    fqdn: list[str] | None = None
    ipv4: list[str] | None = None
    ipv6: list[str] | None = None
    ip_address: list[str] | None = None
    mac_address: Annotated[list[str] | None, Field(max_length=100)] = None
    netbios_name: str | None = None
    hostname: list[str] | None = None
    operating_system: list[str] | None = None
    installed_software: list[str] | None = None
    bigfix_asset_id: list[str] | None = None
    ssh_fingerprint: str | None = None
    bios_uuid: str | None = None
    manufacturer_tpm_id: str | None = None
    mcafee_epo_guid: str | None = None
    mcafee_epo_agent_guid: str | None = None
    symantec_ep_hardware_key: str | None = None
    qualys_asset_id: str | None = None
    qualys_host_id: str | None = None
    servicenow_sys_id: str | None = None
    gcp_project_id: str | None = None
    gcp_zone: str | None = None
    gcp_instance_id: str | None = None
    azure_vm_id: str | None = None
    azure_resource_id: str | None = None
    aws_availability_zone: str | None = None
    aws_ec2_instance_id: str | None = None
    aws_ec2_instance_ami_id: str | None = None
    aws_ec2_instance_group_name: str | None = None
    aws_ec2_instance_state_name: str | None = None
    aws_ec2_instance_type: str | None = None
    aws_ec2_name: str | None = None
    aws_ec2_product_code: str | None = None
    aws_owner_id: str | None = None
    aws_region: str | None = None
    aws_subnet_id: str | None = None
    aws_vpc_id: str | None = None

    @model_validator(mode="after")
    def validate_identifiers(self) -> "AssetImport":
        if not (self.fqdn or self.ipv4 or self.netbios_name or self.mac_address):
            raise ValueError(
                "Each asset requires at least one of fqdn, ipv4, netbios_name, "
                "or mac_address."
            )
        return self


class AssetImportRequest(BaseModel):
    source: str
    assets: Annotated[list[AssetImport], Field(min_length=1)]


class AssetImportCreateResponse(BaseModel):
    job_id: Annotated[UUID, Field(alias="asset_import_job_uuid")]


class AssetImportJob(BaseModel):
    job_id: UUID
    container_id: UUID | None = None
    source: str | None = None
    batches: int | None = None
    uploaded_assets: int | None = None
    failed_assets: int | None = None
    # The API returns these as millisecond-precision unix timestamps, which pydantic
    # will automatically detect and convert.
    start_time: datetime | None = None
    last_update_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None
    status_message: str | None = None


class AssetImportJobListResponse(BaseModel):
    asset_import_jobs: list[AssetImportJob]
