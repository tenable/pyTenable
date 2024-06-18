'''
Testing the attack type option schema
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.attack_type_options.schema import AttackTypeOptionsSchema


@pytest.fixture()
def attacks_type_option_schema():
    return {
        'codename': 'codename',
        'value': '[]',
        'value_type': 'array/string',
        'directory_id': None
    }


def test_attack_type_option_schema(attacks_type_option_schema):
    '''
    test application setting schema request payload
    '''
    test_resp = [{
        'id': 1,
        'codename': 'codename',
        'profileId': 1,
        'attackTypeId': 1,
        'directoryId': None,
        'value': '[]',
        'valueType': 'array/string',
        'name': 'name',
        'description': 'description',
        'translations': ['some translation'],
        'staged': False
    }]
    schema = AttackTypeOptionsSchema()
    req = schema.dump(schema.load(attacks_type_option_schema))
    assert req['codename'] == test_resp[0]['codename']
    assert req['value'] == test_resp[0]['value']
    assert req['valueType'] == test_resp[0]['valueType']
    assert req['directoryId'] == test_resp[0]['directoryId']

    with pytest.raises(ValidationError):
        attacks_type_option_schema['some_val'] = 'something'
        schema.load(attacks_type_option_schema)
