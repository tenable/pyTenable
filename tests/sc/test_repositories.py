import os
import pytest

from tenable.errors import APIError, UnexpectedValueError
from ..checker import check


@pytest.fixture
def repository(request, vcr, admin):
    with vcr.use_cassette('repository'):
        repo = admin.repositories.create(name='Example Repo')

    def teardown():
        try:
            admin.repositories.delete(int(repo['id']))
        except APIError:
            pass

    request.addfinalizer(teardown)
    return repo


def test_repositories_constructor_nessus_sched_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(nessus_sched=1)


def test_repositories_constructor_mobile_sched_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(mobile_sched=1)


def test_repositories_constructor_remote_sched_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(remote_sched=1)


def test_repositories_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(name=1)

    with pytest.raises(TypeError):
        sc.repositories._constructor(nessus_sched={'type': 'dependent', 'dependentID': 1}, name=1)


def test_repositories_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(description=1)


def test_repositories_constructor_format_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(format=1)


def test_repositories_constructor_format_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.repositories._constructor(format='none')


def test_repositories_constructor_orgs_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(orgs=1)


def test_repositories_constructor_org_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(orgs=['one'])


def test_repositories_constructor_trending_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(trending='one')


def test_repositories_constructor_trending_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.repositories._constructor(trending=999)


def test_repositories_constructor_fulltext_search_typerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(fulltext_search='yup')


def test_repositories_constructor_lce_correlation_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(lce_correlation='yup')


def test_repositories_constructor_allowed_ips_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(allowed_ips='127.0.0.1')


def test_repositories_constructor_allowed_ips_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(allowed_ips=[1])


def test_repositories_constructor_remote_ip_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(remote_ip=1)


def test_repositories_constructor_remote_repo_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(remote_repo='one')


def test_repositories_constructor_preferences_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(preferences=1)


def test_repositories_constructor_preferences_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(preferences={1: 'one'})



def test_repositories_constructor_preferences_value_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(preferences={'key': 1})


def test_repositories_constructor_mdm_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(mdm_id='one')


def test_repositories_constructor_scanner_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._constructor(scanner_id='one')


def test_repositories_constructor_success(sc):
    resp = sc.repositories._constructor(
        nessus_sched={'type': 'ical', 'start': 'start', 'repeatRule': 'rule'},
        mobile_sched={'type': 'never'},
        remote_sched={'type': 'never'},
        name='Test Constructor',
        description='Desc',
        format='IPv4',
        repo_type='Local',
        orgs=[1],
        trending=90,
        fulltext_search=True,
        lce_correlation=[1],
        allowed_ips=['127.0.0.1'],
        remote_ip='127.0.0.1',
        remote_repo=1,
        preferences={'name': 'value'},
        mdm_id=1,
        scanner_id=1
    )
    assert resp == {
        'nessusSchedule': {
            'type': 'ical',
            'start': 'start',
            'repeatRule': 'rule'
        },
        'mobileSchedule': {'type': 'never'},
        'remoteSchedule': {'type': 'never'},
        'name': 'Test Constructor',
        'description': 'Desc',
        'dataFormat': 'IPv4',
        'type': 'Local',
        'organizations': [{'id': 1}],
        'trendingDays': 90,
        'trendWithRaw': 'true',
        'correlation': [{'id': 1}],
        'ipRange': '127.0.0.1',
        'remoteIP': '127.0.0.1',
        'remoteID': 1,
        'preferences': {
            'name': 'value'
        },
        'mdm': {'id': 1},
        'scanner': {'id': 1}
    }


@pytest.mark.vcr()
def test_repositories_create_success(repository):
    assert isinstance(repository, dict)
    check(repository, 'createdTime', str)
    check(repository, 'dataFormat', str)
    check(repository, 'description', str)
    check(repository, 'downloadFormat', str)
    check(repository, 'id', str)
    check(repository, 'lastSyncTime', str)
    check(repository, 'lastVulnUpdate', str)
    check(repository, 'modifiedTime', str)
    check(repository, 'name', str)
    check(repository, 'organizations', list)
    check(repository, 'remoteID', str, allow_none=True)
    check(repository, 'remoteIP', str, allow_none=True)
    check(repository, 'running', str)
    check(repository, 'type', str)
    check(repository, 'typeFields', dict)
    check(repository['typeFields'], 'correlation', list)
    check(repository['typeFields'], 'ipCount', str)
    check(repository['typeFields'], 'ipRange', str)
    check(repository['typeFields'], 'lastGenerateNessusTime', str)
    check(repository['typeFields'], 'lastTrendUpdate', str)
    check(repository['typeFields'], 'nessusSchedule', dict)
    check(repository['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(repository['typeFields']['nessusSchedule'], 'start', str)
    check(repository['typeFields']['nessusSchedule'], 'type', str)
    check(repository['typeFields'], 'runningNessus', str)
    check(repository['typeFields'], 'trendWithRaw', str)
    check(repository['typeFields'], 'trendingDays', str)
    check(repository, 'vulnCount', str)


def test_repositories_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.details('one')


def test_repositories_details_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.details(1, fields=1)


def test_repositories_details_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.details(1, fields=[1])


@pytest.mark.vcr()
def test_repositories_remote_sync(admin):
    admin.repositories.remote_sync(200001)


@pytest.mark.vcr()
def test_repositories_mobile_sync(admin):
    admin.repositories.mobile_sync(200001)


@pytest.mark.vcr()
def test_repositories_details_success(admin, repository):
    repository = admin.repositories.details(int(repository['id']))
    assert isinstance(repository, dict)
    check(repository, 'createdTime', str)
    check(repository, 'dataFormat', str)
    check(repository, 'description', str)
    check(repository, 'downloadFormat', str)
    check(repository, 'id', str)
    check(repository, 'lastSyncTime', str)
    check(repository, 'lastVulnUpdate', str)
    check(repository, 'modifiedTime', str)
    check(repository, 'name', str)
    check(repository, 'organizations', list)
    check(repository, 'remoteID', str, allow_none=True)
    check(repository, 'remoteIP', str, allow_none=True)
    check(repository, 'running', str)
    check(repository, 'type', str)
    check(repository, 'typeFields', dict)
    check(repository['typeFields'], 'correlation', list)
    check(repository['typeFields'], 'ipCount', str)
    check(repository['typeFields'], 'ipRange', str)
    check(repository['typeFields'], 'lastGenerateNessusTime', str)
    check(repository['typeFields'], 'lastTrendUpdate', str)
    check(repository['typeFields'], 'nessusSchedule', dict)
    check(repository['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(repository['typeFields']['nessusSchedule'], 'start', str)
    check(repository['typeFields']['nessusSchedule'], 'type', str)
    check(repository['typeFields'], 'runningNessus', str)
    check(repository['typeFields'], 'trendWithRaw', str)
    check(repository['typeFields'], 'trendingDays', str)
    check(repository, 'vulnCount', str)


@pytest.mark.vcr()
def test_repositories_list_success(admin):
    for repo in admin.repositories.list(fields=['id', 'name'], repo_type='Local'):
        assert isinstance(repo, dict)
        check(repo, 'name', str)
        check(repo, 'id', str)


@pytest.mark.vcr()
def test_repositories_create_success_data_format_ipv6(admin):
    repo = admin.repositories.create(dataFormat='IPv6', type='remote')
    assert isinstance(repo, dict)
    check(repo, 'name', str)
    check(repo, 'id', str)
    admin.repositories.delete(int(repo['id']))


@pytest.mark.vcr()
def test_repositories_create_success_data_format_mobile(admin):
    repo = admin.repositories.create(dataFormat='mobile')
    assert isinstance(repo, dict)
    check(repo, 'name', str)
    check(repo, 'id', str)
    admin.repositories.delete(int(repo['id']))


def test_repositories_delete_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.delete('one')


@pytest.mark.vcr()
def test_repositories_delete_success(admin, repository):
    admin.repositories.delete(int(repository['id']))


def test_repositories_edit_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.edit('one')


@pytest.mark.vcr()
def test_repositories_edit_success(admin, repository):
    repository = admin.repositories.edit(int(repository['id']), name='New Name')
    assert isinstance(repository, dict)
    check(repository, 'createdTime', str)
    check(repository, 'dataFormat', str)
    check(repository, 'description', str)
    check(repository, 'downloadFormat', str)
    check(repository, 'id', str)
    check(repository, 'lastSyncTime', str)
    check(repository, 'lastVulnUpdate', str)
    check(repository, 'modifiedTime', str)
    check(repository, 'name', str)
    check(repository, 'organizations', list)
    check(repository, 'remoteID', str, allow_none=True)
    check(repository, 'remoteIP', str, allow_none=True)
    check(repository, 'running', str)
    check(repository, 'type', str)
    check(repository, 'typeFields', dict)
    check(repository['typeFields'], 'correlation', list)
    check(repository['typeFields'], 'ipCount', str)
    check(repository['typeFields'], 'ipRange', str)
    check(repository['typeFields'], 'lastGenerateNessusTime', str)
    check(repository['typeFields'], 'lastTrendUpdate', str)
    check(repository['typeFields'], 'nessusSchedule', dict)
    check(repository['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(repository['typeFields']['nessusSchedule'], 'start', str)
    check(repository['typeFields']['nessusSchedule'], 'type', str)
    check(repository['typeFields'], 'runningNessus', str)
    check(repository['typeFields'], 'trendWithRaw', str)
    check(repository['typeFields'], 'trendingDays', str)
    check(repository, 'vulnCount', str)


def test_repositories_rules_constructor_plugin_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._rules_constructor(plugin_id='one')


def test_repositories_rules_constructor_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._rules_constructor(port='one')


def test_repositories_rules_constructor_org_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._rules_constructor(orgs=1)


def test_repositories_rules_constructor_org_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._rules_constructor(orgs=['one'])


def test_repositories_rules_constructor_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._rules_constructor(fields=1)


def test_repositories_rules_constructor_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories._rules_constructor(fields=[1])


def test_repositories_rules_constructor_success(sc):
    resp = sc.repositories._rules_constructor(
        plugin_id=1,
        port=1,
        orgs=[1, 2],
        fields=['name1', 'name2'])
    assert resp == {
        'pluginID': 1,
        'port': 1,
        'organizationIDs': '1,2',
        'fields': 'name1,name2'
    }


def test_repositories_accept_risk_rules_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.accept_risk_rules('one')


@pytest.mark.skip(reason='Need VCRed data to test against')
@pytest.mark.vcr()
def test_repositories_accept_risk_rules_success():
    pass


def test_repositories_recast_risk_rules_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.recast_risk_rules('one')


@pytest.mark.skip(reason='Need VCRed data to test against')
@pytest.mark.vcr()
def test_repositories_recast_risk_rules_success():
    pass


def test_repositories_asset_intersections_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.asset_intersections('one')


def test_repositories_asset_intersections_uuid_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.asset_intersections(1, uuid=1)


def test_repositories_asset_intersections_uuid_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.repositories.asset_intersections(1, uuid='something')


def test_repositories_asset_intersections_dns_typerrror(sc):
    with pytest.raises(TypeError):
        sc.repositories.asset_intersections(1, dns=1)


def test_repositories_asset_intersections_ip_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.asset_intersections(1, ip=1)


@pytest.mark.vcr()
def test_repositories_asset_intersections_success(admin, repository):
    asset_lists = admin.repositories.asset_intersections(
        int(repository['id']), ip_address='192.168.0.1')
    assert isinstance(asset_lists, list)
    for asset_list in asset_lists:
        check(asset_list, 'description', str)
        check(asset_list, 'id', str)
        check(asset_list, 'name', str)


def test_repositories_import_repository_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.import_repository('one', 1)


@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'sc_repo.tgz'))
def test_repositories_import_repository_success(admin, datafiles, repository):
    # offline = admin.repositories.create(name='Offline', type='Offline')
    with open(os.path.join(str(datafiles), 'sc_repo.tgz'), 'rb') as repo:
        admin.repositories.import_repository(int(repository['id']), repo)


def test_repositories_export_repository_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.export_repository('one', 1)


@pytest.mark.vcr()
def test_repositories_export_repository_success(admin, repository):
    with open('{}'.format(repository['id']), 'wb') as repo:
        admin.repositories.export_repository(int(repository['id']), repo)
    os.remove('{}'.format(repository['id']))


def test_repositories_device_info_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.device_info('one')


def test_repositories_device_into_dns_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.device_info(1, dns=1)


def test_repositories_device_info_ip_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.device_info(1, ip=1)


def test_repositories_device_info_uuid_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.device_info(1, uuid=1)


def test_repositories_device_info_uuid_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.repositories.device_info(1, uuid='something')


def test_repositories_device_info_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.device_info(1, fields=1)


def test_repositories_device_info_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.device_info(1, fields=[1])


@pytest.mark.vcr()
def test_repositories_device_info_success(admin, repository):
    repo = admin.repositories.device_info(int(repository['id']), dns='server')
    assert isinstance(repo, dict)
    check(repo, 'biosGUID', str)
    check(repo, 'hasCompliance', str)
    check(repo, 'hasPassive', str)
    check(repo, 'ip', str)
    check(repo, 'lastAuthRun', str)
    check(repo, 'lastScan', str)
    check(repo, 'lastUnauthRun', str)
    check(repo, 'links', list)
    check(repo, 'macAddress', str)
    check(repo, 'mcafeeGUID', str)
    check(repo, 'netbiosName', str)
    check(repo, 'os', str)
    check(repo, 'osCPE', str)
    check(repo, 'pluginSet', str)
    check(repo, 'pluginSet', str)
    check(repo, 'policyName', str)
    check(repo, 'repository', dict)
    check(repo['repository'], 'description', str)
    check(repo['repository'], 'id', str)
    check(repo['repository'], 'name', str)
    check(repo, 'score', str)
    check(repo, 'severityAll', str)
    check(repo, 'severityCritical', str)
    check(repo, 'severityInfo', str)
    check(repo, 'severityLow', str)
    check(repo, 'severityMedium', str)
    check(repo, 'total', str)
    check(repo, 'tpmID', str)
    check(repo, 'uniqueness', str)
    check(repo, 'uuid', str)


@pytest.mark.vcr()
def test_repositories_device_info_success_ip_info(admin, repository):
    admin.repositories._api.version = "5.6.0"
    repo = admin.repositories.device_info(int(repository['id']), dns='server')
    assert isinstance(repo, dict)
    check(repo, 'biosGUID', str)
    check(repo, 'hasCompliance', str)
    check(repo, 'hasPassive', str)
    check(repo, 'ip', str)


def test_repositories_remote_authorize_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_authorize(1, 'user', 'pass')


def test_repositories_remote_authorize_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_authorize('host', 1, 'pass')


def test_repositories_remote_authorize_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_authorize('host', 'user', 1)


@pytest.mark.skip(reason='No Downstream SC to Test with yet')
def test_repositories_remote_authorize_success():
    pass


def test_repositories_remote_fetch_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_fetch(1)


@pytest.mark.skip(reason='No Downstream SC to Test with yet')
def test_repositories_remote_fetch_success():
    pass
