"""
test file for testing various scenarios in audit files
"""

import os

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError
from ..checker import check


@responses.activate
def test_audit_files_constructor_name_typeerror(tsc):
    """
    test audit files constructor for name type error
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={'error_code': 0, 'response': {'filename': 'scfile_VKzbkj'}},
    )
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(name=1)
    with open('audit-file.xml', 'w+') as file:
        with pytest.raises(TypeError):
            tsc.audit_files.create(name=1, audit_file=file)
    os.remove('audit-file.xml')
    with open('tailoring-file.xml', 'w+') as file:
        with pytest.raises(TypeError):
            tsc.audit_files.create(name=1, tailoring_file=file)
    os.remove('tailoring-file.xml')
    with open('audit-file.xml', 'w+') as file:
        with pytest.raises(TypeError):
            tsc.audit_files.edit(1, name=1, audit_file=file)
    os.remove('audit-file.xml')
    with open('tailoring-file.xml', 'w+') as file:
        with pytest.raises(TypeError):
            tsc.audit_files.edit(1, name=1, tailoring_file=file)
    os.remove('tailoring-file.xml')


def test_audit_files_constructor_description_typeerror(tsc):
    """
    test audit files constructor for description type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(description=1)


def test_audit_files_constructor_type_typeerror(tsc):
    """
    test audit files constructor for 'type' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(type=1)


def test_audit_files_constructor_type_unexpectedvalueerror(tsc):
    """
    test audit files constructor for 'type' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.audit_files._constructor(type='something else')


def test_audit_files_constructor_template_typeerror(tsc):
    """
    test audit files constructor for template type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(template='one')


def test_audit_files_constructor_vars_typeerror(tsc):
    """
    test audit files constructor for vars type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(vars='one')


def test_audit_files_constructor_vars_key_typeerror(tsc):
    """
    test audit files constructor for 'vars key' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(vars={1: 'one'})


def test_audit_files_constructor_vars_value_typeerror(tsc):
    """
    test audit files constructor for 'vars value' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(vars={'one': 1})


def test_audit_files_constructor_filename_typeerror(tsc):
    """
    test audit files constructor for filename type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(filename=1)


def test_audit_files_constructor_orig_filename_typeerror(tsc):
    """
    test audit files constructor for 'orig filename' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(orig_filename=1)


def test_audit_files_constructor_version_typeerror(tsc):
    """
    test audit files constructor for version type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(version=1)


def test_audit_files_constructor_version_unexpectedvalueerror(tsc):
    """
    test audit files constructor for version unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.audit_files._constructor(version='0.9')


def test_audit_files_constructor_benchmark_typeerror(tsc):
    """
    test audit files constructor for benchmark type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(benchmark=1)


def test_audit_files_constructor_profile_typeerror(tsc):
    """
    test audit files constructor for profile type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(profile=1)


def test_audit_files_constructor_data_stream_typeerror(tsc):
    """
    test audit files constructor for 'data stream' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(data_stream=1)


def test_audit_files_constructor_tailoring_filename_typeerror(tsc):
    """
    test audit files constructor for 'tailoring filename' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(tailoring_filename=1)


def test_audit_files_constructor_tailoring_orig_filename_typeerror(tsc):
    """
    test audit files constructor for 'tailoring orig filename' type error
    """
    with pytest.raises(TypeError):
        tsc.audit_files._constructor(tailoring_orig_filename=1)


def test_audit_files_constructor_success(tsc):
    """
    test audit files constructor for success
    """
    audit_file = tsc.audit_files._constructor(
        name='name',
        description='description',
        type='',
        template=1,
        vars={
            'example': 'one',
        },
        filename='test.audit',
        orig_filename='orig.audit',
        version='1.0',
        benchmark='benchmark',
        profile='profile',
        data_stream='datastream',
        tailoring_filename='tf.audit',
        tailoring_orig_filename='orig-tf.audit',
    )
    assert audit_file == {
        'name': 'name',
        'description': 'description',
        'filename': 'test.audit',
        'originalFilename': 'orig.audit',
        'version': '1.0',
        'benchmarkName': 'benchmark',
        'profileName': 'profile',
        'dataStreamName': 'datastream',
        'tailoringFilename': 'tf.audit',
        'tailoringOriginalFilename': 'orig-tf.audit',
        'variables': [{'name': 'example', 'value': 'one'}],
        'auditFileTemplate': {'id': 1},
        'type': '',
    }


@pytest.fixture
def audit_file():
    """
    test fixture for audit file
    """
    return {
        'id': '1000003',
        'name': 'Example',
        'description': '',
        'version': '1.43',
        'type': 'unix',
        'context': '',
        'status': '0',
        'filename': 'scfile_VKzbkj',
        'originalFilename': '',
        'createdTime': '1555432455',
        'modifiedTime': '1555432455',
        'lastRefreshedTime': '1555432455',
        'editor': '[{"id": "BANNER_TEXT", "name": "Banner Text", "type": "entry"}]',
        'canUse': 'true',
        'canManage': 'true',
    }


@responses.activate
def test_audit_files_create_success(tsc):
    """
    test audit files create for success
    """
    responses.post(
        'https://nourl/rest/auditFile',
        json={
            'type': 'regular',
            'response': {
                'id': '1000003',
                'name': 'Example',
                'description': '',
                'version': '1.43',
                'type': 'unix',
                'context': '',
                'status': '0',
                'filename': 'scfile_VKzbkj',
                'originalFilename': '',
                'createdTime': '1555432455',
                'modifiedTime': '1555432455',
                'lastRefreshedTime': '1555432455',
                'editor': '[{"id": "BANNER_TEXT", "name": "Banner Text", "type": "entry"}]',
                'typeFields': {'variables': [{'name': 'BANNER_TEXT', 'value': ''}]},
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'auditFileTemplate': {
                    'id': '162',
                    'name': 'PCI DSS 2.0/3.0 - Red Hat Linux',
                    'categoryName': 'Unix',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1555432455,
        },
    )
    audit_file = tsc.audit_files.create(
        'Example',
        template=162,
        vars={
            'BANNER_TEXT': '',
            'NTP_SERVER_1': '4.2.2.2',
            'NTP_SERVER_2': '192.168.0.1',
            'NTP_SERVER_3': '192.168.0.1',
            'INTERNAL_NETWORK': '192.168.',
            'HOSTS_ALLOW_NETWORK': '192.168.',
            'LOG_SERVER': '192.168.0.1',
        },
    )
    assert isinstance(audit_file, dict)
    check(audit_file, 'auditFileTemplate', dict)
    check(audit_file['auditFileTemplate'], 'id', str)
    check(audit_file['auditFileTemplate'], 'name', str)
    check(audit_file['auditFileTemplate'], 'categoryName', str)
    check(audit_file, 'canManage', str)
    check(audit_file, 'canUse', str)
    check(audit_file, 'context', str)
    check(audit_file, 'createdTime', str)
    check(audit_file, 'creator', dict)
    check(audit_file['creator'], 'id', str)
    check(audit_file['creator'], 'username', str)
    check(audit_file['creator'], 'firstname', str)
    check(audit_file['creator'], 'lastname', str)
    check(audit_file, 'description', str)
    check(audit_file, 'editor', str)
    check(audit_file, 'filename', str)
    check(audit_file, 'groups', list)
    check(audit_file, 'id', str)
    check(audit_file, 'lastRefreshedTime', str)
    check(audit_file, 'modifiedTime', str)
    check(audit_file, 'name', str)
    check(audit_file, 'originalFilename', str)
    check(audit_file, 'owner', dict)
    check(audit_file['owner'], 'id', str)
    check(audit_file['owner'], 'username', str)
    check(audit_file['owner'], 'firstname', str)
    check(audit_file['owner'], 'lastname', str)
    check(audit_file, 'ownerGroup', dict)
    check(audit_file['ownerGroup'], 'id', str)
    check(audit_file['ownerGroup'], 'name', str)
    check(audit_file['ownerGroup'], 'description', str)
    check(audit_file, 'status', str)
    check(audit_file, 'targetGroup', dict)
    check(audit_file['targetGroup'], 'id', int)
    check(audit_file['targetGroup'], 'name', str)
    check(audit_file['targetGroup'], 'description', str)
    check(audit_file, 'type', str)
    check(audit_file, 'typeFields', dict)
    check(audit_file['typeFields'], 'variables', list)
    for variable in audit_file['typeFields']['variables']:
        check(variable, 'name', str)
        check(variable, 'value', str)
    check(audit_file, 'version', str)


@responses.activate
def test_audit_files_delete_success(tsc, audit_file):
    """
    test audit files delete for success
    """
    responses.delete(
        'https://nourl/rest/auditFile/1000003',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1555432456,
        },
    )
    tsc.audit_files.delete(int(audit_file['id']))


@responses.activate
def test_audit_files_edit_success(tsc, audit_file):
    """
    test audit files edit for success
    """
    responses.patch(
        'https://nourl/rest/auditFile/1000003',
        json={
            'type': 'regular',
            'response': {
                'id': '1000008',
                'name': 'updates name',
                'description': '',
                'version': '1.43',
                'type': 'unix',
                'context': '',
                'status': '0',
                'filename': 'scfile_ZiY8iP',
                'originalFilename': '',
                'createdTime': '1555946569',
                'modifiedTime': '1555946570',
                'lastRefreshedTime': '1555946569',
                'editor': '[{"id": "BANNER_TEXT", "name": "Banner Text", "type": "entry"}]',
                'typeFields': {'variables': [{'name': 'BANNER_TEXT', 'value': ''}]},
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'auditFileTemplate': {
                    'id': '162',
                    'name': 'PCI DSS 2.0/3.0 - Red Hat Linux',
                    'categoryName': 'Unix',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1555946569,
        },
    )
    audit_file = tsc.audit_files.edit(int(audit_file['id']), name='updates name')
    assert isinstance(audit_file, dict)
    check(audit_file, 'auditFileTemplate', dict)
    check(audit_file['auditFileTemplate'], 'id', str)
    check(audit_file['auditFileTemplate'], 'name', str)
    check(audit_file['auditFileTemplate'], 'categoryName', str)
    check(audit_file, 'canManage', str)
    check(audit_file, 'canUse', str)
    check(audit_file, 'context', str)
    check(audit_file, 'createdTime', str)
    check(audit_file, 'creator', dict)
    check(audit_file['creator'], 'id', str)
    check(audit_file['creator'], 'username', str)
    check(audit_file['creator'], 'firstname', str)
    check(audit_file['creator'], 'lastname', str)
    check(audit_file, 'description', str)
    check(audit_file, 'editor', str)
    check(audit_file, 'filename', str)
    check(audit_file, 'groups', list)
    check(audit_file, 'id', str)
    check(audit_file, 'lastRefreshedTime', str)
    check(audit_file, 'modifiedTime', str)
    check(audit_file, 'name', str)
    check(audit_file, 'originalFilename', str)
    check(audit_file, 'owner', dict)
    check(audit_file['owner'], 'id', str)
    check(audit_file['owner'], 'username', str)
    check(audit_file['owner'], 'firstname', str)
    check(audit_file['owner'], 'lastname', str)
    check(audit_file, 'ownerGroup', dict)
    check(audit_file['ownerGroup'], 'id', str)
    check(audit_file['ownerGroup'], 'name', str)
    check(audit_file['ownerGroup'], 'description', str)
    check(audit_file, 'status', str)
    check(audit_file, 'targetGroup', dict)
    check(audit_file['targetGroup'], 'id', int)
    check(audit_file['targetGroup'], 'name', str)
    check(audit_file['targetGroup'], 'description', str)
    check(audit_file, 'type', str)
    check(audit_file, 'typeFields', dict)
    check(audit_file['typeFields'], 'variables', list)
    for variable in audit_file['typeFields']['variables']:
        check(variable, 'name', str)
        check(variable, 'value', str)
    check(audit_file, 'version', str)


@responses.activate
def test_audit_files_details_success_for_fields(tsc, audit_file):
    """
    test audit files details success for fields
    """
    responses.get(
        'https://nourl/rest/auditFile/1000003',
        json={
            'type': 'regular',
            'response': {'id': '1000007', 'name': 'Example', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1555946553,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    audit_file = tsc.audit_files.details(
        int(audit_file['id']), fields=['id', 'name', 'description']
    )
    assert isinstance(audit_file, dict)
    check(audit_file, 'id', str)
    check(audit_file, 'name', str)
    check(audit_file, 'description', str)


@responses.activate
def test_audit_files_details_success(tsc, audit_file):
    """
    test audit files details for success
    """
    responses.get(
        'https://nourl/rest/auditFile/1000003',
        json={
            'type': 'regular',
            'response': {
                'id': '1000007',
                'name': 'Example',
                'description': '',
                'version': '1.43',
                'type': 'unix',
                'context': '',
                'status': '0',
                'filename': 'scfile_COlP4j',
                'originalFilename': '',
                'createdTime': '1555946553',
                'modifiedTime': '1555946553',
                'lastRefreshedTime': '1555946553',
                'editor': '[{"id": "BANNER_TEXT", "name": "Banner Text", "type": "entry"}]',
                'typeFields': {'variables': [{'name': 'BANNER_TEXT', 'value': ''}]},
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'auditFileTemplate': {
                    'id': '162',
                    'name': 'PCI DSS 2.0/3.0 - Red Hat Linux',
                    'categoryName': 'Unix',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1555946553,
        },
    )
    audit_file = tsc.audit_files.details(int(audit_file['id']))
    assert isinstance(audit_file, dict)
    check(audit_file, 'auditFileTemplate', dict)
    check(audit_file['auditFileTemplate'], 'id', str)
    check(audit_file['auditFileTemplate'], 'name', str)
    check(audit_file['auditFileTemplate'], 'categoryName', str)
    check(audit_file, 'canManage', str)
    check(audit_file, 'canUse', str)
    check(audit_file, 'context', str)
    check(audit_file, 'createdTime', str)
    check(audit_file, 'creator', dict)
    check(audit_file['creator'], 'id', str)
    check(audit_file['creator'], 'username', str)
    check(audit_file['creator'], 'firstname', str)
    check(audit_file['creator'], 'lastname', str)
    check(audit_file, 'description', str)
    check(audit_file, 'editor', str)
    check(audit_file, 'filename', str)
    check(audit_file, 'groups', list)
    check(audit_file, 'id', str)
    check(audit_file, 'lastRefreshedTime', str)
    check(audit_file, 'modifiedTime', str)
    check(audit_file, 'name', str)
    check(audit_file, 'originalFilename', str)
    check(audit_file, 'owner', dict)
    check(audit_file['owner'], 'id', str)
    check(audit_file['owner'], 'username', str)
    check(audit_file['owner'], 'firstname', str)
    check(audit_file['owner'], 'lastname', str)
    check(audit_file, 'ownerGroup', dict)
    check(audit_file['ownerGroup'], 'id', str)
    check(audit_file['ownerGroup'], 'name', str)
    check(audit_file['ownerGroup'], 'description', str)
    check(audit_file, 'status', str)
    check(audit_file, 'targetGroup', dict)
    check(audit_file['targetGroup'], 'id', int)
    check(audit_file['targetGroup'], 'name', str)
    check(audit_file['targetGroup'], 'description', str)
    check(audit_file, 'type', str)
    check(audit_file, 'typeFields', dict)
    check(audit_file['typeFields'], 'variables', list)
    for variable in audit_file['typeFields']['variables']:
        check(variable, 'name', str)
        check(variable, 'value', str)
    check(audit_file, 'version', str)


@responses.activate
def test_audit_files_list_success(tsc):
    """
    test audit files list for success
    """
    responses.get(
        'https://nourl/rest/auditFile',
        json={
            'type': 'regular',
            'response': {
                'usable': [],
                'manageable': [
                    {
                        'id': '1000001',
                        'name': 'test1',
                        'description': '',
                        'type': 'unix',
                        'status': '0',
                    }
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1555946582,
        },
    )
    a_files = tsc.audit_files.list()
    assert isinstance(a_files, dict)
    for file_type in ['usable', 'manageable']:
        for type in a_files[file_type]:
            check(type, 'name', str)
            check(type, 'description', str)
            check(type, 'type', str)
            check(type, 'status', str)
            check(type, 'id', str)


@responses.activate
def test_audit_files_export_audit(tsc):
    """
    test audit files for export audit
    """
    responses.get(
        'https://nourl/rest/auditFile/1000007/export',
        body='<?xml version="1.0" encoding="UTF-8"?>\n<NessusClientData_v2><Policy><policyName>Example Policy</policyName></Policy></NessusClientData_v2>',
        content_type='text/xml',
        headers={'content-disposition': 'attachment; filename="policy.1000014.1.xml"'},
    )
    with open('1000007.xml', 'wb') as file:
        tsc.audit_files.export_audit(1000007, fobj=file)
    os.remove('1000007.xml')


@responses.activate
def test_audit_files_export_audit_no_file(tsc):
    """
    test audit files for export audit no file
    """
    responses.get(
        'https://nourl/rest/auditFile/1000007/export',
        body='No Content',
        content_type='text/xml',
        headers={'content-disposition': 'attachment; filename="policy.1000014.1.xml"'},
    )
    with open('1000007.xml', 'wb'):
        tsc.audit_files.export_audit(1000007)
    os.remove('1000007.xml')


@responses.activate
def test_audit_files_template_list_success(tsc):
    """
    test audit files template list for success
    """
    responses.get(
        'https://nourl/rest/auditFileTemplate',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'name': 'PCI DSS 2.0/3.0 - Red Hat Linux',
                    'categoryName': 'Unix',
                    'categoryId': '1',
                }
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1555946553,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'categoryID': '1',
                    'searchString': 'categoryName:Unix',
                    'fields': 'id,name,categoryName,categoryId',
                }
            )
        ],
    )
    templates = tsc.audit_files.template_list(
        fields=['id', 'name', 'categoryName', 'categoryId'],
        category=1,
        search='categoryName:Unix',
    )
    assert isinstance(templates, list)
    for template in templates:
        check(template, 'id', str)
        check(template, 'name', str)
        check(template, 'categoryName', str)
        check(template, 'categoryId', str)


@responses.activate
def test_audit_files_template_categories(tsc):
    """
    test audit files template categories for success
    """
    responses.get(
        'https://nourl/rest/auditFileTemplate/categories',
        json={
            'type': 'regular',
            'response': [
                {'categoryName': 'Unix', 'categoryId': '1'},
                {'categoryName': 'Windows', 'categoryId': '2'},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1555946553,
        },
    )
    categories = tsc.audit_files.template_categories()
    assert isinstance(categories, list)
    for category in categories:
        check(category, 'categoryName', str)
        check(category, 'categoryId', str)


@responses.activate
def test_audit_files_list_success_for_fields(tsc):
    """
    test audit files list success for fields
    """
    responses.get(
        'https://nourl/rest/auditFile',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {'id': '1000001', 'name': 'test1', 'description': ''},
                    {'id': '1000002', 'name': 'test', 'description': ''},
                ],
                'manageable': [
                    {'id': '1000001', 'name': 'test1', 'description': ''},
                    {'id': '1000002', 'name': 'test', 'description': ''},
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1555946582,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    audit_files = tsc.audit_files.list(fields=('id', 'name', 'description'))
    assert isinstance(audit_files, dict)
    for types in ['usable', 'manageable']:
        for type in audit_files[types]:
            check(type, 'name', str)
            check(type, 'description', str)
            check(type, 'id', str)


@responses.activate
def test_audit_files_template_details_success(tsc):
    """
    test audit files template details for success
    """
    responses.get(
        'https://nourl/rest/auditFileTemplate/1',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'PCI DSS 2.0/3.0 - Red Hat Linux',
                'categoryName': 'Unix',
                'categoryId': '1',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1555946553,
        },
        match=[
            matchers.query_param_matcher({'fields': 'id,name,categoryName,categoryId'})
        ],
    )
    template = tsc.audit_files.template_details(
        1, fields=['id', 'name', 'categoryName', 'categoryId']
    )
    assert isinstance(template, dict)
    check(template, 'id', str)
    check(template, 'name', str)
    check(template, 'categoryName', str)
    check(template, 'categoryId', str)
