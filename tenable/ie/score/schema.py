import typing
from marshmallow import fields, ValidationError
from tenable.ie.base.schema import CamelCaseSchema


class ScoreRules(fields.Field):
    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        if isinstance(value, list) or isinstance(value, str):
            return value
        else:
            raise ValidationError('Field should be string or list')


class ScoreSchema(CamelCaseSchema):
    profile_id = fields.Str()
    directory_ids = ScoreRules(allow_none=True)
    checker_ids = ScoreRules(allow_none=True)
    reason_ids = ScoreRules(allow_none=True)
    directory_id = fields.Int()
    score = fields.Int(allow_none=True)
