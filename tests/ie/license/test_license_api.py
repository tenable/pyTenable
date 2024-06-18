import datetime
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_license_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/license',
                  json={
                      'customerName': 'pytenable',
                      'maxActiveUserCount': 100,
                      'currentActiveUserCount': 0,
                      'expirationDateUTC': '2021-11-17T13:44:24.259Z',
                      'inAppEula': False,
                      'features': ['something'],
                      'type': 'license type'
                  }
                  )
    resp = api.license.details()
    assert isinstance(resp, dict)
    assert resp['customer_name'] == 'pytenable'
    assert resp['max_active_user_count'] == 100
    assert resp['current_active_user_count'] == 0
    assert resp['expiration_date_utc'] == datetime.datetime(
        2021, 11, 17, 13, 44, 24, 259000, tzinfo=datetime.timezone.utc)
    assert resp['in_app_eula'] == False
    assert resp['features'][0] == 'something'
    assert resp['license_type'] == 'license type'


@responses.activate
def test_license_create(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/license',
                  json={
                      'customerName': 'pytenable',
                      'maxActiveUserCount': 100,
                      'currentActiveUserCount': 0,
                      'expirationDateUTC': '2021-11-17T13:44:24.259Z',
                      'inAppEula': False,
                      'features': ['something'],
                      'type': 'license type'
                  }
                  )
    resp = api.license.create(license='license')
    assert isinstance(resp, dict)
    assert resp['customer_name'] == 'pytenable'
    assert resp['max_active_user_count'] == 100
    assert resp['current_active_user_count'] == 0
    assert resp['expiration_date_utc'] == datetime.datetime(
        2021, 11, 17, 13, 44, 24, 259000, tzinfo=datetime.timezone.utc)
    assert resp['in_app_eula'] == False
    assert resp['features'][0] == 'something'
    assert resp['license_type'] == 'license type'
