from .fixtures import *
from tenable.errors import *
import uuid

def test_folder_name_typeerror(api):
    with pytest.raises(TypeError):
        api.folders.create(1)

def test_create(api, folder):
    assert isinstance(folder, int)

def test_delete(api, folder):
    api.folders.delete(folder)
    assert folder not in [f['id'] for f in api.folders.list()]

def test_edit_name_typeerror(api, folder):
    with pytest.raises(TypeError):
        api.folders.edit(folder, 1)

def test_edit(api, folder):
    api.folders.edit(folder, str(uuid.uuid4())[:20])

def test_list(api, folder):
    folders = api.folders.list()
    assert isinstance(folders, list)
    for f in folders:
        check(f, 'custom', int)
        check(f, 'default_tag', int)
        check(f, 'name', str)
        check(f, 'type', str)
        check(f, 'id', int)
        check(f, 'unread_count', int)