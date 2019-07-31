from tenable.errors import *
from ..checker import check, single
import pytest, os

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
        sc.repositories._constructor(preferences={1:'one'})

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
def test_repositories_create_success(admin, repository):
    assert isinstance(repository, dict)
    r = repository
    check(r, 'createdTime', str)
    check(r, 'dataFormat', str)
    check(r, 'description', str)
    check(r, 'downloadFormat', str)
    check(r, 'id', str)
    check(r, 'lastSyncTime', str)
    check(r, 'lastVulnUpdate', str)
    check(r, 'modifiedTime', str)
    check(r, 'name', str)
    check(r, 'organizations', list)
    check(r, 'remoteID', str, allow_none=True)
    check(r, 'remoteIP', str, allow_none=True)
    check(r, 'running', str)
    check(r, 'type', str)
    check(r, 'typeFields', dict)
    check(r['typeFields'], 'correlation', list)
    check(r['typeFields'], 'ipCount', str)
    check(r['typeFields'], 'ipRange', str)
    check(r['typeFields'], 'lastGenerateNessusTime', str)
    check(r['typeFields'], 'lastTrendUpdate', str)
    check(r['typeFields'], 'nessusSchedule', dict)
    check(r['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(r['typeFields']['nessusSchedule'], 'start', str)
    check(r['typeFields']['nessusSchedule'], 'type', str)
    check(r['typeFields'], 'runningNessus', str)
    check(r['typeFields'], 'trendWithRaw', str)
    check(r['typeFields'], 'trendingDays', str)
    check(r, 'vulnCount', str)

def test_repositories_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.details('one')

def test_repositories_details_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.details(1, fields=1)

def test_repopsitories_details_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.details(1, fields=[1])

@pytest.mark.vcr()
def test_repositories_details_success(admin, repository):
    r = admin.repositories.details(int(repository['id']))
    assert isinstance(r, dict)
    check(r, 'createdTime', str)
    check(r, 'dataFormat', str)
    check(r, 'description', str)
    check(r, 'downloadFormat', str)
    check(r, 'id', str)
    check(r, 'lastSyncTime', str)
    check(r, 'lastVulnUpdate', str)
    check(r, 'modifiedTime', str)
    check(r, 'name', str)
    check(r, 'organizations', list)
    check(r, 'remoteID', str, allow_none=True)
    check(r, 'remoteIP', str, allow_none=True)
    check(r, 'running', str)
    check(r, 'type', str)
    check(r, 'typeFields', dict)
    check(r['typeFields'], 'correlation', list)
    check(r['typeFields'], 'ipCount', str)
    check(r['typeFields'], 'ipRange', str)
    check(r['typeFields'], 'lastGenerateNessusTime', str)
    check(r['typeFields'], 'lastTrendUpdate', str)
    check(r['typeFields'], 'nessusSchedule', dict)
    check(r['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(r['typeFields']['nessusSchedule'], 'start', str)
    check(r['typeFields']['nessusSchedule'], 'type', str)
    check(r['typeFields'], 'runningNessus', str)
    check(r['typeFields'], 'trendWithRaw', str)
    check(r['typeFields'], 'trendingDays', str)
    check(r, 'vulnCount', str)

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
    r = admin.repositories.edit(int(repository['id']), name='New Name')
    assert isinstance(r, dict)
    check(r, 'createdTime', str)
    check(r, 'dataFormat', str)
    check(r, 'description', str)
    check(r, 'downloadFormat', str)
    check(r, 'id', str)
    check(r, 'lastSyncTime', str)
    check(r, 'lastVulnUpdate', str)
    check(r, 'modifiedTime', str)
    check(r, 'name', str)
    check(r, 'organizations', list)
    check(r, 'remoteID', str, allow_none=True)
    check(r, 'remoteIP', str, allow_none=True)
    check(r, 'running', str)
    check(r, 'type', str)
    check(r, 'typeFields', dict)
    check(r['typeFields'], 'correlation', list)
    check(r['typeFields'], 'ipCount', str)
    check(r['typeFields'], 'ipRange', str)
    check(r['typeFields'], 'lastGenerateNessusTime', str)
    check(r['typeFields'], 'lastTrendUpdate', str)
    check(r['typeFields'], 'nessusSchedule', dict)
    check(r['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(r['typeFields']['nessusSchedule'], 'start', str)
    check(r['typeFields']['nessusSchedule'], 'type', str)
    check(r['typeFields'], 'runningNessus', str)
    check(r['typeFields'], 'trendWithRaw', str)
    check(r['typeFields'], 'trendingDays', str)
    check(r, 'vulnCount', str)

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
def test_repositories_accept_risk_rules_success(admin):
    pass

def test_repositories_recast_risk_rules_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.recast_risk_rules('one')

@pytest.mark.skip(reason='Need VCRed data to test against')
@pytest.mark.vcr()
def test_repositories_recast_risk_rules_success(admin):
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
        int(repository['id']), ip='192.168.0.1')
    assert isinstance(asset_lists, list)
    for a in asset_lists:
        check(a, 'description', str)
        check(a, 'id', str)
        check(a, 'name', str)

def test_repositories_import_repository_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.import_repository('one', 1)

@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'sc_repo.tgz'))
def test_repositories_import_repository_success(admin, datafiles, repository):
    #offline = admin.repositories.create(name='Offline', type='Offline')
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
    r = admin.repositories.device_info(int(repository['id']), dns='server')
    assert isinstance(r, dict)
    check(r, 'biosGUID', str)
    check(r, 'hasCompliance', str)
    check(r, 'hasPassive', str)
    check(r, 'ip', str)
    check(r, 'lastAuthRun', str)
    check(r, 'lastScan', str)
    check(r, 'lastUnauthRun', str)
    check(r, 'links', list)
    check(r, 'macAddress', str)
    check(r, 'mcafeeGUID', str)
    check(r, 'netbiosName', str)
    check(r, 'os', str)
    check(r, 'osCPE', str)
    check(r, 'pluginSet', str)
    check(r, 'pluginSet', str)
    check(r, 'policyName', str)
    check(r, 'repository', dict)
    check(r['repository'], 'description', str)
    check(r['repository'], 'id', str)
    check(r['repository'], 'name', str)
    check(r, 'score', str)
    check(r, 'severityAll', str)
    check(r, 'severityCritical', str)
    check(r, 'severityInfo', str)
    check(r, 'severityLow', str)
    check(r, 'severityMedium', str)
    check(r, 'total', str)
    check(r, 'tpmID', str)
    check(r, 'uniqueness', str)
    check(r, 'uuid', str)

def test_repositories_remote_authorize_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_authorize(1, 'user', 'pass')

def test_repositories_remote_authorize_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_authorize('host', 1, 'pass')

def test_remositories_remote_authorize_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_authorize('host', 'user', 1)

@pytest.mark.skip(reason='No Downstream SC to Test with yet')
def test_repositories_remote_autorize_success(admin):
    pass

def test_repositories_remote_fetch_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.repositories.remote_fetch(1)

@pytest.mark.skip(reason='No Downstream SC to Test with yet')
def test_repositories_remote_fetch_success(admin):
    pass