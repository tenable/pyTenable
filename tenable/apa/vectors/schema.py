from marshmallow import fields, Schema, validates_schema, ValidationError


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
    fullName = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Int(allow_none=True)
    labels = fields.List(fields.Str(), allow_none=True)
    procedure_uuid = fields.Str(allow_none=True)


class NodeSchema(Schema):
    name = fields.Str(allow_none=True)
    fullName = fields.Str(allow_none=True)
    asset_id = fields.Str(allow_none=True)
    id = fields.Int(allow_none=True)
    labels = fields.List(fields.Str(), allow_none=True)


class VectorSchema(Schema):
    isNew = fields.Bool(allow_none=True)
    vectorId = fields.Str(allow_none=True)
    path = fields.Raw(allow_none=True)
    techniques = fields.List(fields.Nested(TechniqueSchema), allow_none=True)
    nodes = fields.List(fields.Nested(NodeSchema), allow_none=True)
    findingsNames = fields.List(fields.Str(), allow_none=True)
    name = fields.Str(allow_none=True)
    summary = fields.Str(allow_none=True)
    firstAES = fields.Raw(allow_none=True)
    lastACR = fields.Int(allow_none=True)


class PaginationSchema(Schema):
    pageNumber = fields.Int(allow_none=True)
    totalRecordCount = fields.Int(allow_none=True)
    maxEntriesPerPage = fields.Int(allow_none=True)


class VectorsPageSchema(Schema):
    vectors = fields.List(fields.Nested(VectorSchema), allow_none=True)
    Pagination = fields.Nested(PaginationSchema, allow_none=True)
