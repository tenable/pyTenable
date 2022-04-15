import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)

WAS_FOLDERS_BASE_URL = 'https://cloud.tenable.com/api/v3/was/folders'
SAMPLE_FOLDER_ID = '178fe279-4e37-49ee-a5dc-8a447dd7043a'
SAMPLE_FOLDER = {
    'folder_id': SAMPLE_FOLDER_ID,
    'name': 'Folder name'
}


@responses.activate
def test_create(api):
    '''
    Test was folders create method
    '''
    responses.add(
        responses.POST,
        WAS_FOLDERS_BASE_URL,
        json=SAMPLE_FOLDER
    )
    folder = api.v3.was.folders.create(SAMPLE_FOLDER['name'])
    assert isinstance(folder, dict)
    assert folder['folder_id'] == SAMPLE_FOLDER_ID


@responses.activate
def test_delete(api):
    '''
    Test was folders delete method
    '''
    responses.add(
        responses.DELETE,
        f'{WAS_FOLDERS_BASE_URL}/{SAMPLE_FOLDER_ID}'
    )
    resp = api.v3.was.folders.delete(SAMPLE_FOLDER_ID)
    assert resp is None


@responses.activate
def test_edit(api):
    '''
    Test was folders edit method
    '''
    payload = SAMPLE_FOLDER
    new_name = 'updated name'
    payload['name'] = new_name
    responses.add(
        responses.PUT,
        f'{WAS_FOLDERS_BASE_URL}/{SAMPLE_FOLDER_ID}',
        json=SAMPLE_FOLDER,
    )
    resp = api.v3.was.folders.edit(SAMPLE_FOLDER_ID, new_name)
    assert resp == SAMPLE_FOLDER


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    fields = [
        'name',
        'type',
        'id'
    ]
    sort = [('name', 'desc')]
    filters = ('name', 'eq', 'Western Region')

    payload = {
        'fields': fields,
        'filter': {
            'property': 'name',
            'operator': 'eq',
            'value': 'Western Region'
        }
    }

    api_response = {
        'folders': [
            {
                'folder_id': 'd6280b0f-8cc2-4cbb-bf94-375079e94fef',
                'name': 'Western Region'
            }
        ],
        'pagination': {
            'total': 1
        }
    }
    responses.add(
        responses.POST,
        f'{WAS_FOLDERS_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.was.folders.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.was.folders.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.was.folders.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)
