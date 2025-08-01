"""
Export API Endpoints Schemas
"""

from enum import Enum
from typing import Dict

from marshmallow import Schema, fields, post_dump
from marshmallow import validate as v

from tenable.base.schema.fields import LowerCase, UpperCase
from tenable.base.utils.envelope import envelope


def serialize_tags(data: Dict) -> Dict:
    """
    Converts the Tag tuples into a series of keys with the 'tag.' prefix.
    """
    for tag in data.pop('tags', []):
        tag_name = f'tag.{tag[0]}'
        if tag_name not in data:
            data[tag_name] = []
        data[tag_name].append(tag[1])
    return data


def serialize_compliance_tags(data: Dict) -> Dict:
    """
    Converts the tag tuples into a list of objects
    """
    tags = data.pop('tags', [])
    modified_tags = []
    for tag in tags:
        category = tag[0]
        values = tag[1]
        modified_tags.append({'category': category, 'values': values})

    if tags:
        data['tags'] = modified_tags

    return data


class AssetExportSchema(Schema):
    """
    Asset Export API Schema
    """

    # Temporal fields
    last_scan_id = fields.Str()
    created_at = fields.Int()
    deleted_at = fields.Int()
    first_scan_time = fields.Int()
    last_assessed = fields.Int()
    last_authenticated_scan_time = fields.Int()
    terminated_at = fields.Int()
    updated_at = fields.Int()

    # Boolean flags
    has_plugin_results = fields.Bool()
    is_deleted = fields.Bool()
    is_licensed = fields.Bool()
    is_terminated = fields.Bool()
    servicenow_sysid = fields.Bool()
    include_open_ports = fields.Bool()

    # Other params
    chunk_size = fields.Int(dump_default=1000)
    network_id = fields.UUID()
    sources = fields.List(fields.Str())
    tags = fields.List(fields.Tuple((fields.Str(), fields.Str())))

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = serialize_tags(data)
        data = envelope(data, 'filters', excludes=['chunk_size', 'include_open_ports'])
        return data


class AssetV2ExportSchema(Schema):
    """
    Asset V2 Export API Schema
    """

    # Temporal fields
    created_at = fields.Int()
    updated_at = fields.Int()
    terminated_at = fields.Int()
    deleted_at = fields.Int()

    first_scan_time = fields.Int()
    last_authenticated_scan_time = fields.Int()
    last_assessed = fields.Int()
    since = fields.Int()
    last_scan_id = fields.Str()

    # Boolean flags
    is_terminated = fields.Bool()
    is_deleted = fields.Bool()
    is_licensed = fields.Bool()
    has_plugin_results = fields.Bool()
    servicenow_sysid = fields.Bool()

    include_open_ports = fields.Bool()

    # Other params
    network_id = fields.UUID()
    sources = fields.List(fields.Str())
    types = fields.List(fields.Str(dump_default='host'))

    chunk_size = fields.Int(dump_default=1000)

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = serialize_tags(data)
        data = envelope(data, 'filters', excludes=['chunk_size', 'include_open_ports'])
        return data


class VPRSchema(Schema):
    """
    VPR Sub-object Schema
    """

    eq = fields.List(fields.Float(validate=v.Range(min=0.0, max=10.0)))
    neq = fields.List(fields.Float(validate=v.Range(min=0.0, max=10.0)))
    gt = fields.Float(validate=v.Range(min=0.0, max=10.0))
    gte = fields.Float(validate=v.Range(min=0.0, max=10.0))
    lt = fields.Float(validate=v.Range(min=0.0, max=10.0))
    lte = fields.Float(validate=v.Range(min=0.0, max=10.0))


class VulnExportSchema(Schema):
    """
    Vulnerability Export API Schema
    """

    # Temporal fields
    first_found = fields.Int()
    indexed_at = fields.Int()
    last_fixed = fields.Int()
    last_found = fields.Int()
    since = fields.Int()

    # Plugin fields
    plugin_family = fields.List(fields.Str())
    plugin_id = fields.List(fields.Int())
    plugin_type = fields.Str()

    # Vulnerability Findings fields
    severity = fields.List(LowerCase(fields.Str()))
    state = fields.List(UpperCase(fields.Str()))
    vpr_score = fields.Nested(VPRSchema())
    scan_uuid = fields.Str()
    source = fields.List(fields.Str())
    severity_modification_type = fields.List(fields.Str())

    # Asset fields
    tags = fields.List(fields.Tuple((fields.Str(), fields.Str())))
    network_id = fields.UUID()
    cidr_range = fields.Str()
    include_unlicensed = fields.Bool()

    # Chunking fields
    num_assets = fields.Int(dump_default=500)

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = serialize_tags(data)
        data = envelope(data, 'filters', excludes=['num_assets', 'include_unlicensed'])
        return data


class ComplianceExportSchema(Schema):
    """
    Compliance Export API Schema
    """

    # Temporal fields
    first_seen = fields.Int()
    last_seen = fields.Int()
    ipv4_addresses = fields.List(fields.Str())
    ipv6_addresses = fields.List(fields.Str())
    plugin_name = fields.List(fields.Str())
    plugin_id = fields.List(fields.Int())
    audit_name = fields.Str()
    audit_file_name = fields.Str()
    compliance_results = fields.List(fields.Str())
    last_observed = fields.Int()
    indexed_at = fields.Int()
    since = fields.Int()
    state = fields.List(fields.Str())
    tags = fields.List(fields.Tuple((fields.Str(), fields.List(fields.Str()))))
    network_id = fields.Str()

    # Other params
    asset = fields.List(fields.UUID())
    num_findings = fields.Int(dump_default=5000)

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = serialize_compliance_tags(data)
        data = envelope(data, 'filters', excludes=['asset', 'num_findings'])
        return data


class OWASPChapters(str, Enum):
    """
    Enum of OWASP Chapters
    """

    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    A4 = 'A4'
    A5 = 'A5'
    A6 = 'A6'
    A7 = 'A7'
    A8 = 'A8'
    A9 = 'A9'
    A10 = 'A10'


class OWASPAPIChapters(str, Enum):
    """
    Enum of OWASP API Chapters.
    """

    API1 = 'API1'
    API2 = 'API2'
    API3 = 'API3'
    API4 = 'API4'
    API5 = 'API5'
    API6 = 'API6'
    API7 = 'API7'
    API8 = 'API8'
    API9 = 'API9'
    API10 = 'API10'


class Severity(str, Enum):
    """
    Enum for Severity level
    """

    INFO = 'INFO'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'


class State(str, Enum):
    """
    Enum for Finding State
    """

    OPEN = 'OPEN'
    REOPENED = 'REOPENED'
    FIXED = 'FIXED'


class SeverityModificationType(str, Enum):
    """
    Enum for SeverityModificationType
    """

    NONE = 'NONE'
    ACCEPTED = 'ACCEPTED'
    RECASTED = 'RECASTED'


class WASVulnExportSchema(Schema):
    """
    WAS vulns Export API Schema
    """

    # asset fields
    asset_uuid = fields.List(fields.UUID())
    asset_name = fields.Str()

    # Temporal fields
    first_found = fields.Int()
    last_found = fields.Int()
    last_fixed = fields.Int()
    indexed_at = fields.Int()
    since = fields.Int()

    # Plugin fields
    plugin_ids = fields.List(fields.Int())

    # OWASP fields
    owasp_2010 = fields.List(fields.Enum(OWASPChapters, by_value=True))
    owasp_2013 = fields.List(fields.Enum(OWASPChapters, by_value=True))
    owasp_2017 = fields.List(fields.Enum(OWASPChapters, by_value=True))
    owasp_2021 = fields.List(fields.Enum(OWASPChapters, by_value=True))
    owasp_api_2019 = fields.List(fields.Enum(OWASPAPIChapters, by_value=True))

    # Vulnerability Findings fields
    severity = fields.List(fields.Enum(Severity, by_value=True))
    state = fields.List(fields.Enum(State, by_value=True))
    severity_modification_type = fields.List(
        fields.Enum(SeverityModificationType, by_value=True)
    )
    vpr_score = fields.Nested(VPRSchema())
    ipv4s = fields.List(fields.IPv4())

    include_unlicensed = fields.Bool(default=False)
    # Chunking fields
    num_assets = fields.Int(dump_default=50)

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = envelope(data, 'filters', excludes=['num_assets', 'include_unlicensed'])
        return data
