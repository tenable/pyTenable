import responses
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

VM_FOLDERS_BASE_URL = 'https://cloud.tenable.com/api/v3/scans/folders'
SAMPLE_FOLDER_ID = 18
SAMPLE_FOLDER = {
    'unread_count': 0,
    'custom': 0,
    'default_tag': 0,
    'type': 'main',
    'name': 'my scans',
    'id': SAMPLE_FOLDER_ID
}
SAMPLE_FOLDER_CREATE = {
    'id': SAMPLE_FOLDER_ID
}


@responses.activate
def test_create(api):
    '''
    Test vm folders create method
    '''
    responses.add(
        responses.POST,
        VM_FOLDERS_BASE_URL,
        json=SAMPLE_FOLDER_CREATE
    )
    resp = api.v3.vm.folders.create(SAMPLE_FOLDER['name'])
    assert resp == SAMPLE_FOLDER_ID


@responses.activate
def test_delete(api):
    '''
    Test vm folders delete method
    '''
    responses.add(
        responses.DELETE,
        f'{VM_FOLDERS_BASE_URL}/{SAMPLE_FOLDER_ID}'
    )
    resp = api.v3.vm.folders.delete(SAMPLE_FOLDER_ID)
    assert resp is None


@responses.activate
def test_edit(api):
    '''
    Test vm folders edit method
    '''
    responses.add(
        responses.PUT,
        f'{VM_FOLDERS_BASE_URL}/{SAMPLE_FOLDER_ID}'
    )
    resp = api.v3.vm.folders.edit(SAMPLE_FOLDER_ID, 'edit test')
    assert resp is None


@responses.activate
def test_search(api):
    '''
    Test vm folders search method
    '''
    response = {
        'folders': [
            {
                'id': 18,
                'name': 'Trash',
                'type': 'trash',
                'unread_count': 0
            }
        ]
    }
    fields = [
        'id',
        'name',
        'type',
        'unread_count'
    ]
    filters = {
        'and': [
            {
                'property': 'type',
                'operator': 'eq',
                'value': 'trash'
            }
        ]
    }

    api_payload = {
        'fields': fields,
        'filter': filters,
        'limit': 1,
        'sort': [
            {
                'name': 'desc'
            }
        ],
    }

    responses.add(
        responses.POST,
        f'{VM_FOLDERS_BASE_URL}/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )
    resp = api.v3.vm.folders.search(
        fields=fields,
        filter=filters,
        sort=[('name', 'desc')],
        limit=1
    )
    assert isinstance(resp, SearchIterator)

    for ind, folder in enumerate(resp):
        assert folder == response['folders'][ind]

    resp = api.v3.vm.folders.search(
        fields=fields,
        filter=filters,
        sort=[('name', 'desc')],
        limit=1,
        return_csv=True
    )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.vm.folders.search(
        fields=fields,
        filter=filters,
        sort=[('name', 'desc')],
        limit=1,
        return_resp=True
    )
    assert isinstance(resp, Response)
