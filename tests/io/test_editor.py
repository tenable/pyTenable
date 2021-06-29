'''
test editor
'''
import uuid
import pytest
from tenable.errors import UnexpectedValueError


###
### As the editor endpoints are really meant to drive the UI, the tests here
### are mostly focused on checking the error conditions for the endpoints that
### were exposed in the API documentation to verify that we will be sending
### clean data to the API.  We will NOT be making any calls here, except
### for the list command.
###

@pytest.mark.vcr()
def test_editor_audits_etype_typeerror(api):
    '''test to raise the exception when type of etype is not as defined'''
    with pytest.raises(TypeError):
        api.editor.audits(1, 1, 1)


@pytest.mark.vcr()
def test_editor_audits_etype_unexpectedvalue(api):
    '''test to raise the exception when value of etype is not as defined'''
    with pytest.raises(UnexpectedValueError):
        api.editor.audits('nope', 1, 1)


@pytest.mark.vcr()
def test_editor_audits_object_id_typeerror(api):
    '''test to raise the exception when type of object_id is not as defined'''
    with pytest.raises(TypeError):
        api.editor.audits('scan', 'nope', 1)


@pytest.mark.vcr()
def test_editor_audits_file_id_typeerror(api):
    '''test to raise the exception when type of file_id is not as defined'''
    with pytest.raises(TypeError):
        api.editor.audits('scan', 1, 'nope')


@pytest.mark.vcr()
def test_editor_template_details_etype_typeerror(api):
    '''test to raise the exception when type of etype is not as defined'''
    with pytest.raises(TypeError):
        api.editor.template_details(1, 'uuid')


@pytest.mark.vcr()
def test_editor_template_details_etype_unexpectedvalue(api):
    '''test to raise the exception when value of etype is not as defined'''
    with pytest.raises(UnexpectedValueError):
        api.editor.template_details('nope', 'uuid')


@pytest.mark.vcr()
def test_editor_template_details_id_typeerror(api):
    '''test to raise the exception when type of id is not as defined'''
    with pytest.raises(TypeError):
        api.editor.template_details('scan', 1)


@pytest.mark.vcr()
def test_editor_details_etype_typeerror(api):
    '''test to raise the exception when type of etype is not as defined'''
    with pytest.raises(TypeError):
        api.editor.details(1, 'uuid')


@pytest.mark.vcr()
def test_editor_details_etype_unexpectedvalue(api):
    '''test to raise the exception when value of etype is not as defined'''
    with pytest.raises(UnexpectedValueError):
        api.editor.details('nope', 'uuid')


# @pytest.mark.vcr()
# def test_editor_details_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.editor.details('scan', 'nope')

@pytest.mark.vcr()
def test_editor_template_list_etype_typeerror(api):
    '''test to raise the exception when type of etype is not as defined'''
    with pytest.raises(TypeError):
        api.editor.template_list(1)


@pytest.mark.vcr()
def test_editor_template_list_etype_unexpectedvalue(api):
    '''test to raise the exception when value of etype is not as defined'''
    with pytest.raises(UnexpectedValueError):
        api.editor.template_list('nope')


@pytest.mark.vcr()
def test_editor_template_list(api):
    '''test to get template list'''
    items = api.editor.template_list('scan')
    assert isinstance(items, list)


@pytest.mark.vcr()
def test_editor_plugin_desc_policy_id_typeerror(api):
    '''test to raise the exception when type of policy_id is not as defined'''
    with pytest.raises(TypeError):
        api.editor.plugin_description('nope', 1, 1)


@pytest.mark.vcr()
def test_editor_plugin_desc_family_id_typeerror(api):
    '''test to raise the exception when type of family_id is not as defined'''
    with pytest.raises(TypeError):
        api.editor.plugin_description(1, 'nope', 1)


@pytest.mark.vcr()
def test_editor_plugin_desc_plugin_id_typeerror(api):
    '''test to raise the exception when type of plugin_id is not as defined'''
    with pytest.raises(TypeError):
        api.editor.plugin_description(1, 1, 'nope')


@pytest.mark.vcr()
def test_editor_parse_creds(api):
    '''test to parse creds'''
    data = [{'types':
                 [{'instances':
                       [{'id': 12, 'type': 'entry', 'modes': 'nothing', 'summary': "sample1"},
                        {'id': 34, 'default': 145, 'summary': 'sample2'}], 'name': 'Josh'}],
             'name': 'Joseph'}, {'types': [{'instances': [
        {'id': 12, 'type': 'entry', 'modes': 'nothing', 'summary': 'sample3'},
        {'id': 34, 'summary': 'sample4', 'default': 145}], 'name': 'Dale'}], 'name': 'David'}]

    api.editor.parse_creds(data)


@pytest.mark.vcr()
def test_editor_parse_audits(api):
    '''test to parse audits'''
    data = [{'audits':
                 [{'free': 0, 'type': 'custom', 'summary': 'File: file1', 'id': 1}],
             'name': 'Josh'},
            {'audits':
                 [{'free': 0, 'type': 'Nothing', 'summary': 'File: file2', 'id': 2}],
             'name': 'Leo'}]
    api.editor.parse_audits(data)


@pytest.mark.vcr()
def test_editor_details(api):
    '''
    test the details of the editor for the given scan_id
    '''
    flag = True
    scan_ids_list = []
    while flag:
        scan_id = api.scans.create(
            name='pytest: {}'.format(uuid.uuid4()),
            template='advanced',
            targets=['127.0.0.1'])['id']
        scan_ids_list.append(scan_id)
        editor_details = api.editor.obj_details('scan', scan_id)
        if 'compliance' in editor_details and 'plugins' in editor_details:
            api.editor.details('scan', scan_id)
            flag = False
    for each_scan_id in scan_ids_list:
        api.scans.delete(each_scan_id)

