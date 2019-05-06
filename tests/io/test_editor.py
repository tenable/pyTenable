from tenable.errors import *
from ..checker import check, single
import pytest

###
### As the editor endpoints are really meant to drive the UI, the tests here
### are mostly focused on checking the error conditions for the endpoints that
### were exposed in the API documentation to verify that we will be sending
### clean data to the API.  We will NOT be making any calls here, except
### for the list command.
###

@pytest.mark.vcr()
def test_editor_audits_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.audits(1, 1, 1)

@pytest.mark.vcr()
def test_editor_audits_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.audits('nope', 1, 1)

@pytest.mark.vcr()
def test_editor_audits_object_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.audits('scan', 'nope', 1)

@pytest.mark.vcr()
def test_editor_audits_file_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.audits('scan', 1, 'nope')

@pytest.mark.vcr()
def test_editor_template_details_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.template_details(1, 'uuid')

@pytest.mark.vcr()
def test_editor_template_details_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.template_details('nope', 'uuid')

@pytest.mark.vcr()
def test_editor_template_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.template_details('scan', 1)

@pytest.mark.vcr()
def test_editor_details_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.details(1, 'uuid')

@pytest.mark.vcr()
def test_editor_details_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.details('nope', 'uuid')

@pytest.mark.vcr()
def test_editor_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.details('scan', 'nope')

@pytest.mark.vcr()
def test_editor_template_list_etype_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.template_list(1)

@pytest.mark.vcr()
def test_editor_template_list_etype_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.editor.template_list('nope')

@pytest.mark.vcr()
def test_editor_template_list(api):
    items = api.editor.template_list('scan')
    assert isinstance(items, list)

@pytest.mark.vcr()
def test_editor_plugin_desc_policy_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.plugin_description('nope', 1, 1)

@pytest.mark.vcr()
def test_editor_plugin_desc_family_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.plugin_description(1, 'nope', 1)

@pytest.mark.vcr()
def test_editor_plugin_desc_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.editor.plugin_description(1, 1, 'nope')