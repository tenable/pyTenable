from marshmallow import fields, validate as v, Schema


class NodeInfoSchema(Schema):
    name = fields.Str()
    fullname = fields.Str()
    id = fields.Str()
    labels = fields.List(fields.Str())
    isCrownJewel = fields.Bool()
    vulnerability_id = fields.Str()
    asset_id = fields.Str()


class FindingRelatedNodesSchema(Schema):
    sources = fields.List(fields.Nested(NodeInfoSchema))
    targets = fields.List(fields.Nested(NodeInfoSchema))
    cause = fields.Nested(NodeInfoSchema)


class SourceInformationSchema(Schema):
    id = fields.Str()
    asset_id = fields.Str()
    type = fields.Str()
    provider_detection_id = fields.Str()
    provider_code = fields.Str()
    reason_id = fields.Str()
    reason_code_name = fields.Str()
    detection_code = fields.Str()


class FindingSchema(Schema):
    attack_type_id = fields.Int()
    attack_type_ids = fields.List(fields.Int())
    dc = fields.Str()
    date = fields.DateTime()
    vector = fields.Nested(AttackVectorSchema)
    source = fields.Nested(AttackPathSchema)
    destination = fields.Nested(AttackPathSchema)
    is_closed = fields.Bool()
    resource_type = fields.Str(required=True, validate=v.OneOf(
        ['infrastructure', 'directory', 'hostname', 'ip']))
    resource_value = fields.Str(required=True)
    date_end = fields.DateTime()
    date_start = fields.DateTime()
    include_closed = fields.Str(validate=v.OneOf(['true', 'false']))
    limit = fields.Str()
    order = fields.Str(validate=v.OneOf(['asc', 'desc']))
    search = fields.Str()

    mitre_id = fields.Str()
    mitigations = fields.List(fields.Str())
    malwares = fields.List(fields.Str())
    tools = fields.List(fields.Str())
    groups = fields.List(fields.Str())
    name = fields.Str()
    priority = fields.Str()
    procedureName = fields.Str()
    relatedNodes = fields.Nested(FindingRelatedNodesSchema)
    tactics = fields.List(fields.Str())
    critical_assets_count = fields.Int()
    total_critical_assets_count = fields.Int()
    totalVectorCount = fields.Int()
    vectorCount = fields.Int()
    state = fields.Str()
    status = fields.Str()
    created = fields.Int()
    is_active = fields.Bool()
    has_history = fields.Bool()
    last_updated_at = fields.DateTime()
    source_information = fields.List(fields.Nested(SourceInformationSchema))
    weaknesses_ids = fields.List(fields.Str())
    assets_ids = fields.List(fields.Str())
    detection_ids = fields.List(fields.Str())
    serial_id = fields.Int()
