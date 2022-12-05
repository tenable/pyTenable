from marshmallow import fields

from tenable.ot.graphql.definitions import NodesSchema, SchemaBase
from tenable.ot.graphql.schema.plugins import PluginsSchema
from tenable.ot.schema.assets import (
    Risk,
    Backplane,
    Segment,
    Asset,
    Assets,
    Revision,
    Revisions,
    Segments,
    OSDetails,
    HotFixes,
    Hotfix,
)
from tenable.ot.schema.base import NodesList


class RiskSchema(SchemaBase):
    """
    Schema for retrieving asset's risk information.
    """

    dataclass = Risk

    unresolved_events = fields.Int(required=True, data_key="unresolvedEvents")
    total_risk = fields.Float(required=True, data_key="totalRisk")


class IpsSchema(NodesSchema):
    """
    Schema for retrieving a list of IP addresses.
    """

    dataclass = NodesList

    nodes = fields.List(fields.String())


class MacsSchema(NodesSchema):
    """
    Schema for retrieving a list of MAC addresses.
    """

    dataclass = NodesList

    nodes = fields.List(fields.String())


class BackplaneSchema(SchemaBase):
    """
    Schema for retrieving backplane information.
    """

    dataclass = Backplane

    id = fields.String(required=True)
    name = fields.String(required=True)
    size = fields.Int(required=True)


class SegmentSchema(SchemaBase):
    """
    Schema for retrieving segment information.
    """

    dataclass = Segment

    id = fields.UUID(required=True)
    name = fields.String(required=True)
    type = fields.String(required=True)
    key = fields.String(required=True)
    system_name = fields.String(allow_none=True, data_key="systemName")
    vlan = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    asset_type = fields.String(allow_none=True, data_key="assetType")
    subnet = fields.String(allow_none=True)


class HotfixSchema(SchemaBase):
    dataclass = Hotfix

    name = fields.String(required=True)
    install_date = fields.DateTime(required=True, data_key="installDate")
    description = fields.String(required=True)


class HotfixesSchema(NodesSchema):
    dataclass = HotFixes
    nodes = fields.Nested(HotfixSchema, many=True)


class OSSchema(SchemaBase):
    dataclass = OSDetails
    name = fields.String(allow_none=True)
    architecture = fields.String(allow_none=True)
    version = fields.String(allow_none=True)
    hot_fixes = fields.Nested(HotfixesSchema, data_key="hotFixes")


class SegmentsSchema(NodesSchema):
    """
    Schema for retrieving a list of segments.
    """

    dataclass = Segments

    nodes = fields.List(fields.Nested(SegmentSchema))


class RevisionSchema(SchemaBase):
    dataclass = Revision

    id = fields.UUID(required=True)
    first_seen = fields.DateTime(required=True, data_key="firstSeen")
    last_seen = fields.DateTime(required=True, data_key="lastSeen")
    ordinal = fields.Integer(required=True)
    is_base = fields.Boolean(required=True, data_key="isBase")


class RevisionsSchema(NodesSchema):
    dataclass = Revisions

    nodes = fields.List(fields.Nested(RevisionSchema))


class AssetSchema(SchemaBase):
    """
    Schema for retrieving asset information.
    """

    dataclass = Asset

    backplane = fields.Nested(BackplaneSchema, allow_none=True)
    category = fields.String(required=True)
    criticality = fields.String(required=True)
    custom_field1 = fields.String(allow_none=True, data_key="customField1")
    custom_field2 = fields.String(allow_none=True, data_key="customField2")
    custom_field3 = fields.String(allow_none=True, data_key="customField3")
    custom_field4 = fields.String(allow_none=True, data_key="customField4")
    custom_field5 = fields.String(allow_none=True, data_key="customField5")
    custom_field6 = fields.String(allow_none=True, data_key="customField6")
    custom_field7 = fields.String(allow_none=True, data_key="customField7")
    custom_field8 = fields.String(allow_none=True, data_key="customField8")
    custom_field9 = fields.String(allow_none=True, data_key="customField9")
    custom_field10 = fields.String(allow_none=True, data_key="customField10")
    description = fields.String(allow_none=True)
    details = fields.Dict(required=True)
    family = fields.String(allow_none=True)
    firmware_version = fields.String(allow_none=True, data_key="firmwareVersion")
    first_seen = fields.DateTime(allow_none=True, data_key="firstSeen")
    hidden = fields.Boolean(required=True)
    id = fields.UUID(required=True)
    ips = fields.Nested(IpsSchema, allow_none=True)
    last_seen = fields.DateTime(allow_none=True, data_key="lastSeen")
    last_update = fields.String(required=True, data_key="lastUpdate")
    location = fields.String(allow_none=True)
    macs = fields.Nested(MacsSchema, allow_none=True)
    model = fields.String(allow_none=True)
    name = fields.String(required=True)
    os = fields.String(allow_none=True)
    os_details = fields.Nested(OSSchema, allow_none=True, data_key="osDetails")
    purdue_level = fields.String(required=True, data_key="purdueLevel")
    risk = fields.Nested(RiskSchema, required=True)
    revisions = fields.Nested(RevisionsSchema, allow_none=True)
    run_status = fields.String(required=True, data_key="runStatus")
    run_status_time = fields.DateTime(required=True, data_key="runStatusTime")
    segments = fields.Nested(SegmentsSchema, allow_none=True)
    serial = fields.String(allow_none=True)
    slot = fields.Integer(allow_none=True)
    super_type = fields.String(required=True, data_key="superType")
    type = fields.String(required=True)
    vendor = fields.String(allow_none=True)
    plugins = fields.Nested(PluginsSchema)
    attack_vector = fields.String(data_key="attackVector")


class AssetsSchema(NodesSchema):
    """
    Schema for retrieving a list of assets.
    """

    dataclass = Assets

    nodes = fields.List(fields.Nested(AssetSchema))
