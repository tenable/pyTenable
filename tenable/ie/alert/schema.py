from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema, BoolStr


class AlertSchema(CamelCaseSchema):
    id = fields.Int()
    deviance_id = fields.Int()
    archived = fields.Bool()
    read = fields.Bool()
    date = fields.DateTime()
    directory_id = fields.Int()
    infrastructure_id = fields.Int()
    page = fields.Int(allow_none=True, dump_default=1)
    per_page = fields.Int(allow_none=True)
    max_pages = fields.Int(allow_none=True)
    max_items = fields.Int(allow_none=True)


class AlertParamsSchema(AlertSchema):
    archived = BoolStr()
    read = BoolStr()
