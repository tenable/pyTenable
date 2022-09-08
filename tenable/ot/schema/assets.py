import datetime
import uuid
from dataclasses import dataclass
from typing import List

from tenable.ot.schema.base import NodesList


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

    id: uuid.UUID
    name: str
    size: str


@dataclass
class Segment:
    """
    This class holds a segment's information.
    """

    id: uuid.UUID
    name: str
    type: str
    key: str
    system_name: str = None
    vlan: str = None
    description: str = None
    asset_type: str = None
    subnet: str = None


@dataclass
class Segments(NodesList):
    nodes: List[Segment]


@dataclass
class Revision:
    """
    This class holds a revision's information.
    """

    first_seen: datetime.datetime
    id: uuid.UUID
    is_base: bool
    last_seen: datetime.datetime
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

    backplane: Backplane
    category: str
    criticality: str
    description: str
    details: dict
    family: str
    firmware_version: str
    first_seen: datetime.datetime
    hidden: bool
    id: uuid.UUID
    ips: NodesList
    last_seen: datetime.datetime
    last_update: str
    location: str
    macs: NodesList
    model: str
    name: str
    os: str
    os_details: OSDetails
    purdue_level: str
    revisions: Revisions
    risk: Risk
    run_status: str
    run_status_time: datetime.datetime
    segments: Segments
    serial: str
    slot: int
    super_type: str
    type: str
    vendor: str
    custom_field1: str = None
    custom_field2: str = None
    custom_field3: str = None
    custom_field4: str = None
    custom_field5: str = None
    custom_field6: str = None
    custom_field7: str = None
    custom_field8: str = None
    custom_field9: str = None
    custom_field10: str = None


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
    first_seen: datetime.datetime
    id: uuid.UUID
    ips: str
    last_seen: datetime.datetime
    mac: str
