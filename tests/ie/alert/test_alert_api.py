import datetime
import responses

from tenable.ie.alert.api import AlertIterator
from tests.ie.conftest import RE_BASE


@responses.activate
def test_alert_list_default(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/alerts',
                  json=[{
                      'id': 1,
                      'devianceId': 1,
                      'archived': False,
                      'read': False,
                      'date': '2021-12-24T13:14:41.194Z',
                      'directoryId': 1,
                      'infrastructureId': 1
                  }]
                  )
    alert = api.alerts.list_by_profile(profile_id='1')
    assert isinstance(alert, AlertIterator)

    resp = alert.next()
    assert resp['id'] == 1
    assert resp['deviance_id'] == 1
    assert resp['archived'] is False
    assert resp['read'] is False
    assert resp['date'] == datetime.datetime(
        2021, 12, 24, 13, 14, 41, 194000, tzinfo=datetime.timezone.utc)
    assert resp['directory_id'] == 1
    assert resp['infrastructure_id'] == 1


@responses.activate
def test_alert_list_parameterized(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/alerts'
                  f'?read=false'
                  f'&archived=false'
                  f'&page=1&perPage=1',
                  json=[{
                      'id': 1,
                      'devianceId': 1,
                      'archived': False,
                      'read': False,
                      'date': '2021-12-24T13:14:41.194Z',
                      'directoryId': 1,
                      'infrastructureId': 1
                  }]
                  )
    alert = api.alerts.list_by_profile(
        profile_id='1',
        archived=False,
        read=False,
        page=1,
        per_page=1,
        max_pages=2,
        max_items=5
    )
    assert isinstance(alert, AlertIterator)

    resp = alert.next()
    assert resp['id'] == 1
    assert resp['deviance_id'] == 1
    assert resp['archived'] is False
    assert resp['read'] is False
    assert resp['date'] == datetime.datetime(
        2021, 12, 24, 13, 14, 41, 194000, tzinfo=datetime.timezone.utc)
    assert resp['directory_id'] == 1
    assert resp['infrastructure_id'] == 1


@responses.activate
def test_alert_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/alerts/1',
                  json={
                      'id': 1,
                      'devianceId': 1,
                      'archived': False,
                      'read': False,
                      'date': '2021-12-24T13:14:41.194Z',
                      'directoryId': 1,
                      'infrastructureId': 1
                  }
                  )
    resp = api.alerts.details(alert_id='1')
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['deviance_id'] == 1
    assert resp['archived'] is False
    assert resp['read'] is False
    assert resp['date'] == datetime.datetime(
        2021, 12, 24, 13, 14, 41, 194000, tzinfo=datetime.timezone.utc)
    assert resp['directory_id'] == 1
    assert resp['infrastructure_id'] == 1


@responses.activate
def test_alert_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/alerts/1',
                  json={
                      'id': 1,
                      'devianceId': 1,
                      'archived': False,
                      'read': False,
                      'date': '2021-12-24T13:14:41.194Z',
                      'directoryId': 1,
                      'infrastructureId': 1
                  }
                  )
    resp = api.alerts.update(
        alert_id='1',
        archived=False,
        read=False
    )
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['deviance_id'] == 1
    assert resp['archived'] is False
    assert resp['read'] is False
    assert resp['date'] == datetime.datetime(
        2021, 12, 24, 13, 14, 41, 194000, tzinfo=datetime.timezone.utc)
    assert resp['directory_id'] == 1
    assert resp['infrastructure_id'] == 1


@responses.activate
def test_alert_update_on_profile(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/profiles/1/alerts',
                  json=None
                  )
    resp = api.alerts.update_on_profile(
        profile_id='1',
        archived=False,
        read=False
    )
    assert resp is None
