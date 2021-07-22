'''
test file for testing various scenarios in audit files
'''
import os

import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check


def test_audit_files_constructor_name_typeerror(security_center, vcr):
    '''
    test audit files constructor for name type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(name=1)
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('audit-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_center.audit_files.create(name=1, audit_file=file)
        os.remove('audit-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('tailoring-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_center.audit_files.create(name=1, tailoring_file=file)
        os.remove('tailoring-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('audit-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_center.audit_files.edit(1, name=1, audit_file=file)
        os.remove('audit-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('tailoring-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_center.audit_files.edit(1, name=1, tailoring_file=file)
        os.remove('tailoring-file.xml')


def test_audit_files_constructor_description_typeerror(security_center):
    '''
    test audit files constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(description=1)


def test_audit_files_constructor_type_typeerror(security_center):
    '''
    test audit files constructor for 'type' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(type=1)


def test_audit_files_constructor_type_unexpectedvalueerror(security_center):
    '''
    test audit files constructor for 'type' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.audit_files._constructor(type='something else')


def test_audit_files_constructor_template_typeerror(security_center):
    '''
    test audit files constructor for template type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(template='one')


def test_audit_files_constructor_vars_typeerror(security_center):
    '''
    test audit files constructor for vars type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(vars='one')


def test_audit_files_constructor_vars_key_typeerror(security_center):
    '''
    test audit files constructor for 'vars key' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(vars={1: 'one'})


def test_audit_files_constructor_vars_value_typeerror(security_center):
    '''
    test audit files constructor for 'vars value' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(vars={'one': 1})


def test_audit_files_constructor_filename_typeerror(security_center):
    '''
    test audit files constructor for filename type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(filename=1)


def test_audit_files_constructor_orig_filename_typeerror(security_center):
    '''
    test audit files constructor for 'orig filename' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(orig_filename=1)


def test_audit_files_constructor_version_typeerror(security_center):
    '''
    test audit files constructor for version type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(version=1)


def test_audit_files_constructor_version_unexpectedvalueerror(security_center):
    '''
    test audit files constructor for version unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.audit_files._constructor(version='0.9')


def test_audit_files_constructor_benchmark_typeerror(security_center):
    '''
    test audit files constructor for benchmark type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(benchmark=1)


def test_audit_files_constructor_profile_typeerror(security_center):
    '''
    test audit files constructor for profile type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(profile=1)


def test_audit_files_constructor_data_stream_typeerror(security_center):
    '''
    test audit files constructor for 'data stream' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(data_stream=1)


def test_audit_files_constructor_tailoring_filename_typeerror(security_center):
    '''
    test audit files constructor for 'tailoring filename' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(tailoring_filename=1)


def test_audit_files_constructor_tailoring_orig_filename_typeerror(security_center):
    '''
    test audit files constructor for 'tailoring orig filename' type error
    '''
    with pytest.raises(TypeError):
        security_center.audit_files._constructor(tailoring_orig_filename=1)


def test_audit_files_constructor_success(security_center):
    '''
    test audit files constructor for success
    '''
    audit_file = security_center.audit_files._constructor(
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
        tailoring_orig_filename='orig-tf.audit'
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
def audit_file(request, security_center, vcr):
    '''
    test fixture for audit file
    '''
    with vcr.use_cassette('test_audit_files_create_success'):
        audit_file = security_center.audit_files.create('Example',
                                                        template=162,
                                                        vars={
                                      'BANNER_TEXT': '',
                                      'NTP_SERVER_1': '4.2.2.2',
                                      'NTP_SERVER_2': '192.168.0.1',
                                      'NTP_SERVER_3': '192.168.0.1',
                                      'INTERNAL_NETWORK': '192.168.',
                                      'HOSTS_ALLOW_NETWORK': '192.168.',
                                      'LOG_SERVER': '192.168.0.1',
                                  })

    def teardown():
        try:
            with vcr.use_cassette('test_audit_files_delete_success'):
                security_center.audit_files.delete(int(audit_file['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return audit_file


def test_audit_files_create_success(security_center, audit_file):
    '''
    test audit files create for success
    '''
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


@pytest.mark.vcr()
def test_audit_files_delete_success(security_center, audit_file):
    '''
    test audit files delete for success
    '''
    security_center.audit_files.delete(int(audit_file['id']))


@pytest.mark.vcr()
def test_audit_files_edit_success(security_center, audit_file):
    '''
    test audit files edit for success
    '''
    audit_file = security_center.audit_files.edit(int(audit_file['id']), name='updates name')
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


@pytest.mark.vcr()
def test_audit_files_details_success_for_fields(security_center, audit_file):
    '''
    test audit files details success for fields
    '''
    audit_file = security_center.audit_files.details(int(audit_file['id']), fields=['id', 'name', 'description'])
    assert isinstance(audit_file, dict)
    check(audit_file, 'id', str)
    check(audit_file, 'name', str)
    check(audit_file, 'description', str)


@pytest.mark.vcr()
def test_audit_files_details_success(security_center, audit_file):
    '''
    test audit files details for success
    '''
    audit_file = security_center.audit_files.details(int(audit_file['id']))
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


@pytest.mark.vcr()
def test_audit_files_list_success(security_center):
    '''
    test audit files list for success
    '''
    a_files = security_center.audit_files.list()
    assert isinstance(a_files, dict)
    for file_type in ['usable', 'manageable']:
        for type in a_files[file_type]:
            check(type, 'name', str)
            check(type, 'description', str)
            check(type, 'type', str)
            check(type, 'status', str)
            check(type, 'id', str)


@pytest.mark.vcr()
def test_audit_files_export_audit(security_center):
    '''
    test audit files for export audit
    '''
    with open('1000007.xml', 'wb') as file:
        security_center.audit_files.export_audit(1000007, fobj=file)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_export_audit_no_file(security_center):
    '''
    test audit files for export audit no file
    '''
    with open('1000007.xml', 'wb'):
        security_center.audit_files.export_audit(1000007)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_template_list_success(security_center):
    '''
    test audit files template list for success
    '''
    templates = security_center.audit_files.template_list(fields=['id', 'name', 'categoryName', 'categoryId'],
                                                          category=1,
                                                          search='categoryName:Unix')
    assert isinstance(templates, list)
    for template in templates:
        check(template, 'id', str)
        check(template, 'name', str)
        check(template, 'categoryName', str)
        check(template, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_categories(security_center):
    '''
    test audit files template categories for success
    '''
    categories = security_center.audit_files.template_categories()
    assert isinstance(categories, list)
    for category in categories:
        check(category, 'categoryName', str)
        check(category, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_list_success_for_fields(security_center):
    '''
    test audit files list success for fields
    '''
    audit_files = security_center.audit_files.list(fields=('id', 'name', 'description'))
    assert isinstance(audit_files, dict)
    for types in ['usable', 'manageable']:
        for type in audit_files[types]:
            check(type, 'name', str)
            check(type, 'description', str)
            check(type, 'id', str)


@pytest.mark.vcr()
def test_audit_files_template_details_success(security_center):
    '''
    test audit files template details for success
    '''
    template = security_center.audit_files.template_details(1,
                                                            fields=['id', 'name', 'categoryName', 'categoryId'])
    assert isinstance(template, dict)
    check(template, 'id', str)
    check(template, 'name', str)
    check(template, 'categoryName', str)
    check(template, 'categoryId', str)