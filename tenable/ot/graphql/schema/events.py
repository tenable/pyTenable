from marshmallow import fields

from tenable.ot.graphql.definitions import NodesSchema, SchemaBase
from tenable.ot.schema.assets import NetworkInterface
from tenable.ot.schema.base import (
    NodesList,
    AssetInfoList,
    AssetInfo,
    IP,
    IPList,
    ID,
    IDList
)
from tenable.ot.schema.events import (
    Event,
    EventTypeDetails,
    Group,
    ConnectionPart,
    EventCount,
    Policy,
    GroupMember,
    Events,
    StationSlot,
    RackSlot,
    ActionList,
    Action,
)


class IDSchema(SchemaBase):
    dataclass = ID
    id = fields.UUID(required=True)


class IDListSchema(SchemaBase):
    dataclass = IDList
    nodes = fields.Nested(IDSchema, required=True, many=True)


class IPSchema(SchemaBase):
    dataclass = IP
    ip = fields.IPv4(required=True)


class IPListSchema(SchemaBase):
    dataclass = IPList
    nodes = fields.Nested(IPSchema, required=True, many=True)


class ActionSchema(SchemaBase):
    dataclass = Action
    aid = fields.UUID(required=True)
    type = fields.String(required=True)


class ActionListSchema(SchemaBase):
    dataclass = ActionList
    nodes = fields.Nested(ActionSchema, required=True, many=True)


class NameListSchema(SchemaBase):
    dataclass = NodesList

    nodes = fields.List(fields.String(required=True), required=True)


class RackSlotSchema(SchemaBase):
    """
    Schema for retrieving rack slots.
    """

    dataclass = RackSlot

    rack = fields.Integer(required=True)
    slot = fields.Integer(required=True)


class StationSlotSchema(SchemaBase):
    """
    Schema for retrieving station slots.
    """

    dataclass = StationSlot

    station = fields.Integer(required=True)
    slot = fields.Integer(required=True)


class ConnectionPartSchema(SchemaBase):
    """
    Schema for retrieving connection parts.
    """

    dataclass = ConnectionPart

    connection_type = fields.Integer(required=True)
    backplane_port = fields.Integer(allow_none=True)
    tsap_addr = fields.Integer(allow_none=True)
    cip_ip = fields.IPv4(allow_none=True)
    control_net_addr = fields.Integer(allow_none=True)
    abb_ac_800_position = fields.Integer(allow_none=True)
    abb_rtu_500_position = fields.Integer(allow_none=True)
    bacnet_instance_id = fields.Integer(allow_none=True)
    roc_slot = fields.Integer(allow_none=True)
    melsec_slot = fields.Integer(allow_none=True)
    toyopuc_addr = fields.Nested(RackSlotSchema)
    concept_addr = fields.Nested(RackSlotSchema)
    bachmann_slot = fields.Nested(StationSlotSchema)
    s_7_plus_addr = fields.Nested(RackSlotSchema)
    s_7_addr = fields.Nested(RackSlotSchema)
    ge_pac_addr = fields.Nested(RackSlotSchema)


class GroupSchema(SchemaBase):
    dataclass = Group

    id = fields.UUID(required=True)
    name = fields.String(allow_none=True)
    type = fields.String(allow_none=True)
    archived = fields.Boolean(allow_none=True)
    system = fields.Boolean(allow_none=True)
    key = fields.String(allow_none=True)


class EventTypeDetailsSchema(SchemaBase):
    dataclass = EventTypeDetails

    type = fields.String(required=True)
    group = fields.String(required=True)
    description = fields.String(required=True)
    schema = fields.String(required=True)
    category = fields.String(required=True)
    family = fields.String(allow_none=True)
    can_capture = fields.Boolean(required=True, data_key="canCapture")
    actions = fields.List(fields.String(required=True), required=True)
    exclusion = fields.String(required=True)


class GroupMemberSchema(SchemaBase):
    dataclass = GroupMember

    group = fields.Nested(GroupSchema, required=True)
    negate = fields.Boolean(required=True)


class ProtocolPolicyGroupSchema(SchemaBase):
    id = fields.UUID(required=True)
    name = fields.String(required=True)
    disabled = fields.Boolean(required=True)
    archived = fields.Boolean(allow_none=True)


class EventCountSchema(SchemaBase):
    dataclass = EventCount

    last_24h = fields.Integer(required=True, data_key="last24h")
    last_7d = fields.Integer(required=True, data_key="last7d")
    last_30d = fields.Integer(required=True, data_key="last30d")


class PolicySchema(SchemaBase):
    dataclass = Policy

    id = fields.UUID(required=True)
    index = fields.Integer(required=True)
    title = fields.String(required=True)
    level = fields.String(required=True)
    disabled = fields.Boolean(required=True)
    archived = fields.Boolean(allow_none=True)
    schema = fields.String(required=True)
    continuous = fields.Boolean(required=True)
    snapshot = fields.Boolean()
    system = fields.Boolean(allow_none=True)
    key = fields.String(required=True)
    event_type_details = fields.Nested(
        EventTypeDetailsSchema, required=True, data_key="eventTypeDetails"
    )
    disable_after_hit = fields.Boolean(required=True, data_key="disableAfterHit")
    actions = fields.Nested(ActionListSchema, required=True)
    paused = fields.Boolean(required=True)
    src_asset_group = fields.List(
        fields.Nested(GroupMemberSchema, required=True, many=True),
        data_key="srcAssetGroup",
    )
    dst_asset_group = fields.List(
        fields.Nested(GroupMemberSchema, required=True, many=True),
        data_key="dstAssetGroup",
    )
    schedule = fields.Nested(GroupMemberSchema, allow_none=True)
    protocol_group = fields.Nested(
        GroupMemberSchema, allow_none=True, data_key="protocolGroup"
    )
    port_group = fields.Nested(GroupMemberSchema, allow_none=True, data_key="portGroup")
    tag_group = fields.Nested(GroupMemberSchema, allow_none=True, data_key="tagGroup")
    value_group = fields.Nested(
        GroupMemberSchema, allow_none=True, data_key="valueGroup"
    )
    rule_group = fields.Nested(GroupMemberSchema, allow_none=True, data_key="ruleGroup")
    exclusions = fields.Nested(IDListSchema)
    aggregated_events_count = fields.Nested(
        EventCountSchema, required=True, data_key="aggregatedEventsCount"
    )


class DnsListSchema(SchemaBase):
    dataclass = NodesList

    nodes = fields.List(fields.String(required=True), required=True)


class NetworkInterfaceSchema(SchemaBase):
    dataclass = NetworkInterface

    id = fields.UUID(required=True)
    last_seen = fields.DateTime(allow_none=True, data_key="lastSeen")
    first_seen = fields.DateTime(allow_none=True, data_key="firstSeen")
    mac = fields.String(allow_none=True)
    ips = fields.Nested(IPListSchema, required=True)
    family = fields.String(required=True)
    direct_asset = fields.Nested(IDSchema, allow_none=True, data_key="directAsset")
    dns_names = fields.Nested(DnsListSchema, required=True, data_key="dnsNames")


class AssetInfoSchema(SchemaBase):
    dataclass = AssetInfo

    id = fields.UUID(required=True)
    name = fields.String(required=True)


class AssetListSchema(SchemaBase):
    dataclass = AssetInfoList

    nodes = fields.Nested(AssetInfoSchema, many=True, required=True)


class EventSchema(SchemaBase):
    """
    Schema for retrieving events.
    """

    dataclass = Event

    id = fields.UUID(required=True)
    event_type = fields.Nested(
        EventTypeDetailsSchema, required=True, data_key="eventType"
    )
    src_ip = fields.IPv4(allow_none=True, data_key="srcIP")
    dst_ip = fields.IPv4(allow_none=True, data_key="dstIP")
    protocol_raw = fields.String(required=True, data_key="protocolRaw")
    policy = fields.Nested(PolicySchema, required=True)
    time = fields.DateTime(required=True)
    src_mac = fields.String(allow_none=True, data_key="srcMac")
    dst_mac = fields.String(allow_none=True, data_key="dstMac")
    completion = fields.String(required=True)
    protocol_nice_name = fields.String(allow_none=True, data_key="protocolNiceName")
    resolved = fields.Boolean(required=True)
    resolved_ts = fields.DateTime(allow_none=True, data_key="resolvedTs")
    severity = fields.String(required=True)
    category = fields.String(required=True)
    comment = fields.String(allow_none=True)
    hit_id = fields.UUID(required=True, data_key="hitId")
    log_id = fields.Float(required=True, data_key="logId")
    resolved_user = fields.String(allow_none=True, data_key="resolvedUser")
    type = fields.String(required=True)
    src_assets = fields.Nested(AssetListSchema, required=True, data_key="srcAssets")
    src_interface = fields.Nested(
        NetworkInterfaceSchema, allow_none=True, data_key="srcInterface"
    )
    src_names = fields.Nested(NameListSchema, required=True, data_key="srcNames")
    dst_assets = fields.Nested(AssetListSchema, required=True, data_key="dstAssets")
    dst_interface = fields.Nested(
        NetworkInterfaceSchema, allow_none=True, data_key="dstInterface"
    )
    dst_names = fields.Nested(NameListSchema, required=True, data_key="dstNames")
    has_details = fields.Boolean(required=True, data_key="hasDetails")
    payload_size = fields.Integer(required=True, data_key="payloadSize")
    protocol = fields.String(required=True)
    port = fields.Integer(allow_none=True)
    details = fields.Dict(allow_none=True)
    continuous = fields.Boolean(required=True)


class EventsSchema(NodesSchema):
    dataclass = Events
    nodes = fields.List(fields.Nested(EventSchema), required=True)
