"""
test folders
"""

import uuid

import pytest

from ..checker import check


@pytest.mark.vcr()
def test_folders_create(folder):
    """test to create folder"""
    assert isinstance(folder, int)


@pytest.mark.vcr()
def test_folders_delete(api, folder):
    """test to delete a folder"""
    api.folders.delete(folder)
    assert folder not in [f['id'] for f in api.folders.list()]


@pytest.mark.vcr()
def test_folders_edit(api, folder):
    """test to raise the exception when type of chunk_size is not as defined"""
    api.folders.edit(folder, str(uuid.uuid4())[:20])


@pytest.mark.vcr()
def test_folders_list(api):
    """test to list the folders"""
    folders = api.folders.list()
    assert isinstance(folders, list)
    for data in folders:
        check(data, 'custom', int)
        check(data, 'default_tag', int)
        check(data, 'name', str)
        check(data, 'type', str)
        check(data, 'id', int)
        check(data, 'unread_count', int)
