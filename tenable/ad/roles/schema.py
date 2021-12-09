from marshmallow import fields, pre_load
from tenable.ad.base.schema import CamelCaseSchema, camelcase


class RolePermissionsSchema(CamelCaseSchema):
    entity_name = fields.Str(required=True)
    action = fields.Str(required=True)
    entity_ids = fields.List(fields.Int(), allow_none=True, required=True)
    dynamic_id = fields.Str(allow_none=True)

    @pre_load
    def keys_to_camel(self, data, **kwargs):
        resp = {}
        for key, value in data.items():
            resp[camelcase(key)] = value
        return resp


class RoleSchema(CamelCaseSchema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    permissions = fields.Nested(RolePermissionsSchema, many=True)
