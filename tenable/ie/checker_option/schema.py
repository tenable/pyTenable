from marshmallow import fields, validate
from tenable.ie.base.schema import CamelCaseSchema, BoolInt


class CheckerOptionSchema(CamelCaseSchema):
    profile_id = fields.Int()
    checker_id = fields.Int()
    id = fields.Int()
    codename = fields.Str(required=True)
    directory_id = fields.Int(allow_none=True)
    value = fields.Str(required=True)
    value_type = fields.Str(validate=validate.OneOf(
        ['string', 'regex', 'float', 'integer', 'boolean', 'date',
         'object', 'array/string', 'array/regex', 'array/integer',
         'array/boolean', 'array/select', 'array/object']), required=True)
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    translations = fields.List(fields.Str())
    staged = BoolInt()
