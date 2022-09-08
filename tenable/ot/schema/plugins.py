import datetime
from dataclasses import dataclass
from typing import List

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
    plugin_type: str
    plugin_pub_date: datetime.datetime
    plugin_mod_date: datetime.datetime
    vuln_pub_date: datetime.datetime
    vuln_mod_date: datetime.datetime
    refs: List[PluginRef]
    cpe: str
    cvss_vector: str
    cvss_v3_vector: str
    cvss_base_score: str
    cvss_v3_basescore: str
    cvss_v3_temporal_score: str
    cvss_temporal_score: str
    cvss_v3_temporal_vector: str
    cvss_impact_score: str


@dataclass
class Plugin:
    comment: str
    family: str
    id: int
    name: str
    owner: str
    source: str
    severity: str
    total_affected_assets: int
    vpr_score: float
    details: PluginDetails = None
    affected_assets: AssetInfoList = None


@dataclass
class Plugins(NodesList):
    nodes = List[Plugin]
