from datetime import datetime
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
    solution: str
    see_also: List[str]
    plugin_type: Optional[str]
    plugin_pub_date: Optional[datetime]
    plugin_mod_date: Optional[datetime]
    vuln_pub_date: Optional[datetime]
    vuln_mod_date: Optional[datetime]
    refs: List[PluginRef]
    cvss_vector: str
    cvss_v3_vector: str
    cvss_base_score: str
    cvss_v3_basescore: str
    cvss_v3_temporal_score: str
    cvss_temporal_score: str
    cvss_v3_temporal_vector: str
    cvss_impact_score: Optional[str]
    cpe: Optional[str] = None


@dataclass
class Plugin:
    comment: Optional[str]
    family: str
    id: int
    name: str
    owner: Optional[str]
    source: Optional[str]
    severity: str
    total_affected_assets: int
    vpr_score: Optional[float]
    details: Optional[PluginDetails] = None
    affected_assets: Optional[AssetInfoList] = None


@dataclass
class Plugins(NodesList):
    nodes = List[Plugin]
