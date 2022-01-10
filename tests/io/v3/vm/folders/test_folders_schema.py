'''
Testing the Folders Schema
'''
from tenable.io.v3.vm.folders.schema import FolderSchema

FOLDER_NAME = 'folder'
FOLDER = {
    'name': FOLDER_NAME
}


def test_folders_schema(api):
    schema = FolderSchema()
    payload = schema.dump(schema.load(FOLDER))
    assert payload == FOLDER
