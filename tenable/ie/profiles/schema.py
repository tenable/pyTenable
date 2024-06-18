from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class ProfileSchema(CamelCaseSchema):
    id = fields.Int()
    name = fields.Str()
    deleted = fields.Bool()
    directories = fields.List(fields.Int())
    dirty = fields.Bool()
    has_ever_been_committed = fields.Bool()
