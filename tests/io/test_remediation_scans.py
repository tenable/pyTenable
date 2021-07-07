'''
test Remediation scans
'''
from pprint import pprint
import pytest
from tenable.errors import UnexpectedValueError, NotFoundError
from tests.checker import check, single

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
		targets=['http://127.0.0.1'],
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
def test_remedy_scanned_list(api):
	'''
	test to check remediation scan list
	'''
	scan_list = api.remediationscans.list_remediation_scan(5, 0, 'scan_creation_date:asc')
	for remediation_scan in scan_list:
		check(remediation_scan, 'control', bool)
		check(remediation_scan, 'creation_date', int)
		check(remediation_scan, 'enabled', bool)
		check(remediation_scan, 'id', int)
		check(remediation_scan, 'last_modification_date', int)
		check(remediation_scan, 'name', str)
		check(remediation_scan, 'owner', str)
		check(remediation_scan, 'permissions', int)
		check(remediation_scan, 'policy_id', int)
		check(remediation_scan, 'read', bool)
		check(remediation_scan, 'remediation', int)
		check(remediation_scan, 'scan_creation_date', int)
		check(remediation_scan, 'schedule_uuid', str)
		check(remediation_scan, 'shared', bool)
		check(remediation_scan, 'status', str)
		check(remediation_scan, 'user_permissions', int)


@pytest.mark.vcr()
def test_remedyscan_create_scan_document_template_typeerror(api):
	'''
	test to raise exception when type of template param does not match the expected type.
	'''
	with pytest.raises(TypeError):
		getattr(api.remediationscans, 'create_remediation_scan')({'template': 'advanced'})

@pytest.mark.vcr()
def test_remedyscan_create_scan_document_template_unexpected_value_error(api):
	'''
	test to raise exception when template param value does not match the choices.
	'''
	with pytest.raises(UnexpectedValueError):
		getattr(api.remediationscans, '_create_scan_document')({'template': 'nothing_here'})

@pytest.mark.vcr()
def test_remedyscan_create_scan_document_template_pass(api):
	'''
	test to create scan document basic template
	'''
	templates = api.policies.templates()
	resp = getattr(api.remediationscans, '_create_scan_document')({'template': 'basic'})
	assert isinstance(resp, dict)
	check(resp, 'uuid', 'scanner-uuid')
	assert resp['uuid'] == templates['basic']

@pytest.mark.vcr()
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
def test_remedyscan_create_scan_document_scanner_unexpectedvalueerror(api):
	'''
	test to raise exception when scanner param value does not match the choices.
	'''
	with pytest.raises(UnexpectedValueError):
		getattr(api.remediationscans, '_create_scan_document')({'scanner': 'nothing to see here'})

@pytest.mark.vcr()
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
def test_remedyscan_status(api):
	'''
	test to check scan status
	'''
	remedyscan = api.remediationscans.create_remediation_scan(
		uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
		name='Create Remediation Scan',
		description='This is first remediation scan created',
		scan_time_window=10,
		targets=['http://127.0.0.1'],
		template='advanced'
	)
	status = api.scans.status(remedyscan['id'])
	single(status, str)

@pytest.mark.vcr()
def test_remedyscan_enable_selected_plugins(api):
	'''
	test to enable selected plugin ids
	'''
	plugin_families = sorted(api.plugins.families(), key= lambda family: family['count'])[0]['id']
	plugin_list = [plugin['id'] for plugin in api.plugins.family_details(plugin_families)['plugins']]

	resp = api.remediationscans.create_remediation_scan(
		name='Create Remediation Scan',
		description='This is first remediation scan created',
		scan_time_window=10,
		targets=['http://127.0.0.1'],
		template='advanced',
		enabled_plugins=plugin_list
	)

	assert isinstance(resp, dict)
	check(resp, 'auto_routed', int)
	check(resp, 'creation_date', int)
	check(resp, 'custom_targets', str)
	check(resp, 'default_permissions', int)
	check(resp, 'description', str)
	check(resp, 'emails', str, allow_none=True)
	check(resp, 'enabled', bool)
	check(resp, 'id', int)
	check(resp, 'include_aggregate', bool)
	check(resp, 'last_modification_date', int)
	check(resp, 'name', str)
	check(resp, 'owner', str)
	check(resp, 'owner_id', int)
	check(resp, 'owner_uuid', 'uuid')
	check(resp, 'policy_id', int)
	check(resp, 'remediation', int)
	check(resp, 'rrules', dict, allow_none=True)
	check(resp, 'scan_time_window', int)
	check(resp, 'scanner_id', int, allow_none=True)
	check(resp, 'scanner_uuid', 'scanner-uuid')
	check(resp, 'shared', int)
	check(resp, 'sms', str)
	check(resp, 'starttime', str, allow_none=True)
	check(resp, 'target_network_uuid', 'uuid', allow_none=True)
	check(resp, 'timezone', str, allow_none=True)
	check(resp, 'type', str)
	check(resp, 'user_permissions', int)
	check(resp, 'uuid', str)


@pytest.mark.vcr()
def test_remedyscan_timezones(api):
	'''
	test to get list of allowed timezone strings
	'''
	assert isinstance(api.scans.timezones(), list)

@pytest.mark.vcr()
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
def test_remedyscan_check_auto_targets_limit_typeerror(api):
	'''
	test to raise exception when type of limit param does not match the expected type.
	'''
	with pytest.raises(TypeError):
		api.scans.check_auto_targets('nope', 5, targets=['192.168.16.108'])

@pytest.mark.vcr()
def test_remedyscan_check_auto_targets_matched_resource_limit_typeerror(api):
	'''
	test to raise exception when type of matched_resource_limit param
	does not match the expected type.
	'''
	with pytest.raises(TypeError):
		api.scans.check_auto_targets(10, 'nope', targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remedyscan_check_auto_targets_network_uuid_unexpectedvalueerror(api):
	'''
	test to raise exception when network_uuid param value does not match the choices.
	'''
	with pytest.raises(UnexpectedValueError):
		api.scans.check_auto_targets(10, 5, network_uuid='nope', targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remedyscan_check_auto_targets_network_uuid_typeerror(api):
	'''
	test to raise exception when type of network_uuid param does not match the expected type.
	'''
	with pytest.raises(TypeError):
		api.scans.check_auto_targets(10, 5, network_uuid=1, targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remedyscan_check_auto_targets_tags_unexpectedvalueerror(api):
	'''
	test to raise exception when type of any value in tags param
	does not match the expected type.
	'''
	with pytest.raises(UnexpectedValueError):
		api.scans.check_auto_targets(10, 5, tags=['nope'], targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remedyscan_check_auto_targets_tags_typeerror(api):
	'''
	test to raise exception when type of tags param does not match the expected type.
	'''
	with pytest.raises(TypeError):
		api.scans.check_auto_targets(10, 5, tags=1, targets=['127.0.0.1'])

@pytest.mark.vcr()
def test_remedyscan_check_auto_targets_targets_typeerror(api):
	'''
	test to raise exception when type of targets param does not match the expected type.
	'''
	with pytest.raises(TypeError):
		api.scans.check_auto_targets(10, 5, targets=1)

