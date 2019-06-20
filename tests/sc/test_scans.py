from tenable.errors import *
from ..checker import check, single
import pytest

def test_schedule_constructor_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._schedule_constructor({'type': 1})

def test_schedule_constructor_type_unexpected_value(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._schedule_constructor({'type': 'nothing here'})

def test_schdeule_constructor_start_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._schedule_constructor(
            {'type': 'ical', 'start': 1, 'repeatRule': ''})

def test_schedule_constructor_rrule_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._schedule_constructor(
            {'type': 'ical', 'start': '', 'repeatRule': 1})

def test_scans_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(name=1)

def test_scans_constructor_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(type=1)

def test_scans_constructor_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._constructor(type='something')

def test_scans_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(description=1)

def test_scans_constructor_repo_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(repo='nope')

def test_scans_constructor_repo_success(sc):
    resp = sc.scans._constructor(repo=1)
    assert resp == {'repository': {'id': 1}}

def test_scans_constructor_scan_zone_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(scan_zone='nope')

def test_scans_constructor_scan_zone_success(sc):
    resp = sc.scans._constructor(scan_zone=1)
    assert resp == {'zone': {'id': 1}}

def test_scans_constructor_email_complete_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(email_complete='nope')

def test_scans_constructor_email_complete_success(sc):
    resp = sc.scans._constructor(email_complete=True)
    assert resp == {'emailOnFinish': 'true'}

def test_scans_constructor_email_launch_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(email_launch='nope')

def test_scans_constructor_email_launch_success(sc):
    resp = sc.scans._constructor(email_launch=True)
    assert resp == {'emailOnLaunch': 'true'}

def test_scans_constructor_timeout_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(timeout=1)

def test_scans_constructor_timeout_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._constructor(timeout='something')

def test_scans_constructor_timeout_success(sc):
    resp = sc.scans._constructor(timeout='rollover')
    assert resp == {'timeoutAction': 'rollover'}

def test_scans_constructor_vhosts_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(vhosts='nope')

def test_scans_constructor_vhosts_success(sc):
    resp = sc.scans._constructor(vhosts=True)
    assert resp == {'scanningVirtualHosts': 'true'}

def test_scans_constructor_rollover_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(rollover=1)

def test_scans_constructor_rollover_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._constructor(rollover='something')

def test_scans_constructor_targets_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(targets='something')

def test_scans_constructor_targets_success(sc):
    resp = sc.scans._constructor(targets=['127.0.0.1', '127.0.0.2'])
    assert resp == {'ipList': '127.0.0.1,127.0.0.2'}

def test_scans_constructor_max_time_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(max_time='nope')

def test_scans_constructor_max_time_success(sc):
    resp = sc.scans._constructor(max_time=3600)
    assert resp == {'maxScanTime': '3600'}

def test_scans_constructor_auto_mitigation_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(auto_mitigation='nope')

def test_scans_constructor_auto_mitigation_success(sc):
    resp = sc.scans._constructor(auto_mitigation=True)
    assert resp == {'classifyMitigatedAge': 'true'}

def test_scans_constructor_reports_typeerror_base(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(reports='nope')

def test_scans_constructor_reports_typeerror_id(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(reports=[
            {'id': 'nope', 'reportSource': 'cumulative'}])

def test_scans_constructor_reports_typeerror_report_source(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(reports=[
            {'id': 1, 'reportSource': 1}])

def test_scans_constructor_reports_unexpectedvalueerror_reportsource(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._constructor(reports=[
            {'id': 1, 'reportSource': 'something'}])

def test_scans_constructor_reports_success(sc):
    resp = sc.scans._constructor(reports=[
        {'id': 1, 'reportSource': 'cumulative'}])
    assert resp == {'reports': [{'id': 1, 'reportSource': 'cumulative'}]}

def test_scans_constructor_asset_lists_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(asset_lists=1)

def test_scans_constructor_asset_list_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(asset_lists=['nope',])

def test_scans_constructor_asset_lists_success(sc):
    resp = sc.scans._constructor(asset_lists=[1, 2])
    assert resp == {'assets': [{'id': 1}, {'id': 2}]}

def test_scans_constructor_creds_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(creds=1)

def test_scans_constructor_creds_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(creds=['nope'])

def test_scans_constructor_creds_success(sc):
    resp = sc.scans._constructor(creds=[1, 2])
    assert resp == {'credentials': [{'id': 1}, {'id': 2}]}

def test_scans_constructor_both_policu_and_plugin_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._constructor(plugin_id=1, policy_id=1)

def test_scans_constructor_plugin_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(plugin_id='nope')

def test_scans_constructor_plugin_id_success(sc):
    resp = sc.scans._constructor(plugin_id=19506)
    assert resp == {'type': 'plugin', 'pluginID': 19506}

def test_scans_constructor_policy_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(policy_id='nope')

def test_scans_constructor_policy_id_success(sc):
    resp = sc.scans._constructor(policy_id=1)
    assert resp == {'type': 'policy', 'policy': {'id': 1}}


@pytest.fixture
def scan(request, sc, vcr):
    with vcr.use_cassette('sc_scans_create'):
        scan = sc.scans.create('Example Scan', 1,
            schedule_type='template',
            targets=['127.0.0.1'],
            policy_id=1000001)
    def teardown():
        try:
            sc.scans.delete(int(scan['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return scan

@pytest.mark.vcr()
def test_scans_list(sc):
    scans = sc.scans.list()
    for s in scans['usable']:
        assert isinstance(s, dict)
        check(s, 'id', str)
        check(s, 'name', str)
        check(s, 'description', str)
        check(s, 'status', str)

@pytest.mark.vcr()
def test_scans_details(sc, scan):
    s = sc.scans.details(int(scan['id']))
    assert isinstance(s, dict)
    check(s, 'id', str)
    check(s, 'name', str)
    check(s, 'description', str)
    check(s, 'ipList', str)
    check(s, 'type', str)
    check(s, 'dhcpTracking', str)
    check(s, 'classifyMitigatedAge', str)
    check(s, 'emailOnLaunch', str)
    check(s, 'emailOnFinish', str)
    check(s, 'timeoutAction', str)
    check(s, 'scanningVirtualHosts', str)
    check(s, 'rolloverType', str)
    check(s, 'status', str)
    check(s, 'createdTime', str)
    check(s, 'modifiedTime', str)
    check(s, 'reports', list)
    check(s, 'assets', list)
    check(s, 'numDependents', str)
    check(s, 'schedule', dict)
    check(s['schedule'], 'id', str)
    check(s['schedule'], 'type', str)
    check(s['schedule'], 'start', str)
    check(s['schedule'], 'repeatRule', str)
    check(s['schedule'], 'nextRun', int)
    check(s, 'policy', dict)
    check(s['policy'], 'id', str)
    check(s['policy'], 'name', str)
    check(s['policy'], 'description', str)
    check(s, 'policyPrefs', list)
    check(s, 'repository', dict)
    check(s['repository'], 'id', str)
    check(s['repository'], 'name', str)
    check(s['repository'], 'description', str)
    check(s, 'ownerGroup', dict)
    check(s['ownerGroup'], 'id', str)
    check(s['ownerGroup'], 'name', str)
    check(s['ownerGroup'], 'description', str)
    check(s, 'creator', dict)
    check(s['creator'], 'id', str)
    check(s['creator'], 'username', str)
    check(s['creator'], 'firstname', str)
    check(s['creator'], 'lastname', str)
    check(s, 'owner', dict)
    check(s['owner'], 'id', str)
    check(s['owner'], 'username', str)
    check(s['owner'], 'firstname', str)
    check(s['owner'], 'lastname', str)

@pytest.mark.vcr()
def test_scans_create(scan):
    assert isinstance(scan, dict)
    check(scan, 'id', str)
    check(scan, 'name', str)
    check(scan, 'description', str)
    check(scan, 'ipList', str)
    check(scan, 'type', str)
    check(scan, 'dhcpTracking', str)
    check(scan, 'classifyMitigatedAge', str)
    check(scan, 'emailOnLaunch', str)
    check(scan, 'emailOnFinish', str)
    check(scan, 'timeoutAction', str)
    check(scan, 'scanningVirtualHosts', str)
    check(scan, 'rolloverType', str)
    check(scan, 'status', str)
    check(scan, 'createdTime', str)
    check(scan, 'modifiedTime', str)
    check(scan, 'reports', list)
    check(scan, 'assets', list)
    check(scan, 'numDependents', str)
    check(scan, 'schedule', dict)
    check(scan['schedule'], 'id', str)
    check(scan['schedule'], 'type', str)
    check(scan['schedule'], 'start', str)
    check(scan['schedule'], 'repeatRule', str)
    check(scan['schedule'], 'nextRun', int)
    check(scan, 'policy', dict)
    check(scan['policy'], 'id', str)
    check(scan['policy'], 'name', str)
    check(scan['policy'], 'description', str)
    check(scan, 'policyPrefs', list)
    check(scan, 'repository', dict)
    check(scan['repository'], 'id', str)
    check(scan['repository'], 'name', str)
    check(scan['repository'], 'description', str)
    check(scan, 'ownerGroup', dict)
    check(scan['ownerGroup'], 'id', str)
    check(scan['ownerGroup'], 'name', str)
    check(scan['ownerGroup'], 'description', str)
    check(scan, 'creator', dict)
    check(scan['creator'], 'id', str)
    check(scan['creator'], 'username', str)
    check(scan['creator'], 'firstname', str)
    check(scan['creator'], 'lastname', str)
    check(scan, 'owner', dict)
    check(scan['owner'], 'id', str)
    check(scan['owner'], 'username', str)
    check(scan['owner'], 'firstname', str)
    check(scan['owner'], 'lastname', str)

@pytest.mark.vcr()
def test_scans_edit(sc, scan):
    m = sc.scans.edit(int(scan['id']), name='Edited Example Scan')
    assert isinstance(m, dict)
    check(m, 'id', str)
    check(m, 'name', str)
    check(m, 'description', str)
    check(m, 'ipList', str)
    check(m, 'type', str)
    check(m, 'dhcpTracking', str)
    check(m, 'classifyMitigatedAge', str)
    check(m, 'emailOnLaunch', str)
    check(m, 'emailOnFinish', str)
    check(m, 'timeoutAction', str)
    check(m, 'scanningVirtualHosts', str)
    check(m, 'rolloverType', str)
    check(m, 'status', str)
    check(m, 'createdTime', str)
    check(m, 'modifiedTime', str)
    check(m, 'reports', list)
    check(m, 'assets', list)
    check(m, 'numDependents', str)
    check(m, 'schedule', dict)
    check(m['schedule'], 'id', str)
    check(m['schedule'], 'type', str)
    check(m['schedule'], 'start', str)
    check(m['schedule'], 'repeatRule', str)
    check(m['schedule'], 'nextRun', int)
    check(m, 'policy', dict)
    check(m['policy'], 'id', str)
    check(m['policy'], 'name', str)
    check(m['policy'], 'description', str)
    check(m, 'policyPrefs', list)
    check(m, 'repository', dict)
    check(m['repository'], 'id', str)
    check(m['repository'], 'name', str)
    check(m['repository'], 'description', str)
    check(m, 'ownerGroup', dict)
    check(m['ownerGroup'], 'id', str)
    check(m['ownerGroup'], 'name', str)
    check(m['ownerGroup'], 'description', str)
    check(m, 'creator', dict)
    check(m['creator'], 'id', str)
    check(m['creator'], 'username', str)
    check(m['creator'], 'firstname', str)
    check(m['creator'], 'lastname', str)
    check(m, 'owner', dict)
    check(m['owner'], 'id', str)
    check(m['owner'], 'username', str)
    check(m['owner'], 'firstname', str)
    check(m['owner'], 'lastname', str)

@pytest.mark.vcr()
def test_scans_delete(scan, sc):
    sc.scans.delete(int(scan['id']))

@pytest.mark.vcr()
def test_scans_copy(scan, sc):
    c = sc.scans.copy(int(scan['id']), 'scan_copy', 1)
    sc.scans.delete(int(c['id']))
    assert isinstance(c, dict)
    check(c, 'id', str)
    check(c, 'name', str)
    check(c, 'description', str)
    check(c, 'ipList', str)
    check(c, 'type', str)
    check(c, 'dhcpTracking', str)
    check(c, 'classifyMitigatedAge', str)
    check(c, 'emailOnLaunch', str)
    check(c, 'emailOnFinish', str)
    check(c, 'timeoutAction', str)
    check(c, 'scanningVirtualHosts', str)
    check(c, 'rolloverType', str)
    check(c, 'status', str)
    check(c, 'createdTime', str)
    check(c, 'modifiedTime', str)
    check(c, 'reports', list)
    check(c, 'assets', list)
    check(c, 'numDependents', str)
    check(c, 'schedule', dict)
    check(c['schedule'], 'id', str)
    check(c['schedule'], 'type', str)
    check(c['schedule'], 'start', str)
    check(c['schedule'], 'repeatRule', str)
    check(c['schedule'], 'nextRun', int)
    check(c, 'policy', dict)
    check(c['policy'], 'id', str)
    check(c['policy'], 'name', str)
    check(c['policy'], 'description', str)
    check(c, 'policyPrefs', list)
    check(c, 'repository', dict)
    check(c['repository'], 'id', str)
    check(c['repository'], 'name', str)
    check(c['repository'], 'description', str)
    check(c, 'ownerGroup', dict)
    check(c['ownerGroup'], 'id', str)
    check(c['ownerGroup'], 'name', str)
    check(c['ownerGroup'], 'description', str)
    check(c, 'creator', dict)
    check(c['creator'], 'id', str)
    check(c['creator'], 'username', str)
    check(c['creator'], 'firstname', str)
    check(c['creator'], 'lastname', str)
    check(c, 'owner', dict)
    check(c['owner'], 'id', str)
    check(c['owner'], 'username', str)
    check(c['owner'], 'firstname', str)
    check(c['owner'], 'lastname', str)

@pytest.mark.vcr()
def test_scans_launch(sc, scan):
    i = sc.scans.launch(int(scan['id']))
    assert isinstance(i, dict)
    check(i, 'scanID', str)
    check(i, 'scanResult', dict)
    check(i['scanResult'], 'initiatorID', str)
    check(i['scanResult'], 'ownerID', str)
    check(i['scanResult'], 'scanID', str)
    check(i['scanResult'], 'repositoryID', str)
    check(i['scanResult'], 'jobID', str)
    check(i['scanResult'], 'name', str)
    check(i['scanResult'], 'description', str, allow_none=True)
    check(i['scanResult'], 'details', str)
    check(i['scanResult'], 'status', str)
    check(i['scanResult'], 'downloadFormat', str)
    check(i['scanResult'], 'dataFormat', str)
    check(i['scanResult'], 'id', str)