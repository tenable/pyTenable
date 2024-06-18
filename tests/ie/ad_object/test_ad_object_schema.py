'''
Testing the AD Object schema
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.ad_object.schema import ADObjectSchema, ADObjectChangesSchema


def test_ad_object_schema():
    '''
    test ad object schema
    '''
    test_resp = [{
        'directory_id': 1,
        'id': 1,
        'object_attributes': [{
            'name': 'accountexpires',
            'value': '"NEVER"',
            'value_type': 'string'
        }],
        'object_id': '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'reasons': [1],
        'type': 'LDAP'
    }]

    schema = ADObjectSchema(many=True)
    resp = schema.load(test_resp)
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['directory_id'] == 1
    assert resp[0]['object_attributes'][0]['name'] == 'accountexpires'
    assert resp[0]['object_attributes'][0]['value'] == '"NEVER"'
    assert resp[0]['object_attributes'][0]['value_type'] == 'string'
    assert resp[0]['object_id'] == '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert resp[0]['reasons'] == [1]
    assert resp[0]['type'] == 'LDAP'

    with pytest.raises(ValidationError):
        test_resp[0]['some_val'] = 'something'
        schema.load(test_resp)


def test_ad_object_change_schema():
    '''
    test ad object change schema
    '''
    test_resp = [{
        'attribute_name': 'whencreated',
        'value_type': 'string',
        'values': {
            'after': '"2021-07-29T12:27:50.0000000Z"',
            'before': None,
            'current': '"2021-07-29T12:27:50.0000000Z"'
        }
    }]

    schema = ADObjectChangesSchema(many=True)
    resp = schema.load(test_resp)
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['attribute_name'] == 'whencreated'
    assert resp[0]['value_type'] == 'string'
    assert resp[0]['values']['after'] == '"2021-07-29T12:27:50.0000000Z"'
    assert resp[0]['values']['before'] is None
    assert resp[0]['values']['current'] == '"2021-07-29T12:27:50.0000000Z"'

    with pytest.raises(ValidationError):
        test_resp[0]['some_val'] = 'something'
        schema.load(test_resp)
