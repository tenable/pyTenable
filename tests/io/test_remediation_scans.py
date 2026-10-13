"""
test Remediation scans
"""

import pytest
import responses
from responses import matchers
from tenable.errors import UnexpectedValueError
from tests.checker import check, single

EDITOR_POLICY_TEMPLATES = {
    'templates': [
        {
            'name': 'advanced',
            'title': 'Advanced Network Scan',
            'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        },
        {
            'name': 'basic',
            'title': 'Basic Network Scan',
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
        },
    ]
}

EDITOR_SCAN_POLICY = {
    'credentials': {
        'data': [
            {
                'types': [
                    {
                        'max': 1,
                        'name': 'IBM DataPower Gateway',
                        'instances': [],
                        'settings': None,
                    }
                ],
                'name': 'API Gateway',
                'default_expand': 0,
            }
        ]
    },
    'policy_has_credentials': False,
    'is_was': None,
    'user_permissions': None,
    'owner': None,
    'title': 'Custom Scan',
    'is_agent': None,
    'uuid': 'ab4bacd2-05f6-425c-9d79-3ba3940ad1c24e51e1f403febe40',
    'settings': {
        'basic': {
            'inputs': [
                {'type': 'entry', 'name': 'Name', 'id': 'name', 'required': True}
            ],
            'title': 'Basic',
            'groups': [{'title': 'Schedule', 'name': 'schedule'}],
        }
    },
    'name': 'custom',
}

EDITOR_SCAN_TEMPLATES = {
    'is_was': None,
    'user_permissions': None,
    'is_agent': None,
    'owner': None,
    'title': 'Advanced Network Scan',
    'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'select',
                    'id': 'scanner_id',
                    'name': 'Scanner',
                    'default': None,
                    'options': [
                        {
                            'id': '00000000-0000-0000-0000-00000000000000000000000000001',
                            'name': 'US Cloud Scanner',
                            'type': 'local',
                            'linked': True,
                            'status': 'on',
                        }
                    ],
                }
            ],
            'title': 'Basic',
        }
    },
    'name': 'advanced',
}


@responses.activate
def test_remedy_scanned_list(tvm):
    """
    test to check remediation scan list
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/remediation',
        json={
            'pagination': {
                'offset': 0,
                'total': 1,
                'sort': 'scan_creation_date:asc',
                'limit': 5,
            },
            'scans': [
                {
                    'permissions': 128,
                    'enabled': False,
                    'control': True,
                    'read': True,
                    'last_modification_date': 0,
                    'creation_date': 0,
                    'status': 'empty',
                    'shared': False,
                    'user_permissions': 128,
                    'schedule_uuid': 'template-f2b9d2d8-4ca4-4be7-c33d-0f6e43f3f12a9bc0caab4ec7b0e2',
                    'wizard_uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
                    'scan_creation_date': 1625649892,
                    'owner': 'pytenable_test_user@tenable.com',
                    'policy_id': 462,
                    'id': 463,
                    'remediation': 1,
                    'name': 'Create Remediation Scan',
                }
            ],
        },
        match=[
            matchers.query_param_matcher(
                {'limit': '5', 'offset': '0', 'sort': 'scan_creation_date:asc'}
            )
        ],
    )
    scan_list = tvm.remediationscans.list_remediation_scan(
        5, 0, 'scan_creation_date:asc'
    )
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


def test_remedyscan_create_scan_document_template_typeerror(tvm):
    """
    test to raise exception when type of template param does not match the expected type.
    """
    with pytest.raises(TypeError):
        getattr(tvm.remediationscans, 'create_remediation_scan')(
            {'template': 'advanced'}
        )


@responses.activate
def test_remedyscan_create_scan_document_template_unexpected_value_error(tvm):
    """
    test to raise exception when template param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.remediationscans, '_create_scan_document')(
            {'template': 'nothing_here'}
        )


@responses.activate
def test_remedyscan_create_scan_document_template_pass(tvm):
    """
    test to create scan document basic template
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    templates = tvm.policies.templates()
    resp = getattr(tvm.remediationscans, '_create_scan_document')({'template': 'basic'})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['basic']


@responses.activate
def test_remedyscan_create_advanced_scan_document_template_pass(tvm):
    """
    test to create scan document using advanced template, credentials and compliance
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    templates = tvm.policies.templates()
    resp = getattr(tvm.remediationscans, '_create_scan_document')(
        {
            'template': 'advanced',
            'credentials': {'name': 'Test'},
            'compliance': {'name': 'Policy Compliance'},
        }
    )
    assert isinstance(resp, dict), (
        'Response of create scan template for remediation scan is not of type dict.'
    )
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['advanced'], (
        'UUID of remediation scan template created in this test-case not matched with UUID of advanced scan template.'
    )


@responses.activate
def test_remedyscan_create_scan_document_policies_id_pass(tvm):
    """
    test to create scan document policy param using id
    """
    responses.add(
        responses.GET,
        'https://nourl/policies',
        json={
            'policies': [
                {
                    'no_target': 'false',
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'description': None,
                    'name': 'c3e9fec8-0676-43cb-9128-48bca2b45d07',
                    'owner': 'pytenable_test_user@tenable.com',
                    'visibility': 'private',
                    'shared': 0,
                    'user_permissions': 128,
                    'last_modification_date': 1623213793,
                    'creation_date': 1623213793,
                    'owner_id': 2201492,
                    'id': 154,
                }
            ]
        },
    )
    responses.add(
        responses.GET, 'https://nourl/editor/scan/policy/154', json=EDITOR_SCAN_POLICY
    )
    policies = tvm.policies.list()
    policy = policies[0]
    resp = getattr(tvm.remediationscans, '_create_scan_document')(
        {'policy': policy['id']}
    )
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']


@responses.activate
def test_remedyscan_create_scan_document_policies_name_pass(tvm):
    """
    test to create scan document with policy param using name
    """
    responses.add(
        responses.GET,
        'https://nourl/policies',
        json={
            'policies': [
                {
                    'no_target': 'false',
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'description': None,
                    'name': 'c3e9fec8-0676-43cb-9128-48bca2b45d07',
                    'owner': 'pytenable_test_user@tenable.com',
                    'visibility': 'private',
                    'shared': 0,
                    'user_permissions': 128,
                    'last_modification_date': 1623213793,
                    'creation_date': 1623213793,
                    'owner_id': 2201492,
                    'id': 154,
                }
            ]
        },
    )
    responses.add(
        responses.GET, 'https://nourl/editor/scan/policy/154', json=EDITOR_SCAN_POLICY
    )
    policies = tvm.policies.list()
    policy = policies[0]
    resp = getattr(tvm.remediationscans, '_create_scan_document')(
        {'policy': policy['name']}
    )
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']


# def test_remedyscan_create_scan_document_targets


@responses.activate
def test_remedyscan_create_scan_document_scanner_unexpectedvalueerror(tvm):
    """
    test to raise exception when scanner param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        json={
            'is_was': None,
            'user_permissions': None,
            'is_agent': None,
            'owner': None,
            'title': 'Advanced Network Scan',
            'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
            'settings': {
                'basic': {
                    'inputs': [
                        {
                            'type': 'entry',
                            'name': 'Name',
                            'id': 'name',
                            'required': True,
                        }
                    ],
                    'title': 'Basic',
                }
            },
            'name': 'advanced',
        },
    )
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.remediationscans, '_create_scan_document')(
            {'scanner': 'nothing to see here'}
        )


@responses.activate
def test_remedyscan_create_scan_document_scanner_uuid_pass(tvm):
    """
    test to create scan document with scanner uuid param
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        json=EDITOR_SCAN_TEMPLATES,
    )
    scanners = tvm.scanners.allowed_scanners()
    scanner = scanners[0]
    resp = getattr(tvm.remediationscans, '_create_scan_document')(
        {'scanner': scanner['id']}
    )
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', 'scanner-uuid')
    assert resp['settings']['scanner_id'] == scanner['id']


@responses.activate
def test_remedyscan_create_scan_document_scanner_name_pass(tvm):
    """
    test to create scan document with scanner name param
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        json=EDITOR_SCAN_TEMPLATES,
    )
    scanners = tvm.scanners.allowed_scanners()
    scanner = scanners[0]
    resp = getattr(tvm.remediationscans, '_create_scan_document')(
        {'scanner': scanner['name']}
    )
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', str)
    assert resp['settings']['scanner_id'] == scanner['id']


@responses.activate
def test_remedyscan_status(tvm):
    """
    test to check scan status
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/remediation',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-7f425e81-463c-79ea-2b87-4414b75a0dea989942ce9d21069f',
                'name': 'Create Remediation Scan',
                'description': 'This is first remediation scan created',
                'policy_id': 409,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': 10,
                'custom_targets': 'http://127.0.0.1:3000',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 1,
                'starttime': None,
                'rrules': None,
                'timezone': None,
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1624253797,
                'creation_date': 1624253797,
                'type': 'public',
                'id': 410,
            }
        },
    )
    responses.add(
        responses.GET, 'https://nourl/scans/410/latest-status', json={'status': 'empty'}
    )
    remedyscan = tvm.remediationscans.create_remediation_scan(
        uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
        name='Create Remediation Scan',
        description='This is first remediation scan created',
        scan_time_window=10,
        targets=['http://127.0.0.1'],
        template='advanced',
    )
    status = tvm.scans.status(remedyscan['id'])
    single(status, str)


@responses.activate
def test_remedyscan_enable_selected_plugins(tvm):
    """
    test to enable selected plugin ids
    """
    responses.add(
        responses.GET,
        'https://nourl/plugins/families',
        json={
            'families': [
                {'count': 11396, 'name': 'AIX Local Security Checks', 'id': 27},
                {'count': 1917, 'name': 'CISCO', 'id': 10},
                {'count': 14, 'name': 'Netware', 'id': 12},
            ]
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/plugins/families/12',
        json={
            'plugins': [
                {
                    'id': 12122,
                    'name': 'Novell Groupwise Servlet Manager Default Password',
                },
                {
                    'id': 12050,
                    'name': 'Novell NetBasic Scripting Server Encoded Traversal Arbitrary File Access',
                },
                {
                    'id': 12119,
                    'name': 'Novell NetWare 6.0 Tomcat source.jsp Traversal Arbitrary File Access',
                },
                {
                    'id': 44066,
                    'name': 'Novell NetWare 6.5 OpenSSH Remote Stack Buffer Overflow',
                },
            ],
            'name': 'Netware',
            'id': 12,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/remediation',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-f2b9d2d8-4ca4-4be7-c33d-0f6e43f3f12a9bc0caab4ec7b0e2',
                'name': 'Create Remediation Scan',
                'description': 'This is first remediation scan created',
                'policy_id': 462,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': 10,
                'custom_targets': 'http://127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 1,
                'starttime': None,
                'rrules': None,
                'timezone': None,
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1625649892,
                'creation_date': 1625649892,
                'type': 'public',
                'id': 463,
            }
        },
    )
    plugin_families = sorted(
        tvm.plugins.families(), key=lambda family: family['count']
    )[0]['id']
    plugin_list = [
        plugin['id']
        for plugin in tvm.plugins.family_details(plugin_families)['plugins']
    ]

    resp = tvm.remediationscans.create_remediation_scan(
        name='Create Remediation Scan',
        description='This is first remediation scan created',
        scan_time_window=10,
        targets=['http://127.0.0.1'],
        template='advanced',
        enabled_plugins=plugin_list,
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


@responses.activate
def test_remedyscan_timezones(tvm):
    """
    test to get list of allowed timezone strings
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/timezones',
        json={
            'timezones': [
                {'name': 'Africa/Abidjan', 'value': 'Africa/Abidjan'},
                {'name': 'Etc/UTC', 'value': 'Etc/UTC'},
            ]
        },
    )
    assert isinstance(tvm.scans.timezones(), list)


@responses.activate
def test_remedyscan_check_auto_targets_success(tvm):
    """
    test to evaluates a list of targets and/or tags against
    the scan route configuration of scanner groups
    """
    responses.add(
        responses.POST,
        'https://nourl/scans/check-auto-targets',
        json={
            'missed_targets': ['127.0.0.1'],
            'total_missed_targets': 1,
            'matched_resource_uuids': [],
            'total_matched_resource_uuids': 0,
        },
        match=[
            matchers.query_param_matcher({'limit': '10', 'matched_resource_limit': '5'})
        ],
    )
    resp = tvm.scans.check_auto_targets(10, 5, targets=['127.0.0.1'])
    assert isinstance(resp, dict)
    check(resp, 'matched_resource_uuids', list)
    check(resp, 'missed_targets', list)
    check(resp, 'total_matched_resource_uuids', int)
    check(resp, 'total_missed_targets', int)
