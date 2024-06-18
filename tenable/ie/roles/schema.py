from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class RolePermissionsSchema(CamelCaseSchema):
    entity_name = fields.Str(required=True)
    action = fields.Str(required=True)
    entity_ids = fields.List(fields.Int(), allow_none=True, required=True)
    dynamic_id = fields.Str(allow_none=True)


class RoleSchema(CamelCaseSchema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    permissions = fields.Nested(RolePermissionsSchema, many=True)
