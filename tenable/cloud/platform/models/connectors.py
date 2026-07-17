from datetime import datetime
from typing import Annotated, Any, Literal, Self
from uuid import UUID

from pydantic import Field, TypeAdapter
from restfly import APIModel

from tenable.cloud._common import BaseModel

from .pagination_v1 import PageV1Response, PaginationV1Query

ConnectorType = Literal[
    "aws", "aws_keyless", "aws_fa", "azure", "azure_fa", "gcp", "gcp_keyless"
]


class ConnectorSchedule(BaseModel):
    units: Literal["days", "hours", "minutes"] | None = None
    value: int | None = None


class ConnectorRegion(BaseModel):
    name: str | None = None
    friendly_name: str | None = None


class ConnectorAWSAccountBase(BaseModel):
    id: Annotated[str | None, Field(alias="account_id")] = None
    arn: Annotated[str | None, Field("role_arn")] = None


class ConnectorTrail(BaseModel):
    arn: str
    name: str | None = None
    region: ConnectorRegion | None = None
    availability: Literal["success", "error"] | None = None


class ConnectorTag(BaseModel):
    key: str | None = None
    value: str | None = None


class ConnectorAWSSubAccount(ConnectorAWSAccountBase):
    external_id: str | None = None
    trails: list[ConnectorTrail] | None = None
    incremental_mode: bool | None = None


class ConnectorAWSFAAccount(ConnectorAWSAccountBase): ...


class ConnectorAzureFATarget(BaseModel):
    resource_group: str | None = None
    tag_key: str | None = None
    tag_value: str | None = None


class ConnectorAzureStatus(BaseModel):
    last_event_seen: str | None = None
    release_timestamp: str | None = None
    message: str | None = None
    state: str | None = None


class ConnectorAWSCredentials(BaseModel):
    access_key: str | None = None
    secret_key: str | None = None


#
# Connector-type-specific `params` request payloads
#


class AWSKeyedConnectorParams(BaseModel):
    access_key: str
    secret_key: str
    trails: list[ConnectorTrail] | None = None


class AWSKeylessConnectorParams(BaseModel):
    sub_accounts: list[ConnectorAWSSubAccount]
    tags: list[ConnectorTag] | None = None
    auto_discovery: bool | None = None
    trails: list[ConnectorTrail] | None = None


class AWSFAConnectorParams(BaseModel):
    tag: ConnectorTag | None = None
    account: ConnectorAWSFAAccount | None = None


class AzureConnectorParams(BaseModel):
    application_id: str
    tenant_id: str
    client_secret: str
    subscription_id: str | None = None


class AzureFAConnectorParams(BaseModel):
    targets: list[ConnectorAzureFATarget] | None = None
    scan_all: bool | None = None


class GCPConnectorParams(BaseModel):
    service_account_key: str


class GCPKeylessConnectorParams(BaseModel):
    credentials_config: str


#
# Connector-type-specific create payloads, unified into a discriminated union.
#


class ConnectorBase(BaseModel):
    name: str
    type: ConnectorType
    network_uuid: UUID | None = None
    schedule: ConnectorSchedule | None = None


class AWSKeyedConnector(ConnectorBase):
    type: Literal["aws"] = "aws"
    params: AWSKeyedConnectorParams


class AWSKeylessConnector(ConnectorBase):
    type: Literal["aws_keyless"] = "aws_keyless"
    params: AWSKeylessConnectorParams


class AWSFAConnector(ConnectorBase):
    type: Literal["aws_fa"] = "aws_fa"
    params: AWSFAConnectorParams


class AzureConnector(ConnectorBase):
    type: Literal["azure"] = "azure"
    params: AzureConnectorParams


class AzureFAConnector(ConnectorBase):
    type: Literal["azure_fa"] = "azure_fa"
    params: AzureFAConnectorParams


class GCPConnector(ConnectorBase):
    type: Literal["gcp"] = "gcp"
    params: GCPConnectorParams


class GCPKeylessConnector(ConnectorBase):
    type: Literal["gcp_keyless"] = "gcp_keyless"
    params: GCPKeylessConnectorParams


ConnectorParams = Annotated[
    AWSKeyedConnector
    | AWSKeylessConnector
    | AWSFAConnector
    | AzureConnector
    | AzureFAConnector
    | GCPConnector
    | GCPKeylessConnector,
    Field(discriminator="type"),
]


class ConnectorRequest(BaseModel):
    connector: ConnectorParams


class ConnectorUpdateResponse(BaseModel):
    id: UUID


#
# Connector response models
#


class ConnectorRespBase(APIModel):
    __api_path__ = "/settings/connectors/{model.id}"

    id: UUID
    name: str
    network_uuid: UUID | None = None
    schedule: ConnectorSchedule | None = None
    container_uuid: UUID
    type: ConnectorType
    human_type: str
    data_type: str
    status: str
    is_fa: bool | None = None
    status_message: str | None = None
    schedule_full: ConnectorSchedule | None = None
    date_created: datetime
    date_modified: datetime
    expired: bool
    incremental_mode: bool
    last_sync_time: datetime | None = None
    last_run: datetime | None = None
    last_seen_updated: datetime | None = None

    def save(self) -> Self:
        path = self.__api_path__.format(model=self)
        payload = TypeAdapter(ConnectorParams).validate_python(
            self, from_attributes=True
        )
        resp = self.__api_client__._put(
            path,
            json=ConnectorRequest(connector=payload),
            response_model=ConnectorUpdateResponse,
        )
        assert resp.id == self.id

        resp = self.__api_client__._get(path, response_model=ConnectorEnvelope)
        return resp.connector


class AWSKeyedConnectorResp(ConnectorRespBase):
    type: Literal["aws"] = "aws"
    params: AWSKeyedConnectorParams


class AWSKeylessConnectorResp(ConnectorRespBase):
    type: Literal["aws_keyless"] = "aws_keyless"
    params: AWSKeylessConnectorParams


class AWSFAConnectorResp(ConnectorRespBase):
    type: Literal["aws_fa"] = "aws_fa"
    params: AWSFAConnectorParams


class AzureConnectorResp(ConnectorRespBase):
    type: Literal["azure"] = "azure"
    params: AzureConnectorParams


class AzureFAConnectorResp(ConnectorRespBase):
    type: Literal["azure_fa"] = "azure_fa"
    params: AzureFAConnectorParams


class GCPConnectorResp(ConnectorRespBase):
    type: Literal["gcp"] = "gcp"
    params: GCPConnectorParams


class GCPKeylessConnectorResp(ConnectorRespBase):
    type: Literal["gcp_keyless"] = "gcp_keyless"
    params: GCPKeylessConnectorParams


Connector = Annotated[
    AWSKeyedConnectorResp
    | AWSKeylessConnectorResp
    | AWSFAConnectorResp
    | AzureConnectorResp
    | AzureFAConnectorResp
    | GCPConnectorResp
    | GCPKeylessConnectorResp,
    Field(discriminator="type"),
]


class ConnectorEnvelope(BaseModel):
    connector: Connector


class ConnectorQueryParams(PaginationV1Query):
    sort: str | None = None


class ConnectorListResponse(PageV1Response):
    items: Annotated[list[Connector], Field(validation_alias="connectors")]


class ConnectorCloudtrailRequest(BaseModel):
    region: list[ConnectorRegion]
    credentials: ConnectorAWSCredentials | None = None
    account_id: str | None = None


class ConnectorCloudtrailResponse(BaseModel):
    trails: list[ConnectorTrail]


class ConnectorCFTTemplateRequest(BaseModel):
    connector_id: UUID
    account_id: str


class ConnectorCFTTemplateResponse(BaseModel):
    template_content: str | None = None
    tio_external_id: str | None = None
    tio_bucket_region: str | None = None
    tio_site: str | None = None
    kms_arn: str | None = None
