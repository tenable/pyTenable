'''
Testing the alert schema
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.alert.schema import AlertSchema, AlertParamsSchema


@pytest.fixture()
def alert_schema():
    return {
        'archived': True,
        'read': True
    }


def test_alert_schema(alert_schema):
    '''
    test alert schema
    '''
    test_resp = {
        'id': 1,
        'devianceId': 1,
        'archived': True,
        'read': True,
        'date': '2021-12-24T13:14:41.194Z',
        'directoryId': 1,
        'infrastructureId': 1
    }

    schema = AlertSchema()
    req = schema.dump(schema.load(alert_schema))
    assert test_resp['archived'] == req['archived']
    assert test_resp['read'] == req['read']

    with pytest.raises(ValidationError):
        alert_schema['some_val'] = 'something'
        schema.load(alert_schema)


def test_alert_param_schema(alert_schema):
    '''
    test alert param schema
    '''
    schema = AlertParamsSchema()
    req = schema.dump(schema.load(alert_schema))
    assert req['archived'] == 'true'
    assert req['read'] == 'true'

    with pytest.raises(ValidationError):
        alert_schema['some_val'] = 'something'
        schema.load(alert_schema)
