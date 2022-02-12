import pytest
import responses


FOLDER = {
    'id': 1,
    'name': 'Example Folder',
    'type': 'custom',
    'default_tag': 1,
    'custom': 1,
    'unread_count': 10
}


@responses.activate
def test_folders_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/folders',
                  json=FOLDER
                  )
    resp = nessus.folders.create('Example Folder')
    assert resp == FOLDER['id']


@responses.activate
def test_folders_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/folders/1'
                  )
    nessus.folders.delete(1)


@responses.activate
def test_folders_edit(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/folders/1',
                  )
    nessus.folders.edit(1, name='Updated Name')


@responses.activate
def test_folders_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/folders',
                  json={'folders': [FOLDER for _ in range(10)]}
                  )
    resp = nessus.folders.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == FOLDER
