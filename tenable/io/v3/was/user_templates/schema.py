from marshmallow import Schema, fields, validate


class PermissionSchema(Schema):
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
    name = fields.Str(required=True)
    description = fields.Str()
    owner_id = fields.UUID(required=True)
    default_permissions = fields.Str(
        required=True,
        validate=validate.OneOf(['no_access', 'view', 'configure', 'control'])
    )
    results_visibility = fields.Str(
        required=True,
        validate=validate.OneOf(['dashboard', 'private'])
    )
    permissions = fields.List(fields.Nested(PermissionSchema), required=True)
