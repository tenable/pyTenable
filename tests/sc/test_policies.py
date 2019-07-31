from tenable.errors import *
from ..checker import check, single
import pytest, os

@pytest.fixture
def policy(request, vcr, sc):
    with vcr.use_cassette('scan_policy'):
        policy = sc.policies.create(name='Example Policy')
    def teardown():
        try:
            sc.policies.delete(int(policy['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return policy

def test_policies_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(name=1)

def test_policies_constructor_context_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(context=1)

def test_policies_constructor_context_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.policies._constructor(context='not a scan')

def test_policies_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(description=1)

def test_policies_constructor_tags_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(tags=1)

def test_policies_constructor_preferences_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(preferences=1)

def test_policies_constructor_preference_item_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(preferences={1: 'value'})

def test_policies_constructor_preference_item_value_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(preferences={'name': 1})

def test_policies_constructor_audit_files_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(audit_files=1)

def test_policies_constructor_audit_files_file_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(audit_files=['one'])

def test_policies_constructor_template_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(template_id='one')

def test_policies_constructor_profile_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(profile_name=1)

def test_policies_constructor_xccdf_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(xccdf='yup')

def test_policies_constructor_owner_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies._constructor(owner_id='one')

def test_policies_constructor(sc):
    r = sc.policies._constructor(
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
    assert r == {
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

def test_policies_template_list_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.template_list(fields=1)

@pytest.mark.vcr()
def test_policies_template_list_success(sc):
    resp = sc.policies.template_list()
    assert isinstance(resp, list)
    t = resp[0]
    assert isinstance(t, dict)
    check(t, 'description', str)
    check(t, 'id', str)
    check(t, 'name', str)

def test_policies_template_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.template_details('nope')

def test_policies_template_details_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.template_details(1, fields='noper')

@pytest.mark.vcr()
def test_policies_template_details_success(sc):
    tmpl = sc.policies.template_details(1)
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

def test_policies_create_name_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.policies.create()

@pytest.mark.vcr()
def test_policies_create_name_typerror(sc):
    with pytest.raises(TypeError):
        sc.policies.create(name=1)

@pytest.mark.vcr()
def test_policies_create_template_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.create(name='Test', template_id='one')

@pytest.mark.vcr()
def test_policies_create_success(sc, policy):
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

def test_policies_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.details('one')

def test_policies_details_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.details(1, fields='one')

@pytest.mark.vcr()
def test_policies_details(sc, policy):
    policy = sc.policies.details(int(policy['id']))
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
def test_policies_edit(sc, policy):
    policy = sc.policies.edit(int(policy['id']), name='New Policy Name')
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
def test_policies_list(sc):
    policies = sc.policies.list()
    for policy in policies['manageable']:
        check(policy, 'description', str)
        check(policy, 'id', str)
        check(policy, 'name', str)

def test_policies_delete_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.delete('nothing')

@pytest.mark.vcr()
def test_policies_delete(sc, policy):
    sc.policies.delete(int(policy['id']))

def test_policies_copy_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.copy('nope')

def test_policies_copy_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.copy(1, name=1)

@pytest.mark.vcr()
def test_policies_copy(sc, policy):
    policy = sc.policies.copy(int(policy['id']), name='Copied Policy')
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

def test_policies_export_policy_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.export_policy('nope')

@pytest.mark.vcr()
def test_policies_export_policy(sc, policy):
    with open('{}.xml'.format(policy['id']), 'wb') as pfile:
        sc.policies.export_policy(int(policy['id']), fobj=pfile)
    os.remove('{}.xml'.format(policy['id']))

def test_policies_import_policy_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.import_policy(1, '')

def test_policies_import_policy_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.import_policy('Name', '', description=1)

def test_policies_import_policy_tags_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.import_policy('Name', '', tags=1)

@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'sc_policy.xml'))
def test_policies_import_policy(sc, datafiles):
    with open(os.path.join(str(datafiles), 'sc_policy.xml'), 'rb') as fobj:
        sc.policies.import_policy('Example Imported Policy', fobj)

def test_policies_share_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.share('one')

def test_policies_share_group_typeerror(sc):
    with pytest.raises(TypeError):
        sc.policies.share(1, 'one')

@pytest.mark.vcr()
def test_policies_share(sc, policy):
    policy = sc.policies.share(int(policy['id']), 1)
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
def test_policies_tags(sc):
    tags = sc.policies.tags()
    for tag in tags:
        single(tag, str)