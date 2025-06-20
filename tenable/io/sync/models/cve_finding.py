from typing import Annotated, Literal

from annotated_types import Len
from pydantic import AwareDatetime, Field

from .common import (
    BaseModel,
    CustomAttribute,
    ProductCPE,
    TruncListValidator,
    UniqueList,
    UpperCaseStr,
    int64k,
    intpos,
    str64,
    str128,
    str256,
    str512,
)

CVEStr = Annotated[str, Field(pattern=r'CVE-\d{4}-\d{4,7}')]


class CVEDiscovery(BaseModel):
    first_observed_at: AwareDatetime | None = None
    last_observed_on: AwareDatetime | None = None


class CVERisk(BaseModel):
    cves: Annotated[
        list[CVEStr],
        Len(min_length=1, max_length=512),
        TruncListValidator,
        UniqueList,
    ]


class CVESeverity(BaseModel):
    level: Annotated[Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'], UpperCaseStr]


class CVEExposure(BaseModel):
    severity: CVESeverity | None = None


class CVELibBin(BaseModel):
    path: str512 | None = None
    sha256: str64 | None = None
    size: intpos | None = None


class CVEPortBinding(BaseModel):
    interfaces: list[str] | None = None
    port: int64k
    protocol: Annotated[Literal['ICMP', 'TCP', 'UDP'], UpperCaseStr]


class CVEProcess(BaseModel):
    arguments: list[str] | None = None
    environment_variables: list[CustomAttribute] | None = None
    libraries: list[CVELibBin] | None = None
    name: str64 | None = None
    parent_process_id: intpos | None = None
    port_bindings: CVEPortBinding | None = None
    process_id: intpos | None = None
    software_index: intpos | None = None


class CVESoftware(BaseModel):
    # binary: CVELibBin | None = None # TODO: Engineering Re-evaluating
    # configuration: list[CVELibBin] | None = None # TODO: Engineering Re-evaluating
    product: ProductCPE | None = None
    # script: CVELibBin | None = None # TODO: Engineering Re-evaluating


class CVEObservations(BaseModel):
    # processes: list[CVEProcess] | None = None # TODO: Engineering Re-evaluating
    software: list[CVESoftware] | None = None


class CVEFinding(BaseModel):
    object_type: Literal['cve-finding'] = 'cve-finding'
    asset_id: str128
    custom_attributes: Annotated[list[CustomAttribute], UniqueList] | None = None
    definition_urn: str256 | None = None
    discovery: CVEDiscovery | None = None
    id: str128
    state: Annotated[Literal['ACTIVE', 'INACTIVE', 'REOPENED'], UpperCaseStr] | None = (
        None
    )
    cve: CVERisk | None = None
    observations: CVEObservations | None = None
    exposure: CVEExposure | None = None
