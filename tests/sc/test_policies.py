'''
test file for testing various scenarios in security center
policies functionality
'''
import os

import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check, single


@pytest.fixture
def policy(request, vcr, security_center):
    '''
    test fixture for policy
    '''
    with vcr.use_cassette('scan_policy'):
        policy = security_center.policies.create(name='Example Policy')

    def teardown():
        try:
            security_center.policies.delete(int(policy['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return policy


def test_policies_constructor_name_typeerror(security_center):
    '''
    test policies constructor for name type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(name=1)


def test_policies_constructor_context_typeerror(security_center):
    '''
    test policies constructor for context type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(context=1)


def test_policies_constructor_context_unexpectedvalueerror(security_center):
    '''
    test policies constructor for context unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.policies._constructor(context='not a scan')


def test_policies_constructor_description_typeerror(security_center):
    '''
    test policies constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(description=1)


def test_policies_constructor_tags_typeerror(security_center):
    '''
    test policies constructor for tags type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(tags=1)


def test_policies_constructor_preferences_typeerror(security_center):
    '''
    test policies constructor for preferences type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(preferences=1)


def test_policies_constructor_preference_item_name_typeerror(security_center):
    '''
    test policies constructor for 'item name' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(preferences={1: 'value'})


def test_policies_constructor_preference_item_value_should_not_typeerror(security_center):
    '''
    test policies constructor for 'item value' type error
    '''
    security_center.policies._constructor(preferences={'name': 1})

def test_policies_constructor_audit_files_typeerror(security_center):
    '''
    test policies constructor for 'audit files' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(audit_files=1)


def test_policies_constructor_audit_files_file_typeerror(security_center):
    '''
    test policies constructor for 'audit files file' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(audit_files=['one'])


def test_policies_constructor_template_id_typeerror(security_center):
    '''
    test policies constructor for 'template id' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(template_id='one')


def test_policies_constructor_profile_name_typeerror(security_center):
    '''
    test policies constructor for 'profile name' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(profile_name=1)


def test_policies_constructor_xccdf_typeerror(security_center):
    '''
    test policies constructor for 'xccdf' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(xccdf='yup')


def test_policies_constructor_owner_id_typeerror(security_center):
    '''
    test policies constructor for 'owner id' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies._constructor(owner_id='one')


def test_policies_constructor(security_center):
    '''
    test policies constructor for success
    '''
    resp = security_center.policies._constructor(
        name='Example',
        context='',
        description='Something Special',
        tags='',
        preferences={
            'name1': 'value1',
            'name2': 'value2'
        },
        audit_files=[1],
        template_id=1,
        profile_name='ProfileName',
        xccdf=True,
        owner_id=1
    )
    assert resp == {
        'name': 'Example',
        'context': '',
        'description': 'Something Special',
        'tags': '',
        'preferences': {
            'name1': 'value1',
            'name2': 'value2'
        },
        'auditFiles': [{'id': 1}],
        'policyTemplate': {'id': 1},
        'policyProfileName': 'ProfileName',
        'generateXCCDFResults': 'true',
        'ownerID': 1
    }


def test_policies_template_list_fields_typeerror(security_center):
    '''
    test policies template list for fields type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.template_list(fields=1)


@pytest.mark.vcr()
def test_policies_template_list_success(security_center):
    '''
    test policies template list for success
    '''
    resp = security_center.policies.template_list()
    assert isinstance(resp, list)
    a_resp = resp[0]
    assert isinstance(a_resp, dict)
    check(a_resp, 'description', str)
    check(a_resp, 'id', str)
    check(a_resp, 'name', str)


def test_policies_template_details_id_typeerror(security_center):
    '''
    test policies template details for id type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.template_details('nope')


def test_policies_template_details_fields_typeerror(security_center):
    '''
    test policies template details for 'fields' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.template_details(1, fields='noper')


@pytest.mark.vcr()
def test_policies_template_details_success(security_center):
    '''
    test policies template details for success
    '''
    tmpl = security_center.policies.template_details(1)
    assert isinstance(tmpl, dict)
    check(tmpl, 'createdTime', str)
    check(tmpl, 'credentials', dict)
    for key in tmpl['credentials']:
        single(key, str)
        check(tmpl['credentials'], key, dict)
        for pref in tmpl['credentials'][key]:
            single(pref, str)
            check(tmpl['credentials'][key], pref, str)
    check(tmpl, 'description', str)
    check(tmpl, 'id', str)
    check(tmpl, 'modifiedTime', str)
    check(tmpl, 'name', str)
    check(tmpl, 'preferences', dict)
    for key in tmpl['preferences']:
        single(key, str)
        check(tmpl['preferences'], key, str)
    check(tmpl, 'templateDefModTime', str)
    check(tmpl, 'templateModTime', str)
    check(tmpl, 'templatePubTime', str)


def test_policies_create_name_unexpectedvalueerror(security_center):
    '''
    test policies create for name unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.policies.create()


@pytest.mark.vcr()
def test_policies_create_name_typerror(security_center):
    '''
    test policies create for name type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.create(name=1)


@pytest.mark.vcr()
def test_policies_create_template_id_typeerror(security_center):
    '''
    test policies create template for id typeerror
    '''
    with pytest.raises(TypeError):
        security_center.policies.create(name='Test', template_id='one')


@pytest.mark.vcr()
def test_policies_create_success(policy):
    '''
    test policies create for success
    '''
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


def test_policies_details_id_typeerror(security_center):
    '''
    test policies details for id type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.details('one')


def test_policies_details_fields_typeerror(security_center):
    '''
    test policies details for fields type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.details(1, fields='one')


@pytest.mark.vcr()
def test_policies_details(security_center, policy):
    '''
    test policies details for success
    '''
    policy = security_center.policies.details(int(policy['id']))
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


@pytest.mark.vcr()
def test_policies_edit(security_center, policy):
    '''
    test policies edit for success
    '''
    policy = security_center.policies.edit(int(policy['id']), name='New Policy Name')
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', int)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


@pytest.mark.vcr()
def test_policies_edit_for_remove_pref(security_center, policy):
    '''
    test policies edit success for remove pref
    '''
    policy = security_center.policies.edit(int(policy['id']), name='Policy Name New', remove_prefs=['scan_malware'])
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'name', str)
    assert policy['name'] == "Policy Name New"


@pytest.mark.vcr()
def test_policies_list(security_center):
    '''
    test policies list for success
    '''
    policies = security_center.policies.list()
    for policy in policies['manageable']:
        check(policy, 'description', str)
        check(policy, 'id', str)
        check(policy, 'name', str)


@pytest.mark.vcr()
def test_policies_list_for_fields(security_center):
    '''
    test policies list success for fields
    '''
    policies = security_center.policies.list(fields=["id", "name", "description", "status"])
    for policy in policies['manageable']:
        check(policy, 'description', str)
        check(policy, 'id', str)
        check(policy, 'name', str)
        check(policy, 'status', str)


def test_policies_delete_id_typeerror(security_center):
    '''
    test policies delete for id type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.delete('nothing')


@pytest.mark.vcr()
def test_policies_delete(security_center, policy):
    '''
    test policies delete for success
    '''
    security_center.policies.delete(int(policy['id']))


def test_policies_copy_id_typeerror(security_center):
    '''
    test policies copy for id type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.copy('nope')


def test_policies_copy_name_typeerror(security_center):
    '''
    test policies copy for name type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.copy(1, name=1)


@pytest.mark.vcr()
def test_policies_copy(security_center, policy):
    '''
    test policies copy for success
    '''
    policy = security_center.policies.copy(int(policy['id']), name='Copied Policy')
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


def test_policies_export_policy_id_typeerror(security_center):
    '''
    test policies export for 'policy id' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.export_policy('nope')


@pytest.mark.vcr()
def test_policies_export_policy(security_center, policy):
    '''
    test policies export for success
    '''
    with open('{}.xml'.format(policy['id']), 'wb') as pfile:
        security_center.policies.export_policy(int(policy['id']), fobj=pfile)
    os.remove('{}.xml'.format(policy['id']))


@pytest.mark.vcr()
def test_policies_export_policy_no_file(security_center, policy):
    '''
    test policies export with no file
    '''
    with open('{}.xml'.format(policy['id']), 'wb'):
        security_center.policies.export_policy(int(policy['id']))
    os.remove('{}.xml'.format(policy['id']))


def test_policies_import_policy_name_typeerror(security_center):
    '''
    test policies import for 'policy name' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.import_policy(1, '')


def test_policies_import_policy_description_typeerror(security_center):
    '''
    test policies import for 'policy description' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.import_policy('Name', '', description=1)


def test_policies_import_policy_tags_typeerror(security_center):
    '''
    test policies import for 'policy tags' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.import_policy('Name', '', tags=1)


@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'sc_policy.xml'))
def test_policies_import_policy(security_center, datafiles):
    '''
    test policies import for success
    '''
    with open(os.path.join(str(datafiles), 'sc_policy.xml'), 'rb') as fobj:
        security_center.policies.import_policy('Example Imported Policy', fobj)


def test_policies_share_id_typeerror(security_center):
    '''
    test policies share for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.share('one')


def test_policies_share_group_typeerror(security_center):
    '''
    test policies share for 'group' type error
    '''
    with pytest.raises(TypeError):
        security_center.policies.share(1, 'one')


@pytest.mark.vcr()
def test_policies_share(security_center, policy):
    '''
    test policies share for success
    '''
    policy = security_center.policies.share(int(policy['id']), 1)
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


@pytest.mark.vcr()
def test_policies_tags(security_center):
    '''
    test policies tags for success
    '''
    tags = security_center.policies.tags()
    for tag in tags:
        single(tag, str)
