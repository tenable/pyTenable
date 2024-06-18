from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class PreferenceSchema(CamelCaseSchema):
    language = fields.Str()
    preferred_profile_id = fields.Int()