'''
test file for testing various scenarios in security center's role functionality
'''
import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check


def test_roles_constructor_name_typeerror(security_center):
    '''
    test roles constructor for name type error
    '''
    with pytest.raises(TypeError):
        security_center.roles._constructor(name=1)


def test_roles_constructor_description_typeerror(security_center):
    '''
    test roles constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.roles._constructor(description=1)


def test_roles_constructor_role_mapping_typeerror(security_center):
    '''
    test roles constructor for 'role mapping' type error
    '''
    with pytest.raises(TypeError):
        security_center.roles._constructor(can_view_logs='nothing')


def test_roles_constructor_can_scan_(security_center):
    '''
    test roles constructor for 'can scan' type error
    '''
    with pytest.raises(TypeError):
        security_center.roles._constructor(can_scan=True)
    with pytest.raises(UnexpectedValueError):
        security_center.roles._constructor(can_scan='something')
    assert security_center.roles._constructor(can_scan='full') == {'permScan': 'full'}
    assert security_center.roles._constructor(can_scan='Full') == {'permScan': 'full'}


def test_roles_constructor_success(security_center):
    '''
    test roles constructor for success
    '''
    role = security_center.roles._constructor(
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
        'permViewOrgLogs': 'false',
        'permScan': 'none'
    }


@pytest.fixture
def role(request, security_center, vcr):
    '''
    test fixture for role
    '''
    with vcr.use_cassette('test_roles_create_success'):
        role = security_center.roles.create('Example Role')

    def teardown():
        try:
            with vcr.use_cassette('test_roles_delete_success'):
                security_center.roles.delete(int(role['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return role


@pytest.mark.vcr()
def test_roles_create_success(role):
    '''
    test roles create for success
    '''
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
def test_roles_details_success(security_center, role):
    '''
    test roles details for success
    '''
    role = security_center.roles.details(int(role['id']))
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
    check(role, 'organizationCounts', list)
    for org_count in role['organizationCounts']:
        check(org_count, 'id', str)
        check(org_count, 'userCount', str)
    check(role, 'creator', dict)
    check(role['creator'], 'id', str)
    check(role['creator'], 'username', str)
    check(role['creator'], 'firstname', str)
    check(role['creator'], 'lastname', str)


@pytest.mark.vcr()
def test_roles_details_success_for_fields(security_center, role):
    '''
    test roles details success for fields
    '''
    role = security_center.roles.details(int(role['id']), fields=['id', 'name', 'description'])
    assert isinstance(role, dict)
    check(role, 'id', str)
    check(role, 'name', str)
    check(role, 'description', str)


@pytest.mark.vcr()
def test_roles_list_success(security_center):
    '''
    test roles list for success
    '''
    for role in security_center.roles.list(fields=['id', 'name']):
        assert isinstance(role, dict)
        check(role, 'id', str)
        check(role, 'name', str)


@pytest.mark.vcr()
def test_roles_edit_success(security_center, role):
    '''
    test roles edit for success
    '''
    role = security_center.roles.edit(int(role['id']), name='Updated Role')
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
def test_roles_delete_success(security_center, role):
    '''
    test roles delete for success
    '''
    security_center.roles.delete(int(role['id']))
