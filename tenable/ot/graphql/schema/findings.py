"""
GraphQL Schema for Findings
============================

Marshmallow schemas for deserializing GraphQL findings responses into Python dataclasses.
"""
from marshmallow import fields

from tenable.ot.graphql.definitions import NodesSchema, SchemaBase
from tenable.ot.schema.findings import (
    Finding,
    Findings,
    FindingAsset,
    FindingAssetRisk,
    FindingAssetIPs,
    FindingAssetMACs,
    FindingPlugin,
    FindingPluginDetails,
    PluginRef,
)


class PluginRefSchema(SchemaBase):
    """Schema for plugin reference (CVE, BID, etc.)"""
    dataclass = PluginRef

    name = fields.String(required=True)
    value = fields.String(required=True)
    url = fields.String(required=True)


class FindingPluginDetailsSchema(SchemaBase):
    """Schema for detailed plugin/vulnerability information"""
    dataclass = FindingPluginDetails

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    solution = fields.String(allow_none=True)
    see_also = fields.List(
        fields.String(), allow_none=True, data_key="seeAlso"
    )
    plugin_type = fields.String(allow_none=True, data_key="pluginType")
    plugin_pub_date = fields.DateTime(allow_none=True, data_key="pluginPubDate")
    plugin_mod_date = fields.DateTime(allow_none=True, data_key="pluginModDate")
    vuln_pub_date = fields.DateTime(allow_none=True, data_key="vulnPubDate")
    vuln_mod_date = fields.DateTime(allow_none=True, data_key="vulnModDate")
    refs = fields.List(
        fields.Nested(PluginRefSchema), allow_none=True
    )
    cpe = fields.String(allow_none=True)
    cvss_vector = fields.String(allow_none=True, data_key="cvssVector")
    cvss_v3_vector = fields.String(allow_none=True, data_key="cvssV3Vector")
    cvss_base_score = fields.Float(allow_none=True, data_key="cvssBaseScore")
    cvss_v3_base_score = fields.Float(allow_none=True, data_key="cvssV3BaseScore")
    cvss_temporal_score = fields.Float(allow_none=True, data_key="cvssTemporalScore")
    cvss_v3_temporal_score = fields.Float(allow_none=True, data_key="cvssV3TemporalScore")
    cvss_impact_score = fields.Float(allow_none=True, data_key="cvssImpactScore")


class FindingPluginSchema(SchemaBase):
    """Schema for plugin information within a finding"""
    dataclass = FindingPlugin

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    severity = fields.String(required=True)
    family = fields.String(required=True)
    source = fields.String(required=True)
    vpr_score = fields.Float(allow_none=True, data_key="vprScore")
    comment = fields.String(allow_none=True)
    owner = fields.String(allow_none=True)
    details = fields.Nested(FindingPluginDetailsSchema, allow_none=True)


class FindingAssetRiskSchema(SchemaBase):
    """Schema for asset risk information"""
    dataclass = FindingAssetRisk

    total_risk = fields.Float(required=True, data_key="totalRisk")
    unresolved_events = fields.Integer(required=True, data_key="unresolvedEvents")


class FindingAssetIPsSchema(SchemaBase):
    """Schema for asset IP addresses"""
    dataclass = FindingAssetIPs

    nodes = fields.List(fields.String(), required=True)


class FindingAssetMACsSchema(SchemaBase):
    """Schema for asset MAC addresses"""
    dataclass = FindingAssetMACs

    nodes = fields.List(fields.String(), required=True)


class FindingAssetSchema(SchemaBase):
    """Schema for asset information within a finding"""
    dataclass = FindingAsset

    id = fields.UUID(required=True)
    name = fields.String(required=True)
    type = fields.String(required=True)
    criticality = fields.String(allow_none=True)
    location = fields.String(allow_none=True)
    purdue_level = fields.String(allow_none=True, data_key="purdueLevel")
    risk = fields.Nested(FindingAssetRiskSchema, allow_none=True)
    ips = fields.Nested(FindingAssetIPsSchema, allow_none=True)
    macs = fields.Nested(FindingAssetMACsSchema, allow_none=True)


class FindingSchema(SchemaBase):
    """
    Schema for a security finding.

    Maps GraphQL finding response to Finding dataclass.
    """
    dataclass = Finding

    id = fields.String(required=True)
    status = fields.String(required=True)
    first_hit = fields.DateTime(required=True, data_key="firstHit")
    last_hit = fields.DateTime(required=True, data_key="lastHit")
    fixed_at = fields.DateTime(allow_none=True, data_key="fixedAt")
    port = fields.Integer(required=True)
    protocol = fields.String(required=True)
    svc_name = fields.String(allow_none=True, data_key="svcName")
    output = fields.String(allow_none=True)
    asset = fields.Nested(FindingAssetSchema, required=True)
    plugin = fields.Nested(FindingPluginSchema, required=True)


class FindingsSchema(NodesSchema):
    """
    Schema for a collection of findings.

    Handles pagination and deserialization of multiple findings.
    """
    dataclass = Findings

    nodes = fields.List(fields.Nested(FindingSchema))
