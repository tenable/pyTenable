"""
Test Module for Audit Files
"""
import os

import pytest
from tests.sc.conftest import sc as security_centre
from tenable.errors import APIError, UnexpectedValueError
from ..checker import check


def test_audit_files_constructor_name_typeerror(security_centre, vcr):
    """
    Testing Audit File's constructor
    :param sc:
    :param vcr:
    :return: No return
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(name=1)
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('audit-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_centre.audit_files.create(name=1, audit_file=file)
        os.remove('audit-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('tailoring-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_centre.audit_files.create(name=1, tailoring_file=file)
        os.remove('tailoring-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('audit-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_centre.audit_files.edit(1, name=1, audit_file=file)
        os.remove('audit-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('tailoring-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                security_centre.audit_files.edit(1, name=1, tailoring_file=file)
        os.remove('tailoring-file.xml')


def test_audit_files_constructor_description_typeerror(security_centre):
    """
    Testing Audit File Constructor's Description Testing
    :param security_centre:
    :return: No return
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(description=1)


def test_audit_files_constructor_type_typeerror(security_centre):
    """
    Testing Audit File Constructor's Type
    :param security_centre
    :return: No return
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(type=1)


def test_audit_files_constructor_type_unexpectedvalueerror(security_centre):
    """
    Testing Audit File Constructor's Type
    :param security_centre
    :return: No return
    """
    with pytest.raises(UnexpectedValueError):
        security_centre.audit_files._constructor(type='something else')


def test_audit_files_constructor_template_typeerror(security_centre):
    """
    Testing Audit File Constructor's Type
    :param sc
    :return: No return
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(template='one')


def test_audit_files_constructor_vars_typeerror(security_centre):
    """
    Testing Audit File Constructor's Type
    :param sc
    :return: No return
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(vars='one')


def test_audit_files_constructor_vars_key_typeerror(security_centre):
    """
    test vars keys for the constructor
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(vars={1: 'one'})


def test_audit_files_constructor_vars_value_typeerror(security_centre):
    """
    test vars keys for the constructor
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(vars={'one': 1})


def test_audit_files_constructor_filename_typeerror(security_centre):
    """
    test vars file name type error for constructor
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(filename=1)


def test_audit_files_constructor_orig_filename_typeerror(security_centre):
    """
    test vars origin orig_filename name for constructor
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(orig_filename=1)


def test_audit_files_constructor_version_typeerror(security_centre):
    """
    test vars version for constructor
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(version=1)


def test_audit_files_constructor_version_unexpectedvalueerror(security_centre):
    """
    test vars origin file name and unexpected value error  for constructor
    """
    with pytest.raises(UnexpectedValueError):
        security_centre.audit_files._constructor(version='0.9')


def test_audit_files_constructor_benchmark_typeerror(security_centre):
    """
    test audit files benchmark type error
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(benchmark=1)


def test_audit_files_constructor_profile_typeerror(security_centre):
    """
    test audit files constructor profile
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(profile=1)


def test_audit_files_constructor_data_stream_typeerror(security_centre):
    """
    test audit files constructor data stream
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(data_stream=1)


def test_audit_files_constructor_tailoring_filename_typeerror(security_centre):
    """
    test audit files constructor tailoring
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(tailoring_filename=1)


def test_audit_files_constructor_tailoring_orig_filename_typeerror(security_centre):
    """
    test audit files constructor tailoring origin filename type error
    """
    with pytest.raises(TypeError):
        security_centre.audit_files._constructor(tailoring_orig_filename=1)


def test_audit_files_constructor_success(security_centre):
    """
    test audit files constructor creation
    """
    audit_file = security_centre.audit_files._constructor(
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
def audit_file(request, security_centre, vcr):
    """
    test audit files fixture
    """
    with vcr.use_cassette('test_audit_files_create_success'):
        audit_file = security_centre.audit_files.create('Example',
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
                security_centre.audit_files.delete(int(audit_file['id']))
        except APIError:
            pass

    request.addfinalizer(teardown)
    return audit_file


def test_audit_files_create_success(security_centre, audit_file):
    """
    test audit files create success
    """
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
def test_audit_files_delete_success(security_centre, audit_file):
    """
    test audit files delete function
    """
    security_centre.audit_files.delete(int(audit_file['id']))


@pytest.mark.vcr()
def test_audit_files_edit_success(security_centre, audit_file):
    """
    test audit files edit success
    """
    audit_file = security_centre.audit_files.edit(int(audit_file['id']), name='updates name')
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
def test_audit_files_details_success_for_fields(security_centre, audit_file):
    """
    test audit files details success for fields
    """
    audit_file = security_centre.audit_files.details(int(audit_file['id']), fields=['id', 'name', 'description'])
    assert isinstance(audit_file, dict)
    check(audit_file, 'id', str)
    check(audit_file, 'name', str)
    check(audit_file, 'description', str)


@pytest.mark.vcr()
def test_audit_files_details_success(security_centre, audit_file):
    """
    test audit files details success
    """
    audit_file = security_centre.audit_files.details(int(audit_file['id']))
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
def test_audit_files_list_success(security_centre):
    """
    test audit files list success
    """
    audit_files = security_centre.audit_files.list()
    assert isinstance(audit_files, dict)
    for file_type in ['usable', 'manageable']:
        for audit_file in audit_files[file_type]:
            check(audit_file, 'name', str)
            check(audit_file, 'description', str)
            check(audit_file, 'type', str)
            check(audit_file, 'status', str)
            check(audit_file, 'id', str)


@pytest.mark.vcr()
def test_audit_files_list_success_for_fields(security_centre):
    """
    test audit files list success for fields
    """
    audit_files = security_centre.audit_files.list(fields=('id', 'name', 'description'))
    assert isinstance(audit_files, dict)
    for item in ['usable', 'manageable']:
        for audit_file in audit_files[item]:
            check(audit_file, 'name', str)
            check(audit_file, 'description', str)
            check(audit_file, 'id', str)


@pytest.mark.vcr()
def test_audit_files_export_audit(security_centre):
    """
    test audit files export audit
    """
    with open('1000007.xml', 'wb') as file:
        security_centre.audit_files.export_audit(1000007, fobj=file)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_template_list_success(security_centre):
    """
    test audit files template list success
    """
    templates = security_centre.audit_files.template_list(fields=['id', 'name', 'categoryName', 'categoryId'],
                                             category=1,
                                             search='categoryName:Unix')
    assert isinstance(templates, list)
    for template in templates:
        check(template, 'id', str)
        check(template, 'name', str)
        check(template, 'categoryName', str)
        check(template, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_categories(security_centre):
    """
    test audit files template categories
    """
    categories = security_centre.audit_files.template_categories()
    assert isinstance(categories, list)
    for category in categories:
        check(category, 'categoryName', str)
        check(category, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_details_success(security_centre):
    """
    test audit files template details success
    """
    template = security_centre.audit_files.template_details(1,
                                               fields=['id', 'name', 'categoryName', 'categoryId'])
    assert isinstance(template, dict)
    check(template, 'id', str)
    check(template, 'name', str)
