'''
Testing the users schemas
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.users.schema import UserSchema, UserInfoSchema


@pytest.fixture()
def users_schema():
    return {
        'name': 'some name',
        'email': 'test@domain.com',
        'password': 'some password',
        'surname': 'surname',
        'department': 'some department',
        'biography': 'some biography',
        'active': True,
        'picture': [1, 2]
    }


def test_users_schema(users_schema):
    '''
    Test the users schema
    '''
    test_resp = {
        'id': 1,
        'surname': 'surname',
        'name': 'some name',
        'email': 'test@domain.com',
        'lockedOut': True,
        'department': 'some department',
        'biography': 'some biography',
        'active': True,
        'picture': [1, 2],
        'roles': [1, 2],
        'identifier': 'some identifier',
        'provider': 'tenable',
        'eulaVersion': 1
    }

    schema = UserSchema()
    del users_schema['password']
    req = schema.dump(schema.load(users_schema))
    for key in users_schema:
        assert test_resp[key] == req[key]
    with pytest.raises(ValidationError):
        users_schema['some_val'] = 'something'
        schema.load(users_schema)


@pytest.fixture()
def users_schema_many():
    return [{
        'name': 'some name',
        'email': 'test@domain.com',
        'password': 'some password',
        'surname': 'surname',
        'department': 'some department',
        'biography': 'some biography',
        'active': True,
        'picture': [1, 2]
    }]


def test_users_schema_many(users_schema_many):
    '''
    Test the users schema for create (many=True)
    '''
    test_resp = [{
        'id': 1,
        'surname': 'surname',
        'name': 'some name',
        'email': 'test@domain.com',
        'lockedOut': True,
        'department': 'some department',
        'biography': 'some biography',
        'active': True,
        'picture': [1, 2],
        'roles': [1, 2],
        'identifier': 'some identifier',
        'provider': 'tenable',
        'eulaVersion': 1
    }]

    schema = UserSchema()
    del users_schema_many[0]['password']
    req = schema.dump(schema.load(users_schema_many, many=True), many=True)
    for key in users_schema_many[0]:
        assert test_resp[0][key] == req[0][key]
    with pytest.raises(ValidationError):
        users_schema_many[0]['some_val'] = 'something'
        schema.load(users_schema_many, many=True)


@pytest.fixture()
def users_info_schema():
    return {
        'surname': 'surname',
        'name': 'some name',
        'email': 'test@domain.com',
        'lockedOut': True,
        'department': 'some department',
        'biography': 'some biography',
        'active': True,
        'picture': [1, 2],
        'roles': [{
            'name': 'role name',
            'description': 'role description',
            'permissions': [{
                'entityName': 'entity_name',
                'action': 'action',
                'entityIds': [1, 2],
                'dynamicId': 'some dynamic id'
            }]
        }],
        'identifier': 'some identifier',
        'provider': 'tenable',
        'eulaVersion': 1,
        'internal': True
    }


def test_users_info_schema(users_info_schema):
    '''
    Test the users info schema
    users info schema doesn't have input payload, to test response we are providing dummy input.
    '''
    test_resp = {
        'id': 1,
        'surname': 'surname',
        'name': 'some name',
        'email': 'test@domain.com',
        'lockedOut': True,
        'department': 'some department',
        'biography': 'some biography',
        'active': True,
        'picture': [1, 2],
        'roles': [{
            'id': 1,
            'name': 'role name',
            'description': 'role description',
            'permissions': [{
                'entityName': 'entity_name',
                'action': 'action',
                'entityIds': [1, 2],
                'dynamicId': 'some dynamic id'
            }]
        }],
        'identifier': 'some identifier',
        'provider': 'tenable',
        'eulaVersion': 1,
        'internal': True
    }

    schema = UserInfoSchema()
    req = schema.dump(schema.load(users_info_schema))
    assert req['surname'] == test_resp['surname']
    assert req['name'] == test_resp['name']
    assert req['email'] == test_resp['email']
    assert req['lockedOut'] == test_resp['lockedOut']
    assert req['department'] == test_resp['department']
    assert req['biography'] == test_resp['biography']
    assert req['active'] == test_resp['active']
    assert req['picture'] == test_resp['picture']
    assert req['identifier'] == test_resp['identifier']
    assert req['provider'] == test_resp['provider']
    assert req['eulaVersion'] == test_resp['eulaVersion']
    assert req['internal'] == test_resp['internal']
    assert req['roles'][0]['name'] == test_resp['roles'][0]['name']
    assert req['roles'][0]['description'] == test_resp['roles'][0]['description']
    assert req['roles'][0]['permissions'][0]['entityName'] == test_resp['roles'][0]['permissions'][0]['entityName']
    assert req['roles'][0]['permissions'][0]['action'] == test_resp['roles'][0]['permissions'][0]['action']
    assert req['roles'][0]['permissions'][0]['entityIds'] == test_resp['roles'][0]['permissions'][0]['entityIds']
    assert req['roles'][0]['permissions'][0]['dynamicId'] == test_resp['roles'][0]['permissions'][0]['dynamicId']

    with pytest.raises(ValidationError):
        users_info_schema['some_val'] = 'something'
        schema.load(users_info_schema)


@pytest.fixture()
def users_schema_for_update_user_role():
    return {
        'roles': [1, 2]
    }


def test_users_schema_for_update_user_role(users_schema_for_update_user_role):
    '''
    Test the users schema for updating user roles
    '''
    test_resp = {
        'roles': [1, 2]
    }

    schema = UserSchema()
    assert test_resp['roles'] == schema.dump(schema.load(users_schema_for_update_user_role))['roles']
    with pytest.raises(ValidationError):
        users_schema_for_update_user_role['some_val'] = 'something'
        schema.load(users_schema_for_update_user_role)
