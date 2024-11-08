'''tests for reason APIs'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_reason_list(api):
    responses.add(responses.GET, f'{RE_BASE}/reasons',
                  json=[{
                      'id': 1,
                      'codename': 'codename',
                      'name': 'some_name',
                      'description': 'DESCRIPTION'
                  }])
    req = api.reason.list()
    assert isinstance(req, list)
    assert req[0]['id'] == 1
    assert req[0]['codename'] == 'codename'
    assert req[0]['description'] == 'DESCRIPTION'
    assert req[0]['name'] == 'some_name'


@responses.activate
def test_reason_details(api):
    responses.add(responses.GET, f'{RE_BASE}/reasons/1',
                  json={
                      'id': 1,
                      'codename': 'codename',
                      'name': 'some_name',
                      'description': 'DESCRIPTION'
                  })
    req = api.reason.details(reason_id='1')
    assert isinstance(req, dict)
    assert req['id'] == 1
    assert req['codename'] == 'codename'
    assert req['description'] == 'DESCRIPTION'
    assert req['name'] == 'some_name'


@responses.activate
def test_reason_list_having_deviances(api):
    responses.add(responses.GET, f'{RE_BASE}/profiles/1/checkers/1/reasons',
                  json=[{
                      'id': 1,
                      'codename': 'codename',
                      'name': 'some_name',
                      'description': 'DESCRIPTION'
                  }])
    req = api.reason.list_by_checker(profile_id='1', checker_id='1')
    assert isinstance(req, list)
    assert req[0]['id'] == 1
    assert req[0]['codename'] == 'codename'
    assert req[0]['description'] == 'DESCRIPTION'
    assert req[0]['name'] == 'some_name'


@responses.activate
def test_reason_list_having_deviance_with_profile_directory_event(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/infrastructures/1/directories/1/'
                  f'events/1/reasons',
                  json=[{
                      'codename': 'codename',
                      'description': 'DESCRIPTION',
                      'id': 1,
                      'name': 'some_name'
                  }])
    req = api.reason.list_by_directory_and_event(profile_id='1',
                                                 infrastructure_id='1',
                                                 directory_id='1',
                                                 event_id='1')
    assert isinstance(req, list)
    assert req[0]['id'] == 1
    assert req[0]['codename'] == 'codename'
    assert req[0]['description'] == 'DESCRIPTION'
    assert req[0]['name'] == 'some_name'
