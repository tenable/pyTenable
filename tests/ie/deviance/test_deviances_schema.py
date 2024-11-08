'''
Testing the Deviance schema
'''
import datetime
import pytest
from marshmallow import ValidationError
from tenable.ie.deviance.schema import DevianceSchema


def test_deviance_schema_response():
    '''
    test deviance schema response
    '''
    test_resp = [{
        'adObjectId': 1,
        'attributes': [{
            'name': 'attribute',
            'value': 'test'
        }],
        'checkerId': 1,
        'createdEventId': 1,
        'description': {
            'replacements': [{
                'name': 'attribute',
                'valueType': 'string'
            }],
            'template': 'template'
        },
        'devianceProviderId': '1',
        'directoryId': 1,
        'eventDate': '2021-07-30T00:59:12.000Z',
        'id': 1,
        'ignoreUntil': None,
        'profileId': 1,
        'reasonId': 1,
        'resolvedAt': '2021-08-23T07:30:41.000Z',
        'resolvedEventId': 1
    }]

    schema = DevianceSchema(many=True)
    resp = schema.load(test_resp)
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['ad_object_id'] == 1
    assert resp[0]['attributes'][0]['name'] == 'attribute'
    assert resp[0]['attributes'][0]['value'] == 'test'
    assert resp[0]['checker_id'] == 1
    assert resp[0]['createdEventId'] == 1
    assert resp[0]['description']['replacements'][0]['name'] == 'attribute'
    assert resp[0]['description']['replacements'][0]['value_type'] == 'string'
    assert resp[0]['description']['template'] == 'template'
    assert resp[0]['deviance_provider_id'] == '1'
    assert resp[0]['directory_id'] == 1
    assert resp[0]['event_date'] == datetime.datetime(
        2021, 7, 30, 0, 59, 12, tzinfo=datetime.timezone.utc)
    assert resp[0]['id'] == 1
    assert resp[0]['ignore_until'] is None
    assert resp[0]['profile_id'] == 1
    assert resp[0]['reason_id'] == 1
    assert resp[0]['resolvedEventId'] == 1
    assert resp[0]['resolved_at'] == datetime.datetime(
        2021, 8, 23, 7, 30, 41, tzinfo=datetime.timezone.utc)

    with pytest.raises(ValidationError):
        test_resp[0]['some_val'] = 'something'
        schema.load(test_resp)
