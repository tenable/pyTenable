from marshmallow import fields, Schema


class SourceInformationSchema(Schema):
    provider_detection_id = fields.Str(allow_none=True)
    detection_code = fields.Str(allow_none=True)
    reason_code_name = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Str(allow_none=True)
    provider_code = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    reason_id = fields.Str(allow_none=True)
    plugin_name = fields.Str(allow_none=True)


class TechniqueSchema(Schema):
    source_information = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)
    full_name = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Int(allow_none=True)
    labels = fields.List(fields.Str(), allow_none=True)
    procedure_uuid = fields.Str(allow_none=True)


class NodeSchema(Schema):
    name = fields.Str(allow_none=True)
    full_name = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Int(allow_none=True)
    labels = fields.List(fields.Str(), allow_none=True)


class VectorSchema(Schema):
    is_new = fields.Bool(allow_none=True)
    vector_id = fields.Str(allow_none=True)
    path = fields.Raw(allow_none=True)
    techniques = fields.List(fields.Nested(TechniqueSchema), allow_none=True)
    nodes = fields.List(fields.Nested(NodeSchema), allow_none=True)
    findings_names = fields.List(fields.Str(), allow_none=True)
    name = fields.Str(allow_none=True)
    summary = fields.Str(allow_none=True)
    first_aes = fields.Raw(allow_none=True)
    last_acr = fields.Int(allow_none=True)


class VectorsPageSchema(Schema):
    data = fields.List(fields.Nested(VectorSchema), allow_none=True)
    page_number = fields.Int(allow_none=True)
    count = fields.Int(allow_none=True)
    total = fields.Int(allow_none=True)
