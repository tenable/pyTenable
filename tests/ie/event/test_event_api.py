'''API tests for Event APIs'''
import datetime
import responses
from tests.ie.conftest import RE_BASE


@responses.activate
def test_event_details(api):
    '''test for details method response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/directories/1/events/1',
                  json={
                      'ad_object_id': 1,
                      'date': '2022-01-10T13:57:47.340Z',
                      'directory_id': 1,
                      'id': 1,
                      'type': 'some_type'
                  }
                  )
    resp = api.event.details(event_id='1',
                             infrastructure_id='1',
                             directory_id='1')
    assert isinstance(resp, dict)
    assert resp['ad_object_id'] == 1
    assert resp['date'] == datetime.datetime(2022, 1, 10, 13, 57, 47, 340000,
                                             tzinfo=datetime.timezone.utc)
    assert resp['directory_id'] == 1
    assert resp['id'] == 1
    assert resp['type'] == 'some_type'


@responses.activate
def test_event_search_events(api):
    '''test for search event method response'''
    responses.add(responses.POST,
                  f'{RE_BASE}/events/search',
                  json=[{
                      'ad_object_id': 1,
                      'date': '2022-01-12T09:24:11.000Z',
                      'directory_id': 1,
                      'id': 1,
                      'type': 'object_type'
                  }, {
                      'ad_object_id': 2,
                      'date': '2022-01-13T09:24:11.000Z',
                      'directory_id': 2,
                      'id': 2,
                      'type': 'object_type'
                  }]
                  )
    resp = api.event.search_events(
        expression={'OR': [{'systemOnly': 'True'}]},
        profile_id=1,
        date_start='2022-01-05T00:00:00.000Z',
        date_end='2022-01-12T23:59:59.999Z',
        directory_ids=[2],
        order='desc'
    )

    assert isinstance(resp, list)
    assert len(resp) == 2
    assert resp[0]['ad_object_id'] == 1
    assert resp[0]['date'] == datetime.datetime(2022, 1, 12, 9, 24, 11,
                                                tzinfo=datetime.timezone.utc)
    assert resp[0]['directory_id'] == 1
    assert resp[0]['id'] == 1
    assert resp[0]['type'] == 'object_type'

    assert resp[1]['ad_object_id'] == 2
    assert resp[1]['date'] == datetime.datetime(2022, 1, 13, 9, 24, 11,
                                                tzinfo=datetime.timezone.utc)
    assert resp[1]['directory_id'] == 2
    assert resp[1]['id'] == 2
    assert resp[1]['type'] == 'object_type'
