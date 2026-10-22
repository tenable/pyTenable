from datetime import date, datetime
from typing import Annotated, Any

from pydantic import Field

from tenable.cloud._common import BaseModel


class PluginCvssTemporalVector(BaseModel):
    exploitability: Annotated[str | None, Field(alias="Exploitability")] = None
    remediation_level: Annotated[str | None, Field(alias="RemediationLevel")] = None
    report_confidence: Annotated[str | None, Field(alias="ReportConfidence")] = None
    raw: str | None = None


class PluginCvssVector(BaseModel):
    access_complexity: Annotated[str | None, Field(alias="AccessComplexity")] = None
    access_vector: Annotated[str | None, Field(alias="AccessVector")] = None
    authentication: Annotated[str | None, Field(alias="Authentication")] = None
    availability_impact: Annotated[str | None, Field(alias="Availability-Impact")] = (
        None
    )
    confidentiality_impact: Annotated[
        str | None, Field(alias="Confidentiality-Impact")
    ] = None
    integrity_impact: Annotated[str | None, Field(alias="Integrity-Impact")] = None
    raw: str | None = None


class PluginCvss3TemporalVector(BaseModel):
    exploit_code_maturity: Annotated[str | None, Field(alias="ExploitCodeMaturity")] = (
        None
    )
    remediation_level: Annotated[str | None, Field(alias="RemediationLevel")] = None
    report_confidence: Annotated[str | None, Field(alias="ReportConfidence")] = None
    raw: str | None = None


class PluginCvss3Vector(BaseModel):
    attack_vector: Annotated[str | None, Field(alias="AttackVector")] = None
    attack_complexity: Annotated[str | None, Field(alias="AttackComplexity")] = None
    privileges_required: Annotated[str | None, Field(alias="PrivilegesRequired")] = None
    user_interaction: Annotated[str | None, Field(alias="UserInteraction")] = None
    scope: Annotated[str | None, Field(alias="Scope")] = None
    confidentiality_impact: Annotated[
        str | None, Field(alias="Confidentiality-Impact")
    ] = None
    integrity_impact: Annotated[str | None, Field(alias="Integrity-Impact")] = None
    availability_impact: Annotated[str | None, Field(alias="Availability-Impact")] = (
        None
    )
    raw: str | None = None


class PluginVpr(BaseModel):
    score: float | None = None
    drivers: dict[str, Any] | None = None
    updated: datetime | None = None


class PluginXref(BaseModel):
    type: str
    id: str


class PluginAttributes(BaseModel):
    plugin_modification_date: datetime | None = None
    plugin_version: str | None = None
    plugin_publication_date: datetime | None = None
    plugin_type: str | None = None
    patch_publication_date: datetime | None = None
    vuln_publication_date: datetime | None = None
    description: str | None = None
    synopsis: str | None = None
    solution: str | None = None
    risk_factor: str | None = None
    see_also: list[str] = Field(default_factory=list)
    cve: list[str] = Field(default_factory=list)
    bid: list[int] = Field(default_factory=list)
    cpe: list[str] = Field(default_factory=list)
    xref: list[str] = Field(default_factory=list)
    xrefs: list[PluginXref] = Field(default_factory=list)
    cvss_base_score: float | None = None
    cvss_temporal_score: float | None = None
    cvss_vector: PluginCvssVector | None = None
    cvss_temporal_vector: PluginCvssTemporalVector | None = None
    cvss_score_source: str | None = None
    cvss_score_rationale: str | None = None
    cvss3_base_score: float | None = None
    cvss3_temporal_score: float | None = None
    cvss3_vector: PluginCvss3Vector | None = None
    cvss3_temporal_vector: PluginCvss3TemporalVector | None = None
    cvss3_score_source: str | None = None
    cvss4_base_score: float | None = None
    cvss4_threat_score: float | None = None
    cvss4_vector: str | None = None
    cvss4_threat_vector: str | None = None
    cvss4_supplemental: str | None = None
    cvss4_score_source: str | None = None
    vpr: PluginVpr | None = None
    exploit_available: bool | None = None
    exploitability_ease: str | None = None
    exploited_by_malware: bool | None = None
    exploited_by_nessus: bool | None = None
    exploit_framework_canvas: bool | None = None
    canvas_package: str | None = None
    exploit_framework_core: bool | None = None
    exploit_framework_d2_elliot: bool | None = None
    d2_elliot_name: str | None = None
    exploit_framework_exploithub: bool | None = None
    exploithub_sku: str | None = None
    exploit_framework_metasploit: bool | None = None
    metasploit_name: str | None = None
    unsupported_by_vendor: bool | None = None
    default_account: bool | None = None
    in_the_news: bool | None = None
    has_patch: bool | None = None
    malware: bool | None = None
    agent: str | None = None
    always_run: bool | None = None
    asset_categories: list[str] = Field(default_factory=list)
    asset_inventory: bool | None = None
    asset_inventory_category: str | None = None
    compliance: bool | None = None
    dependencies: list[str] = Field(default_factory=list)
    enable_cgi_scanning: bool | None = None
    excluded_keys: list[str] = Field(default_factory=list)
    fname: str | None = None
    generated_plugin: str | None = None
    hardware_inventory: bool | None = None
    intel_type: str | None = None
    os_identification: bool | None = None
    potential_vulnerability: bool | None = None
    required_keys: list[str] = Field(default_factory=list)
    required_ports: list[str] = Field(default_factory=list)
    required_udp_ports: list[str] = Field(default_factory=list)
    script_copyright: str | None = None
    stig_severity: str | None = None
    thorough_tests: bool | None = None
    vendor_severity: str | None = None
    vendor_unpatched: bool | None = None


class Plugin(BaseModel):
    id: int
    name: str
    family_id: int | None = None
    family_name: str | None = None
    attributes: PluginAttributes | None = None


class PluginListData(BaseModel):
    plugin_details: list[Plugin] = Field(default_factory=list)


class PluginListResponse(BaseModel):
    data: PluginListData
    size: int | None = None
    total_count: int | None = None


class PluginListParams(BaseModel):
    last_updated: date | None = None
    size: Annotated[int | None, Field(ge=1, le=10000)] = None
    page: Annotated[int | None, Field(ge=1)] = None


class PluginDetailAttribute(BaseModel):
    # The details endpoint returns the attributes as raw name/value string pairs, so
    # we leave the values unconverted.
    name: Annotated[str, Field(alias="attribute_name")]
    value: Annotated[str | None, Field(alias="attribute_value")] = None


class PluginDetails(BaseModel):
    id: int
    name: str
    family_name: str | None = None
    attributes: list[PluginDetailAttribute] = Field(default_factory=list)
    vpr: PluginVpr | None = None


class PluginFamily(BaseModel):
    id: int
    name: str
    count: int | None = None


class PluginFamilyListParams(BaseModel):
    all: bool | None = None


class PluginFamilyListResponse(BaseModel):
    families: list[PluginFamily]


class PluginFamilyPlugin(BaseModel):
    id: int
    name: str


class PluginFamilyDetails(BaseModel):
    id: int
    name: str
    plugins: list[PluginFamilyPlugin] = Field(default_factory=list)


class PluginFamilyNameRequest(BaseModel):
    name: str
