"""
test file for testing various scenarios in security center's scans functionality
"""

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError

from ..checker import check


def test_schedule_constructor_type_typeerror(tsc):
    """
    test schedule constructor for 'type' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._schedule_constructor({'type': 1})


def test_schedule_constructor_type_unexpected_value(tsc):
    """
    test schedule constructor for 'type' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.scans._schedule_constructor({'type': 'nothing here'})


def test_schedule_constructor_start_typeerror(tsc):
    """
    test schedule constructor for 'start' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._schedule_constructor({'type': 'ical', 'start': 1, 'repeatRule': ''})


def test_schedule_constructor_rrule_typeerror(tsc):
    """
    test schedule constructor for 'repeat rule' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._schedule_constructor({'type': 'ical', 'start': '', 'repeatRule': 1})


def test_scans_constructor_name_typeerror(tsc):
    """
    test scans constructor for 'name' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(name=1)


def test_scans_constructor_type_typeerror(tsc):
    """
    test scans constructor for 'type' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(type=1)


def test_scans_constructor_type_unexpectedvalueerror(tsc):
    """
    test scans constructor for 'type' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.scans._constructor(type='something')


def test_scans_constructor_description_typeerror(tsc):
    """
    test scans constructor for 'description' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(description=1)


def test_scans_constructor_repo_typeerror(tsc):
    """
    test scans constructor for 'repo' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(repo='nope')


def test_scans_constructor_repo_success(tsc):
    """
    test scans constructor for 'repo' success
    """
    resp = tsc.scans._constructor(repo=1)
    assert resp == {'repository': {'id': 1}}


def test_scans_constructor_scan_zone_typeerror(tsc):
    """
    test scans constructor for 'scan_zone' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(scan_zone='nope')


def test_scans_constructor_scan_zone_success(tsc):
    """
    test scans constructor for 'scan_zone' success
    """
    resp = tsc.scans._constructor(scan_zone=1)
    assert resp == {'zone': {'id': 1}}


def test_scans_constructor_email_complete_typeerror(tsc):
    """
    test scans constructor for 'email complete' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(email_complete='nope')


def test_scans_constructor_email_complete_success(tsc):
    """
    test scans constructor for 'email complete' success
    """
    resp = tsc.scans._constructor(email_complete=True)
    assert resp == {'emailOnFinish': 'true'}


def test_scans_constructor_email_launch_typeerror(tsc):
    """
    test scans constructor for 'email launch' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(email_launch='nope')


def test_scans_constructor_email_launch_success(tsc):
    """
    test scans constructor for 'email launch' success
    """
    resp = tsc.scans._constructor(email_launch=True)
    assert resp == {'emailOnLaunch': 'true'}


def test_scans_constructor_timeout_typeerror(tsc):
    """
    test scans constructor for 'timeout' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(timeout=1)


def test_scans_constructor_inactivity_timeout(tsc):
    """
    Tests inactivity_timeout is mapped correctly in the constructor.
    """
    scan_params = {'inactivity_timeout': 3600, 'policy_id': 1000001}

    scan = tsc.scans._constructor(**scan_params)

    assert 'inactivity_timeout' not in scan
    assert scan['inactivityTimeout'] == '3600'


def test_scans_constructor_timeout_unexpectedvalueerror(tsc):
    """
    test scans constructor for 'timeout' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.scans._constructor(timeout='something')


def test_scans_constructor_timeout_success(tsc):
    """
    test scans constructor for 'timeout' success
    """
    resp = tsc.scans._constructor(timeout='rollover')
    assert resp == {'timeoutAction': 'rollover'}


def test_scans_constructor_host_tracking_typeerror(tsc):
    """
    test scans constructor for 'host tracking' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(host_tracking='something')


def test_scans_constructor_host_tracking_success(tsc):
    """
    test scans constructor for 'host tracking' success
    """
    assert {'dhcpTracking': 'true'} == tsc.scans._constructor(host_tracking=True)


def test_scans_constructor_vhosts_typeerror(tsc):
    """
    test scans constructor for 'vhosts' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(vhosts='nope')


def test_scans_constructor_vhosts_success(tsc):
    """
    test scans constructor for 'vhosts' success
    """
    resp = tsc.scans._constructor(vhosts=True)
    assert resp == {'scanningVirtualHosts': 'true'}


def test_scans_constructor_rollover_typeerror(tsc):
    """
    test scans constructor for 'rollover' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(rollover=1)


def test_scans_constructor_rollover_unexpectedvalueerror(tsc):
    """
    test scans constructor for 'rollover' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.scans._constructor(rollover='something')


def test_scans_constructor_rollover_success(tsc):
    """
    test scans constructor for 'rollover' success
    """
    assert {'rolloverType': 'nextDay'} == tsc.scans._constructor(rollover='nextDay')


def test_scans_constructor_targets_typeerror(tsc):
    """
    test scans constructor for 'targets' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(targets='something')


def test_scans_constructor_targets_success(tsc):
    """
    test scans constructor for 'targets' success
    """
    resp = tsc.scans._constructor(targets=['127.0.0.1', '127.0.0.2'])
    assert resp == {'ipList': '127.0.0.1,127.0.0.2'}


@pytest.mark.skip(reason='No longer checking type for mixed type var')
def test_scans_constructor_max_time_typeerror(tsc):
    """
    test scans constructor for 'max time' type error
    """
    with pytest.raises(ValueError):
        tsc.scans._constructor(max_time='nope')


def test_scans_constructor_max_time_success(tsc):
    """
    test scans constructor for 'max time' success
    """
    resp = tsc.scans._constructor(max_time=3600)
    assert resp == {'maxScanTime': '3600'}


def test_scans_constructor_max_time_zero(tsc):
    """
    test scans constructor for 'max time' zero
    """
    resp = tsc.scans._constructor(max_time=0)
    assert resp == {'maxScanTime': 'unlimited'}
    resp = tsc.scans._constructor(max_time='unlimited')
    assert resp == {'maxScanTime': 'unlimited'}


def test_scans_constructor_schedule_success(tsc):
    """
    test scans constructor for 'schedule' success
    """
    scan = tsc.scans._constructor(schedule={'type': 'ical', 'start': ''})
    assert {'schedule': {'type': 'ical', 'start': ''}} == scan


def test_scans_constructor_auto_mitigation_typeerror(tsc):
    """
    test scans constructor for 'auto mitigation' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(auto_mitigation='nope')


def test_scans_constructor_auto_mitigation_success(tsc):
    """
    test scans constructor for 'auto mitigation' success
    """
    resp = tsc.scans._constructor(auto_mitigation=True)
    assert resp == {'classifyMitigatedAge': 'true'}


def test_scans_constructor_reports_typeerror_base(tsc):
    """
    test scans constructor for 'reports' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(reports='nope')


def test_scans_constructor_reports_typeerror_id(tsc):
    """
    test scans constructor reports for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(reports=[{'id': 'nope', 'reportSource': 'cumulative'}])


def test_scans_constructor_reports_typeerror_report_source(tsc):
    """
    test scans constructor reports for 'report source' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(reports=[{'id': 1, 'reportSource': 1}])


def test_scans_constructor_reports_unexpectedvalueerror_reportsource(tsc):
    """
    test scans constructor reports for 'report source' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.scans._constructor(reports=[{'id': 1, 'reportSource': 'something'}])


def test_scans_constructor_reports_success(tsc):
    """
    test scans constructor reports for success
    """
    resp = tsc.scans._constructor(reports=[{'id': 1, 'reportSource': 'cumulative'}])
    assert resp == {'reports': [{'id': 1, 'reportSource': 'cumulative'}]}


def test_scans_constructor_asset_lists_typeerror(tsc):
    """
    test scans constructor for 'asset lists' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(asset_lists=1)


def test_scans_constructor_asset_list_id_typeerror(tsc):
    """
    test scans constructor for 'asset list id' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(
            asset_lists=[
                'nope',
            ]
        )


def test_scans_constructor_asset_lists_success(tsc):
    """
    test scans constructor for 'asset lists' success
    """
    resp = tsc.scans._constructor(asset_lists=[1, 2])
    assert resp == {'assets': [{'id': 1}, {'id': 2}]}


def test_scans_constructor_creds_typeerror(tsc):
    """
    test scans constructor for 'creds' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(creds=1)


def test_scans_constructor_creds_id_typeerror(tsc):
    """
    test scans constructor for 'creds id' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(creds=['nope'])


def test_scans_constructor_creds_success(tsc):
    """
    test scans constructor for creds success
    """
    resp = tsc.scans._constructor(creds=[1, 2])
    assert resp == {'credentials': [{'id': 1}, {'id': 2}]}


def test_scans_constructor_plugin_id_success(tsc):
    """
    test scans constructor for plugin id success
    """
    resp = tsc.scans._constructor(policy_id=19506)
    assert resp == {'type': 'policy', 'policy': {'id': 19506}}


def test_scans_constructor_policy_id_typeerror(tsc):
    """
    test scans constructor for 'policy id' type error
    """
    with pytest.raises(TypeError):
        tsc.scans._constructor(policy_id='nope')


def test_scans_constructor_policy_id_success(tsc):
    """
    test scans constructor for 'policy id' success
    """
    resp = tsc.scans._constructor(policy_id=1)
    assert resp == {'type': 'policy', 'policy': {'id': 1}}


@pytest.fixture
def scan():
    """
    test fixture for scan
    """
    return {
        'id': '9',
        'name': 'Example Scan',
        'description': '',
        'ipList': '127.0.0.1',
        'type': 'policy',
        'dhcpTracking': 'false',
        'classifyMitigatedAge': '0',
        'emailOnLaunch': 'false',
        'emailOnFinish': 'false',
        'timeoutAction': 'import',
        'scanningVirtualHosts': 'false',
        'rolloverType': 'template',
        'status': '0',
        'createdTime': '1545176959',
        'modifiedTime': '1545176959',
        'maxScanTime': '3600',
        'numDependents': '0',
        'canUse': 'true',
        'canManage': 'true',
    }


@responses.activate
def test_scans_list(tsc):
    """
    test scans list for success
    """
    responses.get(
        'https://nourl/rest/scan',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {
                        'id': '1',
                        'name': 'Daily Internal Scan',
                        'description': '',
                        'status': '0',
                    },
                    {
                        'id': '2',
                        'name': 'Daily Internal Scan',
                        'description': '',
                        'status': '0',
                    },
                ],
                'manageable': [
                    {
                        'id': '1',
                        'name': 'Daily Internal Scan',
                        'description': '',
                        'status': '0',
                    },
                    {
                        'id': '2',
                        'name': 'Daily Internal Scan',
                        'description': '',
                        'status': '0',
                    },
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177468,
        },
    )
    scans = tsc.scans.list()
    for scan in scans['usable']:
        assert isinstance(scan, dict)
        check(scan, 'id', str)
        check(scan, 'name', str)
        check(scan, 'description', str)
        check(scan, 'status', str)


@responses.activate
def test_scans_list_for_fields(tsc):
    """
    test scans list success for fields
    """
    responses.get(
        'https://nourl/rest/scan',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {'id': '1', 'name': 'Daily Internal Scan'},
                    {'id': '2', 'name': 'Daily Internal Scan'},
                ],
                'manageable': [
                    {'id': '1', 'name': 'Daily Internal Scan'},
                    {'id': '2', 'name': 'Daily Internal Scan'},
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177468,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name'})],
    )
    scans = tsc.scans.list(fields=['id', 'name'])
    for scan in scans['usable']:
        assert isinstance(scan, dict)
        check(scan, 'id', str)
        check(scan, 'name', str)


@responses.activate
def test_scans_details(tsc, scan):
    """
    test scans details for success
    """
    responses.get(
        'https://nourl/rest/scan/9',
        json={
            'type': 'regular',
            'response': {
                'id': '28',
                'name': 'Example Scan',
                'description': '',
                'ipList': '127.0.0.1',
                'type': 'policy',
                'dhcpTracking': 'false',
                'classifyMitigatedAge': '0',
                'emailOnLaunch': 'false',
                'emailOnFinish': 'false',
                'timeoutAction': 'import',
                'scanningVirtualHosts': 'false',
                'rolloverType': 'template',
                'status': '0',
                'createdTime': '1545177469',
                'modifiedTime': '1545177469',
                'maxScanTime': '3600',
                'reports': [],
                'assets': [],
                'numDependents': '0',
                'schedule': {
                    'id': '76',
                    'objectType': 'scan',
                    'type': 'template',
                    'start': '',
                    'repeatRule': '',
                    'nextRun': 0,
                },
                'policy': {
                    'id': '1000001',
                    'context': '',
                    'name': 'Full Safe Scan',
                    'description': '',
                    'tags': '',
                },
                'policyPrefs': [],
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
                'canUse': 'true',
                'canManage': 'true',
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1545177469,
        },
    )
    scan = tsc.scans.details(int(scan['id']))
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


@responses.activate
def test_scans_details_for_fields(tsc, scan):
    """
    test scans details success for fields
    """
    responses.get(
        'https://nourl/rest/scan/9',
        json={
            'type': 'regular',
            'response': {'id': '28', 'name': 'Example Scan', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177469,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    scan_details = tsc.scans.details(
        int(scan['id']), fields=['id', 'name', 'description']
    )
    assert isinstance(scan_details, dict)
    check(scan_details, 'id', str)
    check(scan_details, 'name', str)
    check(scan_details, 'description', str)


@responses.activate
def test_scans_create(tsc):
    """
    test scans create for success
    """
    responses.post(
        'https://nourl/rest/scan',
        json={
            'type': 'regular',
            'response': {
                'id': '9',
                'name': 'Example Scan',
                'description': '',
                'ipList': '127.0.0.1',
                'type': 'policy',
                'dhcpTracking': 'false',
                'classifyMitigatedAge': '0',
                'emailOnLaunch': 'false',
                'emailOnFinish': 'false',
                'timeoutAction': 'import',
                'scanningVirtualHosts': 'false',
                'rolloverType': 'template',
                'status': '0',
                'createdTime': '1545176959',
                'modifiedTime': '1545176959',
                'maxScanTime': '3600',
                'reports': [],
                'assets': [],
                'numDependents': '0',
                'schedule': {
                    'id': '57',
                    'objectType': 'scan',
                    'type': 'template',
                    'start': '',
                    'repeatRule': '',
                    'nextRun': 0,
                },
                'policy': {
                    'id': '1000001',
                    'context': '',
                    'name': 'Full Safe Scan',
                    'description': '',
                    'tags': '',
                },
                'policyPrefs': [],
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
                'canUse': 'true',
                'canManage': 'true',
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1545176959,
        },
    )
    scan = tsc.scans.create(
        'Example Scan',
        1,
        schedule_type='template',
        targets=['127.0.0.1'],
        policy_id=1000001,
    )
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


@responses.activate
def test_scans_create_plugin(tsc):
    """
    test scans create plugin for success
    """
    responses.post(
        'https://nourl/rest/scan',
        json={
            'type': 'regular',
            'response': {
                'id': '9',
                'name': 'Example Scan',
                'description': '',
                'ipList': '127.0.0.1',
                'type': 'plugin',
                'dhcpTracking': 'false',
                'classifyMitigatedAge': '0',
                'emailOnLaunch': 'false',
                'emailOnFinish': 'false',
                'timeoutAction': 'import',
                'scanningVirtualHosts': 'false',
                'rolloverType': 'template',
                'status': '0',
                'createdTime': '1545176959',
                'modifiedTime': '1545176959',
                'maxScanTime': '3600',
                'numDependents': '0',
                'canUse': 'true',
                'canManage': 'true',
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1545176959,
        },
    )
    responses.delete(
        'https://nourl/rest/scan/9',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177470,
        },
    )
    scan = tsc.scans.create(
        'Example Scan 9',
        9,
        schedule_type='template',
        targets=['127.0.0.1'],
        plugin_id=1000001,
    )
    assert isinstance(scan, dict)
    check(scan, 'id', str)
    check(scan, 'name', str)
    check(scan, 'description', str)
    tsc.scans.delete(int(scan['id']))


@responses.activate
def test_scans_edit(tsc, scan):
    """
    test scans edit for success
    """
    responses.patch(
        'https://nourl/rest/scan/9',
        json={
            'type': 'regular',
            'response': {
                'id': '30',
                'name': 'Edited Example Scan',
                'description': '',
                'ipList': '127.0.0.1',
                'type': 'policy',
                'dhcpTracking': 'false',
                'classifyMitigatedAge': '0',
                'emailOnLaunch': 'false',
                'emailOnFinish': 'false',
                'timeoutAction': 'import',
                'scanningVirtualHosts': 'false',
                'rolloverType': 'template',
                'status': '0',
                'createdTime': '1545177471',
                'modifiedTime': '1545177472',
                'maxScanTime': '3600',
                'reports': [],
                'assets': [],
                'numDependents': '0',
                'schedule': {
                    'id': '78',
                    'objectType': 'scan',
                    'type': 'template',
                    'start': '',
                    'repeatRule': '',
                    'nextRun': 0,
                },
                'policy': {
                    'id': '1000001',
                    'context': '',
                    'name': 'Full Safe Scan',
                    'description': '',
                    'tags': '',
                },
                'policyPrefs': [],
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
                'canUse': 'true',
                'canManage': 'true',
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1545177471,
        },
    )
    scan = tsc.scans.edit(int(scan['id']), name='Edited Example Scan')
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


@responses.activate
def test_scans_delete(scan, tsc):
    """
    test scans delete for success
    """
    responses.delete(
        'https://nourl/rest/scan/9',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177474,
        },
    )
    tsc.scans.delete(int(scan['id']))


@responses.activate
def test_scans_copy(scan, tsc):
    """
    test scans copy for success
    """
    responses.post(
        'https://nourl/rest/scan/9/copy',
        json={
            'type': 'regular',
            'response': {
                'scan': {
                    'id': '33',
                    'name': 'scan_copy',
                    'description': '',
                    'ipList': '127.0.0.1',
                    'type': 'policy',
                    'dhcpTracking': 'false',
                    'classifyMitigatedAge': '0',
                    'emailOnLaunch': 'false',
                    'emailOnFinish': 'false',
                    'timeoutAction': 'import',
                    'scanningVirtualHosts': 'false',
                    'rolloverType': 'template',
                    'status': '0',
                    'createdTime': '1545177475',
                    'modifiedTime': '1545177475',
                    'maxScanTime': '3600',
                    'reports': [],
                    'assets': [],
                    'numDependents': '0',
                    'schedule': {
                        'id': '81',
                        'objectType': 'scan',
                        'type': 'template',
                        'start': '',
                        'repeatRule': '',
                        'nextRun': 0,
                    },
                    'policy': {
                        'id': '1000001',
                        'context': '',
                        'name': 'Full Safe Scan',
                        'description': '',
                        'tags': '',
                    },
                    'policyPrefs': [],
                    'repository': {'id': '1', 'name': 'Default', 'description': ''},
                    'canUse': 'true',
                    'canManage': 'true',
                    'ownerGroup': {
                        'id': '0',
                        'name': 'Full Access',
                        'description': 'Full Access group',
                    },
                    'creator': {
                        'id': '2',
                        'username': 'api',
                        'firstname': 'api',
                        'lastname': 'user',
                    },
                    'owner': {
                        'id': '1',
                        'username': 'steve',
                        'firstname': 'Steve',
                        'lastname': 'McGrath',
                    },
                }
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1545177475,
        },
    )
    responses.delete(
        'https://nourl/rest/scan/33',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177475,
        },
    )
    scan = tsc.scans.copy(int(scan['id']), 'scan_copy', 1)
    tsc.scans.delete(int(scan['id']))
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


@responses.activate
def test_scans_launch(tsc, scan):
    """
    test scans launch for success
    """
    responses.post(
        'https://nourl/rest/scan/9/launch',
        json={
            'type': 'regular',
            'response': {
                'scanID': '34',
                'scanResult': {
                    'initiatorID': '2',
                    'ownerID': '2',
                    'scanID': '34',
                    'resultsSyncID': -1,
                    'jobID': '3784',
                    'repositoryID': '1',
                    'name': 'Example Scan',
                    'description': '',
                    'details': 'Full Safe Scan',
                    'status': 'Queued',
                    'downloadFormat': 'v2',
                    'dataFormat': 'IPv4',
                    'resultType': 'active',
                    'id': '8',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545177477,
        },
    )
    launch = tsc.scans.launch(
        int(scan['id']), diagnostic_target='target', diagnostic_password='password'
    )
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
