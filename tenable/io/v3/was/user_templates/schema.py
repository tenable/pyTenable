'''
User Templates API Endpoint Schemas
'''
from marshmallow import Schema, fields, validate


class PermissionSchema(Schema):
    '''
    Permission Schema for User-Templates
    '''
    entity = fields.Str(
        required=True,
        validate=validate.OneOf(['user', 'group'])
    )
    entity_id = fields.UUID(required=True)
    level = fields.Str(
        required=True,
        validate=validate.OneOf(['no_access', 'view', 'configure', 'control'])
    )
    permissions_id = fields.UUID(required=True)


class UserTemplateSchema(Schema):
    '''
    User-Templates Schema
    '''
    name = fields.Str()
    description = fields.Str()
    owner_id = fields.UUID()
    default_permissions = fields.Str(
        validate=validate.OneOf(['no_access', 'view', 'configure', 'control'])
    )
    results_visibility = fields.Str(
        validate=validate.OneOf(['dashboard', 'private'])
    )
    permissions = fields.List(fields.Nested(PermissionSchema))
