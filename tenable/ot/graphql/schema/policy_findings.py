"""
GraphQL Schema for Policy Findings
===================================

Marshmallow schemas for deserializing GraphQL policy findings responses into Python dataclasses.
"""
from marshmallow import fields

from tenable.ot.graphql.definitions import NodesSchema, SchemaBase
from tenable.ot.schema.policy_findings import (
    PolicyFinding,
    PolicyFindings,
    PolicyFindingAsset,
    PolicyFindingAssets,
    PolicyFindingAssetRisk,
    EventTypeDetails,
    PolicyInfo,
)


class PolicyFindingAssetRiskSchema(SchemaBase):
    """Schema for asset risk information"""
    dataclass = PolicyFindingAssetRisk

    total_risk = fields.Float(required=True, data_key="totalRisk")
    unresolved_events = fields.Integer(required=True, data_key="unresolvedEvents")


class PolicyFindingAssetSchema(SchemaBase):
    """Schema for asset information within a policy finding"""
    dataclass = PolicyFindingAsset

    id = fields.UUID(required=True)
    name = fields.String(required=True)
    type = fields.String(required=True)
    criticality = fields.String(allow_none=True)
    location = fields.String(allow_none=True)
    purdue_level = fields.String(allow_none=True, data_key="purdueLevel")
    risk = fields.Nested(PolicyFindingAssetRiskSchema, allow_none=True)


class PolicyFindingAssetsSchema(NodesSchema):
    """Schema for collection of assets"""
    dataclass = PolicyFindingAssets

    nodes = fields.List(fields.Nested(PolicyFindingAssetSchema))


class EventTypeDetailsSchema(SchemaBase):
    """Schema for event type information"""
    dataclass = EventTypeDetails

    type = fields.String(required=True)
    description = fields.String(required=True)
    category = fields.String(required=True)
    family = fields.String(allow_none=True)


class PolicyInfoSchema(SchemaBase):
    """Schema for policy information"""
    dataclass = PolicyInfo

    id = fields.UUID(required=True)
    title = fields.String(required=True)
    level = fields.String(required=True)
    schema = fields.String(required=True)
    disabled = fields.Boolean(required=True)
    archived = fields.Boolean(required=True)
    system = fields.Boolean(required=True)


class PolicyFindingSchema(SchemaBase):
    """
    Schema for a policy violation finding.

    Maps GraphQL policy finding response to PolicyFinding dataclass.
    """
    dataclass = PolicyFinding

    id = fields.UUID(required=True)
    status = fields.String(required=True)
    severity = fields.String(required=True)
    category = fields.String(required=True)
    policy_title = fields.String(required=True, data_key="policyTitle")
    first_hit_time = fields.DateTime(required=True, data_key="firstHitTime")
    last_hit_time = fields.DateTime(required=True, data_key="lastHitTime")
    active_policy_hits = fields.Integer(required=True, data_key="activePolicyHits")
    resolved_on = fields.DateTime(allow_none=True, data_key="resolvedOn")
    resolved_user = fields.String(allow_none=True, data_key="resolvedUser")
    src_names = fields.List(fields.String(), allow_none=True, data_key="srcNames")
    src_ips = fields.List(fields.String(), allow_none=True, data_key="srcIps")
    dst_names = fields.List(fields.String(), allow_none=True, data_key="dstNames")
    dst_ips = fields.List(fields.String(), allow_none=True, data_key="dstIps")
    event_type = fields.Nested(EventTypeDetailsSchema, required=True, data_key="eventType")
    policy = fields.Nested(PolicyInfoSchema, required=True)
    src_assets = fields.Nested(PolicyFindingAssetsSchema, required=True, data_key="srcAssets")
    dst_assets = fields.Nested(PolicyFindingAssetsSchema, required=True, data_key="dstAssets")


class PolicyFindingsSchema(NodesSchema):
    """
    Schema for a collection of policy findings.

    Handles pagination and deserialization of multiple policy findings.
    """
    dataclass = PolicyFindings

    nodes = fields.List(fields.Nested(PolicyFindingSchema))
