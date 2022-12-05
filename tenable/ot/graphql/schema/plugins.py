from marshmallow import fields

from tenable.ot.graphql.definitions import NodesSchema, SchemaBase
from tenable.ot.schema.plugins import PluginDetails, Plugin, Plugins, PluginRef


class PluginRefSchema(SchemaBase):
    dataclass = PluginRef

    name = fields.String(required=True)
    value = fields.String(required=True)
    url = fields.String(required=True)


class PluginDetailsSchema(SchemaBase):
    dataclass = PluginDetails

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    source = fields.String(required=True)
    family = fields.String(required=True)
    description = fields.String(required=True)
    solution = fields.String(required=True)
    see_also = fields.List(
        fields.String(required=True), required=True, data_key="seeAlso"
    )
    plugin_type = fields.String(allow_none=True, data_key="pluginType")
    plugin_pub_date = fields.DateTime(allow_none=True, data_key="pluginPubDate")
    plugin_mod_date = fields.DateTime(allow_none=True, data_key="pluginModDate")
    vuln_pub_date = fields.DateTime(allow_none=True, data_key="vulnPubDate")
    vuln_mod_date = fields.DateTime(allow_none=True, data_key="vulnModDate")
    refs = fields.List(fields.Nested(PluginRefSchema, required=True), required=True)
    cpe = fields.String(allow_none=True)
    cvss_vector = fields.String(allow_none=True, data_key="cvssVector")
    cvss_v3_vector = fields.String(allow_none=True, data_key="cvssV3Vector")
    cvss_base_score = fields.String(allow_none=True, data_key="cvssBaseScore")
    cvss_v3_basescore = fields.String(allow_none=True, data_key="cvssV3BaseScore")
    cvss_v3_temporal_score = fields.String(
        allow_none=True, data_key="cvssV3TemporalScore"
    )
    cvss_temporal_score = fields.String(allow_none=True, data_key="cvssTemporalScore")
    cvss_v3_temporal_vector = fields.String(
        allow_none=True, data_key="cvssV3TemporalVector"
    )
    cvss_impact_score = fields.String(allow_none=True, data_key="cvssImpactScore")


class PluginSchema(SchemaBase):
    dataclass = Plugin

    comment = fields.String(allow_none=True)
    family = fields.String(required=True)
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    owner = fields.String(allow_none=True)
    severity = fields.String(required=True)
    source = fields.String(required=True)
    total_affected_assets = fields.Integer(
        required=True, data_key="totalAffectedAssets"
    )
    vpr_score = fields.Float(allow_none=True, data_key="vprScore")
    affected_assets = fields.Nested("AssetListSchema", data_key="affectedAssets")
    details = fields.Nested(PluginDetailsSchema, required=False)


class PluginsSchema(NodesSchema):
    dataclass = Plugins

    nodes = fields.List(fields.Nested(PluginSchema))
