from .fixtures import *
from tenable.errors import *

###
### As the editor endpoints are really meant to drive the UI, the tests here
### are mostly focused on checking the error conditions for the endpoints that
### were exposed in the API documentation to verify that we will be sending
### clean data to the API.  We will NOT be making any calls here, except
### for the list command.
###

def test_audits_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.audits(1, 1, 1)

def test_audits_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.audits('nope', 1, 1)

def test_audits_object_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.audits('scan', 'nope', 1)

def test_audits_file_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.audits('scan', 1, 'nope')

def test_details_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.details(1, 'uuid')

def test_details_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.details('nope', 'uuid')

def test_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.details('scan', 1)

def test_edit_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.edit(1, 'uuid')

def test_edit_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.edit('nope', 'uuid')

def test_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.edit('scan', 'nope')

def test_list_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.list(1)

def test_list_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.list('nope')

def test_list(api):
    items = api.editor.list('scan')
    assert isinstance(items, list)

def test_plugin_desc_policy_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.plugin_description('nope', 1, 1)

def test_plugin_desc_family_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.plugin_description(1, 'nope', 1)

def test_plugin_desc_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.plugin_description(1, 1, 'nope')