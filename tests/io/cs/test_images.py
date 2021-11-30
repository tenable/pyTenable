'''
Test the CS Images API
'''
import re
import pytest
import responses
from tenable.io.cs.iterator import CSIterator


@responses.activate
def test_cs_images_list_endpoint(api):
    '''
    Test images list endpoint
    '''
    responses.add(responses.GET,
                  'https://cloud.tenable.com/container-security/api/v2/images',
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
    assert isinstance(api.cs.images.list(return_json=True), dict)
    assert isinstance(api.cs.images.list(), CSIterator)


@responses.activate
def test_cs_images_details_endpoint(api):
    '''
    Test image details endpoint
    '''
    dummy = {'name': 'Example', 'repository': 'Repo', 'tag': 'TagName'}
    responses.add(responses.GET,
                  re.compile(('https://cloud.tenable.com/container-security'
                              '/api/v2/images/'
                              r'([^/]+)/([^/]+)/([^/]+)'
                              )),
                  json=dummy
                  )
    assert api.cs.images.details('repo', 'name', 'tag') == dummy


@responses.activate
def test_cs_images_delete_endpoint(api):
    '''
    Test image delete endpoint
    '''
    responses.add(responses.DELETE,
                  re.compile(('https://cloud.tenable.com/container-security'
                              '/api/v2/images/'
                              r'([^/]+)/([^/]+)/([^/]+)'
                              ))
                   )
    api.cs.images.delete('repo', 'name', 'tag')
