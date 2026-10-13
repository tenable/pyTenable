"""
test policies
"""

import io

import pytest
import responses

from tenable.errors import NotFoundError, UnexpectedValueError

from ..checker import check

NESSUS_POLICY = (
    '<NessusClientData_v2><Policy><policyName>Example</policyName>'
    '<Preferences/></Policy></NessusClientData_v2>'
)

POLICIES = {
    'settings': {
        'patch_audit_over_telnet': 'no',
        'was_browser_cluster_job_timeout': 10,
        'report_verbosity': 'Normal',
        'enum_local_users_start_uid': '1000',
        'max_checks_per_host': '5',
        'patch_audit_over_rsh': 'no',
        'tcp_scanner': 'no',
        'description': '',
        'enable_plugin_debugging': 'no',
        'wol_wait_time': '5',
        'network_type': 'Mixed (use RFC 1918)',
        'reverse_lookup': 'no',
        'was_http_request_timeout': 5,
        'slice_network_addresses': 'no',
        'svc_detection_on_all_ports': 'yes',
        'ssh_client_banner': 'OpenSSH_5.0',
        'enable_admin_shares': 'no',
        'detect_ssl': 'yes',
        'was_plugins_autothrottle': 'yes',
        'stop_scan_on_disconnect': 'no',
        'name': 'bb600ca4-704b-4265-a894-e962afe41a21',
        'silent_dependencies': 'yes',
        'was_http_request_concurrency': 10,
        'reduce_connections_on_congestion': 'no',
        'additional_snmp_port3': '161',
        'http_login_auth_regex_nocase': 'no',
        'scan_network_printers': 'no',
        'wmi_netstat_scanner': 'yes',
        'wol_mac_addresses': '',
        'http_login_auth_regex_on_headers': 'no',
        'use_kernel_congestion_detection': 'no',
        'max_simult_tcp_sessions_per_scan': '',
        'scan_webapps': 'no',
        'max_simult_tcp_sessions_per_host': '',
        'start_remote_registry': 'no',
        'allow_post_scan_editing': 'yes',
        'additional_snmp_port2': '161',
        'ping_the_remote_host': 'yes',
        'verify_open_ports': 'no',
        'timeout_abort_threshold': 100,
        'host_tagging': 'yes',
        'provided_creds_only': 'yes',
        'additional_snmp_port1': '161',
        'thorough_tests': 'no',
        'report_superseded_patches': 'yes',
        'patch_audit_over_rexec': 'no',
        'portscan_range': 'default',
        'enum_domain_users_end_uid': '1200',
        'unscanned_closed': 'no',
        'enum_domain_users_start_uid': '1000',
        'http_login_max_redir': '0',
        'snmp_scanner': 'yes',
        'http_reauth_delay': 0,
        'log_live_hosts': 'no',
        'network_receive_timeout': '5',
        'udp_scanner': 'no',
        'scan_netware_hosts': 'no',
        'report_paranoia': 'Normal',
        'never_send_win_creds_in_the_clear': 'yes',
        'safe_checks': 'yes',
        'ssh_port': '22',
        'dont_use_ntlmv1': 'yes',
        'only_portscan_if_enum_failed': 'yes',
        'attempt_least_privilege': 'no',
        'syn_scanner': 'yes',
        'ssh_netstat_scanner': 'yes',
        'ssh_known_hosts': '',
        'http_login_invert_auth_regex': 'no',
        'snmp_port': '161',
        'http_login_method': 'POST',
        'request_windows_domain_info': 'yes',
        'scan_ot_devices': 'no',
        'was_plugins_rate_limiter_requests_per_second': 25,
        'test_default_oracle_accounts': 'no',
        'max_hosts_per_scan': '30',
        'display_unreachable_hosts': 'no',
        'enum_local_users_end_uid': '1200',
    },
    'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
}

EDITOR_POLICY_TEMPLATES = {
    'templates': [
        {
            'name': 'agent_advanced',
            'title': 'Advanced Agent Scan',
            'uuid': '549a08c1-e5fd-c0e9-fb8f-c4336582d50ec8ffa8e5034e8da2',
        },
        {
            'name': 'asv',
            'title': 'PCI Quarterly External Scan',
            'uuid': 'cfc46c2d-30e7-bb2b-3b92-c75da136792d080c1fffcc429cfd',
        },
    ]
}


@responses.activate
def test_configure_policy_notfounderror(tvm):
    """
    test to raise the exception when a policy to be configured is not found
    """
    responses.add(
        responses.PUT,
        'https://nourl/policies/1',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.policies.configure(1, dict())


@responses.activate
def test_configure_policy(tvm, policy):
    """
    test to configure the policy
    """
    responses.add(responses.GET, 'https://nourl/policies/13329', json=POLICIES)
    responses.add(responses.PUT, 'https://nourl/policies/13329')
    responses.add(
        responses.GET,
        'https://nourl/policies/13329',
        json={
            'settings': {
                'patch_audit_over_telnet': 'no',
                'was_browser_cluster_job_timeout': '10',
                'report_verbosity': 'Normal',
                'enum_local_users_start_uid': '1000',
                'max_checks_per_host': '5',
                'patch_audit_over_rsh': 'no',
                'tcp_scanner': 'no',
                'description': '',
                'tcp_ping': 'yes',
                'enable_plugin_debugging': 'no',
                'wol_wait_time': '5',
                'network_type': 'Mixed (use RFC 1918)',
                'reverse_lookup': 'no',
                'was_http_request_timeout': '5',
                'slice_network_addresses': 'no',
                'svc_detection_on_all_ports': 'yes',
                'fast_network_discovery': 'no',
                'icmp_ping': 'yes',
                'ssh_client_banner': 'OpenSSH_5.0',
                'enable_admin_shares': 'no',
                'detect_ssl': 'yes',
                'was_plugins_autothrottle': 'yes',
                'stop_scan_on_disconnect': 'no',
                'name': 'MODIFIED',
                'silent_dependencies': 'yes',
                'was_http_request_concurrency': '10',
                'http_login_auth_regex_nocase': 'no',
                'reduce_connections_on_congestion': 'no',
                'additional_snmp_port3': '161',
                'scan_network_printers': 'no',
                'wmi_netstat_scanner': 'yes',
                'wol_mac_addresses': '',
                'http_login_auth_regex_on_headers': 'no',
                'use_kernel_congestion_detection': 'no',
                'max_simult_tcp_sessions_per_scan': '',
                'scan_webapps': 'no',
                'udp_ping': 'no',
                'max_simult_tcp_sessions_per_host': '',
                'start_remote_registry': 'no',
                'allow_post_scan_editing': 'yes',
                'additional_snmp_port2': '161',
                'ping_the_remote_host': 'yes',
                'verify_open_ports': 'no',
                'timeout_abort_threshold': '100',
                'host_tagging': 'yes',
                'provided_creds_only': 'yes',
                'additional_snmp_port1': '161',
                'thorough_tests': 'no',
                'report_superseded_patches': 'yes',
                'patch_audit_over_rexec': 'no',
                'portscan_range': 'default',
                'enum_domain_users_end_uid': '1200',
                'unscanned_closed': 'no',
                'enum_domain_users_start_uid': '1000',
                'http_login_max_redir': '0',
                'http_reauth_delay': '0',
                'snmp_scanner': 'yes',
                'log_live_hosts': 'no',
                'network_receive_timeout': '5',
                'udp_scanner': 'no',
                'scan_netware_hosts': 'no',
                'report_paranoia': 'Normal',
                'never_send_win_creds_in_the_clear': 'yes',
                'safe_checks': 'yes',
                'ssh_port': '22',
                'dont_use_ntlmv1': 'yes',
                'only_portscan_if_enum_failed': 'yes',
                'attempt_least_privilege': 'no',
                'syn_scanner': 'yes',
                'ssh_netstat_scanner': 'yes',
                'ssh_known_hosts': '',
                'http_login_invert_auth_regex': 'no',
                'snmp_port': '161',
                'http_login_method': 'POST',
                'request_windows_domain_info': 'yes',
                'scan_ot_devices': 'no',
                'was_plugins_rate_limiter_requests_per_second': '25',
                'test_default_oracle_accounts': 'no',
                'max_hosts_per_scan': '30',
                'display_unreachable_hosts': 'no',
                'enum_local_users_end_uid': '1200',
                'arp_ping': 'yes',
            },
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
        },
    )
    details = tvm.policies.details(policy['policy_id'])
    details['settings']['name'] = 'MODIFIED'
    tvm.policies.configure(policy['policy_id'], details)
    updated = tvm.policies.details(policy['policy_id'])
    assert updated['settings']['name'] == 'MODIFIED'


@responses.activate
def test_copy_policy_notfounderror(tvm):
    """
    test to raise the exception when the policy to be copied is not found
    """
    responses.add(
        responses.POST,
        'https://nourl/policies/1/copy',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.policies.copy(1)


@responses.activate
def test_copy_policy(tvm, policy):
    """
    test to copy the policy
    """
    responses.add(
        responses.POST,
        'https://nourl/policies/13329/copy',
        json={'name': 'Copy of bb600ca4-704b-4265-a894-e962afe41a21', 'id': 13210},
    )
    responses.add(responses.DELETE, 'https://nourl/policies/13210')
    new = tvm.policies.copy(policy['policy_id'])
    assert isinstance(new, dict)
    check(new, 'id', int)
    check(new, 'name', str)
    assert 'Copy of' in new['name']
    tvm.policies.delete(new['id'])


@responses.activate
def test_create_policy(tvm, policy):
    """test to check types of a policy"""
    responses.add(responses.POST, 'https://nourl/policies', json=policy)
    policy = tvm.policies.create(
        {
            'credentials': {'add': {}, 'delete': [], 'edit': {}},
            'settings': {'name': policy['policy_name']},
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
        }
    )
    assert isinstance(policy, dict)
    check(policy, 'policy_id', int)
    check(policy, 'policy_name', str)


@responses.activate
def test_delete_policy_notfounderror(tvm):
    """
    test to raise the exception when policy to be deleted is not found
    """
    responses.add(
        responses.DELETE,
        'https://nourl/policies/1',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.policies.delete(1)


@responses.activate
def test_delete_policy(tvm, policy):
    """
    test to delete the policy
    """
    responses.add(responses.DELETE, 'https://nourl/policies/13329')
    tvm.policies.delete(policy['policy_id'])


@responses.activate
def test_policy_details_notfounderror(tvm):
    """
    test to raise the exception when the details of the policy is not found
    """
    responses.add(
        responses.GET,
        'https://nourl/policies/1',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.policies.details(1)


@responses.activate
def test_policy_details(tvm, policy):
    """
    test to get the policy details
    """
    responses.add(responses.GET, 'https://nourl/policies/13329', json=POLICIES)
    policy = tvm.policies.details(policy['policy_id'])
    assert isinstance(policy, dict)
    check(policy, 'uuid', 'scanner-uuid')
    check(policy, 'settings', dict)


@responses.activate
def test_policy_export_notfounderror(tvm):
    """
    test to raise the exception when the policy to be exported is not found
    """
    responses.add(
        responses.GET,
        'https://nourl/policies/1/export',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.policies.policy_export(1)


@responses.activate
def test_policy_export(tvm, policy):
    """
    test to export the policy data
    """
    responses.add(
        responses.GET,
        'https://nourl/policies/13329/export',
        body=NESSUS_POLICY,
        content_type='text/xml',
        headers={
            'content-disposition': 'attachment; filename="nessus_policy_f22bb3b0-10ee-43f8-8b1c-65622999cd4b.nessus"'
        },
    )
    pobj = tvm.policies.policy_export(policy['policy_id'])
    assert isinstance(pobj, io.BytesIO)


@responses.activate
def test_policy_import(tvm, policy):
    """
    test to import the policy
    """
    responses.add(
        responses.GET,
        'https://nourl/policies/13329/export',
        body=NESSUS_POLICY,
        content_type='text/xml',
        headers={
            'content-disposition': 'attachment; filename="nessus_policy_2b8a02e0-f9de-42af-a45f-8a163e2994d3.nessus"'
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/file/upload',
        json={'fileuploaded': '942dab49-9aba-42fe-b844-8daa22b21484'},
    )
    responses.add(
        responses.POST,
        'https://nourl/policies/import',
        json={
            'private': 0,
            'no_target': 'false',
            'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
            'description': '\n',
            'name': 'bb600ca4-704b-4265-a894-e962afe41a21_01',
            'owner': 'test_admin@pytenable.io',
            'shared': 0,
            'user_permissions': 128,
            'last_modification_date': 1544138432,
            'creation_date': 1544138432,
            'owner_id': 3,
            'id': 13216,
        },
    )
    pobj = tvm.policies.policy_export(policy['policy_id'])
    resp = tvm.policies.policy_import(pobj)
    assert isinstance(resp, dict)
    check(resp, 'creation_date', int)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'no_target', str)
    check(resp, 'owner', str)
    check(resp, 'owner_id', int)
    check(resp, 'shared', int)
    check(resp, 'template_uuid', 'scanner-uuid')
    check(resp, 'user_permissions', int)


@responses.activate
def test_policy_list(tvm, policy):
    """
    test to get the policy list
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
                    'name': '03640b8b-7709-4483-b4e6-a5c3c600dc13',
                    'owner': 'test_admin@pytenable.io',
                    'visibility': 'private',
                    'shared': 0,
                    'user_permissions': 128,
                    'last_modification_date': 1521561156,
                    'creation_date': 1521561156,
                    'owner_id': 3,
                    'id': 101,
                }
            ]
        },
    )
    policies = tvm.policies.list()
    assert isinstance(policies, list)
    for pol in policies:
        check(pol, 'creation_date', int)
        check(pol, 'description', str, allow_none=True)
        check(pol, 'id', int)
        check(pol, 'last_modification_date', int)
        check(pol, 'name', str)
        check(pol, 'no_target', str)
        check(pol, 'owner', str)
        check(pol, 'owner_id', int)
        check(pol, 'shared', int)
        check(pol, 'template_uuid', 'scanner-uuid')
        check(pol, 'user_permissions', int)
        check(pol, 'visibility', str)


@responses.activate
def test_policy_template_details_success(tvm):
    """
    test to get the template details
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates/549a08c1-e5fd-c0e9-fb8f-c4336582d50ec8ffa8e5034e8da2',
        json={
            'compliance': {
                'data': [
                    {
                        'name': 'Unix',
                        'audits': [
                            {
                                'type': 'custom',
                                'name': '(Upload a custom Unix audit file)',
                                'free': 1,
                                'unlimited': True,
                            }
                        ],
                    }
                ]
            },
            'is_was': None,
            'user_permissions': 128,
            'owner': 'pytenable_test_user@tenable.com',
            'title': 'Advanced Agent Scan',
            'is_agent': True,
            'uuid': '549a08c1-e5fd-c0e9-fb8f-c4336582d50ec8ffa8e5034e8da2',
            'plugins': {
                'families': {
                    'Peer-To-Peer File Sharing': {
                        'count': 17,
                        'id': 29,
                        'status': 'enabled',
                    }
                }
            },
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
                    'groups': [
                        {
                            'title': 'Permissions',
                            'name': 'permissions',
                            'acls': None,
                        }
                    ],
                },
                'advanced': {'inputs': None, 'modes': [], 'title': 'Advanced'},
            },
            'name': 'agent_advanced',
        },
    )
    template_detail = tvm.policies.template_details('agent_advanced')
    assert isinstance(template_detail, dict)
    check(template_detail, 'compliance', dict)
    check(template_detail, 'plugins', dict)
    check(template_detail, 'settings', dict)
    check(template_detail, 'uuid', 'scanner-uuid')


@responses.activate
def test_policy_template_details_keyerror(tvm):
    """
    test to raise the exception when key of template details is not as defined
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.policies.template_details('one')


@responses.activate
def test_policy_template_details_typeerror(tvm):
    """
    test to raise the exception when type of details is not as defined
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    with pytest.raises(TypeError):
        tvm.policies.template_details(1)


@responses.activate
def test_policies_template_details_new_success(tvm):
    """
    test to get template details
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json={
            'templates': [
                {
                    'name': 'custom',
                    'title': 'Custom Scan',
                    'uuid': 'ab4bacd2-05f6-425c-9d79-3ba3940ad1c24e51e1f403febe40',
                },
                {
                    'name': 'agent_custom',
                    'title': 'Custom Agent Scan',
                    'uuid': 'fb18acbc-39cc-d6a6-3d3b-b145f6f2eade659f25cac6837b27',
                },
            ]
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates/ab4bacd2-05f6-425c-9d79-3ba3940ad1c24e51e1f403febe40',
        json={
            'is_was': None,
            'user_permissions': 128,
            'owner': 'pytenable_test_user@tenable.com',
            'title': 'Custom Scan',
            'is_agent': None,
            'uuid': 'ab4bacd2-05f6-425c-9d79-3ba3940ad1c24e51e1f403febe40',
            'settings': {'basic': {'title': 'Basic', 'groups': []}},
            'name': 'custom',
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates/fb18acbc-39cc-d6a6-3d3b-b145f6f2eade659f25cac6837b27',
        json={
            'is_was': None,
            'user_permissions': 128,
            'owner': 'pytenable_test_user@tenable.com',
            'title': 'Custom Agent Scan',
            'is_agent': True,
            'uuid': 'fb18acbc-39cc-d6a6-3d3b-b145f6f2eade659f25cac6837b27',
            'settings': {
                'basic': {
                    'inputs': [
                        {
                            'type': 'entry',
                            'name': 'Name',
                            'id': 'name',
                            'required': True,
                        },
                        {
                            'type': 'textarea',
                            'name': 'Description',
                            'id': 'description',
                        },
                    ],
                    'title': 'Basic',
                    'groups': [
                        {'title': 'Permissions', 'name': 'permissions', 'acls': None}
                    ],
                    'sections': [],
                }
            },
            'filter_attributes': [
                {
                    'operators': ['eq', 'neq'],
                    'control': {'type': 'dropdown', 'list': ['true', 'false']},
                    'name': 'asset_inventory',
                    'readable_name': 'Asset Inventory',
                }
            ],
            'name': 'agent_custom',
        },
    )
    templates = tvm.policies.templates()
    for keys in templates.keys():
        tvm.policies.template_details(keys)


@responses.activate
def test_policies_template_details_credentials_types_settings_success(tvm):
    """
    test to cover settings data from template details
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates/cfc46c2d-30e7-bb2b-3b92-c75da136792d080c1fffcc429cfd',
        json={
            'credentials': {
                'data': [
                    {
                        'types': [
                            {
                                'max': 1,
                                'name': 'HTTP',
                                'instances': [],
                                'settings': {'demokey': 'demovalue'},
                            }
                        ],
                        'name': 'Plaintext Authentication',
                        'default_expand': 1,
                    }
                ]
            },
            'is_was': None,
            'user_permissions': 128,
            'owner': 'triage_musikaar@tenable.com',
            'title': 'PCI Quarterly External Scan',
            'is_agent': None,
            'uuid': 'cfc46c2d-30e7-bb2b-3b92-c75da136792d080c1fffcc429cfd',
            'settings': {
                'basic': {
                    'desc': 'This policy MUST be used for scans submitted to Tenable (an Approved Scanning Vendor) to validate compliance with PCI DS',
                    'inputs': [
                        {
                            'type': 'entry',
                            'name': 'Name',
                            'id': 'name',
                            'required': True,
                        }
                    ],
                    'title': 'Basic',
                    'groups': [
                        {
                            'title': 'Permissions',
                            'name': 'permissions',
                            'acls': None,
                        }
                    ],
                },
                'discovery': {
                    'inputs': None,
                    'modes': {
                        'id': 'discovery_mode',
                        'name': 'mode',
                        'type': 'ui_radio',
                        'default': 'Custom',
                    },
                    'title': 'Discovery',
                },
            },
            'name': 'asv',
        },
    )
    template_detail = tvm.policies.template_details('asv')
    assert isinstance(template_detail, dict)
    check(template_detail, 'credentials', dict)
    check(template_detail, 'settings', dict)
    check(template_detail, 'uuid', 'scanner-uuid')
