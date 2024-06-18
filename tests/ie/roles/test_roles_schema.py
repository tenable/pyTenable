'''
Testing the roles schemas
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.roles.schema import RoleSchema, RolePermissionsSchema


@pytest.fixture()
def role_schema():
    return [{
        'name': 'name',
        'description': 'description'
    }]


def test_role_schema(role_schema):
    '''
    Test the role schema with create payload inputs
    '''
    test_resp = [{
        'id': 1,
        'name': 'name',
        'description': 'description',
        'permissions': [{
            'entityName': 'entity_name',
            'action': 'action',
            'entityIds': [1, 2],
            'dynamicId': 'some dynamic id'
        }]
    }]

    schema = RoleSchema()
    req = schema.dump(schema.load(role_schema, many=True), many=True)[0]
    assert test_resp[0]['name'] == req['name']
    assert test_resp[0]['description'] == req['description']

    with pytest.raises(ValidationError):
        role_schema[0]['some_val'] = 'something'
        schema.load(role_schema, many=True)


@pytest.fixture()
def role_permission_schema():
    return [{
        'entityName': 'entity_name',
        'action': 'action',
        'entityIds': [1, 2],
        'dynamicId': 'some dynamic id'
    }]


def test_role_permission_schema(role_permission_schema):
    '''
    Test the role schema with replace role permissions payload inputs
    '''
    test_resp = [{
        'id': 1,
        'name': 'name',
        'description': 'description',
        'permissions': [{
            'entityName': 'entity_name',
            'action': 'action',
            'entityIds': [1, 2],
            'dynamicId': 'some dynamic id'
        }]
    }]

    schema = RolePermissionsSchema()
    req = schema.dump(
        schema.load(role_permission_schema, many=True),
        many=True)[0]
    assert test_resp[0]['permissions'][0]['entityName'] == req['entityName']
    assert test_resp[0]['permissions'][0]['action'] == req['action']
    assert test_resp[0]['permissions'][0]['entityIds'] == req['entityIds']
    assert test_resp[0]['permissions'][0]['dynamicId'] == req['dynamicId']

    with pytest.raises(ValidationError):
        role_permission_schema[0]['some_val'] = 'something'
        schema.load(role_permission_schema, many=True)
