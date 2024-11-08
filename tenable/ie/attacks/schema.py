from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema


class AttackAttributesSchema(CamelCaseSchema):
    name = fields.Str()
    value = fields.Str()
    value_type = fields.Str()


class AttackVectorSchema(CamelCaseSchema):
    template = fields.Str()
    attributes = fields.Nested(AttackAttributesSchema, many=True)


class AttackPathSchema(CamelCaseSchema):
    ip = fields.Str()
    hostname = fields.Str()
    type = fields.Str()


class AttackSchema(CamelCaseSchema):
    id = fields.Int()
    directory_id = fields.Int()
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
