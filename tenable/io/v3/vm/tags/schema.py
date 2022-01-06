'''
Tags API Endpoint Schemas
'''
from marshmallow import Schema, fields, pre_load, validate, validates_schema
from marshmallow.exceptions import ValidationError


class TagCategorySchema(Schema):
    '''
    Schema for tags category methods
    '''
    name = fields.Str()
    description = fields.Str()

    @validates_schema
    def validate_name(self, data, **kwargs):
        '''
        Supproting method to validate name string length
        '''
        if len(data['name']) >= 127:
            raise ValidationError('The name must not exceed 127 characters.')


class AssetTagSchema(Schema):
    '''
    Schema for asset tags methods
    '''
    action = fields.Str(data_key='action')
    assets = fields.List(fields.UUID, data_key='assets')
    tags = fields.List(fields.UUID, data_key='tags')


class CurrentDomainPermissionSchema(Schema):
    '''
    Supporting schema for AccessControlSchema class
    '''
    id = fields.UUID(required=True)
    name = fields.Str(required=True)
    type = fields.Str(
        validate=validate.OneOf(['USER', 'GROUP']),
        required=True
    )
    permissions = fields.List(
        fields.Str(
            validate=validate.OneOf(
                ['ALL', 'CAN_USE', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
            )
        ),
        required=True
    )

    @pre_load
    def permission_constructor(self, data, **kwargs):
        '''
        Supporting method to construct permission constructor
        '''
        if isinstance(data, dict) and len(data) == 4:
            return data
        elif isinstance(data, tuple) and len(data) == 4:
            return {
                'id': data[0],
                'name': data[1],
                'type': data[2],
                'permissions': data[3]
            }
        else:
            return ValidationError('Invalid Permissions definition')


class AccessControlSchema(Schema):
    '''
    Supporting schema for TagValueSchema class
    '''
    current_user_permissions = fields.List(
        fields.Str(
            validate=validate.OneOf(
                ['ALL', 'CAN_USE', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
            )
        ),
        default=['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],

    )
    all_users_permissions = fields.List(
        fields.Str(
            validate=validate.OneOf(
                ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
            )
        ),
        default=[]
    )
    current_domain_permissions = fields.List(
        fields.Nested(CurrentDomainPermissionSchema),
        default=[]
    )
    defined_domain_permissions = fields.List(
        fields.Str(
            validate=validate.OneOf(
                ['ALL', 'CAN_USE', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
            )
        ),
    )
    version = fields.Int(data_key='version')


class TagValueSchema(Schema):
    '''
    Schema for tags values related methods
    '''
    value_id = fields.List(fields.UUID, data_key='values')
    category_id = fields.UUID(data_key='category_uuid')
    category_name = fields.Str()
    category_description = fields.Str()
    value = fields.Str(required=True)
    description = fields.Str()
    access_control = fields.Nested(AccessControlSchema, required=True)
    filters = fields.Dict()
    filter_type = fields.Str(
        default='and',
        validate=validate.OneOf(['and', 'or'])
    )
