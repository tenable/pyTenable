from tenable.cloud._common import BaseModel

from .pagination_v1 import BaseFilterV1Resp


class ScanFilterItem(BaseModel):
    name: str
    operators: list[str]
    type: str
    allowed: list[str] | None = None


class ScanFilters(BaseModel):
    filters: list[ScanFilterItem]


class AgentFilters(BaseFilterV1Resp): ...


class AssetFilters(BaseFilterV1Resp): ...


class CredentialFilters(BaseFilterV1Resp): ...


class ScanHistoryFilters(BaseFilterV1Resp): ...


class VulnerabilityFilters(BaseFilterV1Resp): ...


class ReportFilters(ScanFilters): ...
