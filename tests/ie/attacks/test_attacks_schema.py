'''
Testing the attack schema
'''
import datetime
import pytest
from marshmallow import ValidationError
from tenable.ie.attacks.schema import AttackSchema


@pytest.fixture()
def attacks_schema_request_payload():
    return {
        'resource_type': 'infrastructure',
        'resource_value': '1',
        'attack_type_ids': [1, 2],
        'include_closed': 'false',
        'limit': '10',
        'order': 'asc',
        'search': 'Unknown',
        'date_end': '2022-12-31T18:30:00.000Z',
        'date_start': '2002-12-31T18:30:00.000Z'
    }


def test_attacks_schema_request_payload(attacks_schema_request_payload):
    '''
    test attacks schema list api request payload
    '''
    schema = AttackSchema()
    req = schema.dump(schema.load(attacks_schema_request_payload))
    assert req['resourceType'] == 'infrastructure'
    assert req['resourceValue'] == '1'
    assert req['attackTypeIds'] == [1, 2]
    assert req['includeClosed'] == 'false'
    assert req['limit'] == '10'
    assert req['order'] == 'asc'
    assert req['search'] == 'Unknown'
    assert req['dateEnd'] == '2022-12-31T18:30:00+00:00'
    assert req['dateStart'] == '2002-12-31T18:30:00+00:00'

    with pytest.raises(ValidationError):
        attacks_schema_request_payload['some_val'] = 'something'
        schema.load(attacks_schema_request_payload)


def test_attacks_schema_response_object():
    '''
    test attacks schema list api response object
    '''
    test_resp = [{
        'attackTypeId': 1,
        'date': '2022-01-14T07:24:50.424Z',
        'dc': 'dc',
        'destination': {
            'hostname': 'test',
            'ip': '192.168.1.1',
            'type': 'computer'
        },
        'directoryId': 1,
        'id': 1,
        'isClosed': False,
        'source': {
            'hostname': 'Unknown',
            'ip': '127.0.0.1',
            'type': 'computer'
        },
        'vector': {
            'attributes': [{
                'name': 'source_hostname',
                'value': 'Unknown',
                'valueType': 'string'
            }],
            'template': 'template'
        }
    }]

    schema = AttackSchema()
    resp = schema.load(test_resp, many=True, partial=True)
    assert resp[0]['attack_type_id'] == 1
    assert resp[0]['source']['hostname'] == 'Unknown'
    assert resp[0]['source']['type'] == 'computer'
    assert resp[0]['source']['ip'] == '127.0.0.1'
    assert resp[0]['date'] == datetime.datetime(
        2022, 1, 14, 7, 24, 50, 424000, tzinfo=datetime.timezone.utc)
    assert resp[0]['dc'] == 'dc'
    assert resp[0]['destination']['hostname'] == 'test'
    assert resp[0]['destination']['type'] == 'computer'
    assert resp[0]['destination']['ip'] == '192.168.1.1'
    assert resp[0]['vector']['template'] == 'template'
    assert resp[0]['vector']['attributes'][0]['value'] == 'Unknown'
    assert resp[0]['vector']['attributes'][0]['name'] == 'source_hostname'
    assert resp[0]['vector']['attributes'][0]['value_type'] == 'string'
    assert resp[0]['directory_id'] == 1
    assert resp[0]['is_closed'] == False

    with pytest.raises(ValidationError):
        test_resp[0]['some_val'] = 'something'
        schema.load(test_resp, many=True)
