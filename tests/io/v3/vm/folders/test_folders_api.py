import pytest
import responses

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
    resp = api.v3.vm.folders.edit(SAMPLE_FOLDER_ID, "edit test")
    assert resp is None


@responses.activate
def test_search(api):
    '''
    Test vm folders search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.folders.search()
