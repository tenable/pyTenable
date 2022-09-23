from datetime import datetime
from uuid import UUID
from dataclasses import dataclass
from typing import List, Optional

from tenable.ot.schema.base import NodesList
from tenable.ot.schema.plugins import Plugin


@dataclass
class Risk:
    """
    This class holds the risk information.
    """

    unresolved_events: int
    total_risk: float


@dataclass
class Backplane:
    """
    This class holds a backplane's information.
    """

    id: UUID
    name: str
    size: str


@dataclass
class Segment:
    """
    This class holds a segment's information.
    """

    id: UUID
    name: str
    type: str
    key: str
    system_name: Optional[str] = None
    vlan: Optional[str] = None
    description: Optional[str] = None
    asset_type: Optional[str] = None
    subnet: Optional[str] = None


@dataclass
class Segments(NodesList):
    nodes: List[Segment]


@dataclass
class Revision:
    """
    This class holds a revision's information.
    """

    first_seen: datetime
    id: UUID
    is_base: bool
    last_seen: datetime
    ordinal: int


@dataclass
class Revisions:
    nodes: List[Revision]


@dataclass
class OSDetails:
    name: str
    architecture: str


@dataclass
class Asset:
    """
    This class holds asset information.
    """

    category: str
    criticality: str
    details: dict
    family: str
    firmware_version: str
    first_seen: datetime
    hidden: bool
    id: UUID
    ips: NodesList
    last_seen: datetime
    last_update: str
    macs: NodesList
    model: str
    name: str
    plugins: List[Plugin]
    purdue_level: str
    revisions: Revisions
    risk: Risk
    run_status: str
    run_status_time: datetime
    segments: Segments
    serial: str
    super_type: str
    type: str
    vendor: str
    backplane: Optional[Backplane] = None
    description: Optional[str] = None
    location: Optional[str] = None
    os: Optional[str] = None
    os_details: Optional[OSDetails] = None
    slot: Optional[int] = None
    custom_field1: Optional[str] = None
    custom_field2: Optional[str] = None
    custom_field3: Optional[str] = None
    custom_field4: Optional[str] = None
    custom_field5: Optional[str] = None
    custom_field6: Optional[str] = None
    custom_field7: Optional[str] = None
    custom_field8: Optional[str] = None
    custom_field9: Optional[str] = None
    custom_field10: Optional[str] = None


@dataclass
class Assets(NodesList):
    nodes: List[Asset]


@dataclass
class NetworkInterface:
    """
    This class holds a network interface's information.
    """

    direct_asset: Asset
    family: str
    first_seen: datetime
    id: UUID
    ips: str
    last_seen: datetime
    mac: str
