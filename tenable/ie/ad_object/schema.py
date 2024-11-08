from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class ADObjectChangeValuesSchema(CamelCaseSchema):
    after = fields.Str()
    before = fields.Str(allow_none=True)
    current = fields.Str()


class ADObjectChangesSchema(CamelCaseSchema):
    attribute_name = fields.Str()
    values = fields.Nested(ADObjectChangeValuesSchema)
    value_type = fields.Str()


class ADObjectAttributesSchema(CamelCaseSchema):
    name = fields.Str()
    value = fields.Str()
    value_type = fields.Str()


class ADObjectSchema(CamelCaseSchema):
    id = fields.Int()
    directory_id = fields.Int()
    object_id = fields.Str()
    type = fields.Str()
    object_attributes = fields.Nested(ADObjectAttributesSchema, many=True)
    reasons = fields.List(fields.Int())
    wanted_values = fields.List(fields.Str())
    expression = fields.Mapping()
    directories = fields.List(fields.Int())
    date_start = fields.DateTime()
    date_end = fields.DateTime()
    show_ignored = fields.Bool()
    page = fields.Int(allow_none=True)
    per_page = fields.Int(allow_none=True)
    max_pages = fields.Int(allow_none=True)
    max_items = fields.Int(allow_none=True)
