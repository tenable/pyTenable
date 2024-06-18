'''tests for dashboard APIs'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_dashboard_details(api):
    '''testing the details response with the actual details response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/dashboards/1',
                  json={
                      'id': 2,
                      'name': 'test_name',
                      'order': 5,
                      'userId': 10
                  }
                  )
    resp = api.dashboard.details(dashboard_id='1')
    assert isinstance(resp, dict)
    assert resp['name'] == 'test_name'


@responses.activate
def test_dashboard_create(api):
    '''testing the create response with the actual create response'''
    responses.add(responses.POST,
                  f'{RE_BASE}/dashboards',
                  json={
                      'id': 3,
                      'name': 'test_dashboard',
                      'order': 10,
                      'userId': 20
                  }
                  )
    resp = api.dashboard.create(name='test_dashboard', order=5)
    assert isinstance(resp, dict)
    assert resp['name'] == 'test_dashboard'


@responses.activate
def test_dashboard_list(api):
    '''testing the list response with the actual list response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/dashboards',
                  json=[{
                      'id': 1,
                      'name': 'test_dashboard1',
                      'order': 1,
                      'userId': 1001
                  }, {
                      'id': 2,
                      'name': 'test_dashboard2',
                      'order': 2,
                      'userId': 1002
                  }]
                  )
    resp = api.dashboard.list()
    assert isinstance(resp, list)
    assert len(resp) == 2


@responses.activate
def test_dashboard_update(api):
    '''testing the update response with the actual update response'''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/dashboards/1',
                  json=[{
                      'id': 1,
                      'name': 'updated_test_dashboard',
                      'order': 10,
                      'userId': 20
                  }]
                  )
    resp = api.dashboard.update(dashboard_id='1',
                                name='test_dashboard',
                                order=1)
    assert isinstance(resp, list)
    assert resp[0]['name'] == 'updated_test_dashboard'


@responses.activate
def test_dashboard_delete(api):
    '''testing the delete response with the actual delete response'''
    responses.add(responses.DELETE,
                  f'{RE_BASE}/dashboards/1',
                  json=None)
    resp = api.dashboard.delete(dashboard_id='1')
    assert resp is None
