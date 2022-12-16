'''
Export API Endpoints Schemas
'''
from typing import Dict
from marshmallow import Schema, fields, post_dump, validate as v
from tenable.base.schema.fields import LowerCase
from tenable.base.utils.envelope import envelope


def serialize_tags(data: Dict) -> Dict:
    '''
    Converts the Tag tuples into a series of keys with the 'tag.' prefix.
    '''
    for tag in data.pop('tags', []):
        tag_name = f'tag.{tag[0]}'
        if tag_name not in data:
            data[tag_name] = []
        data[tag_name].append(tag[1])
    return data


class AssetExportSchema(Schema):
    '''
    Asset Export API Schema
    '''
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

    # Other params
    chunk_size = fields.Int(dump_default=1000)
    network_id = fields.UUID()
    sources = fields.List(fields.Str())
    tags = fields.List(fields.Tuple((fields.Str(), fields.Str())))

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = serialize_tags(data)
        data = envelope(data, 'filters', excludes=['chunk_size'])
        return data


class VPRSchema(Schema):
    '''
    VPR Sub-object Schema
    '''
    eq = fields.List(fields.Float(validate=v.Range(min=0.0, max=10.0)))
    neq = fields.List(fields.Float(validate=v.Range(min=0.0, max=10.0)))
    gt = fields.Float(validate=v.Range(min=0.0, max=10.0))
    gte = fields.Float(validate=v.Range(min=0.0, max=10.0))
    lt = fields.Float(validate=v.Range(min=0.0, max=10.0))
    lte = fields.Float(validate=v.Range(min=0.0, max=10.0))


class VulnExportSchema(Schema):
    '''
    Vulnerability Export API Schema
    '''
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
    state = fields.List(LowerCase(fields.Str()))
    vpr_score = fields.Nested(VPRSchema())
    scan_uuid = fields.Str()

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
        data = envelope(data, 'filters', excludes=['num_assets',
                                                   'include_unlicensed'
                                                   ])
        return data


class ComplianceExportSchema(Schema):
    '''
    Compliance Export API Schema
    '''
    # Temporal fields
    first_seen = fields.Int()
    last_seen = fields.Int()

    # Other params
    asset = fields.List(fields.UUID())
    num_findings = fields.Int(dump_default=5000)

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = serialize_tags(data)
        data = envelope(data, 'filters', excludes=['asset',
                                                   'num_findings'
                                                   ])
        return data
