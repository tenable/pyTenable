'''
test Remediation scans
'''
import uuid
from pprint import pprint
import pytest
from tenable.errors import UnexpectedValueError, NotFoundError
from tests.checker import check, single

@pytest.fixture
def scheduled_scan(request, api):
    '''
    test to create remediation scan document advanced template
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True)
    # remediation scan
    remedyscan =api.remediationscans.create_remediation_scan(
        uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
        name='Create Remediation Scan',
        description='This is first remediation scan created',
        scan_time_window=10,
        targets=['http://127.0.0.1:3000'],
        template='advanced'
    )


    def teardown():
        try:
            api.scans.delete(remedyscan['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return remedyscan


@pytest.fixture
def remediationscanned_list(api):
    '''
    test to check remediation scan list
    '''
    scan_list = api.remediationscans.list_remediation_scan(5, 5, 'scan_creation_date:asc')
    for remediation_scan in scan_list:
        pprint(remediation_scan)
    return scan_list


@pytest.mark.vcr()
def test_remediationscan_create_scan_document_template_typeerror(api):
    '''
    test to raise exception when type of template param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.remediationscans, 'create_remediation_scan')({'template': 'advanced'})

@pytest.mark.vcr()
def test_remediationscan_create_scan_document_template_unexpected_value_error(api):
    '''
    test to raise exception when template param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.remediationscans, '_create_scan_document')({'template': 'nothing_here'})

@pytest.mark.vcr()
def test_remediationscan_create_scan_socument_template_pass(api):
    '''
    test to create scan document basic template
    '''
    templates = api.policies.templates()
    resp = getattr(api.remediationscans, '_create_scan_document')({'template': 'basic'})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['basic']

@pytest.mark.vcr()
def test_remediationscan_create_scan_document_policies_id_pass(api):
    '''
    test to create scan document policy param using id
    '''
    policies = api.policies.list()
    policy = policies[0]
    resp = getattr(api.remediationscans, '_create_scan_document')({'policy': policy['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']

@pytest.mark.vcr()
def test_remediationscan_create_scan_document_policies_name_pass(api):
    '''
    test to create scan document with policy param using name
    '''
    policies = api.policies.list()
    policy = policies[0]
    resp = getattr(api.remediationscans, '_create_scan_document')({'policy': policy['name']})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']

#def test_scan_create_scan_document_targets

@pytest.mark.vcr()
def test_remediationscan_create_scan_document_scanner_unexpectedvalueerror(api):
    '''
    test to raise exception when scanner param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.remediationscans, '_create_scan_document')({'scanner': 'nothing to see here'})

@pytest.mark.vcr()
def test_remediationscan_create_scan_document_scanner_uuid_pass(api):
    '''
    test to create scan document with scanner uuid param
    '''
    scanners = api.scanners.allowed_scanners()
    scanner = scanners[1]
    resp = getattr(api.remediationscans, '_create_scan_document')({'scanner': scanner['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', 'scanner-uuid')
    assert resp['settings']['scanner_id'] == scanner['id']

@pytest.mark.vcr()
def test_remediationscan_create_scan_document_scanner_name_pass(api):
    '''
    test to create scan document with scanner name param
    '''
    scanners = api.scanners.allowed_scanners()
    scanner = scanners[1]
    resp = getattr(api.remediationscans, '_create_scan_document')({'scanner': scanner['name']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', str)
    assert resp['settings']['scanner_id'] == scanner['id']

@pytest.mark.vcr()
def test_remediationscan_create_no_template_pass(scan):
    '''
    test to create scan when no template is provided by user
    '''
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)

@pytest.mark.vcr()
def test_remediationscan_create(api):
    '''
    test to create was scan
    '''
    scan = api.scans.create(template='advanced', name=str(uuid.uuid4()),
        plugins={
            'Authentication & Session': {'status': 'enabled'},
            'Code Execution': {'status': 'enabled'},
            'Component Vulnerability': {'status': 'enabled'},
            'Cross Site Request Forgery': {'status': 'enabled'},
            'Cross Site Scripting': {'status': 'enabled'},
            'Data Exposure': {'status': 'enabled'},
            'File Inclusion': {'status': 'enabled'},
            'Injection': {'status': 'enabled'},
            'Web Applications': {'status': 'enabled'},
            'Web Servers': {'status': 'enabled'},
        },
        assessment_mode='Quick',
        targets=['http://127.0.0.1:3000'],
        was_timeout='00:05:00'
    )
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)

@pytest.mark.vcr()
def test_remediationscan_results(scan_results):
    '''
    test to get scan results
    '''
    assert isinstance(scan_results, dict)
    result = scan_results
    check(result, 'info', dict)
    info = result['info']
    check(info, 'acls', list, allow_none=True)
    for acls in result['info']['acls']:
        check(acls, 'owner', int, allow_none=True)
        check(acls, 'type', str, allow_none=True)
        check(acls, 'permissions', int, allow_none=True)
        check(acls, 'id', int, allow_none=True)
        check(acls, 'name', str, allow_none=True)
        check(acls, 'display_name', str, allow_none=True)
    check(info, 'schedule_uuid', 'scanner-uuid', allow_none=True)
    check(info, 'edit_allowed', bool)
    check(info, 'status', str)
    check(info, 'alt_targets_used', str, allow_none=True)
    check(info, 'scanner_start', int, allow_none=True)
    check(info, 'policy', str, allow_none=True)
    check(info, 'pci-can-upload', bool, allow_none=True)
    check(info, 'scan_start', int, allow_none=True)
    check(info, 'hasaudittrail', bool)
    check(info, 'user_permissions', int)
    check(info, 'folder_id', int, allow_none=True)
    check(info, 'no_target', bool)
    check(info, 'owner', str)
    check(info, 'targets', str, allow_none=True)
    check(info, 'control', bool)
    check(info, 'object_id', int)
    check(info, 'scanner_name', str, allow_none=True)
    check(info, 'uuid', str)
    check(info, 'haskb', bool)
    check(info, 'scanner_end', int, allow_none=True)
    check(info, 'scan_end', int)
    check(info, 'hostcount', int)
    check(info, 'scan_type', str, allow_none=True)
    check(info, 'name', str)

    check(result, 'comphosts', list)
    for comphosts in result['comphosts']:
        check(comphosts, 'totalchecksconsidered', int)
        check(comphosts, 'numchecksconsidered', int)
        check(comphosts, 'scanprogresstotal', int)
        check(comphosts, 'scanprogresscurrent', int)
        check(comphosts, 'host_index', int)
        check(comphosts, 'score', int)
        check(comphosts, 'severitycount', dict)
        check(comphosts, 'progress', str)
        check(comphosts, 'critical', int)
        check(comphosts, 'high', int)
        check(comphosts, 'medium', int)
        check(comphosts, 'low', int)
        check(comphosts, 'info', int)
        check(comphosts, 'host_id', int)
        check(comphosts, 'hostname', str)

    check(result, 'hosts', list)
    for hosts in result['hosts']:
        check(hosts, 'totalchecksconsidered', int)
        check(hosts, 'numchecksconsidered', int)
        check(hosts, 'scanprogresstotal', int)
        check(hosts, 'scanprogresscurrent', int)
        check(hosts, 'host_index', int)
        check(hosts, 'score', int)
        check(hosts, 'severitycount', dict)
        check(hosts, 'progress', str)
        check(hosts, 'critical', int)
        check(hosts, 'high', int)
        check(hosts, 'medium', int)
        check(hosts, 'low', int)
        check(hosts, 'info', int)
        check(hosts, 'host_id', int)
        check(hosts, 'hostname', str)

    check(result, 'notes', list)
    for notes in result['notes']:
        check(notes, 'title', str)
        check(notes, 'message', str)
        check(notes, 'severity', int)

    check(result, 'remediations', dict)
    check(result['remediations'], 'num_hosts', int)
    check(result['remediations'], 'num_cves', int)
    check(result['remediations'], 'num_impacted_hosts', int)
    check(result['remediations'], 'num_remediated_cves', int)
    check(result['remediations'], 'remediations', list)
    for remediation in result['remediations']['remediations']:
        check(remediation, 'value', str)
        check(remediation, 'remediation', str)
        check(remediation, 'hosts', int)
        check(remediation, 'vulns', int)

    check(result, 'vulnerabilities', list)
    for vulnerability in result['vulnerabilities']:
        check(vulnerability, 'count', int)
        check(vulnerability, 'plugin_name', str)
        check(vulnerability, 'vuln_index', int)
        check(vulnerability, 'severity', int)
        check(vulnerability, 'plugin_id', int)
        # Mentioned in the docs, however doesn't appear to show in testing
        #check(vulnerability, 'severity_index', int)
        check(vulnerability, 'plugin_family', str)

    check(result, 'history', list)
    for history in result['history']:
        check(history, 'alt_targets_used', bool)
        check(history, 'scheduler', int)
        check(history, 'status', str)
        check(history, 'type', str, allow_none=True)
        check(history, 'uuid', str)
        check(history, 'last_modification_date', int)
        check(history, 'creation_date', int)
        check(history, 'owner_id', int)
        check(history, 'history_id', int)

    check(result, 'compliance', list)
    for compliance in result['compliance']:
        check(compliance, 'count', int)
        check(compliance, 'plugin_name', str)
        check(compliance, 'vuln_index', int)
        check(compliance, 'severity', int)
        check(compliance, 'plugin_id', int)
        # Mentioned in the docs, however doesn't appear to show in testing
        #check(compliance, 'severity_index', int)
        check(compliance, 'plugin_family', str)

@pytest.mark.vcr()
def test_remediationscan_status(api, scan):
    '''
    test to check scan status
    '''
    status = api.scans.status(scan['id'])
    single(status, str)

@pytest.mark.vcr()
def test_remediationscan_timezones(api):
    '''
    test to get list of allowed timezone strings
    '''
    assert isinstance(api.scans.timezones(), list)

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_success(api):
    '''
    test to evaluates a list of targets and/or tags against
    the scan route configuration of scanner groups
    '''
    resp = api.scans.check_auto_targets(10, 5, targets=['127.0.0.1'])
    assert isinstance(resp, dict)
    check(resp, 'matched_resource_uuids', list)
    check(resp, 'missed_targets', list)
    check(resp, 'total_matched_resource_uuids', int)
    check(resp, 'total_missed_targets', int)

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets('nope', 5, targets=['192.168.16.108'])

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_matched_resource_limit_typeerror(api):
    '''
    test to raise exception when type of matched_resource_limit param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 'nope', targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_network_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when network_uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.check_auto_targets(10, 5, network_uuid='nope', targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_network_uuid_typeerror(api):
    '''
    test to raise exception when type of network_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, network_uuid=1, targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_tags_unexpectedvalueerror(api):
    '''
    test to raise exception when type of any value in tags param
    does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.check_auto_targets(10, 5, tags=['nope'], targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_tags_typeerror(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, tags=1, targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remediationscan_check_auto_targets_targets_typeerror(api):
    '''
    test to raise exception when type of targets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, targets=1)
