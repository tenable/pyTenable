"""
Findings Schema
================

Schema definitions for Tenable OT Security findings.
A finding represents a detected vulnerability (plugin) on a specific asset.
"""
import datetime
import uuid
from dataclasses import dataclass
from typing import List, Optional

from tenable.ot.schema.base import NodesList


@dataclass
class FindingAssetRisk:
    """
    Risk information for an asset in a finding.
    """
    total_risk: float
    unresolved_events: int


@dataclass
class FindingAssetIPs:
    """
    IP addresses associated with an asset in a finding.
    """
    nodes: List[str]


@dataclass
class FindingAssetMACs:
    """
    MAC addresses associated with an asset in a finding.
    """
    nodes: List[str]


@dataclass
class FindingAsset:
    """
    Asset information within a finding.
    Contains basic asset details to identify which asset has the vulnerability.
    """
    id: uuid.UUID
    name: str
    type: str
    criticality: Optional[str] = None
    location: Optional[str] = None
    purdue_level: Optional[str] = None
    risk: Optional[FindingAssetRisk] = None
    ips: Optional[FindingAssetIPs] = None
    macs: Optional[FindingAssetMACs] = None


@dataclass
class PluginRef:
    """
    Reference information for a plugin (CVE, BID, etc.).
    """
    name: str
    value: str
    url: str


@dataclass
class FindingPluginDetails:
    """
    Detailed information about a plugin/vulnerability.
    """
    id: int
    name: str
    description: Optional[str] = None
    solution: Optional[str] = None
    see_also: Optional[List[str]] = None
    plugin_type: Optional[str] = None
    plugin_pub_date: Optional[datetime.datetime] = None
    plugin_mod_date: Optional[datetime.datetime] = None
    vuln_pub_date: Optional[datetime.datetime] = None
    vuln_mod_date: Optional[datetime.datetime] = None
    refs: Optional[List[PluginRef]] = None
    cpe: Optional[str] = None
    cvss_vector: Optional[str] = None
    cvss_v3_vector: Optional[str] = None
    cvss_base_score: Optional[float] = None
    cvss_v3_base_score: Optional[float] = None
    cvss_temporal_score: Optional[float] = None
    cvss_v3_temporal_score: Optional[float] = None
    cvss_impact_score: Optional[float] = None


@dataclass
class FindingPlugin:
    """
    Plugin (vulnerability check) information within a finding.
    Contains details about what vulnerability was detected.
    """
    id: int
    name: str
    severity: str
    family: str
    source: str
    vpr_score: Optional[float] = None
    comment: Optional[str] = None
    owner: Optional[str] = None
    details: Optional[FindingPluginDetails] = None


@dataclass
class Finding:
    """
    A security finding representing a detected vulnerability on an asset.

    Attributes:
        id: Unique identifier for the finding (SHA256 hash)
        status: Current status (Active, Resolved, Resurfaced)
        first_hit: Timestamp when the finding was first detected
        last_hit: Timestamp when the finding was last detected
        fixed_at: Timestamp when the finding was marked as resolved (if applicable)
        port: Network port number where the vulnerability was detected
        protocol: Network protocol (tcp, udp, etc.)
        svc_name: Service name running on the port
        output: Plugin output/details from the detection
        asset: Asset information where the finding was detected
        plugin: Plugin/vulnerability information
    """
    id: str
    status: str
    first_hit: datetime.datetime
    last_hit: datetime.datetime
    port: int
    protocol: str
    asset: FindingAsset
    plugin: FindingPlugin
    fixed_at: Optional[datetime.datetime] = None
    svc_name: Optional[str] = None
    output: Optional[str] = None


@dataclass
class Findings(NodesList):
    """
    Collection of findings with iteration support.

    Example:
        >>> findings = tot.findings.list()
        >>> for finding in findings:
        ...     print(f"{finding.asset.name}: {finding.plugin.name}")
    """
    nodes: List[Finding]
