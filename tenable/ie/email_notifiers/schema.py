from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema


class EmailNotifierSchema(CamelCaseSchema):
    id = fields.Int()
    address = fields.Str(required=True)
    criticity_threshold = fields.Int()
    directories = fields.List(
        fields.Int(),
        validate=v.Length(min=1, error="Required minimum 1 value"))
    description = fields.Str(allow_none=True)
    checkers = fields.List(
        fields.Int(), allow_none=True, required=True,
        validate=v.Length(min=1, error="Required minimum 1 value"))
    attack_types = fields.List(
        fields.Int(), allow_none=True, required=True,
        validate=v.Length(min=1, error="Required minimum 1 value"))
    profiles = fields.List(
        fields.Int(), required=True,
        validate=v.Length(min=1, error="Required minimum 1 value"))
    should_notify_on_initial_full_security_check = fields.Bool(required=True)
    input_type = fields.Str(validate=v.OneOf(['deviances', 'attacks']))
