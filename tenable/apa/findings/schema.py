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
    mitre_id = fields.Str()
    mitigations = fields.List(fields.Str())
    malwares = fields.List(fields.Str())
    tools = fields.List(fields.Str())
    groups = fields.List(fields.Str())
    name = fields.Str()
    priority = fields.Str(validate=v.OneOf(['critical', 'high', 'medium', 'low']))
    procedureName = fields.Str()
    relatedNodes = fields.Nested(FindingRelatedNodesSchema)
    tactics = fields.List(fields.Str())
    critical_assets_count = fields.Int()
    total_critical_assets_count = fields.Int()
    totalVectorCount = fields.Int()
    vectorCount = fields.Int()
    state = fields.Str(validate=v.OneOf(['open', 'archive']))
    status = fields.Str(validate=v.OneOf(['in_progress', 'done', 'to_do', 'in_review']))
    created = fields.Int()
    is_active = fields.Bool()
    has_history = fields.Bool()
    last_updated_at = fields.DateTime()
    source_information = fields.List(fields.Nested(SourceInformationSchema))
    weaknesses_ids = fields.List(fields.Str())
    assets_ids = fields.List(fields.Str())
    detection_ids = fields.List(fields.Str())
    serial_id = fields.Int()


class FindingPageSchema(Schema):
    data = fields.List(fields.Nested(FindingSchema))
    next = fields.Str()
    page_number = fields.Int()
    count = fields.Int()
    total = fields.Int()
