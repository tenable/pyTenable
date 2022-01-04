'''
Scanners API Endpoint Schemas
'''
from typing import Dict

from marshmallow import Schema, ValidationError
from marshmallow import fields as m_fields
from marshmallow import post_dump, pre_load
from marshmallow import validate as v


class ScannerEditSchema(Schema):
    '''
    Schema for edit functions in api.py

    Args:

    '''

    force_plugin_update = m_fields.Bool()
    force_ui_update = m_fields.Bool()
    finish_update = m_fields.Bool()
    registration_code = m_fields.Str()
    aws_update_interval = m_fields.Int()

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = dict(
            filter(
                lambda item: item[1] not in m_fields.Bool.falsy,
                data.items()
            )
        )
        data.update(
            map(
                lambda item: (
                    item[0], 1) if item[1] in m_fields.Bool.truthy else item,
                data.items(),
            )
        )
        return data


class CredentialsCreateSchema(Schema):
    '''
    Schema for create function in credentials.py
    Args:
    '''

    name = m_fields.Str()
    description = m_fields.Str(default='')
    type = m_fields.Str()
    settings = m_fields.Dict()
    permissions = m_fields.List(m_fields.Dict())


class CredentialsPermissionsSchema(Schema):
    '''
    Schema for permissions function in credentials.py
    Args:
    '''

    type = m_fields.Str(validate=v.OneOf(['user', 'group']))
    permissions = m_fields.Int(validate=v.OneOf([32, 64]))
    grantee_uuid = m_fields.UUID()

    @pre_load
    def validate_and_transform(self, data, **kwargs):
        '''
        Handles schema validation and data transform based on the data
        presented.
        '''

        if isinstance(data, dict) and len(data) == 3 and \
                ('type' and 'permissions' and 'grantee_uuid' in data.keys()):
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

            >>> f = ('user', 64, '0000000-0000000-0000-0000')
            >>> filter.dump(filter.load(f))
            {'type': 'filter', 'permissions': 64, 'grantee_uuid':
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
            'grantee_uuid': data[2]
        }


class CredentialsEditSchema(Schema):
    '''
    Schema for Edit function in credentials.py
    Args:
    '''

    name = m_fields.Str()
    description = m_fields.Str()
    ad_hoc = m_fields.Bool()
    settings = m_fields.Dict()
    permissions = m_fields.List(m_fields.Dict())
