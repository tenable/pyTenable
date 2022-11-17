import datetime
from dataclasses import dataclass
from typing import List, Optional

from tenable.ot.schema.base import AssetInfoList, NodesList


@dataclass
class PluginRef:
    name: str
    value: str
    url: str


@dataclass
class PluginDetails:
    id: int
    name: str
    source: str
    family: str
    description: str
    cpe: Optional[str] = None
    cvss_base_score: Optional[str] = None
    cvss_impact_score: Optional[str] = None
    cvss_temporal_score: Optional[str] = None
    cvss_v3_basescore: Optional[str] = None
    cvss_v3_temporal_score: Optional[str] = None
    cvss_v3_temporal_vector: Optional[str] = None
    cvss_v3_vector: Optional[str] = None
    cvss_vector: Optional[str] = None
    plugin_mod_date: Optional[datetime.datetime] = None
    plugin_pub_date: Optional[datetime.datetime] = None
    plugin_type: Optional[str] = None
    refs: Optional[List[PluginRef]] = None
    see_also: Optional[List[str]] = None
    solution: Optional[str] = None
    vuln_mod_date: Optional[datetime.datetime] = None
    vuln_pub_date: Optional[datetime.datetime] = None


@dataclass
class Plugin:
    family: str
    id: int
    name: str

    source: str
    severity: str
    total_affected_assets: int

    comment: Optional[str] = None
    vpr_score: Optional[float] = None
    owner: Optional[str] = None
    details: Optional[PluginDetails] = None
    affected_assets: Optional[AssetInfoList] = None


@dataclass
class Plugins(NodesList):
    nodes: List[Plugin]
