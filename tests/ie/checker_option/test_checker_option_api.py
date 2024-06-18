'''tests for checker option APIs'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_checker_option_list(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/checkers/1/checker-options?staged=0',
                  json=[{
                      'checkerId': 1,
                      'codename': 'O-DUMMY-OPTION',
                      'description': 'Example of an option users can give '
                                     'to this checker.',
                      'directoryId': None,
                      'id': 2609,
                      'name': 'Option example',
                      'profileId': 1,
                      'staged': False,
                      'value': 'true',
                      'valueType': 'boolean'
                  }]
                  )
    resp = api.checker_option.list(profile_id='1',
                                   checker_id='1',
                                   staged=False,
                                   )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['checker_id'] == 1
    assert resp[0]['profile_id'] == 1
    assert resp[0]['staged'] is False


@responses.activate
def test_checker_option_create(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/checkers/1/checker-options',
                  json=[{
                      'checkerId': 1,
                      'codename': 'codename',
                      'description': None,
                      'directoryId': None,
                      'id': 3269,
                      'name': None,
                      'profileId': 1,
                      'staged': True,
                      'value': 'false',
                      'valueType': 'boolean'
                  }]
                  )
    resp = api.checker_option.create(profile_id='1',
                                     checker_id='1',
                                     codename='codename',
                                     value='false',
                                     value_type='boolean')
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['checker_id'], resp[0]['profile_id'] == 1
    assert resp[0]['staged'] is True
