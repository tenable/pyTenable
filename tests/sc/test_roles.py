from tenable.errors import *
from ..checker import check, single
import pytest, os

def test_roles_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(name=1)

def test_roles_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(description=1)

def test_roles_constructor_role_mapping_typeerror(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(can_view_logs='nothing')

def test_roles_constructor_success(sc):
    role = sc.roles._constructor(
        name='Example',
        description='stuff',
        manage_attributes=True,
        can_share=True,
        create_policies=True,
        can_view_logs=False
    )
    assert role == {
        'name': 'Example',
        'description': 'stuff',
        'permManageAttributeSets': 'true',
        'permShareObjects': 'true',
        'permCreatePolicies': 'true',
        'permViewOrgLogs': 'false'
    }

@pytest.fixture
def role(request, sc, vcr):
    with vcr.use_cassette('test_roles_create_success'):
        role = sc.roles.create('Example Role')
    def teardown():
        try:
            with vcr.use_cassette('test_roles_delete_success'):
                sc.roles.delete(int(role['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return role

@pytest.mark.vcr()
def test_roles_create_success(sc, role):
    assert isinstance(role, dict)
    check(role, 'id', str)
    check(role, 'name', str)
    check(role, 'description', str)
    check(role, 'createdTime', str)
    check(role, 'modifiedTime', str)
    check(role, 'permManageApp', str)
    check(role, 'permManageGroups', str)
    check(role, 'permManageRoles', str)
    check(role, 'permManageImages', str)
    check(role, 'permManageGroupRelationships', str)
    check(role, 'permManageBlackoutWindows', str)
    check(role, 'permManageAttributeSets', str)
    check(role, 'permCreateTickets', str)
    check(role, 'permCreateAlerts', str)
    check(role, 'permCreateAuditFiles', str)
    check(role, 'permCreateLDAPAssets', str)
    check(role, 'permCreatePolicies', str)
    check(role, 'permPurgeTickets', str)
    check(role, 'permPurgeScanResults', str)
    check(role, 'permPurgeReportResults', str)
    check(role, 'permScan', str)
    check(role, 'permAgentsScan', str)
    check(role, 'permShareObjects', str)
    check(role, 'permUpdateFeeds', str)
    check(role, 'permShareObjects', str)
    check(role, 'permUploadNessusResults', str)
    check(role, 'permViewOrgLogs', str)
    check(role, 'permManageAcceptRiskRules', str)
    check(role, 'permManageRecastRiskRules', str)

@pytest.mark.vcr()
def test_roles_details_success(sc, role):
    r = sc.roles.details(int(role['id']))
    assert isinstance(r, dict)
    check(r, 'id', str)
    check(r, 'name', str)
    check(r, 'description', str)
    check(r, 'createdTime', str)
    check(r, 'modifiedTime', str)
    check(r, 'permManageApp', str)
    check(r, 'permManageGroups', str)
    check(r, 'permManageRoles', str)
    check(r, 'permManageImages', str)
    check(r, 'permManageGroupRelationships', str)
    check(r, 'permManageBlackoutWindows', str)
    check(r, 'permManageAttributeSets', str)
    check(r, 'permCreateTickets', str)
    check(r, 'permCreateAlerts', str)
    check(r, 'permCreateAuditFiles', str)
    check(r, 'permCreateLDAPAssets', str)
    check(r, 'permCreatePolicies', str)
    check(r, 'permPurgeTickets', str)
    check(r, 'permPurgeScanResults', str)
    check(r, 'permPurgeReportResults', str)
    check(r, 'permScan', str)
    check(r, 'permAgentsScan', str)
    check(r, 'permShareObjects', str)
    check(r, 'permUpdateFeeds', str)
    check(r, 'permShareObjects', str)
    check(r, 'permUploadNessusResults', str)
    check(r, 'permViewOrgLogs', str)
    check(r, 'permManageAcceptRiskRules', str)
    check(r, 'permManageRecastRiskRules', str)
    check(r, 'organizationCounts', list)
    for i in r['organizationCounts']:
        check(i, 'id', str)
        check(i, 'userCount', str)
    check(r, 'creator', dict)
    check(r['creator'], 'id', str)
    check(r['creator'], 'username', str)
    check(r['creator'], 'firstname', str)
    check(r['creator'], 'lastname', str)

@pytest.mark.vcr()
def test_roles_edit_success(sc, role):
    r = sc.roles.edit(int(role['id']), name='Updated Role')
    assert isinstance(r, dict)
    check(r, 'id', str)
    check(r, 'name', str)
    check(r, 'description', str)
    check(r, 'createdTime', str)
    check(r, 'modifiedTime', str)
    check(r, 'permManageApp', str)
    check(r, 'permManageGroups', str)
    check(r, 'permManageRoles', str)
    check(r, 'permManageImages', str)
    check(r, 'permManageGroupRelationships', str)
    check(r, 'permManageBlackoutWindows', str)
    check(r, 'permManageAttributeSets', str)
    check(r, 'permCreateTickets', str)
    check(r, 'permCreateAlerts', str)
    check(r, 'permCreateAuditFiles', str)
    check(r, 'permCreateLDAPAssets', str)
    check(r, 'permCreatePolicies', str)
    check(r, 'permPurgeTickets', str)
    check(r, 'permPurgeScanResults', str)
    check(r, 'permPurgeReportResults', str)
    check(r, 'permScan', str)
    check(r, 'permAgentsScan', str)
    check(r, 'permShareObjects', str)
    check(r, 'permUpdateFeeds', str)
    check(r, 'permShareObjects', str)
    check(r, 'permUploadNessusResults', str)
    check(r, 'permViewOrgLogs', str)
    check(r, 'permManageAcceptRiskRules', str)
    check(r, 'permManageRecastRiskRules', str)

@pytest.mark.vcr()
def test_roles_delete_success(sc, role):
    sc.roles.delete(int(role['id']))