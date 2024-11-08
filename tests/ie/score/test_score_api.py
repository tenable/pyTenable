'''tests for score API endpoints'''
import pytest
import responses
from marshmallow import ValidationError

from tests.ie.conftest import RE_BASE


@responses.activate
def test_score_list_required_param(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/scores',
                  json=[{
                      'directoryId': 3,
                      'score': 100
                  }, {
                      'directoryId': 9,
                      'score': 100
                  }]
                  )
    resp = api.score.list(profile_id='1')
    assert isinstance(resp, list)
    assert len(resp) == 2


@responses.activate
def test_score_list_optional_params_single_element(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/scores?directoryIds=3&checkerIds=1'
                  f'&reasonIds=1',
                  json=[{
                      'directoryId': 3,
                      'score': None
                  }]
                  )
    resp = api.score.list(profile_id='1',
                          directory_ids='3',
                          checker_ids='1',
                          reason_ids='1')
    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
def test_score_list_optional_params_multiple_elements(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/scores?checkerIds=3&checkerIds=4'
                  f'&directoryIds=3&directoryIds=4&reasonIds=3&reasonIds=4',
                  json=[{
                      'directoryId': 3,
                      'score': 100
                  }, {
                      'directoryId': 4,
                      'score': None
                  }]
                  )
    resp = api.score.list(profile_id='1', directory_ids=['3', '4'],
                          checker_ids=['3', '4'],
                          reason_ids=['3', '4'])
    assert isinstance(resp, list)
    assert len(resp) == 2


@responses.activate
def test_score_validation_error(api):
    '''
    test to raise the exception when directory_ids doesn't match with
    expected type
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/scores?checkerIds=3&checkerIds=4'
                  f'&directoryIds=3&directoryIds=4&reasonIds=3&reasonIds=4',
                  json=[{
                      'directoryId': 3,
                      'score': 100
                  }, {
                      'directoryId': 4,
                      'score': None
                  }]
                  )
    with pytest.raises(ValidationError):
        api.score.list(profile_id='1', directory_ids=True)
