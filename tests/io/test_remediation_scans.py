'''
test Remediation scans
'''
from pprint import pprint

import pytest
import vcr

from tenable.errors import UnexpectedValueError, NotFoundError
from tests.checker import check, single


@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_create.yaml', record_mode='once')
def remedy_scan(request, api):
    '''
    test to create remediation scan document advanced template
    '''
    # remediation scan
    remedyscan = api.remediationscans.create_remediation_scan(
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


@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_list.yaml', record_mode='once')
def remedy_scanned_list(api):
    '''
    test to get remediation scan list
    '''
    scan_list = api.remediationscans.list_remediation_scan(5, 5, 'scan_creation_date:asc')
    for remediation_scan in scan_list:
        pprint(remediation_scan)
    return scan_list


@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_create_scan_document_template_typeerror.yaml', record_mode='once')
def test_remedyscan_create_scan_document_template_typeerror(api):
    '''
    test to raise exception when type of template param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.remediationscans, 'create_remediation_scan')({'template': 'advanced'})

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_create_scan_document_template_unexpect_err.yaml', record_mode='once')
def test_remedyscan_create_scan_document_template_unexpect_value_err(api):
    '''
    test to raise exception when template param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.remediationscans, '_create_scan_document')({'template': 'nothing_here'})

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_create_scan_document_template.yaml', record_mode='once')
def test_remedyscan_create_scan_socument_template_pass(api):
    '''
    test to create scan document basic template
    '''
    templates = api.policies.templates()
    resp = getattr(api.remediationscans, '_create_scan_document')({'template': 'basic'})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['basic']


@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_create_policies_id.yaml', record_mode='once')
def test_remedyscan_create_scan_document_policies_id_pass(api):
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
@vcr.use_cassette('cassettes/test_remedyscan_create_policies.yaml', record_mode='once')
def test_remedyscan_create_scan_document_policies_name_pass(api):
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

#def test_remedyscan_create_scan_document_targets

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_scan_doc_unexpect_err.yaml', record_mode='once')
def test_remedyscan_create_scan_document_scanner_unexpect_err(api):
    '''
    test to raise exception when scanner param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.remediationscans, '_create_scan_document')({'scanner': 'nothing to see here'})

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_scanner_uuid.yaml', record_mode='once')
def test_remedyscan_create_scan_document_scanner_uuid_pass(api):
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
@vcr.use_cassette('cassettes/test_remedyscan_scanner_name.yaml', record_mode='once')
def test_remedyscan_create_scan_document_scanner_name_pass(api):
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
@vcr.use_cassette('cassettes/test_notemplate_pass.yaml', record_mode='once')
def test_remedyscan_create_no_template_pass(scan):
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
@vcr.use_cassette('cassettes/test_remedyscan_status.yaml', record_mode='once')
def test_remedyscan_status(api):
    '''
    test to check scan status
    '''
    remedyscan =api.remediationscans.create_remediation_scan(
        uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
        name='Create Remediation Scan',
        description='This is first remediation scan created',
        scan_time_window=10,
        targets=['http://127.0.0.1:3000'],
        template='advanced'
    )
    status = api.scans.status(remedyscan['id'])
    single(status, str)

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_timezones.yaml', record_mode='once')
def test_remedyscan_timezones(api):
    '''
    test to get list of allowed timezone strings
    '''
    assert isinstance(api.scans.timezones(), list)

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_success.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_success(api):
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
@vcr.use_cassette('cassettes/test_remedyscan_targets_limit_type_err.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets('nope', 5, targets=['192.168.16.108'])

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_matched_resource_err.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_matched_resource_limit_typeerror(api):
    '''
    test to raise exception when type of matched_resource_limit param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 'nope', targets=['127.0.0.1'])

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_networkuuid_err.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_network_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when network_uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.check_auto_targets(10, 5, network_uuid='nope', targets=['127.0.0.1'])

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_networktype_err.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_network_uuid_typeerror(api):
    '''
    test to raise exception when type of network_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, network_uuid=1, targets=['127.0.0.1'])

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_tags_unexpect_err.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_tags_unexpectedvalueerror(api):
    '''
    test to raise exception when type of any value in tags param
    does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.check_auto_targets(10, 5, tags=['nope'], targets=['127.0.0.1'])

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_tags.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_tags_typeerror(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, tags=1, targets=['127.0.0.1'])

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_targets_type.yaml', record_mode='once')
def test_remedyscan_check_auto_targets_typeerror(api):
    '''
    test to raise exception when type of targets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, targets=1)

@pytest.mark.vcr()
@vcr.use_cassette('cassettes/test_remedyscan_results_datatype.yaml', record_mode='once')
def test_remedyscan_results_datatype(api):
    '''
    test remedy scan results
    '''
    result = api.remediationscans.create_remediation_scan(
        uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
        name='Create Remediation Scan',
        description='This is first remediation scan created',
        scan_time_window=10,
        targets=['http://127.0.0.1:3000'],
        template='advanced'
    )
    assert isinstance(result, dict)
    check(result, 'auto_routed', int)
    check(result, 'container_id', str)
    check(result, 'creation_date', int)
    check(result, 'custom_targets', str)
    check(result, 'default_permissions', int)
    check(result, 'default_permissions', int)
    check(result, 'enabled', bool)
    check(result, 'id', int)
    check(result, 'include_aggregate', bool)
    check(result, 'last_modification_date', int)
    check(result, 'name', str)
    check(result, 'owner', str)
    check(result, 'owner_uuid', str)
    check(result, 'policy_id', int)
    check(result, 'remediation', int)
    check(result, 'scan_time_window', int)
    check(result, 'scanner_uuid', str)
    check(result, 'shared', int)
    check(result, 'sms', str)
    check(result, 'type', str)
    check(result, 'user_permissions', int)

