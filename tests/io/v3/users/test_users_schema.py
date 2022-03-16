'''
Testing the users schemas
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.users.schema import (UserEditSchema, UsersCommonSchema,
                                        UsersCreateSchema)


@pytest.fixture
def users_create():
    '''
    Example users create request
    '''
    return {
        'username': 'test_username',
        'password': 'password',
        'permissions': 32,
        'name': 'test',
        'email': 'test@tenable.com',
        'type': 'local'
    }


@pytest.fixture
def users_edit():
    '''
    Example users edit request
    '''
    return {
        'permissions': 32,
        'name': 'test',
        'email': 'test@tenable.com',
        'enabled': True
    }


def test_users_create_schema(users_create):
    '''
    Test the users create schema
    '''
    test_resp = {
        'username': 'test_username',
        'password': 'password',
        'permissions': 32,
        'name': 'test',
        'email': 'test@tenable.com',
        'type': 'local'
    }

    schema = UsersCreateSchema()
    assert test_resp == schema.dump(schema.load(users_create))

    with pytest.raises(ValidationError):
        users_create['new_val'] = 'something'
        schema.load(users_create)


def test_users_edit_schema(users_edit):
    '''
    Test the users create schema
    '''
    test_resp = {
        'permissions': 32,
        'name': 'test',
        'email': 'test@tenable.com',
        'enabled': True
    }

    schema = UserEditSchema()
    assert test_resp == schema.dump(schema.load(users_edit))

    with pytest.raises(ValidationError):
        users_edit['new_val'] = 'something'
        schema.load(users_edit)


def test_users_common_schema():
    '''
    Test the users common schema
    '''
    payload = dict(
        email_enabled=True,
        sms_enabled=True,
        sms_phone='3458394544',
        password='password',
        current_password='curr_pass'
    )
    test_resp = {
        'email_enabled': True,
        'sms_enabled': True,
        'sms_phone': '3458394544',
        'password': 'password',
        'current_password': 'curr_pass'
    }

    schema = UsersCommonSchema()
    assert test_resp == schema.dump(schema.load(payload))

    with pytest.raises(ValidationError):
        payload['new_val'] = 'something'
        schema.load(payload)
