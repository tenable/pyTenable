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
    source_information = fields.List(fields.Nested(SourceInformationSchema))
    name = fields.Str(allow_none=True)
    fullName = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Int(allow_none=True)
    labels = fields.List(fields.Str())
    procedure_uuid = fields.Str(allow_none=True)


class NodeSchema(Schema):
    name = fields.Str(allow_none=True)
    fullName = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Int(allow_none=True)
    labels = fields.List(fields.Str())


class VectorSchema(Schema):
    isNew = fields.Bool(allow_none=True)
    vectorId = fields.Str(allow_none=True)
    path = fields.Raw(allow_none=True)
    techniques = fields.List(fields.Nested(TechniqueSchema))
    nodes = fields.List(fields.Nested(NodeSchema))
    findingsNames = fields.List(fields.Str())
    name = fields.Str(allow_none=True)
    summary = fields.Str(allow_none=True)
    firstAES = fields.Raw(allow_none=True)
    lastACR = fields.Int(allow_none=True)


class PaginationSchema(Schema):
    totalRecordCount = fields.Int(allow_none=True)
    maxEntriesPerPage = fields.Int(allow_none=True)


class VectorsPageSchema(Schema):
    vectors = fields.List(fields.Nested(VectorSchema))
    pagination = fields.Nested(PaginationSchema)
