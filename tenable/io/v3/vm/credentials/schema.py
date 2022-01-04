'''
Credentials API Endpoint Schemas
'''
from typing import Dict

from marshmallow import Schema, ValidationError, fields, pre_load
from marshmallow import validate as v


class CredentialsPermissionsSchema(Schema):
    '''
    Schema for permissions function in credentials.py
    Args:
    '''

    type = fields.Str(validate=v.OneOf(['user', 'group']))
    permissions = fields.Int(validate=v.OneOf([32, 64]))
    grantee_id = fields.UUID()

    @pre_load
    def validate_and_transform(self, data, **kwargs):
        '''
        Handles schema validation and data transform based on the data
        presented.
        '''

        if isinstance(data, dict) and len(data) == 3 and \
                ('type' and 'permissions' and 'grantee_id' in data.keys()):
            return data
        elif isinstance(data, tuple) and len(data) == 3:
            return self.permissions_tuple_expansion(data)
        else:
            return ValidationError('Invalid Permissions definition')

    def permissions_tuple_expansion(self, data: tuple) -> Dict:
        '''
        Handles expanding a tuple definition of a filter into the dictionary
        equivalent.

        Example:

            >>> f = ('user', 64, '00000000-0000-0000-0000-000000000000')
            >>> filter.dump(filter.load(f))
            {'type': 'filter', 'permissions': 64, 'grantee_id':
            'value'}
        '''
        permission_val = data[1]
        if isinstance(permission_val, str):
            if permission_val == 'use':
                permission_val = 32
            elif permission_val == 'edit':
                permission_val = 64

        return {
            'type': data[0], 'permissions': permission_val,
            'grantee_id': data[2]
        }


class CredentialsCreateSchema(Schema):
    '''
    Schema for create function in credentials.py
    Args:
    '''

    name = fields.Str()
    description = fields.Str(default='')
    type = fields.Str()
    settings = fields.Dict()
    permissions = fields.List(fields.Nested(CredentialsPermissionsSchema))


class CredentialsEditSchema(Schema):
    '''
    Schema for Edit function in credentials.py
    Args:
    '''

    name = fields.Str()
    description = fields.Str(default='')
    ad_hoc = fields.Bool()
    settings = fields.Dict()
    permissions = fields.List(fields.Nested(CredentialsPermissionsSchema))
