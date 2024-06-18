'''
Tenable Identity Exposure user schema
'''
from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class UserSchema(CamelCaseSchema):
    id = fields.Int()
    surname = fields.Str(allow_none=True)
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    locked_out = fields.Bool()
    department = fields.Str(allow_none=True)
    role = fields.List(fields.Int())
    biography = fields.Str(allow_none=True)
    active = fields.Bool()
    picture = fields.List(fields.Int(), allow_none=True)
    roles = fields.List(fields.Int())
    identifier = fields.Str()
    provider = fields.Str()
    eula_version = fields.Int()
    token = fields.Str()
    old_password = fields.Str()
    new_password = fields.Str()


class UserPermissionsSchema(CamelCaseSchema):
    entity_name = fields.Str()
    action = fields.Str()
    entity_ids = fields.List(fields.Int(), allow_none=True)
    dynamic_id = fields.Str(allow_none=True)


class UserRolesSchema(CamelCaseSchema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    permissions = fields.Nested(UserPermissionsSchema, many=True)


class UserInfoSchema(UserSchema):
    internal = fields.Bool()
    roles = fields.Nested(UserRolesSchema, many=True)
