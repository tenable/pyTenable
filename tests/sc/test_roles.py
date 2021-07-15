import pytest
from ..checker import check
from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception


def test_roles_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(name=1)


def test_roles_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(description=1)


def test_roles_constructor_role_mapping_typeerror(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(can_view_logs='nothing')


def test_roles_constructor_can_scan_(sc):
    with pytest.raises(TypeError):
        sc.roles._constructor(can_scan=True)
    with pytest.raises(UnexpectedValueError):
        sc.roles._constructor(can_scan='something')
    assert sc.roles._constructor(can_scan='full') == {'permScan': 'full'}
    assert sc.roles._constructor(can_scan='Full') == {'permScan': 'full'}


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
        'permViewOrgLogs': 'false',
        'permScan': 'none'
    }


@pytest.fixture
def role(request, sc, vcr):
    with vcr.use_cassette('test_roles_create_success'):
        role = sc.roles.create('Example Role')

    def teardown():
        try:
            with vcr.use_cassette('test_roles_delete_success'):
                sc.roles.delete(int(role['id']))
        except APIError as error:
            log_exception(error)

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
    role = sc.roles.details(int(role['id']))
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
def test_roles_details_success_for_fields(sc, role):
    role = sc.roles.details(int(role['id']), fields=['id', 'name', 'description'])
    assert isinstance(role, dict)
    check(role, 'id', str)
    check(role, 'name', str)
    check(role, 'description', str)


@pytest.mark.vcr()
def test_roles_list_success(sc):
    for role in sc.roles.list(fields=['id', 'name']):
        assert isinstance(role, dict)
        check(role, 'id', str)
        check(role, 'name', str)


@pytest.mark.vcr()
def test_roles_edit_success(sc, role):
    role = sc.roles.edit(int(role['id']), name='Updated Role')
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
def test_roles_delete_success(sc, role):
    sc.roles.delete(int(role['id']))
