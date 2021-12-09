from marshmallow import fields, pre_load
from tenable.ad.base.schema import CamelCaseSchema, camelcase


class PreferenceSchema(CamelCaseSchema):
    language = fields.Str()
    preferred_profile_id = fields.Int()

    @pre_load
    def keys_to_camel(self, data, **kwargs):
        resp = {}
        for key, value in data.items():
            resp[camelcase(key)] = value
        return resp
