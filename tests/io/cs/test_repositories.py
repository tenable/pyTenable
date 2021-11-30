'''
Test the CS Images API
'''
import re
import pytest
import responses
from tenable.io.cs.iterator import CSIterator


@responses.activate
def test_cs_repositories_list_endpoint(api):
    '''
    Test Repo list endpoint
    '''
    responses.add(responses.GET,
                  ('https://cloud.tenable.com/container-security'
                   '/api/v2/repositories'
                   ),
                  json={
                    'pagination': {
                        'total': 100,
                    },
                    'items': [
                        {'id': 1, 'name': 'One'},
                        {'id': 2, 'name': 'Two'},
                        {'id': 3, 'name': 'Three'},
                        {'id': 4, 'name': 'Four'},
                        {'id': 5, 'name': 'Five'}
                    ]
                  })
    assert isinstance(api.cs.repositories.list(return_json=True), dict)
    assert isinstance(api.cs.repositories.list(), CSIterator)


@responses.activate
def test_cs_repositories_details_endpoint(api):
    '''
    Test Repo details endpoint
    '''
    dummy = {'name': 'Example', 'repository': 'Repo', 'tag': 'TagName'}
    responses.add(responses.GET,
                  re.compile(('https://cloud.tenable.com/container-security'
                              r'/api/v2/repositories/([^/]+)'
                              )),
                  json=dummy
                  )
    assert api.cs.repositories.details('repo') == dummy


@responses.activate
def test_cs_repositories_delete_endpoint(api):
    '''
    Test repo delete endpoint
    '''
    responses.add(responses.DELETE,
                  re.compile(('https://cloud.tenable.com/container-security'
                              r'/api/v2/repositories/([^/]+)'
                              ))
                  )
    api.cs.repositories.delete('repo')
