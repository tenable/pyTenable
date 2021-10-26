'''
test policies
'''
import io
import pytest
from tenable.errors import NotFoundError, UnexpectedValueError
from ..checker import check


@pytest.mark.vcr()
def test_configure_id_typeerror(api):
    '''
    test to raise the exception when type of id is not as defined
    '''
    with pytest.raises(TypeError):
        api.policies.configure('nope', dict())


@pytest.mark.vcr()
def test_configure_policy_typeerror(api):
    '''
    test to raise the exception when type of policy is not as defined
    '''
    with pytest.raises(TypeError):
        api.policies.configure(1, 'nope')


@pytest.mark.vcr()
def test_configure_policy_notfounderror(api):
    '''
    test to raise the exception when a policy to be configured is not found
    '''
    with pytest.raises(NotFoundError):
        api.policies.configure(1, dict())


@pytest.mark.vcr()
def test_configure_policy(api, policy):
    '''
    test to configure the policy
    '''
    details = api.policies.details(policy['policy_id'])
    details['settings']['name'] = 'MODIFIED'
    api.policies.configure(policy['policy_id'], details)
    updated = api.policies.details(policy['policy_id'])
    assert updated['settings']['name'] == 'MODIFIED'


@pytest.mark.vcr()
def test_copy_policy_id_typeerror(api):
    '''
    test to raise the exception when type of policy_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.policies.copy('nope')


@pytest.mark.vcr()
def test_copy_policy_notfounderror(api):
    '''
    test to raise the exception when the policy to be copied is not found
    '''
    with pytest.raises(NotFoundError):
        api.policies.copy(1)


@pytest.mark.vcr()
def test_copy_policy(api, policy):
    '''
    test to copy the policy
    '''
    new = api.policies.copy(policy['policy_id'])
    assert isinstance(new, dict)
    check(new, 'id', int)
    check(new, 'name', str)
    assert 'Copy of' in new['name']
    api.policies.delete(new['id'])


@pytest.mark.vcr()
def test_create_policy(api, policy):
    '''test to check types of a policy'''
    assert isinstance(policy, dict)
    check(policy, 'policy_id', int)
    check(policy, 'policy_name', str)


@pytest.mark.vcr()
def test_delete_policy_id_typeerror(api):
    '''
    test to raise the exception when type of policy_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.policies.delete('nope')


@pytest.mark.vcr()
def test_delete_policy_notfounderror(api):
    '''
    test to raise the exception when policy to be deleted is not found
    '''
    with pytest.raises(NotFoundError):
        api.policies.delete(1)


@pytest.mark.vcr()
def test_delete_policy(api, policy):
    '''
    test to delete the policy
    '''
    api.policies.delete(policy['policy_id'])


@pytest.mark.vcr()
def test_policy_details_id_typeerror(api):
    '''
    test to raise the exception when the type of id is
    not of the expected type
    '''
    with pytest.raises(TypeError):
        api.policies.details('nope')


@pytest.mark.vcr()
def test_policy_details_notfounderror(api):
    '''
    test to raise the exception when the details of the policy is not found
    '''
    with pytest.raises(NotFoundError):
        api.policies.details(1)


@pytest.mark.vcr()
def test_policy_details(api, policy):
    '''
    test to get the policy details
    '''
    policy = api.policies.details(policy['policy_id'])
    assert isinstance(policy, dict)
    check(policy, 'uuid', 'scanner-uuid')
    check(policy, 'settings', dict)


@pytest.mark.vcr()
def test_policy_export_id_typeerror(api):
    '''
    test to raise the exception when type of export id is not as defined
    '''
    with pytest.raises(TypeError):
        api.policies.policy_export('nope')


@pytest.mark.vcr()
def test_policy_export_notfounderror(api):
    '''
    test to raise the exception when the policy to be exported is not found
    '''
    with pytest.raises(NotFoundError):
        api.policies.policy_export(1)


@pytest.mark.vcr()
def test_policy_export(api, policy):
    '''
    test to export the policy data
    '''
    pobj = api.policies.policy_export(policy['policy_id'])
    assert isinstance(pobj, io.BytesIO)


@pytest.mark.vcr()
def test_policy_import(api, policy):
    '''
    test to import the policy
    '''
    pobj = api.policies.policy_export(policy['policy_id'])
    resp = api.policies.policy_import(pobj)
    assert isinstance(resp, dict)
    check(resp, 'creation_date', int)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'no_target', str)
    check(resp, 'owner', str)
    check(resp, 'owner_id', int)
    check(resp, 'shared', int)
    check(resp, 'template_uuid', 'scanner-uuid')
    check(resp, 'user_permissions', int)


@pytest.mark.vcr()
def test_policy_list(api, policy):
    '''
    test to get the policy list
    '''
    policies = api.policies.list()
    assert isinstance(policies, list)
    for pol in policies:
        check(pol, 'creation_date', int)
        check(pol, 'description', str, allow_none=True)
        check(pol, 'id', int)
        check(pol, 'last_modification_date', int)
        check(pol, 'name', str)
        check(pol, 'no_target', str)
        check(pol, 'owner', str)
        check(pol, 'owner_id', int)
        check(pol, 'shared', int)
        check(pol, 'template_uuid', 'scanner-uuid')
        check(pol, 'user_permissions', int)
        check(pol, 'visibility', str)


@pytest.mark.vcr()
def test_policy_template_details_success(api):
    '''
    test to get the template details
    '''
    template_detail = api.policies.template_details('agent_advanced')
    assert isinstance(template_detail, dict)
    check(template_detail, 'compliance', dict)
    check(template_detail, 'plugins', dict)
    check(template_detail, 'settings', dict)
    check(template_detail, 'uuid', 'scanner-uuid')


@pytest.mark.vcr()
def test_policy_template_details_keyerror(api):
    '''
    test to raise the exception when key of template details is not as defined
    '''
    with pytest.raises(UnexpectedValueError):
        api.policies.template_details('one')


@pytest.mark.vcr()
def test_policy_template_details_typeerror(api):
    '''
    test to raise the exception when type of details is not as defined
    '''
    with pytest.raises(TypeError):
        api.policies.template_details(1)


@pytest.mark.vcr()
def test_policies_template_details_new_success(api):
    '''
    test to get template details
    '''
    templates = api.policies.templates()
    for keys in templates.keys():
        api.policies.template_details(keys)
