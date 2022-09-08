import datetime
import ipaddress
import uuid
from dataclasses import dataclass
from typing import List

from tenable.ot.schema.assets import NetworkInterface
from tenable.ot.schema.base import NodesList, AssetInfoList


@dataclass
class Group:
    id: uuid.UUID
    name: str = None
    type: str = None
    archived: bool = None
    system: bool = None
    key: str = None


@dataclass
class GroupMember:
    group: Group
    negate: bool


@dataclass
class GroupMember:
    group: Group
    negate: bool


@dataclass
class EventTypeDetails:
    type: str
    group: str
    description: str
    schema: str
    category: str
    family: str
    can_capture: bool
    actions: List[str]
    exclusion: str


@dataclass
class EventCount:
    last_24h: int
    last_7d: int
    last_30d: int


@dataclass
class Policy:
    """
    This class holds a policy's information.
    """

    id: uuid.UUID
    index: int
    title: str
    level: str
    disabled: bool
    archived: bool
    schema: str
    continuous: bool
    snapshot: bool
    system: bool
    key: str
    event_type_details: EventTypeDetails
    disable_after_hit: bool
    actions: NodesList
    paused: bool
    src_asset_group: List[List[GroupMember]]
    dst_asset_group: List[List[GroupMember]]
    schedule: GroupMember
    protocol_group: GroupMember
    port_group: List[GroupMember]
    tag_group: List[GroupMember]
    value_group: List[GroupMember]
    rule_group: List[GroupMember]
    exclusions: NodesList
    aggregated_events_count: EventCount


@dataclass
class Event:
    """
    Schema for retrieving events.
    """

    category: str
    comment: str
    completion: str
    continuous: bool
    dst_assets: AssetInfoList
    dst_interface: List[NetworkInterface]
    dst_ip: ipaddress.IPv4Address
    dst_mac: str
    dst_names: NodesList
    event_type: EventTypeDetails
    has_details: bool
    hit_id: uuid.UUID
    id: uuid.UUID
    log_id: float
    payload_size: int
    policy: Policy
    port: int
    protocol: str
    protocol_nice_name: str
    protocol_raw: str
    resolved: bool
    resolved_ts: datetime.datetime
    resolved_user: str
    severity: str
    src_assets: AssetInfoList
    src_interface: List[NetworkInterface]
    src_ip: ipaddress.IPv4Address
    src_mac: str
    src_names: NodesList
    time: datetime.datetime
    type: str


@dataclass
class Events(NodesList):
    nodes: List[Event]


@dataclass
class RackSlot:
    rack: int
    slot: int


@dataclass
class StationSlot:
    """
    Schema for retrieving station slots.
    """

    station: int
    slot: int


@dataclass
class ConnectionPart:
    connection_type: int
    backplane_port: int
    tsap_addr: int
    cip_ip: str
    control_net_addr: int
    abb_ac_800_position: int
    abb_rtu_500_position: int
    bacnet_instance_id: int
    roc_slot: int
    melsec_slot: int
    toyopuc_addr: RackSlot
    concept_addr: RackSlot
    bachmann_slot: StationSlot
    s_7_plus_addr: RackSlot
    s_7_addr: RackSlot
    ge_pac_addr: RackSlot


@dataclass
class EventCount:
    last_24h: int
    last_7d: int
    last_30d: int
