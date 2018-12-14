from tenable.errors import *
from ..checker import check, single
import uuid, io, pytest

@pytest.mark.vcr()
def test_configure_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.configure('nope', dict())

@pytest.mark.vcr()
def test_configure_policy_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.configure(1, 'nope')

@pytest.mark.vcr()
def test_configure_policy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.configure(1, dict())

@pytest.mark.vcr()
def test_configure_policy(api, policy):
    details = api.policies.details(policy['policy_id'])
    details['settings']['name'] = 'MODIFIED'
    api.policies.configure(policy['policy_id'], details)
    updated = api.policies.details(policy['policy_id'])
    assert updated['settings']['name'] == 'MODIFIED'

@pytest.mark.vcr()
def test_copy_policy_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.copy('nope')

@pytest.mark.vcr()
def test_copy_policy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.copy(1)

@pytest.mark.vcr()
def test_copy_policy(api, policy):
    new = api.policies.copy(policy['policy_id'])
    assert isinstance(new, dict)
    check(new, 'id', int)
    check(new, 'name', str)
    assert 'Copy of' in new['name']
    api.policies.delete(new['id'])

@pytest.mark.vcr()
def test_create_policy(api, policy):
    assert isinstance(policy, dict)
    check(policy, 'policy_id', int)
    check(policy, 'policy_name', str)

@pytest.mark.vcr()
def test_delete_policy_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.delete('nope')

@pytest.mark.vcr()
def test_delete_policy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.delete(1)

@pytest.mark.vcr()
def test_delete_policy(api, policy):
    api.policies.delete(policy['policy_id'])

@pytest.mark.vcr()
def test_policy_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.details('nope')

@pytest.mark.vcr()
def test_policy_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.details(1)

@pytest.mark.vcr()
def test_policy_details(api, policy):
    policy = api.policies.details(policy['policy_id'])
    assert isinstance(policy, dict)
    check(policy, 'uuid', 'scanner-uuid')
    check(policy, 'settings', dict)

@pytest.mark.vcr()
def test_policy_export_id_typeerror(api):
    with pytest.raises(TypeError):
        api.policies.policy_export('nope')

@pytest.mark.vcr()
def test_policy_export_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.policies.policy_export(1)

@pytest.mark.vcr()
def test_policy_export(api, policy):
    pobj = api.policies.policy_export(policy['policy_id'])
    assert isinstance(pobj, io.BytesIO)

@pytest.mark.vcr()
def test_policy_import(api, policy):
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
    policies = api.policies.list()
    assert isinstance(policies, list)
    for p in policies:
        check(p, 'creation_date', int)
        check(p, 'description', str, allow_none=True)
        check(p, 'id', int)
        check(p, 'last_modification_date', int)
        check(p, 'name', str)
        check(p, 'no_target', str)
        check(p, 'owner', str)
        check(p, 'owner_id', int)
        check(p, 'shared', int)
        check(p, 'template_uuid', 'scanner-uuid')
        check(p, 'user_permissions', int)
        check(p, 'visibility', str)