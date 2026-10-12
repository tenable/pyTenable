"""
test file for testing various scenarios in security center
policies functionality
"""

import os

import pytest
import json
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError
from ..checker import check, single

POLICY_TEMPLATE_CREDENTIALS = {
    'groups': [
        {
            'id': 'host',
            'name': 'Host',
            'credentials': [
                {
                    'name': 'SNMPv3',
                    'max': 1,
                    'id': 'snmpv3',
                    'inputs': [
                        {'type': 'entry', 'name': 'Username', 'id': 'username'},
                        {
                            'type': 'dropdown',
                            'name': 'Security Level',
                            'default': 'Authentication and privacy',
                            'id': 'security_level',
                            'conditionalSettings': {
                                'Authentication without privacy': {
                                    'inputs': [
                                        {
                                            'type': 'dropdown',
                                            'name': 'Authentication algorithm',
                                            'default': 'SHA1',
                                            'id': 'auth_algorithm',
                                        }
                                    ]
                                },
                                'Authentication and privacy': {
                                    'inputs': [
                                        {
                                            'type': 'dropdown',
                                            'name': 'Authentication algorithm',
                                            'default': 'SHA1',
                                            'id': 'auth_algorithm',
                                        }
                                    ]
                                },
                            },
                        },
                    ],
                }
            ],
        }
    ]
}

POLICY_TEMPLATE_EDITOR = {
    'compliance': 'true',
    'globalSettings': [
        {
            'id': 'hpprocurve',
            'name': 'HP ProCurve',
            'preferenceID': 'procurve_config_to_audit',
        },
        {'id': 'cisco', 'name': 'Cisco IOS', 'preferenceID': 'cisco_config_to_audit'},
    ],
    'credentials': json.dumps(POLICY_TEMPLATE_CREDENTIALS),
    'sections': [
        {
            'name': 'Setup',
            'id': 'setup',
            'subsections': [
                {
                    'id': 'setup_general',
                    'name': 'General',
                    'inputs': [
                        {
                            'id': 'name',
                            'type': 'entry',
                            'name': 'Name',
                            'required': 'true',
                            'preferenceID': 'name',
                        },
                        {
                            'id': 'description',
                            'type': 'textarea',
                            'name': 'Description',
                            'preferenceID': 'description',
                        },
                    ],
                },
                {'id': 'setup_modes', 'name': 'Configuration', 'inputs': []},
            ],
            'section': 'setup',
        },
        {
            'name': 'Advanced',
            'subsections': [
                {
                    'name': 'General Settings',
                    'inputs': [
                        {
                            'id': 'safe_checks',
                            'type': 'checkbox',
                            'name': 'Enable safe checks',
                            'default': 'yes',
                            'preferenceID': 'safe_checks',
                        },
                        {
                            'id': 'stop_scan_on_disconnect',
                            'type': 'checkbox',
                            'name': 'Stop scanning hosts that become unresponsive during the scan',
                            'default': 'no',
                            'preferenceID': 'stop_scan_on_disconnect',
                        },
                    ],
                    'id': 'advanced_advanced',
                },
                {
                    'name': 'Performance Options',
                    'inputs': [
                        {
                            'id': 'reduce_connections_on_congestion',
                            'type': 'checkbox',
                            'name': 'Slow down the scan when network congestion is detected',
                            'default': 'no',
                            'preferenceID': 'reduce_connections_on_congestion',
                        },
                        {
                            'id': 'use_kernel_congestion_detection',
                            'type': 'checkbox',
                            'name': 'Use Linux kernel congestion detection',
                            'default': 'no',
                            'preferenceID': 'use_kernel_congestion_detection',
                        },
                        {
                            'id': 'network_receive_timeout',
                            'type': 'small-entry',
                            'default': '5',
                            'name': 'Network timeout (in seconds)',
                            'regex': '^\\d+$',
                            'preferenceID': 'checks_read_timeout',
                        },
                        {
                            'id': 'max_checks_per_host',
                            'type': 'small-entry',
                            'name': 'Max simultaneous checks per host',
                            'default': '5',
                            'regex': '^\\d+$',
                            'preferenceID': 'max_checks',
                        },
                        {
                            'id': 'max_hosts_per_scan',
                            'type': 'small-entry',
                            'name': 'Max simultaneous hosts per scan',
                            'default': '30',
                            'regex': '^\\d+$',
                            'preferenceID': 'max_hosts',
                        },
                        {
                            'id': 'max_simult_tcp_sessions_per_host',
                            'type': 'medium-entry',
                            'name': 'Max number of concurrent TCP sessions per host',
                            'preferenceID': 'host.max_simult_tcp_sessions',
                        },
                        {
                            'id': 'max_simult_tcp_sessions_per_scan',
                            'type': 'medium-entry',
                            'name': 'Max number of concurrent TCP sessions per scan',
                            'preferenceID': 'max_simult_tcp_sessions',
                        },
                    ],
                    'id': 'advanced_performance',
                    'section': 'advanced',
                },
            ],
            'id': 'advanced',
            'section': 'advanced',
        },
    ],
}

POLICY = {
    'type': 'regular',
    'response': {
        'usable': [
            {
                'id': '1000001',
                'name': 'Full Safe Scan',
                'description': '',
                'status': '0',
            },
            {'id': '1000006', 'name': 'example1', 'description': '', 'status': '0'},
        ],
        'manageable': [
            {
                'id': '1000001',
                'name': 'Full Safe Scan',
                'description': '',
                'status': '0',
            },
            {'id': '1000006', 'name': 'example1', 'description': '', 'status': '0'},
        ],
    },
    'error_code': 0,
    'error_msg': '',
    'warnings': [],
    'timestamp': 1550267453,
}


@pytest.fixture
def policy():
    """
    test fixture for policy
    """
    return {
        'id': '1000007',
        'name': 'Example Policy',
        'description': '',
        'tags': '',
        'createdTime': '1550265754',
        'modifiedTime': '1550265754',
        'generateXCCDFResults': 'false',
        'context': '',
        'status': '0',
        'canUse': 'true',
        'canManage': 'true',
    }


def test_policies_constructor_name_typeerror(tsc):
    """
    test policies constructor for name type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(name=1)


def test_policies_constructor_context_typeerror(tsc):
    """
    test policies constructor for context type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(context=1)


def test_policies_constructor_context_unexpectedvalueerror(tsc):
    """
    test policies constructor for context unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.policies._constructor(context='not a scan')


def test_policies_constructor_description_typeerror(tsc):
    """
    test policies constructor for description type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(description=1)


def test_policies_constructor_tags_typeerror(tsc):
    """
    test policies constructor for tags type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(tags=1)


def test_policies_constructor_preferences_typeerror(tsc):
    """
    test policies constructor for preferences type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(preferences=1)


def test_policies_constructor_preference_item_name_typeerror(tsc):
    """
    test policies constructor for 'item name' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(preferences={1: 'value'})


def test_policies_constructor_preference_item_value_should_not_typeerror(tsc):
    """
    test policies constructor for 'item value' type error
    """
    tsc.policies._constructor(preferences={'name': 1})


def test_policies_constructor_audit_files_typeerror(tsc):
    """
    test policies constructor for 'audit files' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(audit_files=1)


def test_policies_constructor_audit_files_file_typeerror(tsc):
    """
    test policies constructor for 'audit files file' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(audit_files=['one'])


def test_policies_constructor_template_id_typeerror(tsc):
    """
    test policies constructor for 'template id' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(template_id='one')


def test_policies_constructor_profile_name_typeerror(tsc):
    """
    test policies constructor for 'profile name' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(profile_name=1)


def test_policies_constructor_xccdf_typeerror(tsc):
    """
    test policies constructor for 'xccdf' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(xccdf='yup')


def test_policies_constructor_owner_id_typeerror(tsc):
    """
    test policies constructor for 'owner id' type error
    """
    with pytest.raises(TypeError):
        tsc.policies._constructor(owner_id='one')


def test_policies_constructor(tsc):
    """
    test policies constructor for success
    """
    resp = tsc.policies._constructor(
        name='Example',
        context='',
        description='Something Special',
        tags='',
        preferences={'name1': 'value1', 'name2': 'value2'},
        audit_files=[1],
        template_id=1,
        profile_name='ProfileName',
        xccdf=True,
        owner_id=1,
    )
    assert resp == {
        'name': 'Example',
        'context': '',
        'description': 'Something Special',
        'tags': '',
        'preferences': {'name1': 'value1', 'name2': 'value2'},
        'auditFiles': [{'id': 1}],
        'policyTemplate': {'id': 1},
        'policyProfileName': 'ProfileName',
        'generateXCCDFResults': 'true',
        'ownerID': 1,
    }


def test_policies_template_list_fields_typeerror(tsc):
    """
    test policies template list for fields type error
    """
    with pytest.raises(TypeError):
        tsc.policies.template_list(fields=1)


@responses.activate
def test_policies_template_list_success(tsc):
    """
    test policies template list for success
    """
    responses.get(
        'https://nourl/rest/policyTemplate',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'name': 'Advanced Scan',
                    'description': 'Configure a scan without using any recommendations.',
                },
                {
                    'id': '2',
                    'name': 'Host Discovery',
                    'description': 'A simple scan to discover live hosts and open ports.',
                },
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550265920,
        },
    )
    resp = tsc.policies.template_list()
    assert isinstance(resp, list)
    a_resp = resp[0]
    assert isinstance(a_resp, dict)
    check(a_resp, 'description', str)
    check(a_resp, 'id', str)
    check(a_resp, 'name', str)


def test_policies_template_details_id_typeerror(tsc):
    """
    test policies template details for id type error
    """
    with pytest.raises(TypeError):
        tsc.policies.template_details('nope')


def test_policies_template_details_fields_typeerror(tsc):
    """
    test policies template details for 'fields' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.template_details(1, fields='noper')


@responses.activate
def test_policies_template_details_success(tsc):
    """
    test policies template details for success
    """
    responses.get(
        'https://nourl/rest/policyTemplate/1',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'Advanced Scan',
                'description': 'Configure a scan without using any recommendations.',
                'editor': json.dumps(POLICY_TEMPLATE_EDITOR),
                'createdTime': '1406151204',
                'modifiedTime': '1547791860',
                'templateModTime': '1547743926',
                'templatePubTime': '1406151204',
                'templateDefModTime': '1547743926',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550265920,
        },
    )
    tmpl = tsc.policies.template_details(1)
    assert isinstance(tmpl, dict)
    check(tmpl, 'createdTime', str)
    check(tmpl, 'credentials', dict)
    for key in tmpl['credentials']:
        single(key, str)
        check(tmpl['credentials'], key, dict)
        for pref in tmpl['credentials'][key]:
            single(pref, str)
            check(tmpl['credentials'][key], pref, str)
    check(tmpl, 'description', str)
    check(tmpl, 'id', str)
    check(tmpl, 'modifiedTime', str)
    check(tmpl, 'name', str)
    check(tmpl, 'preferences', dict)
    for key in tmpl['preferences']:
        single(key, str)
        check(tmpl['preferences'], key, str)
    check(tmpl, 'templateDefModTime', str)
    check(tmpl, 'templateModTime', str)
    check(tmpl, 'templatePubTime', str)


def test_policies_create_name_unexpectedvalueerror(tsc):
    """
    test policies create for name unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.policies.create()


@responses.activate
def test_policies_create_name_typerror(tsc):
    """
    test policies create for name type error
    """
    responses.get(
        'https://nourl/rest/policyTemplate/1',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'Advanced Scan',
                'description': 'Configure a scan without using any recommendations.',
                'editor': json.dumps(POLICY_TEMPLATE_EDITOR),
                'createdTime': '1406151204',
                'modifiedTime': '1547791860',
                'templateModTime': '1547743926',
                'templatePubTime': '1406151204',
                'templateDefModTime': '1547743926',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550265920,
        },
    )
    with pytest.raises(TypeError):
        tsc.policies.create(name=1)


def test_policies_create_template_id_typeerror(tsc):
    """
    test policies create template for id typeerror
    """
    with pytest.raises(TypeError):
        tsc.policies.create(name='Test', template_id='one')


@responses.activate
def test_policies_create_success(tsc):
    """
    test policies create for success
    """
    responses.get(
        'https://nourl/rest/policyTemplate/1',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'Advanced Scan',
                'description': 'Configure a scan without using any recommendations.',
                'editor': json.dumps(POLICY_TEMPLATE_EDITOR),
                'createdTime': '1406151204',
                'modifiedTime': '1547791860',
                'templateModTime': '1547743926',
                'templatePubTime': '1406151204',
                'templateDefModTime': '1547743926',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550265753,
        },
    )
    responses.post(
        'https://nourl/rest/policy',
        json={
            'type': 'regular',
            'response': {
                'id': '1000007',
                'name': 'Example Policy',
                'description': '',
                'tags': '',
                'createdTime': '1550265754',
                'modifiedTime': '1550265754',
                'generateXCCDFResults': 'false',
                'context': '',
                'auditFiles': [],
                'preferences': {
                    'abort_generic_webapp_if_login_fails': 'no',
                    'arp_ping': 'yes',
                    'av_grace_period': '0',
                    'cert_expiry_warning_days': '60',
                    'check_crl': 'no',
                    'combo_arg_values': 'one value',
                    'detect_ssl': 'yes',
                    'disable_dns_resolution': 'no',
                    'display_unreachable_hosts': 'no',
                    'enable_file_scanning': 'no',
                    'enable_filescan_programdata': 'no',
                    'enable_filescan_programfiles': 'no',
                    'enable_filescan_programfilesx86': 'no',
                    'enable_filescan_systemroot': 'no',
                    'enable_filescan_userprofiles': 'no',
                    'enum_domain_users_end_uid': '1200',
                    'enum_domain_users_start_uid': '1000',
                    'enum_local_users_end_uid': '1200',
                    'enum_local_users_start_uid': '1000',
                    'enumerate_all_ciphers': 'yes',
                    'fast_network_discovery': 'yes',
                    'filescan_custom_dir': '',
                    'generateXCCDFResults': 'no',
                    'generic_webapp_tests': 'no',
                    'generic_webapp_tests_max_time': '5',
                    'host_whitelist': '',
                    'http_param_pollution': 'no',
                    'hydra_add_other_accounts': 'yes',
                    'hydra_always_enable': 'no',
                    'hydra_cisco_logon_pw': '',
                    'hydra_empty_passwords': 'yes',
                    'hydra_exit_on_success': 'no',
                    'hydra_ldap_dn': '',
                    'hydra_login_as_pw': 'yes',
                    'hydra_logins_file': '',
                    'hydra_parallel_tasks': '16',
                    'hydra_passwords_file': '',
                    'hydra_postgresql_db_name': '',
                    'hydra_proxy_test_site': '',
                    'hydra_timeout': '30',
                    'hydra_web_page': '',
                    'hydra_win_account_type': 'Local accounts',
                    'hydra_win_pw_as_hash': 'no',
                    'icmp_ping': 'yes',
                    'icmp_ping_retries': '2',
                    'icmp_unreach_means_host_down': 'no',
                    'log_live_hosts': 'no',
                    'max_checks_per_host': '5',
                    'max_hosts_per_scan': '30',
                    'modbus_end_reg': '16',
                    'modbus_start_reg': '0',
                    'network_receive_timeout': '5',
                    'network_type': 'Mixed (use RFC 1918)',
                    'only_portscan_if_enum_failed': 'yes',
                    'ping_the_remote_host': 'yes',
                    'portscan_range': 'default',
                    'provided_creds_only': 'yes',
                    'reduce_connections_on_congestion': 'no',
                    'report_paranoia': 'Normal',
                    'report_superseded_patches': 'yes',
                    'report_verbosity': 'Normal',
                    'request_windows_domain_info': 'yes',
                    'reverse_lookup': 'no',
                    'safe_checks': 'yes',
                    'scan_malware': 'no',
                    'scan_netware_hosts': 'no',
                    'scan_network_printers': 'no',
                    'scan_ot_devices': 'no',
                    'scan_webapps': 'no',
                    'silent_dependencies': 'yes',
                    'smtp_domain': 'example.com',
                    'smtp_from': 'nobody@example.com',
                    'smtp_to': 'postmaster@[AUTO_REPLACED_IP]',
                    'snmp_scanner': 'yes',
                    'ssh_netstat_scanner': 'yes',
                    'ssl_prob_ports': 'Known SSL ports',
                    'start_cotp_tsap': '8',
                    'stop_at_first_flaw': 'per CGI',
                    'stop_cotp_tsap': '8',
                    'stop_scan_on_disconnect': 'no',
                    'svc_detection_on_all_ports': 'yes',
                    'syn_firewall_detection': 'Automatic (normal)',
                    'syn_scanner': 'yes',
                    'tcp_firewall_detection': 'Automatic (normal)',
                    'tcp_ping': 'yes',
                    'tcp_ping_dest_ports': 'built-in',
                    'tcp_scanner': 'no',
                    'test_default_oracle_accounts': 'no',
                    'test_embedded_web_servers': 'no',
                    'test_local_nessus_host': 'yes',
                    'thorough_tests': 'no',
                    'try_all_http_methods': 'no',
                    'udp_ping': 'no',
                    'udp_scanner': 'no',
                    'unscanned_closed': 'no',
                    'url_for_rfi': 'http://rfi.nessus.org/rfi.txt',
                    'use_kernel_congestion_detection': 'no',
                    'user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
                    'verify_open_ports': 'no',
                    'webcrawl_exclude_regex': '/server_privileges\\.php|logout',
                    'webcrawl_follow_dynamic_pages': 'no',
                    'webcrawl_max_depth': '6',
                    'webcrawler_max_pages': '1000',
                    'webcrawler_start_page': '/',
                    'win_known_bad_hashes': '',
                    'win_known_good_hashes': '',
                    'wmi_netstat_scanner': 'yes',
                    'wol_mac_addresses': '',
                    'wol_wait_time': '5',
                    'yarascan_rules_file': '',
                },
                'families': [],
                'status': '0',
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
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
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'policyTemplate': {
                    'id': '1',
                    'name': 'Advanced Scan',
                    'description': 'Configure a scan without using any recommendations.',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550265753,
        },
    )
    policy = tsc.policies.create(name='Example Policy')
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


def test_policies_details_id_typeerror(tsc):
    """
    test policies details for id type error
    """
    with pytest.raises(TypeError):
        tsc.policies.details('one')


def test_policies_details_fields_typeerror(tsc):
    """
    test policies details for fields type error
    """
    with pytest.raises(TypeError):
        tsc.policies.details(1, fields='one')


@responses.activate
def test_policies_details(tsc, policy):
    """
    test policies details for success
    """
    responses.get(
        'https://nourl/rest/policy/1000007',
        json={
            'type': 'regular',
            'response': {
                'id': '1000009',
                'name': 'Example Policy',
                'description': '',
                'tags': '',
                'createdTime': '1550266947',
                'modifiedTime': '1550266947',
                'generateXCCDFResults': 'false',
                'context': '',
                'auditFiles': [],
                'preferences': {
                    'abort_generic_webapp_if_login_fails': 'no',
                    'arp_ping': 'yes',
                    'av_grace_period': '0',
                    'cert_expiry_warning_days': '60',
                    'check_crl': 'no',
                    'combo_arg_values': 'one value',
                    'detect_ssl': 'yes',
                    'disable_dns_resolution': 'no',
                    'display_unreachable_hosts': 'no',
                    'enable_file_scanning': 'no',
                    'enable_filescan_programdata': 'no',
                    'enable_filescan_programfiles': 'no',
                    'enable_filescan_programfilesx86': 'no',
                    'enable_filescan_systemroot': 'no',
                    'enable_filescan_userprofiles': 'no',
                    'enum_domain_users_end_uid': '1200',
                    'enum_domain_users_start_uid': '1000',
                    'enum_local_users_end_uid': '1200',
                    'enum_local_users_start_uid': '1000',
                    'enumerate_all_ciphers': 'yes',
                    'fast_network_discovery': 'yes',
                    'filescan_custom_dir': '',
                    'generateXCCDFResults': 'no',
                    'generic_webapp_tests': 'no',
                    'generic_webapp_tests_max_time': '5',
                    'host_whitelist': '',
                    'http_param_pollution': 'no',
                    'hydra_add_other_accounts': 'yes',
                    'hydra_always_enable': 'no',
                    'hydra_cisco_logon_pw': '',
                    'hydra_empty_passwords': 'yes',
                    'hydra_exit_on_success': 'no',
                    'hydra_ldap_dn': '',
                    'hydra_login_as_pw': 'yes',
                    'hydra_logins_file': '',
                    'hydra_parallel_tasks': '16',
                    'hydra_passwords_file': '',
                    'hydra_postgresql_db_name': '',
                    'hydra_proxy_test_site': '',
                    'hydra_timeout': '30',
                    'hydra_web_page': '',
                    'hydra_win_account_type': 'Local accounts',
                    'hydra_win_pw_as_hash': 'no',
                    'icmp_ping': 'yes',
                    'icmp_ping_retries': '2',
                    'icmp_unreach_means_host_down': 'no',
                    'log_live_hosts': 'no',
                    'max_checks_per_host': '5',
                    'max_hosts_per_scan': '30',
                    'modbus_end_reg': '16',
                    'modbus_start_reg': '0',
                    'network_receive_timeout': '5',
                    'network_type': 'Mixed (use RFC 1918)',
                    'only_portscan_if_enum_failed': 'yes',
                    'ping_the_remote_host': 'yes',
                    'portscan_range': 'default',
                    'provided_creds_only': 'yes',
                    'reduce_connections_on_congestion': 'no',
                    'report_paranoia': 'Normal',
                    'report_superseded_patches': 'yes',
                    'report_verbosity': 'Normal',
                    'request_windows_domain_info': 'yes',
                    'reverse_lookup': 'no',
                    'safe_checks': 'yes',
                    'scan_malware': 'no',
                    'scan_netware_hosts': 'no',
                    'scan_network_printers': 'no',
                    'scan_ot_devices': 'no',
                    'scan_webapps': 'no',
                    'silent_dependencies': 'yes',
                    'smtp_domain': 'example.com',
                    'smtp_from': 'nobody@example.com',
                    'smtp_to': 'postmaster@[AUTO_REPLACED_IP]',
                    'snmp_scanner': 'yes',
                    'ssh_netstat_scanner': 'yes',
                    'ssl_prob_ports': 'Known SSL ports',
                    'start_cotp_tsap': '8',
                    'stop_at_first_flaw': 'per CGI',
                    'stop_cotp_tsap': '8',
                    'stop_scan_on_disconnect': 'no',
                    'svc_detection_on_all_ports': 'yes',
                    'syn_firewall_detection': 'Automatic (normal)',
                    'syn_scanner': 'yes',
                    'tcp_firewall_detection': 'Automatic (normal)',
                    'tcp_ping': 'yes',
                    'tcp_ping_dest_ports': 'built-in',
                    'tcp_scanner': 'no',
                    'test_default_oracle_accounts': 'no',
                    'test_embedded_web_servers': 'no',
                    'test_local_nessus_host': 'yes',
                    'thorough_tests': 'no',
                    'try_all_http_methods': 'no',
                    'udp_ping': 'no',
                    'udp_scanner': 'no',
                    'unscanned_closed': 'no',
                    'url_for_rfi': 'http://rfi.nessus.org/rfi.txt',
                    'use_kernel_congestion_detection': 'no',
                    'user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
                    'verify_open_ports': 'no',
                    'webcrawl_exclude_regex': '/server_privileges\\.php|logout',
                    'webcrawl_follow_dynamic_pages': 'no',
                    'webcrawl_max_depth': '6',
                    'webcrawler_max_pages': '1000',
                    'webcrawler_start_page': '/',
                    'win_known_bad_hashes': '',
                    'win_known_good_hashes': '',
                    'wmi_netstat_scanner': 'yes',
                    'wol_mac_addresses': '',
                    'wol_wait_time': '5',
                    'yarascan_rules_file': '',
                },
                'families': [],
                'status': '0',
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
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
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'policyTemplate': {
                    'id': '1',
                    'name': 'Advanced Scan',
                    'description': 'Configure a scan without using any recommendations.',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550266947,
        },
    )
    policy = tsc.policies.details(int(policy['id']))
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


@responses.activate
def test_policies_edit(tsc, policy):
    """
    test policies edit for success
    """
    responses.patch(
        'https://nourl/rest/policy/1000007',
        json={
            'type': 'regular',
            'response': {
                'id': '1000010',
                'name': 'New Policy Name',
                'description': '',
                'tags': '',
                'createdTime': '1550267202',
                'modifiedTime': '1550267202',
                'generateXCCDFResults': 'false',
                'context': '',
                'auditFiles': [],
                'preferences': {
                    'abort_generic_webapp_if_login_fails': 'no',
                    'arp_ping': 'yes',
                    'av_grace_period': '0',
                    'cert_expiry_warning_days': '60',
                    'check_crl': 'no',
                    'combo_arg_values': 'one value',
                    'detect_ssl': 'yes',
                    'disable_dns_resolution': 'no',
                    'display_unreachable_hosts': 'no',
                    'enable_file_scanning': 'no',
                    'enable_filescan_programdata': 'no',
                    'enable_filescan_programfiles': 'no',
                    'enable_filescan_programfilesx86': 'no',
                    'enable_filescan_systemroot': 'no',
                    'enable_filescan_userprofiles': 'no',
                    'enum_domain_users_end_uid': '1200',
                    'enum_domain_users_start_uid': '1000',
                    'enum_local_users_end_uid': '1200',
                    'enum_local_users_start_uid': '1000',
                    'enumerate_all_ciphers': 'yes',
                    'fast_network_discovery': 'yes',
                    'filescan_custom_dir': '',
                    'generateXCCDFResults': 'no',
                    'generic_webapp_tests': 'no',
                    'generic_webapp_tests_max_time': '5',
                    'host_whitelist': '',
                    'http_param_pollution': 'no',
                    'hydra_add_other_accounts': 'yes',
                    'hydra_always_enable': 'no',
                    'hydra_cisco_logon_pw': '',
                    'hydra_empty_passwords': 'yes',
                    'hydra_exit_on_success': 'no',
                    'hydra_ldap_dn': '',
                    'hydra_login_as_pw': 'yes',
                    'hydra_logins_file': '',
                    'hydra_parallel_tasks': '16',
                    'hydra_passwords_file': '',
                    'hydra_postgresql_db_name': '',
                    'hydra_proxy_test_site': '',
                    'hydra_timeout': '30',
                    'hydra_web_page': '',
                    'hydra_win_account_type': 'Local accounts',
                    'hydra_win_pw_as_hash': 'no',
                    'icmp_ping': 'yes',
                    'icmp_ping_retries': '2',
                    'icmp_unreach_means_host_down': 'no',
                    'log_live_hosts': 'no',
                    'max_checks_per_host': '5',
                    'max_hosts_per_scan': '30',
                    'modbus_end_reg': '16',
                    'modbus_start_reg': '0',
                    'network_receive_timeout': '5',
                    'network_type': 'Mixed (use RFC 1918)',
                    'only_portscan_if_enum_failed': 'yes',
                    'ping_the_remote_host': 'yes',
                    'portscan_range': 'default',
                    'provided_creds_only': 'yes',
                    'reduce_connections_on_congestion': 'no',
                    'report_paranoia': 'Normal',
                    'report_superseded_patches': 'yes',
                    'report_verbosity': 'Normal',
                    'request_windows_domain_info': 'yes',
                    'reverse_lookup': 'no',
                    'safe_checks': 'yes',
                    'scan_malware': 'no',
                    'scan_netware_hosts': 'no',
                    'scan_network_printers': 'no',
                    'scan_ot_devices': 'no',
                    'scan_webapps': 'no',
                    'silent_dependencies': 'yes',
                    'smtp_domain': 'example.com',
                    'smtp_from': 'nobody@example.com',
                    'smtp_to': 'postmaster@[AUTO_REPLACED_IP]',
                    'snmp_scanner': 'yes',
                    'ssh_netstat_scanner': 'yes',
                    'ssl_prob_ports': 'Known SSL ports',
                    'start_cotp_tsap': '8',
                    'stop_at_first_flaw': 'per CGI',
                    'stop_cotp_tsap': '8',
                    'stop_scan_on_disconnect': 'no',
                    'svc_detection_on_all_ports': 'yes',
                    'syn_firewall_detection': 'Automatic (normal)',
                    'syn_scanner': 'yes',
                    'tcp_firewall_detection': 'Automatic (normal)',
                    'tcp_ping': 'yes',
                    'tcp_ping_dest_ports': 'built-in',
                    'tcp_scanner': 'no',
                    'test_default_oracle_accounts': 'no',
                    'test_embedded_web_servers': 'no',
                    'test_local_nessus_host': 'yes',
                    'thorough_tests': 'no',
                    'try_all_http_methods': 'no',
                    'udp_ping': 'no',
                    'udp_scanner': 'no',
                    'unscanned_closed': 'no',
                    'url_for_rfi': 'http://rfi.nessus.org/rfi.txt',
                    'use_kernel_congestion_detection': 'no',
                    'user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
                    'verify_open_ports': 'no',
                    'webcrawl_exclude_regex': '/server_privileges\\.php|logout',
                    'webcrawl_follow_dynamic_pages': 'no',
                    'webcrawl_max_depth': '6',
                    'webcrawler_max_pages': '1000',
                    'webcrawler_start_page': '/',
                    'win_known_bad_hashes': '',
                    'win_known_good_hashes': '',
                    'wmi_netstat_scanner': 'yes',
                    'wol_mac_addresses': '',
                    'wol_wait_time': '5',
                    'yarascan_rules_file': '',
                },
                'families': [],
                'status': 0,
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
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
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'policyTemplate': {
                    'id': '1',
                    'name': 'Advanced Scan',
                    'description': 'Configure a scan without using any recommendations.',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550267202,
        },
    )
    policy = tsc.policies.edit(int(policy['id']), name='New Policy Name')
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', int)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


@responses.activate
def test_policies_edit_for_remove_pref(tsc, policy):
    """
    test policies edit success for remove pref
    """
    responses.patch(
        'https://nourl/rest/policy/1000007',
        json={
            'type': 'regular',
            'response': {
                'id': '1000010',
                'name': 'Policy Name New',
                'description': '',
                'tags': '',
                'createdTime': '1550267202',
                'modifiedTime': '1550267202',
                'generateXCCDFResults': 'false',
                'context': '',
                'auditFiles': [],
                'status': 0,
                'canUse': 'true',
                'canManage': 'true',
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550267202,
        },
    )
    policy = tsc.policies.edit(
        int(policy['id']), name='Policy Name New', remove_prefs=['scan_malware']
    )
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'name', str)
    assert policy['name'] == 'Policy Name New'


@responses.activate
def test_policies_list(tsc):
    """
    test policies list for success
    """
    responses.get('https://nourl/rest/policy', json=POLICY)
    policies = tsc.policies.list()
    for policy in policies['manageable']:
        check(policy, 'description', str)
        check(policy, 'id', str)
        check(policy, 'name', str)


@responses.activate
def test_policies_list_for_fields(tsc):
    """
    test policies list success for fields
    """
    responses.get(
        'https://nourl/rest/policy',
        json=POLICY,
        match=[matchers.query_param_matcher({'fields': 'id,name,description,status'})],
    )
    policies = tsc.policies.list(fields=['id', 'name', 'description', 'status'])
    for policy in policies['manageable']:
        check(policy, 'description', str)
        check(policy, 'id', str)
        check(policy, 'name', str)
        check(policy, 'status', str)


def test_policies_delete_id_typeerror(tsc):
    """
    test policies delete for id type error
    """
    with pytest.raises(TypeError):
        tsc.policies.delete('nothing')


@responses.activate
def test_policies_delete(tsc, policy):
    """
    test policies delete for success
    """
    responses.delete(
        'https://nourl/rest/policy/1000007',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550267935,
        },
    )
    tsc.policies.delete(int(policy['id']))


def test_policies_copy_id_typeerror(tsc):
    """
    test policies copy for id type error
    """
    with pytest.raises(TypeError):
        tsc.policies.copy('nope')


def test_policies_copy_name_typeerror(tsc):
    """
    test policies copy for name type error
    """
    with pytest.raises(TypeError):
        tsc.policies.copy(1, name=1)


@responses.activate
def test_policies_copy(tsc, policy):
    """
    test policies copy for success
    """
    responses.post(
        'https://nourl/rest/policy/1000007/copy',
        json={
            'type': 'regular',
            'response': {
                'id': '1000013',
                'name': 'Copied Policy',
                'description': '',
                'tags': '',
                'createdTime': '1550268291',
                'modifiedTime': '1550268291',
                'generateXCCDFResults': 'false',
                'context': '',
                'auditFiles': [],
                'preferences': {
                    'abort_generic_webapp_if_login_fails': 'no',
                    'arp_ping': 'yes',
                    'av_grace_period': '0',
                    'cert_expiry_warning_days': '60',
                    'check_crl': 'no',
                    'combo_arg_values': 'one value',
                    'detect_ssl': 'yes',
                    'disable_dns_resolution': 'no',
                    'display_unreachable_hosts': 'no',
                    'enable_file_scanning': 'no',
                    'enable_filescan_programdata': 'no',
                    'enable_filescan_programfiles': 'no',
                    'enable_filescan_programfilesx86': 'no',
                    'enable_filescan_systemroot': 'no',
                    'enable_filescan_userprofiles': 'no',
                    'enum_domain_users_end_uid': '1200',
                    'enum_domain_users_start_uid': '1000',
                    'enum_local_users_end_uid': '1200',
                    'enum_local_users_start_uid': '1000',
                    'enumerate_all_ciphers': 'yes',
                    'fast_network_discovery': 'yes',
                    'filescan_custom_dir': '',
                    'generateXCCDFResults': 'no',
                    'generic_webapp_tests': 'no',
                    'generic_webapp_tests_max_time': '5',
                    'host_whitelist': '',
                    'http_param_pollution': 'no',
                    'hydra_add_other_accounts': 'yes',
                    'hydra_always_enable': 'no',
                    'hydra_cisco_logon_pw': '',
                    'hydra_empty_passwords': 'yes',
                    'hydra_exit_on_success': 'no',
                    'hydra_ldap_dn': '',
                    'hydra_login_as_pw': 'yes',
                    'hydra_logins_file': '',
                    'hydra_parallel_tasks': '16',
                    'hydra_passwords_file': '',
                    'hydra_postgresql_db_name': '',
                    'hydra_proxy_test_site': '',
                    'hydra_timeout': '30',
                    'hydra_web_page': '',
                    'hydra_win_account_type': 'Local accounts',
                    'hydra_win_pw_as_hash': 'no',
                    'icmp_ping': 'yes',
                    'icmp_ping_retries': '2',
                    'icmp_unreach_means_host_down': 'no',
                    'log_live_hosts': 'no',
                    'max_checks_per_host': '5',
                    'max_hosts_per_scan': '30',
                    'modbus_end_reg': '16',
                    'modbus_start_reg': '0',
                    'network_receive_timeout': '5',
                    'network_type': 'Mixed (use RFC 1918)',
                    'only_portscan_if_enum_failed': 'yes',
                    'ping_the_remote_host': 'yes',
                    'portscan_range': 'default',
                    'provided_creds_only': 'yes',
                    'reduce_connections_on_congestion': 'no',
                    'report_paranoia': 'Normal',
                    'report_superseded_patches': 'yes',
                    'report_verbosity': 'Normal',
                    'request_windows_domain_info': 'yes',
                    'reverse_lookup': 'no',
                    'safe_checks': 'yes',
                    'scan_malware': 'no',
                    'scan_netware_hosts': 'no',
                    'scan_network_printers': 'no',
                    'scan_ot_devices': 'no',
                    'scan_webapps': 'no',
                    'silent_dependencies': 'yes',
                    'smtp_domain': 'example.com',
                    'smtp_from': 'nobody@example.com',
                    'smtp_to': 'postmaster@[AUTO_REPLACED_IP]',
                    'snmp_scanner': 'yes',
                    'ssh_netstat_scanner': 'yes',
                    'ssl_prob_ports': 'Known SSL ports',
                    'start_cotp_tsap': '8',
                    'stop_at_first_flaw': 'per CGI',
                    'stop_cotp_tsap': '8',
                    'stop_scan_on_disconnect': 'no',
                    'svc_detection_on_all_ports': 'yes',
                    'syn_firewall_detection': 'Automatic (normal)',
                    'syn_scanner': 'yes',
                    'tcp_firewall_detection': 'Automatic (normal)',
                    'tcp_ping': 'yes',
                    'tcp_ping_dest_ports': 'built-in',
                    'tcp_scanner': 'no',
                    'test_default_oracle_accounts': 'no',
                    'test_embedded_web_servers': 'no',
                    'test_local_nessus_host': 'yes',
                    'thorough_tests': 'no',
                    'try_all_http_methods': 'no',
                    'udp_ping': 'no',
                    'udp_scanner': 'no',
                    'unscanned_closed': 'no',
                    'url_for_rfi': 'http://rfi.nessus.org/rfi.txt',
                    'use_kernel_congestion_detection': 'no',
                    'user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
                    'verify_open_ports': 'no',
                    'webcrawl_exclude_regex': '/server_privileges\\.php|logout',
                    'webcrawl_follow_dynamic_pages': 'no',
                    'webcrawl_max_depth': '6',
                    'webcrawler_max_pages': '1000',
                    'webcrawler_start_page': '/',
                    'win_known_bad_hashes': '',
                    'win_known_good_hashes': '',
                    'wmi_netstat_scanner': 'yes',
                    'wol_mac_addresses': '',
                    'wol_wait_time': '5',
                    'yarascan_rules_file': '',
                },
                'families': [],
                'status': '0',
                'groups': [],
                'canUse': 'true',
                'canManage': 'true',
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
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'policyTemplate': {
                    'id': '1',
                    'name': 'Advanced Scan',
                    'description': 'Configure a scan without using any recommendations.',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550268291,
        },
    )
    policy = tsc.policies.copy(int(policy['id']), name='Copied Policy')
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'canManage', str)
    check(policy, 'canUse', str)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


def test_policies_export_policy_id_typeerror(tsc):
    """
    test policies export for 'policy id' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.export_policy('nope')


@responses.activate
def test_policies_export_policy(tsc, policy):
    """
    test policies export for success
    """
    responses.post(
        'https://nourl/rest/policy/1000007/export',
        body='<?xml version="1.0" encoding="UTF-8"?>\n<NessusClientData_v2><Policy><policyName>Example Policy</policyName></Policy></NessusClientData_v2>',
        content_type='text/xml',
        headers={'content-disposition': 'attachment; filename="policy.1000014.1.xml"'},
    )
    with open('{}.xml'.format(policy['id']), 'wb') as pfile:
        tsc.policies.export_policy(int(policy['id']), fobj=pfile)
    os.remove('{}.xml'.format(policy['id']))


@responses.activate
def test_policies_export_policy_no_file(tsc, policy):
    """
    test policies export with no file
    """
    responses.post(
        'https://nourl/rest/policy/1000007/export',
        body='No Content',
        content_type='text/xml',
        headers={'content-disposition': 'attachment; filename="policy.1000014.1.xml"'},
    )
    with open('{}.xml'.format(policy['id']), 'wb'):
        tsc.policies.export_policy(int(policy['id']))
    os.remove('{}.xml'.format(policy['id']))


def test_policies_import_policy_name_typeerror(tsc):
    """
    test policies import for 'policy name' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.import_policy(1, '')


def test_policies_import_policy_description_typeerror(tsc):
    """
    test policies import for 'policy description' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.import_policy('Name', '', description=1)


def test_policies_import_policy_tags_typeerror(tsc):
    """
    test policies import for 'policy tags' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.import_policy('Name', '', tags=1)


@pytest.mark.datafiles(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_files', 'sc_policy.xml'
    )
)
@responses.activate
def test_policies_import_policy(tsc, datafiles):
    """
    test policies import for success
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={
            'type': 'regular',
            'response': {
                'filename': 'IoWlhe',
                'originalFilename': 'sc_policy.xml',
                'content': '',
                'context': '',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550269350,
        },
    )
    responses.post(
        'https://nourl/rest/policy/import',
        json={
            'type': 'regular',
            'response': {
                'id': '1000015',
                'name': 'Example Imported Policy',
                'description': 'Nessus Policy exported from SecurityCenter',
                'tags': '',
                'createdTime': '1550269351',
                'modifiedTime': '1550269351',
                'generateXCCDFResults': 'false',
                'context': '',
                'status': '0',
                'canUse': 'true',
                'canManage': 'true',
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550269350,
        },
    )
    with open(os.path.join(str(datafiles), 'sc_policy.xml'), 'rb') as fobj:
        tsc.policies.import_policy('Example Imported Policy', fobj)


def test_policies_share_id_typeerror(tsc):
    """
    test policies share for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.share('one')


def test_policies_share_group_typeerror(tsc):
    """
    test policies share for 'group' type error
    """
    with pytest.raises(TypeError):
        tsc.policies.share(1, 'one')


@responses.activate
def test_policies_share(tsc, policy):
    """
    test policies share for success
    """
    responses.post(
        'https://nourl/rest/policy/1000007/share',
        json={
            'type': 'regular',
            'response': {
                'id': '1000016',
                'name': 'Example Policy',
                'description': '',
                'tags': '',
                'createdTime': '1550269888',
                'modifiedTime': '1550269888',
                'generateXCCDFResults': 'false',
                'context': '',
                'auditFiles': [],
                'preferences': {
                    'abort_generic_webapp_if_login_fails': 'no',
                    'arp_ping': 'yes',
                    'av_grace_period': '0',
                    'cert_expiry_warning_days': '60',
                    'check_crl': 'no',
                    'combo_arg_values': 'one value',
                    'detect_ssl': 'yes',
                    'disable_dns_resolution': 'no',
                    'display_unreachable_hosts': 'no',
                    'enable_file_scanning': 'no',
                    'enable_filescan_programdata': 'no',
                    'enable_filescan_programfiles': 'no',
                    'enable_filescan_programfilesx86': 'no',
                    'enable_filescan_systemroot': 'no',
                    'enable_filescan_userprofiles': 'no',
                    'enum_domain_users_end_uid': '1200',
                    'enum_domain_users_start_uid': '1000',
                    'enum_local_users_end_uid': '1200',
                    'enum_local_users_start_uid': '1000',
                    'enumerate_all_ciphers': 'yes',
                    'fast_network_discovery': 'yes',
                    'filescan_custom_dir': '',
                    'generateXCCDFResults': 'no',
                    'generic_webapp_tests': 'no',
                    'generic_webapp_tests_max_time': '5',
                    'host_whitelist': '',
                    'http_param_pollution': 'no',
                    'hydra_add_other_accounts': 'yes',
                    'hydra_always_enable': 'no',
                    'hydra_cisco_logon_pw': '',
                    'hydra_empty_passwords': 'yes',
                    'hydra_exit_on_success': 'no',
                    'hydra_ldap_dn': '',
                    'hydra_login_as_pw': 'yes',
                    'hydra_logins_file': '',
                    'hydra_parallel_tasks': '16',
                    'hydra_passwords_file': '',
                    'hydra_postgresql_db_name': '',
                    'hydra_proxy_test_site': '',
                    'hydra_timeout': '30',
                    'hydra_web_page': '',
                    'hydra_win_account_type': 'Local accounts',
                    'hydra_win_pw_as_hash': 'no',
                    'icmp_ping': 'yes',
                    'icmp_ping_retries': '2',
                    'icmp_unreach_means_host_down': 'no',
                    'log_live_hosts': 'no',
                    'max_checks_per_host': '5',
                    'max_hosts_per_scan': '30',
                    'modbus_end_reg': '16',
                    'modbus_start_reg': '0',
                    'network_receive_timeout': '5',
                    'network_type': 'Mixed (use RFC 1918)',
                    'only_portscan_if_enum_failed': 'yes',
                    'ping_the_remote_host': 'yes',
                    'portscan_range': 'default',
                    'provided_creds_only': 'yes',
                    'reduce_connections_on_congestion': 'no',
                    'report_paranoia': 'Normal',
                    'report_superseded_patches': 'yes',
                    'report_verbosity': 'Normal',
                    'request_windows_domain_info': 'yes',
                    'reverse_lookup': 'no',
                    'safe_checks': 'yes',
                    'scan_malware': 'no',
                    'scan_netware_hosts': 'no',
                    'scan_network_printers': 'no',
                    'scan_ot_devices': 'no',
                    'scan_webapps': 'no',
                    'silent_dependencies': 'yes',
                    'smtp_domain': 'example.com',
                    'smtp_from': 'nobody@example.com',
                    'smtp_to': 'postmaster@[AUTO_REPLACED_IP]',
                    'snmp_scanner': 'yes',
                    'ssh_netstat_scanner': 'yes',
                    'ssl_prob_ports': 'Known SSL ports',
                    'start_cotp_tsap': '8',
                    'stop_at_first_flaw': 'per CGI',
                    'stop_cotp_tsap': '8',
                    'stop_scan_on_disconnect': 'no',
                    'svc_detection_on_all_ports': 'yes',
                    'syn_firewall_detection': 'Automatic (normal)',
                    'syn_scanner': 'yes',
                    'tcp_firewall_detection': 'Automatic (normal)',
                    'tcp_ping': 'yes',
                    'tcp_ping_dest_ports': 'built-in',
                    'tcp_scanner': 'no',
                    'test_default_oracle_accounts': 'no',
                    'test_embedded_web_servers': 'no',
                    'test_local_nessus_host': 'yes',
                    'thorough_tests': 'no',
                    'try_all_http_methods': 'no',
                    'udp_ping': 'no',
                    'udp_scanner': 'no',
                    'unscanned_closed': 'no',
                    'url_for_rfi': 'http://rfi.nessus.org/rfi.txt',
                    'use_kernel_congestion_detection': 'no',
                    'user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
                    'verify_open_ports': 'no',
                    'webcrawl_exclude_regex': '/server_privileges\\.php|logout',
                    'webcrawl_follow_dynamic_pages': 'no',
                    'webcrawl_max_depth': '6',
                    'webcrawler_max_pages': '1000',
                    'webcrawler_start_page': '/',
                    'win_known_bad_hashes': '',
                    'win_known_good_hashes': '',
                    'wmi_netstat_scanner': 'yes',
                    'wol_mac_addresses': '',
                    'wol_wait_time': '5',
                    'yarascan_rules_file': '',
                },
                'families': [],
                'status': '0',
                'groups': [],
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
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
                'policyTemplate': {
                    'id': '1',
                    'name': 'Advanced Scan',
                    'description': 'Configure a scan without using any recommendations.',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550269888,
        },
    )
    policy = tsc.policies.share(int(policy['id']), 1)
    assert isinstance(policy, dict)
    check(policy, 'auditFiles', list)
    check(policy, 'context', str)
    check(policy, 'createdTime', str)
    check(policy, 'creator', dict)
    check(policy['creator'], 'firstname', str)
    check(policy['creator'], 'id', str)
    check(policy['creator'], 'lastname', str)
    check(policy['creator'], 'username', str)
    check(policy, 'description', str)
    check(policy, 'families', list)
    check(policy, 'generateXCCDFResults', str)
    check(policy, 'groups', list)
    check(policy, 'id', str)
    check(policy, 'modifiedTime', str)
    check(policy, 'name', str)
    check(policy, 'owner', dict)
    check(policy['owner'], 'firstname', str)
    check(policy['owner'], 'id', str)
    check(policy['owner'], 'lastname', str)
    check(policy['owner'], 'username', str)
    check(policy, 'ownerGroup', dict)
    check(policy['ownerGroup'], 'description', str)
    check(policy['ownerGroup'], 'id', str)
    check(policy['ownerGroup'], 'name', str)
    check(policy, 'policyTemplate', dict)
    check(policy['policyTemplate'], 'description', str)
    check(policy['policyTemplate'], 'id', str)
    check(policy['policyTemplate'], 'name', str)
    check(policy, 'preferences', dict)
    for key in policy['preferences']:
        single(key, str)
        check(policy['preferences'], key, str)
    check(policy, 'status', str)
    check(policy, 'tags', str)
    check(policy, 'targetGroup', dict)
    check(policy['targetGroup'], 'description', str)
    check(policy['targetGroup'], 'id', int)
    check(policy['targetGroup'], 'name', str)


@responses.activate
def test_policies_tags(tsc):
    """
    test policies tags for success
    """
    responses.get(
        'https://nourl/rest/policy/tag',
        json={
            'type': 'regular',
            'response': [],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550270106,
        },
    )
    tags = tsc.policies.tags()
    for tag in tags:
        single(tag, str)
