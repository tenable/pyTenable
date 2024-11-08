from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema, BoolInt


class AttackTypeOptionsSchema(CamelCaseSchema):
    id = fields.Int()
    codename = fields.Str(required=True)
    profile_id = fields.Int()
    attack_type_id = fields.Int()
    directory_id = fields.Int(allow_none=True)
    value = fields.Str(required=True)
    value_type = fields.Str(required=True, validate=v.OneOf([
        'string',
        'regex',
        'float',
        'integer',
        'boolean',
        'date',
        'object',
        'array/string',
        'array/regex',
        'array/integer',
        'array/boolean',
        'array/select',
        'array/object',
    ]))
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    translations = fields.List(fields.Str())
    staged = BoolInt()
