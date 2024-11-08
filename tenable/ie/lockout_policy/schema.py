from marshmallow import fields, pre_load
from tenable.ie.base.schema import CamelCaseSchema, camelcase


class LockoutPolicySchema(CamelCaseSchema):
    enabled = fields.Bool()
    lockout_duration = fields.Int()
    failed_attempt_threshold = fields.Int()
    failed_attempt_period = fields.Int()

    @pre_load
    def keys_to_camel(self, data, **kwargs):
        resp = {}
        for key, value in data.items():
            resp[camelcase(key)] = value
        return resp
