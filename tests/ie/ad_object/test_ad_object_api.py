import responses

from tenable.ie.ad_object.api import ADObjectIterator
from tests.ie.conftest import RE_BASE


@responses.activate
def test_ad_object_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/directories/1/ad-objects/1',
                  json={
                      'directory_id': 1,
                      'id': 1,
                      'object_attributes': [{
                          'name': 'accountexpires',
                          'value': '"NEVER"',
                          'value_type': 'string'
                      }],
                      'object_id': '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                      'type': 'LDAP'
                  }
                  )
    resp = api.ad_object.details(
        infrastructure_id='1',
        directory_id='1',
        ad_object_id='1'
    )
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['directory_id'] == 1
    assert resp['object_attributes'][0]['name'] == 'accountexpires'
    assert resp['object_attributes'][0]['value'] == '"NEVER"'
    assert resp['object_attributes'][0]['value_type'] == 'string'
    assert resp['object_id'] == '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert resp['type'] == 'LDAP'


@responses.activate
def test_ad_object_details_by_profile_and_checker(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/checkers/1/ad-objects/1',
                  json={
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
                  }
                  )
    resp = api.ad_object.details_by_profile_and_checker(
        profile_id='1',
        checker_id='1',
        ad_object_id='1'
    )
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['directory_id'] == 1
    assert resp['object_attributes'][0]['name'] == 'accountexpires'
    assert resp['object_attributes'][0]['value'] == '"NEVER"'
    assert resp['object_attributes'][0]['value_type'] == 'string'
    assert resp['object_id'] == '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert resp['reasons'] == [1]
    assert resp['type'] == 'LDAP'


@responses.activate
def test_ad_object_details_by_event(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/'
                  f'directories/1/events/1/ad-objects/1',
                  json={
                      'directory_id': 1,
                      'id': 1,
                      'object_attributes': [{
                          'name': 'accountexpires',
                          'value': '"NEVER"',
                          'value_type': 'string'
                      }],
                      'object_id': '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                      'type': 'LDAP'
                  }
                  )
    resp = api.ad_object.details_by_event(
        infrastructure_id='1',
        directory_id='1',
        event_id='1',
        ad_object_id='1'
    )
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['directory_id'] == 1
    assert resp['object_attributes'][0]['name'] == 'accountexpires'
    assert resp['object_attributes'][0]['value'] == '"NEVER"'
    assert resp['object_attributes'][0]['value_type'] == 'string'
    assert resp['object_id'] == '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert resp['type'] == 'LDAP'


@responses.activate
def test_ad_object_get_changes(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1/'
                  f'directories/1/events/1/ad-objects/1/changes'
                  f'?wantedValues=after'
                  f'&wantedValues=before'
                  f'&wantedValues=current',
                  json=[{
                      'attribute_name': 'whencreated',
                      'value_type': 'string',
                      'values': {
                          'after': '"2021-07-29T12:27:50.0000000Z"',
                          'before': None,
                          'current': '"2021-07-29T12:27:50.0000000Z"'
                      }
                  }]
                  )
    resp = api.ad_object.get_changes(
        infrastructure_id='1',
        directory_id='1',
        ad_object_id='1',
        event_id='1',
        wanted_values=['after', 'before', 'current']
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['attribute_name'] == 'whencreated'
    assert resp[0]['value_type'] == 'string'
    assert resp[0]['values']['after'] == '"2021-07-29T12:27:50.0000000Z"'
    assert resp[0]['values']['before'] is None
    assert resp[0]['values']['current'] == '"2021-07-29T12:27:50.0000000Z"'


@responses.activate
def test_ad_object_search_all(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/checkers/1/ad-objects/search',
                  json=[{
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
                  )
    ado = api.ad_object.search_all(
        profile_id='1',
        checker_id='1',
        show_ignored=True,
        reasons=[1],
        directories=[1],
        expression={'OR': [{'whencreated': '2021-07-29T12:27:50.0000000Z'}]},
        date_end='2022-12-31T18:30:00.000Z',
        date_start='2021-12-31T18:30:00.000Z',
        page=1,
        per_page=10,
        max_pages=10,
        max_items=1000
    )
    assert isinstance(ado, ADObjectIterator)

    resp = ado.next()
    assert resp['id'] == 1
    assert resp['directory_id'] == 1
    assert resp['object_attributes'][0]['name'] == 'accountexpires'
    assert resp['object_attributes'][0]['value'] == '"NEVER"'
    assert resp['object_attributes'][0]['value_type'] == 'string'
    assert resp['object_id'] == '1:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert resp['reasons'] == [1]
    assert resp['type'] == 'LDAP'
