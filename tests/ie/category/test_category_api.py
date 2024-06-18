'''tests for category APIs'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_category_details(api):
    '''testing the details response with the actual details response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/categories/1',
                  json={
                      'id': 1,
                      'name': 'test_name'
                  }
                  )
    resp = api.category.details(category_id='1')
    assert isinstance(resp, dict)
    assert resp['name'] == 'test_name'


@responses.activate
def test_category_list(api):
    '''testing the list response with the actual list response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/categories',
                  json=[{
                      'id': 1,
                      'name': 'test_category1'
                  }, {
                      'id': 2,
                      'name': 'test_category2'
                  }]
                  )
    resp = api.category.list()
    assert isinstance(resp, list)
    assert len(resp) == 2
