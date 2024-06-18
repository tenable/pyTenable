'''Schema test for Event API schemas'''
import datetime
import pytest
from marshmallow import ValidationError
from tenable.ie.event.schema import EventSchema


@pytest.fixture
def event_schema():
    return {
        'expression': {'OR': [{'systemOnly': 'True'}]},
        'profileId': 1,
        'dateStart': '2022-11-12T23:59:10.214Z',
        'dateEnd': '2022-01-13T23:59:59.999Z',
        'directoryIds': [1],
        'order': {'column': 'id', 'direction': 'desc'}
    }


def test_event_schema_search(event_schema):
    '''test to check the Event schema'''
    test_resp = {
        'adObjectId': 1,
        'date': '2022-11-12T23:59:10.214Z',
        'directoryId': 1,
        'id': 1,
        'type': 'type'
    }
    schema = EventSchema()
    req = schema.load(event_schema)
    assert req['date_start'] == datetime.datetime(2022, 11, 12, 23, 59,
                                                  10, 214000,
                                                  tzinfo=datetime.
                                                  timezone.utc)
    assert test_resp['adObjectId'] == 1
    assert test_resp['directoryId'] == 1
    assert test_resp['id'] == 1
    assert test_resp['type'] == 'type'
    with pytest.raises(ValidationError):
        event_schema['new_val'] = 'something'
        schema.load(event_schema)
