from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class ReasonSchema(CamelCaseSchema):
    id = fields.Int()
    codename = fields.Str()
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
