import datetime
import ipaddress
import typing
import uuid
from typing import List, Optional

from dataclasses import dataclass

from tenable.ot.schema.base import NodesList, IPList, ID
from tenable.ot.schema.plugins import Plugin, Plugins


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

    first_seen: datetime.datetime
    id: uuid.UUID
    is_base: bool
    last_seen: datetime.datetime
    ordinal: int


@dataclass
class Revisions:
    nodes: List[Revision]


@dataclass
class Hotfix:
    name: str
    install_date: datetime
    description: str


@dataclass
class HotFixes:
    nodes: typing.List[Hotfix]


@dataclass
class OSDetails:
    name: str
    architecture: str
    version: Optional[str]
    hot_fixes: HotFixes


@dataclass
class Asset:
    """
    This class holds asset information.
    """

    category: str
    criticality: str
    details: dict
    first_seen: datetime.datetime
    hidden: bool
    id: uuid.UUID
    ips: NodesList
    last_seen: datetime.datetime
    last_update: str
    macs: NodesList
    name: str
    plugins: Plugins
    purdue_level: str
    revisions: Revisions
    risk: Risk
    run_status: str
    run_status_time: datetime.datetime
    segments: Segments
    super_type: str
    type: str
    backplane: Optional[Backplane] = None
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
    description: Optional[str] = None
    family: Optional[str] = None
    firmware_version: Optional[str] = None
    location: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None
    os_details: Optional[OSDetails] = None
    serial: Optional[str] = None
    slot: Optional[int] = None
    vendor: Optional[str] = None


@dataclass
class Assets(NodesList):
    nodes: List[Asset]


@dataclass
class NetworkInterface:
    """
    This class holds a network interface's information.
    """

    id: uuid.UUID
    last_seen: datetime.datetime
    first_seen: datetime.datetime
    mac: str
    family: str
    direct_asset: ID
    ips: IPList
    dns_names: NodesList
