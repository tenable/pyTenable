from typing import List, Literal, Optional

from annotated_types import Len
from pydantic import AfterValidator, AwareDatetime, BaseModel, Field
from typing_extensions import Annotated

from .common import (
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


class CVEDiscovery(BaseModel, strict=True):
    first_observed_at: Optional[AwareDatetime] = None
    last_observed_on: Optional[AwareDatetime] = None


class CVERisk(BaseModel, strict=True):
    cves: Annotated[List[str], Len(min_length=1, max_length=512)]


class CVESeverity(BaseModel, strict=True):
    level: Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']


class CVEExposure(BaseModel, strict=True):
    severity: Optional[CVESeverity] = None


class CVELibBin(BaseModel, strict=True):
    path: Optional[str512] = None
    sha256: Optional[str64] = None
    size: Optional[intpos] = None


class CVEPortBinding(BaseModel, strict=True):
    interfaces: Optional[List[str]] = None
    port: int64k
    protocol: Literal['ICMP', 'TCP', 'UDP']


class CVEProcess(BaseModel, strict=True):
    arguments: Optional[List[str]] = None
    environment_variables: Optional[List[CustomAttribute]] = None
    libraries: Optional[List[CVELibBin]] = None
    name: Optional[str64] = None
    parent_process_id: Optional[intpos] = None
    port_bindings: Optional[CVEPortBinding] = None
    process_id: Optional[intpos] = None
    software_index: Optional[intpos] = None


class CVESoftware(BaseModel, strict=True):
    binary: Optional[CVELibBin] = None
    configuration: Optional[List[CVELibBin]] = None
    product: Optional[ProductCPE] = None
    script: Optional[CVELibBin] = None


class CVEObservations(BaseModel, strict=True):
    processes: Optional[List[CVEProcess]] = None
    software: Optional[List[CVESoftware]] = None


class CVEFinding(BaseModel, strict=True):
    object_type: Literal['cve-finding'] = 'cve-finding'
    asset_id: str128
    custom_attributes: Optional[List[CustomAttribute]] = None
    definition_urn: Optional[str256] = None
    discovery: Optional[CVEDiscovery] = None
    id: str128
    state: Optional[Literal['ACTIVE', 'INACTIVE', 'REOPENED']] = None
    cve: Optional[CVERisk] = None
    observations: Optional[CVEObservations] = None
    exposure: Optional[CVEExposure] = None
