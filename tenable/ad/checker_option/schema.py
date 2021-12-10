import typing
from marshmallow import fields, validate, ValidationError
from tenable.ad.base.schema import CamelCaseSchema


class StagedRule(fields.Field):
    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        if isinstance(value, str) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('Field should be string or boolean.')


class CheckerOptionSchema(CamelCaseSchema):
    profile_id = fields.Int()
    checker_id = fields.Int()
    id = fields.Int()
    codename = fields.Str()
    directory_id = fields.Int(allow_none=True)
    value = fields.Str()
    value_type = fields.Str(validate=validate.OneOf(
        ['string', 'regex', 'float', 'integer', 'boolean', 'date',
         'object', 'array/string', 'array/regex', 'array/integer',
         'array/boolean', 'array/select', 'array/object']))
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    translations = fields.List(fields.Str())
    staged = StagedRule()
    per_page = fields.Str()
    page = fields.Str()
