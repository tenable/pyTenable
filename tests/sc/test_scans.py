import pytest
from ..checker import check
from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception


def test_schedule_constructor_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._schedule_constructor({'type': 1})


def test_schedule_constructor_type_unexpected_value(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scans._schedule_constructor({'type': 'nothing here'})


def test_schedule_constructor_start_typeerror(sc):
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


def test_scans_constructor_host_tracking_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scans._constructor(host_tracking='something')


def test_scans_constructor_host_tracking_success(sc):
    assert {'dhcpTracking': 'true'} == sc.scans._constructor(host_tracking=True)


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


def test_scans_constructor_rollover_success(sc):
    assert {'rolloverType': 'nextDay'} == sc.scans._constructor(rollover='nextDay')


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


def test_scans_constructor_max_time_zero(sc):
    resp = sc.scans._constructor(max_time=0)
    assert resp == {'maxScanTime': 'unlimited'}


def test_scans_constructor_schedule_success(sc):
    scan = sc.scans._constructor(schedule={'type': 'ical', 'start': ''})
    assert {'schedule': {'type': 'ical', 'start': ''}} == scan


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
        sc.scans._constructor(asset_lists=['nope', ])



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
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return scan


@pytest.mark.vcr()
def test_scans_list(sc):
    scans = sc.scans.list()
    for scan in scans['usable']:
        assert isinstance(scan, dict)
        check(scan, 'id', str)
        check(scan, 'name', str)
        check(scan, 'description', str)
        check(scan, 'status', str)


@pytest.mark.vcr()
def test_scans_list_for_fields(sc):
    scans = sc.scans.list(fields=['id', 'name'])
    for scan in scans['usable']:
        assert isinstance(scan, dict)
        check(scan, 'id', str)
        check(scan, 'name', str)


@pytest.mark.vcr()
def test_scans_details(sc, scan):
    scan = sc.scans.details(int(scan['id']))
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
def test_scans_details_for_fields(sc, scan):
    scan_details = sc.scans.details(int(scan['id']), fields=['id', 'name', 'description'])
    assert isinstance(scan_details, dict)
    check(scan_details, 'id', str)
    check(scan_details, 'name', str)
    check(scan_details, 'description', str)


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
def test_scans_create_plugin(sc):
    scan = sc.scans.create('Example Scan 9', 9,
                           schedule_type='template',
                           targets=['127.0.0.1'],
                           plugin_id=1000001)
    assert isinstance(scan, dict)
    check(scan, 'id', str)
    check(scan, 'name', str)
    check(scan, 'description', str)
    sc.scans.delete(int(scan['id']))


@pytest.mark.vcr()
def test_scans_edit(sc, scan):
    scan = sc.scans.edit(int(scan['id']), name='Edited Example Scan')
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
def test_scans_delete(scan, sc):
    sc.scans.delete(int(scan['id']))


@pytest.mark.vcr()
def test_scans_copy(scan, sc):
    scan = sc.scans.copy(int(scan['id']), 'scan_copy', 1)
    sc.scans.delete(int(scan['id']))
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
def test_scans_launch(sc, scan):
    launch = sc.scans.launch(int(scan['id']), diagnostic_target='target', diagnostic_password='password')
    assert isinstance(launch, dict)
    check(launch, 'scanID', str)
    check(launch, 'scanResult', dict)
    check(launch['scanResult'], 'initiatorID', str)
    check(launch['scanResult'], 'ownerID', str)
    check(launch['scanResult'], 'scanID', str)
    check(launch['scanResult'], 'repositoryID', str)
    check(launch['scanResult'], 'jobID', str)
    check(launch['scanResult'], 'name', str)
    check(launch['scanResult'], 'description', str, allow_none=True)
    check(launch['scanResult'], 'details', str)
    check(launch['scanResult'], 'status', str)
    check(launch['scanResult'], 'downloadFormat', str)
    check(launch['scanResult'], 'dataFormat', str)
    check(launch['scanResult'], 'id', str)
