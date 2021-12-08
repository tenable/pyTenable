from marshmallow import fields, pre_load, post_load
from tenable.ad.base.schema import CamelCaseSchema


class RolePermissionsSchema(CamelCaseSchema):
    entity_name = fields.Str()
    action = fields.Str()
    entity_ids = fields.List(fields.Int(), allow_none=True)
    dynamic_id = fields.Str(allow_none=True)


class RoleSchema(CamelCaseSchema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    permissions = fields.Nested(RolePermissionsSchema, many=True)
