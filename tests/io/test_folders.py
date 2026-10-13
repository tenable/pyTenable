"""
test folders
"""

import uuid

import responses

from ..checker import check


@responses.activate
def test_folders_create(tvm, folder):
    """test to create folder"""
    responses.add(responses.POST, 'https://nourl/folders', json={'id': folder})
    folder = tvm.folders.create('example')
    assert isinstance(folder, int)


@responses.activate
def test_folders_delete(tvm, folder):
    """test to delete a folder"""
    responses.add(responses.DELETE, 'https://nourl/folders/13203')
    responses.add(
        responses.GET,
        'https://nourl/folders',
        json={
            'folders': [
                {
                    'unread_count': 48,
                    'custom': 0,
                    'default_tag': 0,
                    'type': 'trash',
                    'name': 'Trash',
                    'id': 10,
                },
                {
                    'unread_count': 104,
                    'custom': 0,
                    'default_tag': 1,
                    'type': 'main',
                    'name': 'My Scans',
                    'id': 11,
                },
            ]
        },
    )
    tvm.folders.delete(folder)
    assert folder not in [f['id'] for f in tvm.folders.list()]


@responses.activate
def test_folders_edit(tvm, folder):
    """test to raise the exception when type of chunk_size is not as defined"""
    responses.add(responses.PUT, 'https://nourl/folders/13203')
    tvm.folders.edit(folder, str(uuid.uuid4())[:20])


@responses.activate
def test_folders_list(tvm):
    """test to list the folders"""
    responses.add(
        responses.GET,
        'https://nourl/folders',
        json={
            'folders': [
                {
                    'unread_count': 48,
                    'custom': 0,
                    'default_tag': 0,
                    'type': 'trash',
                    'name': 'Trash',
                    'id': 10,
                }
            ]
        },
    )
    folders = tvm.folders.list()
    assert isinstance(folders, list)
    for data in folders:
        check(data, 'custom', int)
        check(data, 'default_tag', int)
        check(data, 'name', str)
        check(data, 'type', str)
        check(data, 'id', int)
        check(data, 'unread_count', int)
