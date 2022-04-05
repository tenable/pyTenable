'''
Test cases for Policies API endpoint
'''
import os

import pytest
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

FILE_BASE_URL = 'https://cloud.tenable.com/api/v3/file'
FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'policies_test.nessus'
)
POLICIES_BASE_URL = r'https://cloud.tenable.com/api/v3/policies'
POLICY_ID = 25
POLICY_DETAILS = {
    'settings': {
        'patch_audit_over_telnet': 'no',
        'enable_plugin_list': 'no',
        'enumerate_all_ciphers': 'yes',
        'report_verbosity': 'Normal',
        'max_checks_per_host': '5',
        'patch_audit_over_rsh': 'no',
        'tcp_scanner': 'no',
        'icmp_unreach_means_host_down': 'no',
        'description': '',
        'custom_find_filepath_exclusions': '',
        'adsi_query': 'yes',
        'tcp_ping': 'yes',
        'enable_plugin_debugging': 'no',
        'wol_wait_time': '5',
        'syn_firewall_detection': 'Automatic (normal)',
        'reverse_lookup': 'no',
        'display_unicode_characters': 'no',
        'scan.allow_multi_target': 'no',
        'dtls_prob_ports': 'None',
        'slice_network_addresses': 'no',
        'svc_detection_on_all_ports': 'yes',
        'fast_network_discovery': 'no',
        'icmp_ping': 'yes',
        'ssh_client_banner': 'OpenSSH_5.0',
        'enable_admin_shares': 'no',
        'detect_ssl': 'yes',
        'stop_scan_on_disconnect': 'no',
        'custom_find_filesystem_exclusions': '',
        'name': 'Test Policy',
        'silent_dependencies': 'yes',
        'tcp_ping_dest_ports': 'built-in',
        'start_server_service': 'no',
        'http_login_auth_regex_nocase': 'no',
        'additional_snmp_port3': '161',
        'reduce_connections_on_congestion': 'no',
        'scan_network_printers': 'no',
        'wmi_netstat_scanner': 'yes',
        'wol_mac_addresses': '',
        'http_login_auth_regex_on_headers': 'no',
        'max_simult_tcp_sessions_per_scan': '',
        'check_crl': 'no',
        'scan_webapps': 'no',
        'udp_ping': 'no',
        'max_simult_tcp_sessions_per_host': '',
        'oracle_database_use_detected_sids': 'no',
        'start_remote_registry': 'no',
        'allow_post_scan_editing': 'yes',
        'additional_snmp_port2': '161',
        'icmp_ping_retries': '2',
        'wmi_query': 'yes',
        'ping_the_remote_host': 'yes',
        'verify_open_ports': 'no',
        'rid_brute_forcing': 'no',
        'host_tagging': 'yes',
        'provided_creds_only': 'yes',
        'additional_snmp_port1': '161',
        'report_superseded_patches': 'yes',
        'thorough_tests': 'no',
        'patch_audit_over_rexec': 'no',
        'portscan_range': 'default',
        'unscanned_closed': 'no',
        'http_login_max_redir': '0',
        'http_reauth_delay': '0',
        'log_live_hosts': 'no',
        'audit_trail': 'none',
        'snmp_scanner': 'yes',
        'network_receive_timeout': '5',
        'udp_scanner': 'no',
        'scan_netware_hosts': 'no',
        'ssl_prob_ports': 'All ports',
        'auto_accept_disclaimer': 'no',
        'report_paranoia': 'Normal',
        'never_send_win_creds_in_the_clear': 'yes',
        'safe_checks': 'yes',
        'cert_expiry_warning_days': '60',
        'ssh_port': '22',
        'dont_use_ntlmv1': 'yes',
        'only_portscan_if_enum_failed': 'yes',
        'samr_enumeration': 'yes',
        'attempt_least_privilege': 'no',
        'syn_scanner': 'yes',
        'ssh_netstat_scanner': 'yes',
        'ssh_known_hosts': '',
        'http_login_invert_auth_regex': 'no',
        'snmp_port': '161',
        'http_login_method': 'POST',
        'request_windows_domain_info': 'no',
        'scan_ot_devices': 'no',
        'test_default_oracle_accounts': 'no',
        'max_hosts_per_scan': '30',
        'display_unreachable_hosts': 'no',
        'custom_find_filepath_inclusions': '',
        'arp_ping': 'yes',
    },
    'uuid': '123e4567-e89b-12d3-a456-556642440000',
}
POLICY_IMPORT = {
    'private': 'integer',
    'id': '43',
    'no_target': 'false',
    'template_uuid': 'd684f1a6-bcf1-4a24-9bac-4a3b9bab086bd24bd260ef5f9e66',
    'description': 'An example policy.',
    'name': 'Test Policy 1',
    'owner': {
        'name': 'api@api.demo',
        'id': 3
    },
    'shared': 1,
    'user_permissions': 128,
    'last_modification_date': '2021-12-14T11:49:05Z',
    'creation_date': '2021-12-14T11:49:05Z'
}


@responses.activate
def test_configure(api):
    '''
    Test Policies configure method
    '''
    responses.add(
        responses.PUT,
        f'{POLICIES_BASE_URL}/{POLICY_ID}',
        match=[matchers.json_params_matcher(POLICY_DETAILS)]
        )
    resp = api.v3.vm.policies.configure(POLICY_ID, POLICY_DETAILS)
    assert resp is None


@responses.activate
def test_copy(api):
    '''
    Test Policies copy method
    '''
    responses.add(
        responses.POST,
        f'{POLICIES_BASE_URL}/{POLICY_ID}/copy',
        json={
            'name': 'Test Policy',
            'id': 27
        }
    )
    resp = api.v3.vm.policies.copy(POLICY_ID)
    assert resp['id'] == 27


@responses.activate
def test_create(api):
    '''
    Test Policies create method
    '''
    responses.add(
        responses.POST,
        f'{POLICIES_BASE_URL}',
        match=[matchers.json_params_matcher(POLICY_DETAILS)],
        json={
            'policy_name': 'Test Policy',
            'policy_id': 29
        }
    )
    resp = api.v3.vm.policies.create(POLICY_DETAILS)
    assert resp['policy_id'] == 29


@responses.activate
def test_delete(api):
    '''
    Test Policies delete method
    '''
    responses.add(
        responses.DELETE,
        f'{POLICIES_BASE_URL}/{POLICY_ID}'
    )
    resp = api.v3.vm.policies.delete(POLICY_ID)
    assert resp is None


@responses.activate
def test_details(api):
    '''
    Test Policies details method
    '''
    responses.add(
        responses.GET,
        f'{POLICIES_BASE_URL}/{POLICY_ID}',
        json=POLICY_DETAILS
    )
    resp = api.v3.vm.policies.details(POLICY_ID)
    assert resp == POLICY_DETAILS


@responses.activate
def test_policy_import(api):
    '''
    Test Policy import method
    '''
    responses.add(
        responses.POST,
        f'{FILE_BASE_URL}/upload',
        json={
            'fileuploaded': 'policies_test.nessus'
        }
    )
    responses.add(
        responses.POST,
        f'{POLICIES_BASE_URL}/import',
        json=POLICY_IMPORT
    )
    with open(FILE_PATH) as fobj:
        resp = api.v3.vm.policies.policy_import(fobj)
        assert resp == POLICY_IMPORT


@responses.activate
def test_policy_export(api):
    '''
    Test Policy export method
    '''
    with open(FILE_PATH, 'rb') as fobj:
        file_contents = fobj.read()
    responses.add(
        responses.GET,
        f'{POLICIES_BASE_URL}/{POLICY_ID}/export',
        body=file_contents
    )
    output_file_name = 'export_output_file.txt'
    with open(output_file_name, 'wb') as output_file_obj:
        api.v3.vm.policies.policy_export(
            POLICY_ID,
            output_file_obj
        )
    with open(output_file_name, 'rb') as output_file_obj:
        assert output_file_obj.read() == file_contents
    # Validate the method when fileObj is not passed
    res = (api.v3.vm.policies.policy_export(POLICY_ID)).read()
    assert file_contents == res
    os.remove(output_file_name)


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    test_response: dict = {
        'policies': [
            {
                'no_target': 'false',
                'template_id':
                    'd684f1a6-bcf1-4a24-9bac-4a3b9bab086bd24bd260ef5f9e66',
                'description': 'An example policy.',
                'name': 'Test Policy 1',
                'owner': {
                    'name': 'api@api.demo',
                    'id': 3
                },
                'visibility': 'shared',
                'shared': 1,
                'user_permissions': 128,
                'last_modification_date': '2021-12-14T11:49:05Z',
                'creation_date': '2021-12-14T11:49:05Z',
                'id': 43
            }
        ],
        'pagination': {
            'next': 'nextToken',
            'total': 1
        }
    }

    fields: list = [
        'id'
        'no_target',
        'template_id',
        'description',
        'name',
        'owner',
        'visibility',
        'shared',
        'user_permissions'
        'last_modification_date'
        'creation_date'
    ]

    filter = {
        'and': [
            {
                'property': 'id',
                'operator': 'eq',
                'value': 43
            },
            {
                'property': 'name',
                'operator': 'eq',
                'value': 'Test Policy 1'
            }
        ]
    }

    sort = [('id', 'asc')]

    # Let's create sample payload for search exclusion endpoint
    payload = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'id': 'asc'}],
    }

    # Let's register the mock response for search endpoint
    responses.add(
        responses.POST,
        f'{POLICIES_BASE_URL}/search',
        json=test_response,
        match=[responses.matchers.json_params_matcher(payload)],
    )

    iterator = api.v3.vm.policies.search(
        fields=fields, filter=filter, sort=sort, limit=200
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == test_response['pagination']['total']

    iterator = api.v3.vm.policies.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.policies.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)


@responses.activate
def test_templates(api):
    '''
    Test the templates method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.policies.templates()


@responses.activate
def test_templates_details(api):
    '''
    Test the template details method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.policies.template_details('basic')
