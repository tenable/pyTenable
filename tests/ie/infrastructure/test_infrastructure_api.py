'''tests for infrastructure api'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_infrastructure_create(api):
    '''tests the create API response with actual create response'''
    responses.add(responses.POST,
                  f'{RE_BASE}/infrastructures',
                  json=[{
                      'id': 1,
                      'name': 'test',
                      'login': 'test@gmail.com',
                      'directories': [0, 1, 2]
                  }]
                  )
    resp = api.infrastructure.create(
        name='test',
        login='test@gmail.com',
        password='password'
    )
    assert isinstance(resp, list)
    assert resp[0]['name'] == 'test'


@responses.activate
def test_infrastructure_delete(api):
    '''tests the delete API response with actual delete response'''
    responses.add(responses.DELETE,
                  f'{RE_BASE}/infrastructures/1',
                  json=None
                  )
    resp = api.infrastructure.delete(infrastructure_id=1)
    assert isinstance(resp, list)
    assert len(resp) == 0


@responses.activate
def test_infrastructure_update(api):
    '''tests the update API response with actual update response'''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/infrastructures/1',
                  json={
                      'id': 1,
                      'name': 'test',
                      'login': 'test@gmail.com'
                  }
                  )
    resp = api.infrastructure.update(
        infrastructure_id='1',
        name='test',
        login='test@gmail.com',
        password='password'
    )
    assert isinstance(resp, dict)
    assert resp['name'] == 'test'


@responses.activate
def test_infrastructure_details(api):
    '''tests the details API response with actual details response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures/1',
                  json={
                      'id': 1,
                      'name': 'test',
                      'login': 'test@gmail.com',
                      'directories': [0, 1, 2]
                  }
                  )
    resp = api.infrastructure.details(infrastructure_id='1')
    assert isinstance(resp, dict)
    assert resp['name'] == 'test'
    assert resp['directories'] == [0, 1, 2]


@responses.activate
def test_infrastructure_list(api):
    '''tests the list API response with actual list response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/infrastructures',
                  json=[{
                      'id': 1,
                      'name': 'test',
                      'login': 'test@gmail.com',
                      'directories': [0, 1, 2]
                  }]
                  )
    resp = api.infrastructure.list()
    assert isinstance(resp, list)
    assert resp[0]['name'] == 'test'
    assert resp[0]['directories'] == [0, 1, 2]
