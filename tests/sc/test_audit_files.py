import os

import pytest

from tenable.errors import *
from ..checker import check


def test_audit_files_constructor_name_typeerror(sc, vcr):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(name=1)
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('audit-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                sc.audit_files.create(name=1, audit_file=file)
        os.remove('audit-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('tailoring-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                sc.audit_files.create(name=1, tailoring_file=file)
        os.remove('tailoring-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('audit-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                sc.audit_files.edit(1, name=1, audit_file=file)
        os.remove('audit-file.xml')
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open('tailoring-file.xml', 'w+') as file:
            with pytest.raises(TypeError):
                sc.audit_files.edit(1, name=1, tailoring_file=file)
        os.remove('tailoring-file.xml')


def test_audit_files_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(description=1)


def test_audit_files_constructor_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(type=1)


def test_audit_files_constructor_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.audit_files._constructor(type='something else')


def test_audit_files_constructor_template_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(template='one')


def test_audit_files_constructor_vars_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(vars='one')


def test_audit_files_constructor_vars_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(vars={1: 'one'})


def test_audit_files_constructor_vars_value_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(vars={'one': 1})


def test_audit_files_constructor_filename_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(filename=1)


def test_audit_files_constructor_orig_filename_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(orig_filename=1)


def test_audit_files_constructor_version_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(version=1)


def test_audit_files_constructor_version_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.audit_files._constructor(version='0.9')


def test_audit_files_constructor_benchmark_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(benchmark=1)


def test_audit_files_constructor_profile_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(profile=1)


def test_audit_files_constructor_data_stream_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(data_stream=1)


def test_audit_files_constructor_tailoring_filename_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(tailoring_filename=1)


def test_audit_files_constructor_tailoring_orig_filename_typeerror(sc):
    with pytest.raises(TypeError):
        sc.audit_files._constructor(tailoring_orig_filename=1)


def test_audit_files_constructor_success(sc):
    af = sc.audit_files._constructor(
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
    assert af == {
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
def auditfile(request, sc, vcr):
    with vcr.use_cassette('test_audit_files_create_success'):
        a = sc.audit_files.create('Example',
                                  template=162,
                                  vars={
                                      'BANNER_TEXT': '',
                                      'NTP_SERVER_1': '4\.2\.2\.2',
                                      'NTP_SERVER_2': '192\.168\.0\.1',
                                      'NTP_SERVER_3': '192\.168\.0\.1',
                                      'INTERNAL_NETWORK': '192\.168\.',
                                      'HOSTS_ALLOW_NETWORK': '192\.168\.',
                                      'LOG_SERVER': '192\.168\.0\.1',
                                  })

    def teardown():
        try:
            with vcr.use_cassette('test_audit_files_delete_success'):
                sc.audit_files.delete(int(a['id']))
        except APIError:
            pass

    request.addfinalizer(teardown)
    return a


def test_audit_files_create_success(sc, auditfile):
    assert isinstance(auditfile, dict)
    check(auditfile, 'auditFileTemplate', dict)
    check(auditfile['auditFileTemplate'], 'id', str)
    check(auditfile['auditFileTemplate'], 'name', str)
    check(auditfile['auditFileTemplate'], 'categoryName', str)
    check(auditfile, 'canManage', str)
    check(auditfile, 'canUse', str)
    check(auditfile, 'context', str)
    check(auditfile, 'createdTime', str)
    check(auditfile, 'creator', dict)
    check(auditfile['creator'], 'id', str)
    check(auditfile['creator'], 'username', str)
    check(auditfile['creator'], 'firstname', str)
    check(auditfile['creator'], 'lastname', str)
    check(auditfile, 'description', str)
    check(auditfile, 'editor', str)
    check(auditfile, 'filename', str)
    check(auditfile, 'groups', list)
    check(auditfile, 'id', str)
    check(auditfile, 'lastRefreshedTime', str)
    check(auditfile, 'modifiedTime', str)
    check(auditfile, 'name', str)
    check(auditfile, 'originalFilename', str)
    check(auditfile, 'owner', dict)
    check(auditfile['owner'], 'id', str)
    check(auditfile['owner'], 'username', str)
    check(auditfile['owner'], 'firstname', str)
    check(auditfile['owner'], 'lastname', str)
    check(auditfile, 'ownerGroup', dict)
    check(auditfile['ownerGroup'], 'id', str)
    check(auditfile['ownerGroup'], 'name', str)
    check(auditfile['ownerGroup'], 'description', str)
    check(auditfile, 'status', str)
    check(auditfile, 'targetGroup', dict)
    check(auditfile['targetGroup'], 'id', int)
    check(auditfile['targetGroup'], 'name', str)
    check(auditfile['targetGroup'], 'description', str)
    check(auditfile, 'type', str)
    check(auditfile, 'typeFields', dict)
    check(auditfile['typeFields'], 'variables', list)
    for i in auditfile['typeFields']['variables']:
        check(i, 'name', str)
        check(i, 'value', str)
    check(auditfile, 'version', str)


@pytest.mark.vcr()
def test_audit_files_delete_success(sc, auditfile):
    sc.audit_files.delete(int(auditfile['id']))


@pytest.mark.vcr()
def test_audit_files_edit_success(sc, auditfile):
    a = sc.audit_files.edit(int(auditfile['id']), name='updates name')
    assert isinstance(a, dict)
    check(a, 'auditFileTemplate', dict)
    check(a['auditFileTemplate'], 'id', str)
    check(a['auditFileTemplate'], 'name', str)
    check(a['auditFileTemplate'], 'categoryName', str)
    check(a, 'canManage', str)
    check(a, 'canUse', str)
    check(a, 'context', str)
    check(a, 'createdTime', str)
    check(a, 'creator', dict)
    check(a['creator'], 'id', str)
    check(a['creator'], 'username', str)
    check(a['creator'], 'firstname', str)
    check(a['creator'], 'lastname', str)
    check(a, 'description', str)
    check(a, 'editor', str)
    check(a, 'filename', str)
    check(a, 'groups', list)
    check(a, 'id', str)
    check(a, 'lastRefreshedTime', str)
    check(a, 'modifiedTime', str)
    check(a, 'name', str)
    check(a, 'originalFilename', str)
    check(a, 'owner', dict)
    check(a['owner'], 'id', str)
    check(a['owner'], 'username', str)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'lastname', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a['ownerGroup'], 'description', str)
    check(a, 'status', str)
    check(a, 'targetGroup', dict)
    check(a['targetGroup'], 'id', int)
    check(a['targetGroup'], 'name', str)
    check(a['targetGroup'], 'description', str)
    check(a, 'type', str)
    check(a, 'typeFields', dict)
    check(a['typeFields'], 'variables', list)
    for i in a['typeFields']['variables']:
        check(i, 'name', str)
        check(i, 'value', str)
    check(a, 'version', str)


@pytest.mark.vcr()
def test_audit_files_details_success_for_fields(sc, auditfile):
    audit_file = sc.audit_files.details(int(auditfile['id']), fields=['id', 'name', 'description'])
    assert isinstance(audit_file, dict)
    check(audit_file, 'id', str)
    check(audit_file, 'name', str)
    check(audit_file, 'description', str)


@pytest.mark.vcr()
def test_audit_files_details_success(sc, auditfile):
    a = sc.audit_files.details(int(auditfile['id']))
    assert isinstance(a, dict)
    check(a, 'auditFileTemplate', dict)
    check(a['auditFileTemplate'], 'id', str)
    check(a['auditFileTemplate'], 'name', str)
    check(a['auditFileTemplate'], 'categoryName', str)
    check(a, 'canManage', str)
    check(a, 'canUse', str)
    check(a, 'context', str)
    check(a, 'createdTime', str)
    check(a, 'creator', dict)
    check(a['creator'], 'id', str)
    check(a['creator'], 'username', str)
    check(a['creator'], 'firstname', str)
    check(a['creator'], 'lastname', str)
    check(a, 'description', str)
    check(a, 'editor', str)
    check(a, 'filename', str)
    check(a, 'groups', list)
    check(a, 'id', str)
    check(a, 'lastRefreshedTime', str)
    check(a, 'modifiedTime', str)
    check(a, 'name', str)
    check(a, 'originalFilename', str)
    check(a, 'owner', dict)
    check(a['owner'], 'id', str)
    check(a['owner'], 'username', str)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'lastname', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a['ownerGroup'], 'description', str)
    check(a, 'status', str)
    check(a, 'targetGroup', dict)
    check(a['targetGroup'], 'id', int)
    check(a['targetGroup'], 'name', str)
    check(a['targetGroup'], 'description', str)
    check(a, 'type', str)
    check(a, 'typeFields', dict)
    check(a['typeFields'], 'variables', list)
    for i in a['typeFields']['variables']:
        check(i, 'name', str)
        check(i, 'value', str)
    check(a, 'version', str)


@pytest.mark.vcr()
def test_audit_files_list_success(sc):
    afiles = sc.audit_files.list()
    assert isinstance(afiles, dict)
    for c in ['usable', 'manageable']:
        for a in afiles[c]:
            check(a, 'name', str)
            check(a, 'description', str)
            check(a, 'type', str)
            check(a, 'status', str)
            check(a, 'id', str)


@pytest.mark.vcr()
def test_audit_files_list_success_for_fields(sc):
    audit_files = sc.audit_files.list(fields=('id', 'name', 'description'))
    assert isinstance(audit_files, dict)
    for c in ['usable', 'manageable']:
        for a in audit_files[c]:
            check(a, 'name', str)
            check(a, 'description', str)
            check(a, 'id', str)


@pytest.mark.vcr()
def test_audit_files_export_audit(sc):
    with open('1000007.xml', 'wb') as file:
        sc.audit_files.export_audit(1000007, fobj=file)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_export_audit_no_file(sc):
    with open('1000007.xml', 'wb'):
        sc.audit_files.export_audit(1000007)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_template_details_success(sc):
    template = sc.audit_files.template_details(1,
                                               fields=['id', 'name', 'categoryName', 'categoryId'])
    assert isinstance(template, dict)
    check(template, 'id', str)
    check(template, 'name', str)
    check(template, 'categoryName', str)
    check(template, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_list_success(sc):
    templates = sc.audit_files.template_list(fields=['id', 'name', 'categoryName', 'categoryId'],
                                             category=1,
                                             search='categoryName:Unix')
    assert isinstance(templates, list)
    for template in templates:
        check(template, 'id', str)
        check(template, 'name', str)
        check(template, 'categoryName', str)
        check(template, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_categories(sc):
    categories = sc.audit_files.template_categories()
    assert isinstance(categories, list)
    for category in categories:
        check(category, 'categoryName', str)
        check(category, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_list_success_for_fields(sc):
    audit_files = sc.audit_files.list(fields=('id', 'name', 'description'))
    assert isinstance(audit_files, dict)
    for c in ['usable', 'manageable']:
        for a in audit_files[c]:
            check(a, 'name', str)
            check(a, 'description', str)
            check(a, 'id', str)


@pytest.mark.vcr()
def test_audit_files_export_audit(sc):
    with open('1000007.xml', 'wb') as file:
        sc.audit_files.export_audit(1000007, fobj=file)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_export_audit_no_file(sc):
    with open('1000007.xml', 'wb'):
        sc.audit_files.export_audit(1000007)
    os.remove('1000007.xml')


@pytest.mark.vcr()
def test_audit_files_template_details_success(sc):
    template = sc.audit_files.template_details(1,
                                               fields=['id', 'name', 'categoryName', 'categoryId'])
    assert isinstance(template, dict)
    check(template, 'id', str)
    check(template, 'name', str)
    check(template, 'categoryName', str)
    check(template, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_list_success(sc):
    templates = sc.audit_files.template_list(fields=['id', 'name', 'categoryName', 'categoryId'],
                                             category=1,
                                             search='categoryName:Unix')
    assert isinstance(templates, list)
    for template in templates:
        check(template, 'id', str)
        check(template, 'name', str)
        check(template, 'categoryName', str)
        check(template, 'categoryId', str)


@pytest.mark.vcr()
def test_audit_files_template_categories(sc):
    categories = sc.audit_files.template_categories()
    assert isinstance(categories, list)
    for category in categories:
        check(category, 'categoryName', str)
        check(category, 'categoryId', str)
