from typing import Annotated, Literal

from annotated_types import Len
from pydantic import AfterValidator, AwareDatetime

from .common import (
    BaseModel,
    CustomAttribute,
    ProductCPE,
    intpos,
    str64,
    str128,
    str256,
    str512,
)


def int_range_64k(v: int) -> int:
    assert v >= 0 and v <= 65535, f'{v} is not between 0 and 65535'
    return v


int64k = Annotated[int, AfterValidator(int_range_64k)]


class CVEDiscovery(BaseModel):
    first_observed_at: AwareDatetime | None = None
    last_observed_on: AwareDatetime | None = None


class CVERisk(BaseModel):
    cves: Annotated[list[str], Len(min_length=1, max_length=512)]


class CVESeverity(BaseModel):
    level: Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']


class CVEExposure(BaseModel):
    severity: CVESeverity | None = None


class CVELibBin(BaseModel):
    path: str512 | None = None
    sha256: str64 | None = None
    size: intpos | None = None


class CVEPortBinding(BaseModel):
    interfaces: list[str] | None = None
    port: int64k
    protocol: Literal['ICMP', 'TCP', 'UDP']


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
    binary: CVELibBin | None = None
    configuration: list[CVELibBin] | None = None
    product: ProductCPE | None = None
    script: CVELibBin | None = None


class CVEObservations(BaseModel):
    processes: list[CVEProcess] | None = None
    software: list[CVESoftware] | None = None


class CVEFinding(BaseModel):
    object_type: Literal['cve-finding'] = 'cve-finding'
    asset_id: str128
    custom_attributes: list[CustomAttribute] | None = None
    definition_urn: str256 | None = None
    discovery: CVEDiscovery | None = None
    id: str128
    state: Literal['ACTIVE', 'INACTIVE', 'REOPENED'] | None = None
    cve: CVERisk | None = None
    observations: CVEObservations | None = None
    exposure: CVEExposure | None = None
