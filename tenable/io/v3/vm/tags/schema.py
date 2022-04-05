'''
Tags API Endpoint Schemas
'''
from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_dump, pre_load
from marshmallow.exceptions import ValidationError

from tenable.io.v3.base.schema.explore.filters import ParseFilterSchema


class TagCategorySchema(Schema):
    '''
    Schema for tags category methods
    '''
    name = fields.Str(
        validate=validate.Length(1, 127),
        required=True
    )
    description = fields.Str()


class AssetTagSchema(Schema):
    '''
    Schema for asset tags methods
    '''
    action = fields.Str(validate=validate.OneOf(['add', 'remove']))
    assets = fields.List(fields.UUID)
    tags = fields.List(fields.UUID)


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
        load_default=['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS'],
    )
    all_users_permissions = fields.List(
        fields.Str(
            validate=validate.OneOf(
                ['ALL', 'CAN_USE', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
            )
        ),
        load_default=[]
    )
    current_domain_permissions = fields.List(
        fields.Nested(CurrentDomainPermissionSchema),
        load_default=[]
    )
    defined_domain_permissions = fields.List(
        fields.Str(
            validate=validate.OneOf(
                ['ALL', 'CAN_USE', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
            )
        ),
    )
    version = fields.Int()


class TagsFilterSchema(ParseFilterSchema):
    '''
    Validate filters using ParseFilterSchema
    '''
    _filters = None


class TagValueSchema(Schema):
    '''
    Schema for tags values related methods
    '''
    value_id = fields.List(fields.UUID, data_key='values')
    category_uuid = fields.UUID()
    category_name = fields.Str()
    category_description = fields.Str()
    value = fields.Str(required=True)
    description = fields.Str()
    access_control = fields.Nested(AccessControlSchema, required=True)
    filter_type = fields.Str(
        load_default='and',
        validate=validate.OneOf(['and', 'or'])
    )
    filters = fields.List(fields.Nested(TagsFilterSchema))

    @post_dump
    def post_serialization(self, data, **kwargs):
        '''
        Convert the filter dictionary to asset filter definition
        '''
        if 'filters' in list(data.keys()):
            resp: dict = {
                'asset': {
                    data['filter_type']: data['filters']
                }
            }
            data['filters'] = resp
        data.pop('filter_type', '')
        return data
