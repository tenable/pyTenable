"""
Policy Findings Schema
======================

Schema definitions for Tenable OT Security policy findings.
A policy finding represents one or more policy violations (events) grouped together.
"""
import datetime
import uuid
from dataclasses import dataclass
from typing import List, Optional

from tenable.ot.schema.base import NodesList


@dataclass
class PolicyFindingAssetRisk:
    """
    Risk information for an asset in a policy finding.
    """
    total_risk: float
    unresolved_events: int


@dataclass
class PolicyFindingAsset:
    """
    Asset information within a policy finding.
    Represents either a source or destination asset involved in the policy violation.
    """
    id: uuid.UUID
    name: str
    type: str
    criticality: Optional[str] = None
    location: Optional[str] = None
    purdue_level: Optional[str] = None
    risk: Optional[PolicyFindingAssetRisk] = None


@dataclass
class PolicyFindingAssets(NodesList):
    """
    Collection of assets within a policy finding.
    """
    nodes: List[PolicyFindingAsset]


@dataclass
class EventTypeDetails:
    """
    Event type information for the policy finding.
    """
    type: str
    description: str
    category: str
    family: Optional[str] = None


@dataclass
class PolicyInfo:
    """
    Policy information for the policy finding.
    """
    id: uuid.UUID
    title: str
    level: str
    schema: str
    disabled: bool
    archived: bool
    system: bool


@dataclass
class PolicyFinding:
    """
    A policy violation finding representing one or more grouped policy events.

    Attributes:
        id: Unique identifier for the policy finding
        status: Current status (Active, Resolved, Resurfaced)
        severity: Severity level (Critical, High, Medium, Low, Info)
        category: Event category
        policy_title: Title of the policy that was violated
        first_hit_time: Timestamp when the violation was first detected
        last_hit_time: Timestamp when the violation was last detected
        active_policy_hits: Number of active (non-resolved) events in this finding
        resolved_on: Timestamp when the finding was resolved (if applicable)
        resolved_user: User who resolved the finding (if applicable)
        src_names: List of source asset names involved
        src_ips: List of source IP addresses involved
        dst_names: List of destination asset names involved
        dst_ips: List of destination IP addresses involved
        event_type: Event type information
        policy: Policy information
        src_assets: Source assets involved in the violation
        dst_assets: Destination assets involved in the violation
    """
    id: uuid.UUID
    status: str
    severity: str
    category: str
    policy_title: str
    first_hit_time: datetime.datetime
    last_hit_time: datetime.datetime
    active_policy_hits: int
    event_type: EventTypeDetails
    policy: PolicyInfo
    src_assets: PolicyFindingAssets
    dst_assets: PolicyFindingAssets
    resolved_on: Optional[datetime.datetime] = None
    resolved_user: Optional[str] = None
    src_names: Optional[List[str]] = None
    src_ips: Optional[List[str]] = None
    dst_names: Optional[List[str]] = None
    dst_ips: Optional[List[str]] = None


@dataclass
class PolicyFindings(NodesList):
    """
    Collection of policy findings with iteration support.

    Example:
        >>> findings = tot.policy_findings.list()
        >>> for finding in findings:
        ...     print(f"{finding.policy_title}: {finding.src_names} -> {finding.dst_names}")
    """
    nodes: List[PolicyFinding]
