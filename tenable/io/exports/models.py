from datetime import datetime
from ipaddress import IPv4Address, IPv4Network, IPv6Address
from typing import Annotated, Any, Literal
from uuid import UUID

import arrow
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    SerializerFunctionWrapHandler,
    model_serializer,
)


def to_lower(value: Any) -> Any:
    if isinstance(value, str):
        return value.lower()
    return value


def to_upper(value: Any) -> Any:
    if isinstance(value, str):
        return value.upper()
    return value


def ser_to_ts(value: Any) -> int:
    return arrow.get(value).int_timestamp


Timestamp = Annotated[datetime | int | str, PlainSerializer(ser_to_ts)]
ComplianceState = Annotated[
    Literal['PASSED', 'FAILED', 'WARNING', 'SKIPPED', 'ERROR', 'UNKNOWN'],
    BeforeValidator(to_upper),
]
CVECategory = Annotated[
    Literal[
        'cisa known exploitable',
        'emerging threats',
        'in the news',
        'persistently exploited',
        'ransomware',
        'recent active exploitation',
        'top 50 vpr',
    ],
    BeforeValidator(to_lower),
]
CVEId = Annotated[str, Field(pattern=r'^CVE-\d{4}-\d{1,5}$')]
CVSSScore = Annotated[float, Field(ge=0, le=10)]
ExploitMaturity = Annotated[
    Literal['high', 'functional', 'poc', 'unproven'], BeforeValidator(to_lower)
]
EPSSScore = Annotated[float, Field(le=0, ge=100)]
OWASPChapters = Annotated[
    Literal['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'],
    BeforeValidator(to_upper),
]
OWASPAPIChapters = Annotated[
    Literal[
        'API1', 'API2', 'API3', 'API4', 'API5', 'API6', 'API7', 'API8', 'API9', 'API10'
    ],
    BeforeValidator(to_upper),
]
Severity = Annotated[
    Literal['info', 'low', 'medium', 'high', 'critical'],
    BeforeValidator(to_lower),
]
SeverityModificationType = Annotated[
    Literal['NONE', 'ACCEPTED', 'RECASTED'], BeforeValidator(to_upper)
]
State = Annotated[Literal['OPEN', 'REOPENED', 'FIXED'], BeforeValidator(to_upper)]
ThreatIntensity = Annotated[
    Literal['very high', 'high', 'medium', 'low', 'very low'],
    BeforeValidator(to_lower),
]
Weaponization = Annotated[
    Literal['apt', 'botnet', 'malware', 'ransomware', 'rootkit'],
    BeforeValidator(to_lower),
]


class ExportFilterV1Base(BaseModel):
    tags: list[tuple[str, list[str] | str]] | None = None

    @model_serializer(mode='wrap')
    def serialize_tags(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data = handler(self)
        tags = data.pop('tags', None)
        if tags:
            for category, value in tags:
                name = f'tag.{category.replace(" ", "_")}'
                if name not in data:
                    data[name] = []
                if isinstance(value, list):
                    data[name] + value
                elif isinstance(value, str):
                    data[name].append(value)
        return data


class AssetExportBase(BaseModel):
    chunk_size: Annotated[int, Field(ge=50, le=10000)] = 1000
    include_open_ports: bool | None = None
    include_resource_tags: bool | None = None


class AssetExportFiltersBase(BaseModel):
    # Timestamp filters
    created_at: Timestamp | None = None
    updated_at: Timestamp | None = None
    deleted_at: Timestamp | None = None
    terminated_at: Timestamp | None = None
    first_scan_time: Timestamp | None = None
    last_authenticated_scan_time: Timestamp | None = None
    last_assessed: Timestamp | None = None

    # Boolean Flags
    is_deleted: bool | None = None
    is_licensed: bool | None = None
    is_terminated: bool | None = None
    has_plugin_results: bool | None = None
    servicenow_sysid: bool | None = None

    # Other Filters
    last_scan_id: str | None = None
    network_id: UUID | None = None
    sources: list[str] | None = None


class AssetExportFiltersV1(ExportFilterV1Base, AssetExportFiltersBase):
    pass


class AssetExportFiltersV2(AssetExportFiltersBase):
    since: Timestamp | None = None
    types: list[str] | None = None


class AssetExportV1(AssetExportBase):
    model_config = ConfigDict(extra='forbid')
    filters: AssetExportFiltersV1


class AssetExportV2(AssetExportBase):
    model_config = ConfigDict(extra='forbid')
    filters: AssetExportFiltersV2


class TimeTakenToFix(BaseModel):
    gte: int | None = None
    lte: int | None = None


class CVSSScores(BaseModel):
    eq: list[CVSSScore] | None = None
    neq: list[CVSSScore] | None = None
    gt: CVSSScore | None = None
    gte: CVSSScore | None = None
    lt: CVSSScore | None = None
    lte: CVSSScore | None = None


class EPSSScores(BaseModel):
    eq: list[EPSSScore] | None = None
    neq: list[EPSSScore] | None = None
    gt: EPSSScore | None = None
    gte: EPSSScore | None = None
    lt: EPSSScore | None = None
    lte: EPSSScore | None = None


class VulnerabilityExportFiltersV1(ExportFilterV1Base):
    # Timestamp filters
    since: Timestamp | None = None
    first_found: Timestamp | None = None
    first_seen: Timestamp | None = None
    last_found: Timestamp | None = None
    last_seen: Timestamp | None = None
    indexed_at: Timestamp | None = None
    last_fixed: Timestamp | None = None
    resurfaced_date: Timestamp | None = None

    time_taken_to_fix: TimeTakenToFix | None = None
    cidr_range: IPv4Network | None = None
    cve_id: list[CVEId] | None = None
    cve_category: list[CVECategory] | None = None
    cvss4_base_score: CVSSScores | None = None
    epss_score: EPSSScores | None = None
    exploit_maturity: list[ExploitMaturity] | None = None
    initiative_id: UUID | None = None
    network_id: UUID | None = None
    plugin_family: list[str] | None = None
    plugin_id: list[int] | None = None
    plugin_type: str | None = None
    scan_uuid: str | None = None
    severity: list[Severity] | None = None
    severity_modification_type: list[SeverityModificationType] | None = None
    state: list[State] | None = None
    source: list[str] | None = None
    vpr_score: CVSSScores | None = None
    vpr_v2_score: CVSSScores | None = None
    vpr_threat_intensity: list[ThreatIntensity] | None = None
    weaponization: list[Weaponization] | None = None


class VulnerabilityExportV1(BaseModel):
    model_config = ConfigDict(extra='forbid')
    num_assets: Annotated[int, Field(ge=50, le=5000)] = 500
    include_unlicensed: bool = True
    filters: VulnerabilityExportFiltersV1


class ComplianceExportFiltersV1(BaseModel):
    # Time filters
    last_seen: Timestamp | None = None
    first_seen: Timestamp | None = None
    last_observed: Timestamp | None = None
    indexed_at: Timestamp | None = None
    since: Timestamp | None = None

    audit_name: str | None = None
    audit_file_name: str | None = None
    compliance_results: list[ComplianceState] | None = None
    ipv4_addresses: list[IPv4Address] | None = None
    ipv6_addresses: list[IPv6Address] | None = None
    network_id: UUID | None = None
    plugin_id: list[int] | None = None
    state: list[State] | None = None
    tags: list[tuple[str, list[str] | str]] | None = None

    @model_serializer(mode='wrap')
    def serialize_tags(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data = handler(self)
        tags = data.pop('tags', None)
        if tags:
            data['tags'] = {}
            for category, value in tags:
                if category not in data['tags']:
                    data['tags'][category] = []
                if isinstance(value, list):
                    data['tags'][category] + value
                elif isinstance(value, str):
                    data['tags'][category].append(value)
        return data


class ComplianceExportV1(BaseModel):
    model_config = ConfigDict(extra='forbid')
    num_findings: int = 5000
    asset: list[UUID] | None = None
    filters: ComplianceExportFiltersV1


class WASExportFiltersV1(BaseModel):
    # Time filters
    first_found: Timestamp | None = None
    last_fixed: Timestamp | None = None
    last_found: Timestamp | None = None
    indexed_at: Timestamp | None = None
    since: Timestamp | None = None

    asset_uuid: list[UUID] | None = None
    asset_name: str | None = None
    cvss4_base_score: CVSSScores | None = None
    epss_score: EPSSScores | None = None
    ipv4s: list[IPv4Address] | None = None
    owasp_2010: list[OWASPChapters] | None = None
    owasp_2013: list[OWASPChapters] | None = None
    owasp_2017: list[OWASPChapters] | None = None
    owasp_2021: list[OWASPChapters] | None = None
    owasp_api_2019: list[OWASPAPIChapters] | None = None
    plugin_ids: list[int] | None = None
    severity: list[Severity] | None = None
    severity_modification_type: list[SeverityModificationType] | None = None
    state: list[State] | None = None
    vpr_score: CVSSScores | None = None
    vpr_v2_score: CVSSScores | None = None


class WASExportV1(BaseModel):
    model_config = ConfigDict(extra='forbid')
    num_assets: int = 500
    include_unlicensed: bool = True
    filters: WASExportFiltersV1
