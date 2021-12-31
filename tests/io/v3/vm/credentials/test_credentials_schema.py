'''
Testing the Credentials schemas
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.vm.credentials.schema import (CredentialsCreateSchema,
                                                 CredentialsEditSchema)

PERMISSION_DATA = [
    ('group', 64, '00000000-0000-0000-0000-000000000000'),
    ('group', 'use', '00000000-0000-0000-0000-000000000000'),
    ('group', 'edit', '00000000-0000-0000-0000-000000000000'),
    ('user', 32, '00000000-0000-0000-0000-000000000000'),
]

PERMISSION_VALIDATED_DATA = [
    {
        'grantee_id': '00000000-0000-0000-0000-000000000000',
        'type': 'group',
        'permissions': 64,
    },
    {
        'grantee_id': '00000000-0000-0000-0000-000000000000',
        'type': 'group',
        'permissions': 32,
    },
    {
        'grantee_id': '00000000-0000-0000-0000-000000000000',
        'type': 'group',
        'permissions': 64,
    },
    {
        'grantee_id': '00000000-0000-0000-0000-000000000000',
        'type': 'user',
        'permissions': 32,
    },
]


def test_credentials_edit_schema():
    '''
    Test the edit schema
    '''
    payload = {
        'name': 'test1',
        'description': '',
        'ad_hoc': True,
        'settings': {},
        'permissions': PERMISSION_DATA,
    }
    test_resp = {
        'name': 'test1',
        'description': '',
        'ad_hoc': True,
        'settings': {},
        'permissions': PERMISSION_VALIDATED_DATA,
    }
    schema = CredentialsEditSchema()
    assert test_resp == schema.dump(schema.load(payload))

    with pytest.raises(ValidationError):
        data = 'something'
        schema.load(data)


def test_credentials_create_schema():
    '''
    Test the create schema
    '''
    payload = {
        'name': 'test1',
        'description': '',
        'type': 'SSH',
        'settings': {},
        'permissions': PERMISSION_DATA,
    }
    test_resp = {
        'name': 'test1',
        'description': '',
        'type': 'SSH',
        'settings': {},
        'permissions': PERMISSION_VALIDATED_DATA,
    }
    schema = CredentialsCreateSchema()
    assert test_resp == schema.dump(schema.load(payload))

    with pytest.raises(ValidationError):
        payload['permissions'] = 'something'
        schema.load(payload)

    with pytest.raises(ValidationError):
        payload['permissions'] = ['something']
        schema.load(payload)
