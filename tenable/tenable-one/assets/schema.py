from marshmallow import fields, validate as v, Schema


class NodeInfoSchema(Schema):
    name = fields.Str(allow_none=True)
    fullname = fields.Str(allow_none=True)
    id = fields.Str(allow_none=True)
    labels = fields.List(fields.Str())
    isCrownJewel = fields.Bool()
    vulnerability_id = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)


class FindingRelatedNodesSchema(Schema):
    sources = fields.List(fields.Nested(NodeInfoSchema))
    targets = fields.List(fields.Nested(NodeInfoSchema))
    cause = fields.Nested(NodeInfoSchema)


class SourceInformationSchema(Schema):
    id = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    provider_detection_id = fields.Str(allow_none=True)
    provider_code = fields.Str(allow_none=True)
    reason_id = fields.Str(allow_none=True)
    reason_code_name = fields.Str(allow_none=True)
    detection_code = fields.Str(allow_none=True)


class FindingSchema(Schema):
    mitre_id = fields.Str(allow_none=True)
    mitigations = fields.List(fields.Str())
    malwares = fields.List(fields.Str())
    tools = fields.List(fields.Str())
    groups = fields.List(fields.Str())
    name = fields.Str(allow_none=True)
    priority = fields.Str(validate=v.OneOf(["critical", "high",
                                            "medium", "low"]))
    procedureName = fields.Str(allow_none=True)
    relatedNodes = fields.Nested(FindingRelatedNodesSchema)
    tactics = fields.List(fields.Str())
    critical_assets_count = fields.Int(allow_none=True)
    total_critical_assets_count = fields.Int(allow_none=True)
    totalVectorCount = fields.Int(allow_none=True)
    vectorCount = fields.Int(allow_none=True)
    state = fields.Str(validate=v.OneOf(["open", "archive"]))
    status = fields.Str(validate=v.OneOf(["in_progress", "done",
                                          "to_do", "in_review"]))
    created = fields.Int(allow_none=True)
    is_active = fields.Bool(allow_none=True)
    has_history = fields.Bool(allow_none=True)
    last_updated_at = fields.DateTime(allow_none=True)
    source_information = fields.List(fields.Nested(SourceInformationSchema))
    weaknesses_ids = fields.List(fields.Str())
    assets_ids = fields.List(fields.Str())
    detection_ids = fields.List(fields.Str())
    serial_id = fields.Int(allow_none=True)


class FindingsPageSchema(Schema):
    data = fields.List(fields.Nested(FindingSchema))
    next = fields.Str(allow_none=True)
    page_number = fields.Int(allow_none=True)
    count = fields.Int(allow_none=True)
    total = fields.Int(allow_none=True)
