"""
test workbenches
"""

import uuid
from io import BytesIO

import pytest
import responses
from responses import matchers

from tenable.errors import NotFoundError, UnexpectedValueError
from tests.checker import check

NESSUS_REPORT = (
    '<?xml version="1.0" ?><NessusClientData_v2>'
    '<Report name="pytest-scan"><ReportHost name="127.0.0.1">'
    '<HostProperties><tag name="host-ip">127.0.0.1</tag></HostProperties>'
    '<ReportItem port="0" svc_name="general" protocol="tcp" severity="0" '
    'pluginID="19506" pluginName="Nessus Scan Information" pluginFamily="Settings">'
    '<description>Information about this scan.</description>'
    '</ReportItem></ReportHost></Report></NessusClientData_v2>'
)

FILTERS_WORKBENCHES_ASSETS = {
    'filters': [
        {
            'control': {
                'list': [{'name': 'us-east-1a', 'value': 'us-east-1a'}],
                'type': 'dropdown',
            },
            'name': 'aws_availability_zone',
            'operators': ['eq', 'neq'],
            'readable_name': 'AWS Availability Zone',
        }
    ]
}

WORKBENCHES_ASSETS = {
    'assets': [
        {
            'id': '775c6fd5-9ad6-4be5-9da4-d247a879140a',
            'has_agent': False,
            'has_plugin_results': True,
            'created_at': '2021-06-10T11:07:45.092Z',
            'terminated_at': None,
            'terminated_by': None,
            'updated_at': '2021-06-17T21:21:15.539Z',
            'first_seen': '2021-06-10T11:07:43.000Z',
            'last_seen': '2021-06-10T11:45:02.000Z',
            'first_scan_time': '2021-06-10T11:07:43.000Z',
            'last_scan_time': '2021-06-10T11:45:02.000Z',
            'last_scan_target': '162.159.130.74',
            'last_authenticated_scan_date': None,
            'last_licensed_scan_date': '2021-06-10T11:45:02.000Z',
            'last_scan_id': '9ddc6f77-d4ce-2352-b576-3fb5032d9b9e2f9714bd97fe285f',
            'last_schedule_id': '0b855588-62dc-afc9-6b17-89e3f07a4fe49f731c78911f348a',
            'sources': [
                {
                    'name': 'NESSUS_SCAN',
                    'first_seen': '2021-06-10T11:07:43.000Z',
                    'last_seen': '2021-06-10T11:45:02.000Z',
                }
            ],
            'tags': [],
            'acr_score': None,
            'acr_drivers': None,
            'exposure_score': 558,
            'interfaces': [
                {
                    'name': 'UNKNOWN',
                    'fqdn': [],
                    'mac_address': [],
                    'ipv4': ['162.159.130.74'],
                    'ipv6': [],
                }
            ],
            'network_id': ['00000000-0000-0000-0000-000000000000'],
            'ipv4': ['162.159.130.74'],
            'ipv6': [],
            'fqdn': [],
            'mac_address': [],
            'netbios_name': [],
            'operating_system': [],
            'system_type': [],
            'tenable_uuid': [],
            'hostname': [],
            'agent_name': [],
            'bios_uuid': [],
            'aws_ec2_instance_id': [],
            'aws_ec2_instance_ami_id': [],
            'aws_owner_id': [],
            'aws_availability_zone': [],
            'aws_region': [],
            'aws_vpc_id': [],
            'aws_ec2_instance_group_name': [],
            'aws_ec2_instance_state_name': [],
            'aws_ec2_instance_type': [],
            'aws_subnet_id': [],
            'aws_ec2_product_code': [],
            'aws_ec2_name': [],
            'azure_vm_id': [],
            'azure_resource_id': [],
            'gcp_project_id': [],
            'gcp_zone': [],
            'gcp_instance_id': [],
            'ssh_fingerprint': [],
            'mcafee_epo_guid': [],
            'mcafee_epo_agent_guid': [],
            'qualys_asset_id': [],
            'qualys_host_id': [],
            'manufacturer_tpm_id': [],
            'symantec_ep_hardware_key': [],
            'servicenow_sysid': [],
            'installed_software': [],
            'security_protection_level': None,
            'container_uuid': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'tag_id': [],
            'access_group_id': [],
            'acr_score_value': None,
            'exposure_score_value': 558,
            'exposure_confidence_value': 0.25,
        }
    ],
    'total': 13,
}

FILTERS_WORKBENCHES_VULNERABILITIES = {
    'filters': [
        {
            'control': {
                'readable_regex': 'e.g. Windows',
                'type': 'entry',
                'regex': '.*',
            },
            'name': 'operating_system',
            'operators': ['eq', 'neq', 'match'],
            'readable_name': 'Operating System',
            'group_name': 'asset',
        },
        {
            'name': 'severity',
            'readable_name': 'Severity',
            'control': {'type': 'dropdown_multi', 'list': ['Info', 'Low', 'Medium']},
            'operators': ['eq', 'neq'],
            'group_name': 'vulnerability',
        },
    ]
}

WORKBENCHES_ASSETS_2 = {
    'assets': [
        {
            'id': '6f64b69e-e5b9-4bb4-9624-d6b1b4b435f9',
            'has_agent': False,
            'has_plugin_results': True,
            'created_at': '2021-06-10T11:07:45.128Z',
            'terminated_at': None,
            'terminated_by': None,
            'updated_at': '2021-06-17T21:22:16.508Z',
            'first_seen': '2021-06-10T11:07:43.000Z',
            'last_seen': '2021-06-10T11:45:02.000Z',
            'first_scan_time': '2021-06-10T11:07:43.000Z',
            'last_scan_time': '2021-06-10T11:45:02.000Z',
            'last_scan_target': '162.159.130.73',
            'last_authenticated_scan_date': None,
            'last_licensed_scan_date': '2021-06-10T11:45:02.000Z',
            'last_scan_id': '9ddc6f77-d4ce-2352-b576-3fb5032d9b9e2f9714bd97fe285f',
            'last_schedule_id': '0b855588-62dc-afc9-6b17-89e3f07a4fe49f731c78911f348a',
            'acr_score': None,
            'acr_drivers': None,
            'exposure_score': 558,
            'security_protection_level': None,
            'container_uuid': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'acr_score_value': None,
            'exposure_score_value': 558,
            'exposure_confidence_value': 0.25,
        }
    ],
    'total': 13,
}

WORKBENCHES_VULNERABILITIES = {
    'vulnerabilities': [
        {
            'count': 1,
            'plugin_family': 'CentOS Local Security Checks',
            'plugin_id': 139422,
            'plugin_name': 'CentOS 7 : java-1.8.0-openjdk (CESA-2020:2968)',
            'vulnerability_state': 'New',
            'vpr_score': 6.5,
            'accepted_count': 0,
            'recasted_count': 0,
            'counts_by_severity': [{'count': 1, 'value': 2}],
            'cvss_base_score': 5.8,
            'cvss3_base_score': 4.8,
            'severity': 2,
        }
    ],
    'total_vulnerability_count': 45,
    'total_asset_count': 0,
}


pytestmark = pytest.mark.filterwarnings('ignore::DeprecationWarning')


@responses.activate
def test_workbench_assets(tvm):
    """
    test to get workbench assets
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json=WORKBENCHES_ASSETS,
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    assets = tvm.workbenches.assets()
    assert isinstance(assets, list)
    if assets:
        asset = assets[0]
        check(asset, 'access_group_id', list)
        check(asset, 'agent_name', list)
        check(asset, 'aws_availability_zone', list)
        check(asset, 'aws_ec2_instance_ami_id', list)
        check(asset, 'aws_ec2_instance_group_name', list)
        check(asset, 'aws_ec2_instance_id', list)
        check(asset, 'aws_ec2_instance_state_name', list)
        check(asset, 'aws_ec2_instance_type', list)
        check(asset, 'aws_ec2_name', list)
        check(asset, 'aws_ec2_product_code', list)
        check(asset, 'aws_owner_id', list)
        check(asset, 'aws_region', list)
        check(asset, 'aws_subnet_id', list)
        check(asset, 'aws_vpc_id', list)
        check(asset, 'azure_resource_id', list)
        check(asset, 'azure_vm_id', list)
        check(asset, 'bios_uuid', list)
        check(asset, 'created_at', 'datetime')
        check(asset, 'first_scan_time', 'datetime', allow_none=True)
        check(asset, 'first_seen', 'datetime', allow_none=True)
        check(asset, 'fqdn', list)
        check(asset, 'gcp_instance_id', list)
        check(asset, 'gcp_project_id', list)
        check(asset, 'gcp_zone', list)
        check(asset, 'has_agent', bool)
        check(asset, 'hostname', list)
        check(asset, 'id', 'uuid')
        check(asset, 'installed_software', list)
        check(asset, 'interfaces', list)
        for interface in asset['interfaces']:
            check(interface, 'fqdn', list)
            check(interface, 'ipv4', list)
            check(interface, 'ipv6', list)
            check(interface, 'mac_address', list)
            check(interface, 'name', str)
        check(asset, 'ipv4', list)
        check(asset, 'ipv6', list)
        check(asset, 'last_authenticated_scan_date', 'datetime', allow_none=True)
        check(asset, 'last_licensed_scan_date', 'datetime', allow_none=True)
        check(asset, 'last_scan_id', 'scanner-uuid', allow_none=True)
        check(asset, 'last_scan_target', str, allow_none=True)
        check(asset, 'last_schedule_id', str, allow_none=True)
        check(asset, 'last_scan_time', 'datetime', allow_none=True)
        check(asset, 'last_seen', 'datetime', allow_none=True)
        check(asset, 'mac_address', list)
        check(asset, 'manufacturer_tpm_id', list)
        check(asset, 'mcafee_epo_agent_guid', list)
        check(asset, 'mcafee_epo_guid', list)
        check(asset, 'netbios_name', list)
        check(asset, 'network_id', list)
        check(asset, 'operating_system', list)
        check(asset, 'qualys_asset_id', list)
        check(asset, 'qualys_host_id', list)
        check(asset, 'servicenow_sysid', list)
        check(asset, 'sources', list)
        for source in asset['sources']:
            check(source, 'first_seen', 'datetime')
            check(source, 'last_seen', 'datetime')
            check(source, 'name', str)
        check(asset, 'ssh_fingerprint', list)
        check(asset, 'symantec_ep_hardware_key', list)
        check(asset, 'system_type', list)
        check(asset, 'tag_id', list)
        check(asset, 'tags', list)
        check(asset, 'tenable_uuid', list)
        check(asset, 'terminated_at', 'datetime', allow_none=True)
        check(asset, 'terminated_by', str, allow_none=True)
        check(asset, 'updated_at', 'datetime')


@responses.activate
def test_workbench_asset_activity(tvm):
    """
    test to get workbench asset activity
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json=WORKBENCHES_ASSETS,
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/775c6fd5-9ad6-4be5-9da4-d247a879140a/activity',
        json={
            'activity': [
                {
                    'type': 'seen',
                    'timestamp': '2021-06-10T11:45:02.000Z',
                    'scan_id': '9ddc6f77-d4ce-2352-b576-3fb5032d9b9e2f9714bd97fe285f',
                    'schedule_id': '0b855588-62dc-afc9-6b17-89e3f07a4fe49f731c78911f348a',
                    'source': 'NESSUS_SCAN',
                }
            ]
        },
    )
    assets = tvm.workbenches.assets()
    try:
        if assets:
            history = tvm.workbenches.asset_activity(assets[0]['id'])
            assert isinstance(history, list)
            for data in history:
                check(data, 'timestamp', 'datetime')
                check(data, 'type', str)
                if data['type'] in ['tagging', 'updated']:
                    check(data, 'updates', list)
                    for update in data['updates']:
                        check(update, 'method', str)
                        check(update, 'property', str)
                        check(update, 'value', str)
                if data['type'] == 'discovered':
                    check(data, 'details', dict)
                    check(data['details'], 'assetId', 'uuid')
                    check(data['details'], 'createdAt', 'datetime')
                    check(data['details'], 'firstScanTime', 'datetime')
                    check(data['details'], 'hasAgent', bool)
                    check(data['details'], 'lastLicensedScanTime', 'datetime')
                    check(data['details'], 'lastLicensedScanTimeV2', 'datetime')
                    check(data['details'], 'lastScanTime', 'datetime')
                    check(data['details'], 'properties', dict)
                    for keys in data['details']['properties'].keys():
                        check(data['details']['properties'][keys], 'values', list)
                    check(data['details'], 'sources', list)
                    for status in data['details']['sources']:
                        check(status, 'firstSeen', 'datetime')
                        check(status, 'lastSeen', 'datetime')
                        check(status, 'name', str)
                    check(data['details'], 'updatedAt', 'datetime')
                if data['type'] in ['discovered', 'seen']:
                    check(data, 'scan_id', 'scanner-uuid')
                    check(data, 'schedule_id', str)
                    check(data, 'source', str)
    except NotFoundError:
        print('Activity for the asset uuid is not found')


def test_workbench_asset_info_all_fields_typeerror(tvm):
    """
    test to raise exception when type of all_fields param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.workbenches.asset_info('', all_fields='one')


@responses.activate
def test_workbench_asset_info(tvm):
    """
    test to get workbench assets info
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json={
            'assets': [
                {
                    'id': 'b666e9f5-fde7-4cd8-9c07-12c19246b616',
                    'has_agent': False,
                    'has_plugin_results': True,
                    'created_at': '2018-03-14T20:43:04.159Z',
                    'terminated_at': None,
                    'terminated_by': None,
                    'updated_at': '2018-03-29T21:43:13.770Z',
                    'first_seen': '2018-03-14T20:43:03.000Z',
                    'last_seen': '2018-03-29T21:43:12.000Z',
                    'first_scan_time': '2018-03-14T20:43:03.000Z',
                    'last_scan_time': '2018-03-29T21:43:12.000Z',
                    'last_authenticated_scan_date': '2018-03-29T21:42:04.000Z',
                    'last_licensed_scan_date': '2018-03-29T21:43:12.000Z',
                }
            ],
            'total': 242,
        },
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/b666e9f5-fde7-4cd8-9c07-12c19246b616/info',
        json={
            'info': {
                'time_end': '2018-03-29T21:43:12Z',
                'time_start': '2018-03-29T21:43:12Z',
                'id': 'b666e9f5-fde7-4cd8-9c07-12c19246b616',
                'uuid': 'b666e9f5-fde7-4cd8-9c07-12c19246b616',
                'has_agent': False,
                'created_at': '2018-03-14T20:43:04.159Z',
                'updated_at': '2018-03-29T21:43:13.770Z',
                'first_seen': '2018-03-14T20:43:03.000Z',
                'last_seen': '2018-03-29T21:43:12.000Z',
                'last_authenticated_scan_date': '2018-03-29T21:42:04.000Z',
                'last_licensed_scan_date': '2018-03-29T21:43:12.000Z',
            }
        },
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    assets = tvm.workbenches.assets()
    tvm.workbenches.asset_info(assets[0]['id'])


@responses.activate
def test_workbench_asset_vulns_age_typeerror(tvm):
    """
    test to raise exception when type of age param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.asset_vulns(str(uuid.uuid4()), age='none')


@responses.activate
def test_workbench_asset_vulns_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.asset_vulns(str(uuid.uuid4()), filter_type=123)


@responses.activate
def test_workbench_asset_vulns_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.asset_vulns(str(uuid.uuid4()), filter_type='NOT')


@responses.activate
def test_workbench_asset_vulns_invalid_filter(tvm):
    """
    test to raise exception when any of filter param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.asset_vulns(
            str(uuid.uuid4()), ('operating_system', 'contains', 'Linux')
        )


@responses.activate
def test_workbench_asset_vulns(tvm):
    """
    test to get workbench asset vulnerabilities
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json=WORKBENCHES_ASSETS_2,
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/6f64b69e-e5b9-4bb4-9624-d6b1b4b435f9/vulnerabilities',
        json={
            'vulnerabilities': [
                {
                    'count': 13,
                    'plugin_family': 'Web Servers',
                    'plugin_id': 10107,
                    'plugin_name': 'HTTP Server Type and Version',
                    'vulnerability_state': 'New',
                    'accepted_count': 0,
                    'recasted_count': 0,
                    'counts_by_severity': [{'count': 13, 'value': 0}],
                    'severity': 0,
                }
            ],
            'total_vulnerability_count': 54,
            'total_asset_count': 0,
        },
    )
    assets = tvm.workbenches.assets()
    if assets:
        vulns = tvm.workbenches.asset_vulns(assets[0]['id'])
        assert isinstance(vulns, list)
        if vulns:
            vulnerability = vulns[0]
            check(vulnerability, 'accepted_count', int)
            check(vulnerability, 'count', int)
            check(vulnerability, 'counts_by_severity', list)
            for counts_by_severity in vulnerability['counts_by_severity']:
                check(counts_by_severity, 'count', int)
                check(counts_by_severity, 'value', int)
            check(vulnerability, 'plugin_family', str)
            check(vulnerability, 'plugin_id', int)
            check(vulnerability, 'plugin_name', str)
            check(vulnerability, 'recasted_count', int)
            check(vulnerability, 'severity', int)
            check(vulnerability, 'vulnerability_state', str)


@responses.activate
def test_workbench_asset_vulns_filtered(tvm):
    """
    test to get filtered workbench asset vulnerabilities
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json=WORKBENCHES_ASSETS_2,
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/6f64b69e-e5b9-4bb4-9624-d6b1b4b435f9/vulnerabilities',
        json={
            'vulnerabilities': [
                {
                    'count': 13,
                    'plugin_family': 'Web Servers',
                    'plugin_id': 10107,
                    'plugin_name': 'HTTP Server Type and Version',
                    'vulnerability_state': 'New',
                    'accepted_count': 0,
                    'recasted_count': 0,
                    'counts_by_severity': [{'count': 13, 'value': 0}],
                    'severity': 0,
                }
            ],
            'total_vulnerability_count': 54,
            'total_asset_count': 0,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'filter.0.filter': 'severity',
                    'filter.0.quality': 'eq',
                    'filter.0.value': 'Info',
                }
            )
        ],
    )
    assets = tvm.workbenches.assets()
    if assets:
        vulns = tvm.workbenches.asset_vulns(assets[0]['id'], ('severity', 'eq', 'Info'))
        assert isinstance(vulns, list)
        if vulns:
            vulnerability = vulns[0]
            check(vulnerability, 'accepted_count', int)
            check(vulnerability, 'count', int)
            check(vulnerability, 'counts_by_severity', list)
            for counts_by_severity in vulnerability['counts_by_severity']:
                check(counts_by_severity, 'count', int)
                check(counts_by_severity, 'value', int)
            check(vulnerability, 'plugin_family', str)
            check(vulnerability, 'plugin_id', int)
            check(vulnerability, 'plugin_name', str)
            check(vulnerability, 'severity', int)
            check(vulnerability, 'vulnerability_state', str)


@responses.activate
def test_workbench_asset_vuln_info_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, filter_type='NOT')


@responses.activate
def test_workbench_asset_vuln_info_invalid_filter(tvm):
    """
    test to raise exception when uuid param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.asset_vuln_info(
            str(uuid.uuid4()), 19506, ('operating_system', 'contains', 'Linux')
        )


@responses.activate
def test_workbench_asset_vuln_info(tvm):
    """
    test to get workbench asset vulnerabilities info
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/vulnerabilities',
        json={
            'assets': [
                {
                    'id': '9a89c820-ef78-45a5-9573-76326189555e',
                    'severities': [
                        {'count': 0, 'level': 0, 'name': 'Info'},
                        {'count': 5, 'level': 1, 'name': 'Low'},
                    ],
                    'total': 45,
                    'fqdn': ['swat.lab.tenablesecurity.com'],
                    'ipv4': ['172.26.103.174'],
                    'ipv6': ['fe80:0:0:0:250:56ff:fea6:1425'],
                    'last_seen': '2021-06-10T12:09:19.241Z',
                    'netbios_name': [],
                    'agent_name': ['swat'],
                }
            ],
            'total_asset_count': 1,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/9a89c820-ef78-45a5-9573-76326189555e/vulnerabilities',
        json={
            'vulnerabilities': [
                {
                    'count': 6,
                    'plugin_family': 'Port scanners',
                    'plugin_id': 14272,
                    'plugin_name': 'Netstat Portscanner (SSH)',
                    'vulnerability_state': 'New',
                    'accepted_count': 0,
                    'recasted_count': 0,
                    'counts_by_severity': [{'count': 6, 'value': 0}],
                    'severity': 0,
                }
            ],
            'total_vulnerability_count': 84,
            'total_asset_count': 0,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/9a89c820-ef78-45a5-9573-76326189555e/vulnerabilities/14272/info',
        json={
            'info': {
                'count': 6,
                'vuln_count': 6,
                'recasted_count': 0,
                'accepted_count': 0,
                'description': "Nessus was able to run 'netstat' on the remote host to enumerate the open ports.\n\nSee the section 'plugins options' abou",
                'synopsis': 'Remote open ports can be enumerated via SSH.',
                'discovery': {
                    'seen_first': '2021-06-10T12:09:19.241Z',
                    'seen_last': '2021-06-10T12:09:19.241Z',
                },
                'severity': 0,
                'plugin_details': {
                    'family': 'Port scanners',
                    'modification_date': '2020-06-12T00:00:00Z',
                    'name': 'Netstat Portscanner (SSH)',
                    'publication_date': '2004-08-15T00:00:00Z',
                    'type': 'remote',
                    'version': '1.92',
                    'severity': 0,
                },
                'reference_information': [],
                'risk_information': {
                    'risk_factor': 'None',
                    'cvss_vector': None,
                    'cvss_base_score': None,
                    'cvss_temporal_vector': None,
                    'cvss_temporal_score': None,
                    'cvss3_vector': None,
                    'cvss3_base_score': None,
                    'cvss3_temporal_vector': None,
                    'cvss3_temporal_score': None,
                    'stig_severity': None,
                },
                'see_also': ['https://en.wikipedia.org/wiki/Netstat'],
            }
        },
    )
    vuln = tvm.workbenches.vuln_assets()
    if vuln and vuln[0]['ipv4']:
        vuln_list = tvm.workbenches.asset_vulns(vuln[0]['id'])
        if vuln_list:
            plugin_id = vuln_list[0]['plugin_id']
            info = tvm.workbenches.asset_vuln_info(vuln[0]['id'], plugin_id)
            check(info, 'accepted_count', int)
            check(info, 'count', int)
            check(info, 'discovery', dict)
            check(info['discovery'], 'seen_first', 'datetime', allow_none=True)
            check(info['discovery'], 'seen_last', 'datetime', allow_none=True)
            check(info, 'plugin_details', dict)
            check(info['plugin_details'], 'family', str)
            check(
                info['plugin_details'], 'modification_date', 'datetime', allow_none=True
            )
            check(info['plugin_details'], 'name', str)
            check(
                info['plugin_details'], 'publication_date', 'datetime', allow_none=True
            )
            check(info['plugin_details'], 'severity', int)
            check(info['plugin_details'], 'type', str, allow_none=True)
            check(info['plugin_details'], 'version', str, allow_none=True)
            check(info, 'recasted_count', int)
            check(info, 'reference_information', list)
            check(info, 'risk_information', dict)
            check(info['risk_information'], 'cvss3_base_score', str, allow_none=True)
            check(
                info['risk_information'], 'cvss3_temporal_score', str, allow_none=True
            )
            check(
                info['risk_information'], 'cvss3_temporal_vector', str, allow_none=True
            )
            check(info['risk_information'], 'cvss3_vector', str, allow_none=True)
            check(info['risk_information'], 'cvss_base_score', str, allow_none=True)
            check(info['risk_information'], 'cvss_temporal_score', str, allow_none=True)
            check(
                info['risk_information'], 'cvss_temporal_vector', str, allow_none=True
            )
            check(info['risk_information'], 'cvss_vector', str, allow_none=True)
            check(info['risk_information'], 'risk_factor', str, allow_none=True)
            check(info['risk_information'], 'stig_severity', str, allow_none=True)
            check(info, 'see_also', list)
            check(info, 'severity', int)
            check(info, 'vuln_count', int)


@responses.activate
def test_workbench_asset_vuln_output_age_typeerror(tvm):
    """
    test to raise exception when type of age param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, age='none')


@responses.activate
def test_workbench_asset_vuln_output_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, filter_type=123)


@responses.activate
def test_workbench_asset_vuln_output_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, filter_type='NOT')


@responses.activate
def test_workbench_asset_vuln_output_invalid_filter(tvm):
    """
    test to raise exception when any of filter param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.asset_vuln_output(
            str(uuid.uuid4()), 19506, ('operating_system', 'contains', 'Linux')
        )


@responses.activate
def test_workbench_asset_vuln_output(tvm):
    """
    test to get workbench asset vulnerabilities output
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/vulnerabilities',
        json={
            'assets': [
                {
                    'id': '9a89c820-ef78-45a5-9573-76326189555e',
                    'severities': [
                        {'count': 0, 'level': 0, 'name': 'Info'},
                        {'count': 5, 'level': 1, 'name': 'Low'},
                    ],
                    'total': 45,
                    'fqdn': ['swat.lab.tenablesecurity.com'],
                    'ipv4': ['172.26.103.174'],
                    'ipv6': ['fe80:0:0:0:250:56ff:fea6:1425'],
                    'last_seen': '2021-06-10T12:09:19.241Z',
                    'netbios_name': [],
                    'agent_name': ['swat'],
                }
            ],
            'total_asset_count': 1,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/9a89c820-ef78-45a5-9573-76326189555e/vulnerabilities',
        json={
            'vulnerabilities': [
                {
                    'count': 6,
                    'plugin_family': 'Port scanners',
                    'plugin_id': 14272,
                    'plugin_name': 'Netstat Portscanner (SSH)',
                    'vulnerability_state': 'New',
                    'accepted_count': 0,
                    'recasted_count': 0,
                    'counts_by_severity': [{'count': 6, 'value': 0}],
                    'severity': 0,
                }
            ],
            'total_vulnerability_count': 84,
            'total_asset_count': 0,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/9a89c820-ef78-45a5-9573-76326189555e/vulnerabilities/14272/outputs',
        json={
            'outputs': [
                {
                    'plugin_output': 'Port 8834/tcp was found to be open',
                    'states': [
                        {
                            'name': 'New',
                            'results': [
                                {
                                    'application_protocol': 'www',
                                    'port': 8834,
                                    'transport_protocol': 'tcp',
                                    'assets': [
                                        {
                                            'hostname': 'swat',
                                            'id': '9a89c820-ef78-45a5-9573-76326189555e',
                                            'uuid': '9a89c820-ef78-45a5-9573-76326189555e',
                                            'netbios_name': None,
                                            'fqdn': 'swat',
                                            'ipv4': '172.26.103.174',
                                            'first_seen': '2021-06-10T12:09:19.241Z',
                                            'last_seen': '2021-06-10T12:09:19.241Z',
                                        }
                                    ],
                                    'severity': 0,
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    )
    vuln = tvm.workbenches.vuln_assets()
    if vuln and vuln[0]['ipv4']:
        vuln_list = tvm.workbenches.asset_vulns(vuln[0]['id'])
        if vuln_list:
            plugin_id = vuln_list[0]['plugin_id']
            outputs = tvm.workbenches.asset_vuln_output(vuln[0]['id'], plugin_id)
            assert isinstance(outputs, list)
            output = outputs[0]
            check(output, 'plugin_output', str)
            check(output, 'states', list)
            for state in output['states']:
                check(state, 'name', str)
                check(state, 'results', list)
                for result in state['results']:
                    check(result, 'application_protocol', str, allow_none=True)
                    check(result, 'assets', list)
                    for asset in result['assets']:
                        check(asset, 'first_seen', 'datetime', allow_none=True)
                        check(asset, 'fqdn', str, allow_none=True)
                        check(asset, 'hostname', str)
                        check(asset, 'id', 'uuid')
                        check(asset, 'ipv4', str, allow_none=True)
                        check(asset, 'last_seen', 'datetime', allow_none=True)
                        check(asset, 'netbios_name', str, allow_none=True)
                        check(asset, 'uuid', 'uuid')
                    check(result, 'port', int)
                    check(result, 'severity', int)
                    check(result, 'transport_protocol', str)


@responses.activate
def test_workbench_vuln_assets(tvm):
    """
    test to get workbench vulnerability assets
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/vulnerabilities',
        json={
            'assets': [
                {
                    'id': '11c22357-e10e-4d99-8109-9c8b4c0ecb1b',
                    'severities': [
                        {'count': 0, 'level': 0, 'name': 'Info'},
                        {'count': 4, 'level': 1, 'name': 'Low'},
                    ],
                    'total': 124,
                    'fqdn': ['adam.ad.demo.io'],
                    'ipv4': ['192.168.16.133'],
                    'ipv6': [],
                    'last_seen': '2018-12-06T23:22:09.000Z',
                    'netbios_name': ['ADAM'],
                    'agent_name': [],
                }
            ],
            'total_asset_count': 47,
        },
    )
    assets = tvm.workbenches.vuln_assets()
    assert isinstance(assets, list)
    asset = assets[0]
    check(asset, 'fqdn', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4', list)
    check(asset, 'ipv6', list)
    check(asset, 'severities', list)
    for severity in asset['severities']:
        check(severity, 'count', int)
        check(severity, 'level', int)
        check(severity, 'name', str)
    check(asset, 'total', int)

    # loop on list of keys which may be present in response
    for key, value in {
        'agent_name': list,
        'last_seen': 'datetime',
        'netbios_name': list,
    }.items():
        if key in asset:
            check(asset, key, value)


@responses.activate
def test_workbench_export_format_typeerror(tvm):
    """
    test to raise exception when type of format param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.export(format=1234)


@responses.activate
def test_workbench_export_format_unexpectedvalueerror(tvm):
    """
    test to raise exception when format param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.export(format='something else')


@responses.activate
def test_workbench_export_chapters_typeerror(tvm):
    """
    test to raise exception when type of chapter param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.export(format='html', chapters='diff')


@responses.activate
def test_workbench_export_chapters_unexpectedvalueerror(tvm):
    """
    test to raise exception when chapter param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.export(format='html', chapters=['something'])


@responses.activate
def test_workbench_export_missing_chapters(tvm):
    """
    test to raise exception when chapter param value not provided with format.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.export(format='html')


@responses.activate
def test_workbench_export_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(TypeError):
        tvm.workbenches.export(filter_type=1)


@responses.activate
def test_workbench_export_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.workbenches.export(filter_type='NOT')


@responses.activate
def test_workbench_export(tvm):
    """
    test workbench export
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export',
        json={'file': 2140081529},
        match=[
            matchers.query_param_matcher(
                {
                    'report': 'vulnerabilities',
                    'chapter': 'vuln_by_asset',
                    'format': 'nessus',
                }
            )
        ],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/2140081529/status',
        json={'progress_total': '1961', 'progress': '0', 'status': 'loading'},
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/2140081529/status',
        json={'progress_total': '0', 'progress': '0', 'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/2140081529/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={
            'content-disposition': 'attachment; filename="9de2242d7b151694f571e34a11d4346a.nessus"'
        },
    )
    fobj = tvm.workbenches.export()
    assert isinstance(fobj, BytesIO)


@responses.activate
def test_workbench_vulns(tvm):
    """
    test to get workbench vulnerabilities
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities',
        json=WORKBENCHES_VULNERABILITIES,
    )
    vulns = tvm.workbenches.vulns()
    assert isinstance(vulns, list)
    if vulns:
        vulnerability = vulns[0]
        check(vulnerability, 'accepted_count', int)
        check(vulnerability, 'counts_by_severity', list)
        for counts_by_severity in vulnerability['counts_by_severity']:
            check(counts_by_severity, 'count', int)
            check(counts_by_severity, 'value', int)
        check(vulnerability, 'plugin_family', str)
        check(vulnerability, 'plugin_id', int)
        check(vulnerability, 'plugin_name', str)
        check(vulnerability, 'recasted_count', int)
        check(vulnerability, 'vulnerability_state', str)


@responses.activate
def test_workbench_vuln_info(tvm):
    """
    test to get workbench vulnerability info
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities',
        json=WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities/139422/info',
        json={
            'info': {
                'count': 1,
                'vuln_count': 1,
                'recasted_count': 0,
                'accepted_count': 0,
                'description': 'The remote CentOS Linux 7 host has packages installed that are affected by multiple vulnerabilities as referenced in the',
                'synopsis': 'The remote CentOS Linux host is missing one or more security updates.',
                'solution': 'Update the affected packages.',
                'discovery': {
                    'seen_first': '2021-06-10T12:09:19.241Z',
                    'seen_last': '2021-06-10T12:09:19.241Z',
                },
                'severity': 2,
                'plugin_details': {
                    'family': 'CentOS Local Security Checks',
                    'modification_date': '2020-11-30T00:00:00Z',
                    'name': 'CentOS 7 : java-1.8.0-openjdk (CESA-2020:2968)',
                    'publication_date': '2020-08-07T00:00:00Z',
                    'type': 'local',
                    'version': '1.3',
                    'severity': 2,
                },
                'reference_information': [],
                'risk_information': {
                    'risk_factor': 'Medium',
                    'cvss_vector': 'AV:N/AC:M/Au:N/C:P/I:P/A:N',
                    'cvss_base_score': '5.8',
                    'cvss_temporal_vector': 'E:U/RL:OF/RC:C',
                    'cvss_temporal_score': '4.3',
                    'cvss3_vector': 'AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N',
                    'cvss3_base_score': '4.8',
                    'cvss3_temporal_vector': 'E:U/RL:O/RC:C',
                    'cvss3_temporal_score': '4.2',
                    'stig_severity': None,
                },
                'see_also': [
                    'https://cwe.mitre.org/data/definitions/20.html',
                    'https://cwe.mitre.org/data/definitions/119.html',
                    'https://cwe.mitre.org/data/definitions/248.html',
                ],
            }
        },
    )
    vulns = tvm.workbenches.vulns()
    if vulns:
        info = tvm.workbenches.vuln_info(vulns[0]['plugin_id'])
        assert isinstance(info, dict)
        check(info, 'accepted_count', int)
        check(info, 'count', int)
        check(info, 'discovery', dict)
        check(info['discovery'], 'seen_first', 'datetime', allow_none=True)
        check(info['discovery'], 'seen_last', 'datetime', allow_none=True)
        check(info, 'plugin_details', dict)
        check(info['plugin_details'], 'family', str)
        check(info['plugin_details'], 'modification_date', 'datetime', allow_none=True)
        check(info['plugin_details'], 'name', str)
        check(info['plugin_details'], 'publication_date', 'datetime', allow_none=True)
        check(info['plugin_details'], 'severity', int)
        check(info['plugin_details'], 'type', str, allow_none=True)
        check(info['plugin_details'], 'version', str, allow_none=True)
        check(info, 'recasted_count', int)
        check(info, 'reference_information', list)
        check(info, 'risk_information', dict)
        check(info['risk_information'], 'cvss3_base_score', str, allow_none=True)
        check(info['risk_information'], 'cvss3_temporal_score', str, allow_none=True)
        check(info['risk_information'], 'cvss3_temporal_vector', str, allow_none=True)
        check(info['risk_information'], 'cvss3_vector', str, allow_none=True)
        check(info['risk_information'], 'cvss_base_score', str, allow_none=True)
        check(info['risk_information'], 'cvss_temporal_score', str, allow_none=True)
        check(info['risk_information'], 'cvss_temporal_vector', str, allow_none=True)
        check(info['risk_information'], 'cvss_vector', str, allow_none=True)
        check(info['risk_information'], 'risk_factor', str, allow_none=True)
        check(info['risk_information'], 'stig_severity', str, allow_none=True)
        check(info, 'see_also', list)
        check(info, 'severity', int)
        check(info, 'vuln_count', int)


@responses.activate
def test_workbench_vuln_outputs(tvm):
    """
    test to get workbench vulnerability output
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities',
        json=WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities/139422/outputs',
        json={
            'outputs': [
                {
                    'plugin_output': '\nRemote package installed : java-1.8.0-openjdk-1.8.0.252.b09-2.el7_8\nShould be                : java-1.8.0-openjdk-1.8.0',
                    'states': [
                        {
                            'name': 'New',
                            'results': [
                                {
                                    'application_protocol': None,
                                    'port': 0,
                                    'transport_protocol': 'tcp',
                                    'assets': [
                                        {
                                            'hostname': 'swat',
                                            'id': '9a89c820-ef78-45a5-9573-76326189555e',
                                            'uuid': '9a89c820-ef78-45a5-9573-76326189555e',
                                            'netbios_name': None,
                                            'fqdn': 'swat',
                                            'ipv4': '172.26.103.174',
                                            'first_seen': '2021-06-10T12:09:19.241Z',
                                            'last_seen': '2021-06-10T12:09:19.241Z',
                                        }
                                    ],
                                    'severity': 2,
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    )
    vulns = tvm.workbenches.vulns()
    if vulns:
        outputs = tvm.workbenches.vuln_outputs(vulns[0]['plugin_id'])
        assert isinstance(outputs, list)
        if outputs:
            output = outputs[0]
            check(output, 'plugin_output', str)
            check(output, 'states', list)
            for state in output['states']:
                check(state, 'name', str)
                check(state, 'results', list)
                for result in state['results']:
                    check(result, 'application_protocol', str, allow_none=True)
                    check(result, 'assets', list)
                    for asset in result['assets']:
                        check(asset, 'first_seen', 'datetime', allow_none=True)
                        check(asset, 'fqdn', str, allow_none=True)
                        check(asset, 'hostname', str)
                        check(asset, 'id', 'uuid')
                        check(asset, 'ipv4', str, allow_none=True)
                        check(asset, 'last_seen', 'datetime', allow_none=True)
                        check(asset, 'netbios_name', str, allow_none=True)
                        check(asset, 'uuid', 'uuid')
                    check(result, 'port', int)
                    check(result, 'severity', int)
                    check(result, 'transport_protocol', str)


@pytest.mark.skip("We don't want to delete asset")
def test_workbenches_asset_delete_success(tvm):
    """
    test to delete asset
    """
    asset = tvm.workbenches.assets()[0]
    tvm.workbenches.asset_delete(asset['id'])


@responses.activate
def test_workbench_assets_fields(tvm):
    """
    test to get the workbench assets and verifying their types
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json={'total': 13},
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    assets = tvm.workbenches.assets(
        all_fields=True,
        authenticated=True,
        exploitable=True,
        resolvable=True,
        severity='critical',
    )
    assert isinstance(assets, list)
    asset = assets[0]
    check(asset, 'agent_name', list)
    check(asset, 'aws_availability_zone', list)
    check(asset, 'aws_ec2_instance_ami_id', list)
    check(asset, 'aws_ec2_instance_group_name', list)
    check(asset, 'aws_ec2_instance_id', list)
    check(asset, 'aws_ec2_instance_state_name', list)
    check(asset, 'aws_ec2_instance_type', list)
    check(asset, 'aws_ec2_name', list)
    check(asset, 'aws_ec2_product_code', list)
    check(asset, 'aws_owner_id', list)
    check(asset, 'aws_region', list)
    check(asset, 'aws_subnet_id', list)
    check(asset, 'aws_vpc_id', list)
    check(asset, 'azure_resource_id', list)
    check(asset, 'azure_vm_id', list)
    check(asset, 'bios_uuid', list)
    check(asset, 'created_at', 'datetime')
    check(asset, 'first_scan_time', 'datetime', allow_none=True)
    check(asset, 'first_seen', 'datetime', allow_none=True)
    check(asset, 'fqdn', list)
    check(asset, 'gcp_instance_id', list)
    check(asset, 'gcp_project_id', list)
    check(asset, 'gcp_zone', list)
    check(asset, 'has_agent', bool)
    check(asset, 'hostname', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4', list)
    check(asset, 'ipv6', list)
    check(asset, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_scan_time', 'datetime', allow_none=True)
    check(asset, 'last_seen', 'datetime', allow_none=True)
    check(asset, 'mac_address', list)
    check(asset, 'manufacturer_tpm_id', list)
    check(asset, 'mcafee_epo_agent_guid', list)
    check(asset, 'mcafee_epo_guid', list)
    check(asset, 'netbios_name', list)
    check(asset, 'operating_system', list)
    check(asset, 'qualys_asset_id', list)
    check(asset, 'qualys_host_id', list)
    check(asset, 'servicenow_sysid', list)
    check(asset, 'sources', list)
    for source in asset['sources']:
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')
        check(source, 'name', str)
    check(asset, 'ssh_fingerprint', list)
    check(asset, 'symantec_ep_hardware_key', list)
    check(asset, 'system_type', list)
    check(asset, 'tags', list)
    check(asset, 'tenable_uuid', list)
    check(asset, 'terminated_at', 'datetime', allow_none=True)
    check(asset, 'terminated_by', str, allow_none=True)
    check(asset, 'updated_at', 'datetime')


@responses.activate
def test_workbenches_export_success(tvm):
    """
    test to export the data from vulnerability workbench
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export',
        json={'file': 244300085},
        match=[
            matchers.query_param_matcher(
                {
                    'report': 'vulnerabilities',
                    'chapter': 'vuln_by_asset',
                    'format': 'nessus',
                    'filter.search_type': 'or',
                }
            )
        ],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/244300085/status',
        json={'progress_total': '0', 'progress': '0', 'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/244300085/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={
            'Content-Disposition': 'attachment; filename="50d25632fe55ca90706ca33234ecaa40.nessus"'
        },
    )
    with open('example.nessus', 'wb') as fobj:
        tvm.workbenches.export(filter_type='or', fobj=fobj)


@responses.activate
def test_workbench_vulns_fields(tvm):
    """
    test to get the workbench vulnerabilities
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities',
        json={
            'vulnerabilities': [
                {
                    'count': 1,
                    'plugin_family': 'CentOS Local Security Checks',
                    'plugin_id': 141584,
                    'plugin_name': 'CentOS 7 : httpd (CESA-2020:3958)',
                    'vulnerability_state': 'New',
                    'vpr_score': 6.7,
                    'accepted_count': 0,
                    'recasted_count': 0,
                    'counts_by_severity': [{'count': 1, 'value': 2}],
                    'cvss_base_score': 6.8,
                    'cvss3_base_score': 8.1,
                    'severity': 2,
                }
            ],
            'total_vulnerability_count': 2,
            'total_asset_count': 0,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'authenticated': 'True',
                    'exploitable': 'True',
                    'resolvable': 'True',
                    'severity': 'medium',
                }
            )
        ],
    )
    vulns = tvm.workbenches.vulns(
        authenticated=True, severity='medium', exploitable=True, resolvable=True
    )
    assert isinstance(vulns, list)
    each_vuln = vulns[0]
    check(each_vuln, 'accepted_count', int)
    check(each_vuln, 'counts_by_severity', list)
    for data in each_vuln['counts_by_severity']:
        check(data, 'count', int)
        check(data, 'value', int)
    check(each_vuln, 'plugin_family', str)
    check(each_vuln, 'plugin_id', int)
    check(each_vuln, 'plugin_name', str)
    check(each_vuln, 'recasted_count', int)
    check(each_vuln, 'vulnerability_state', str)


@responses.activate
def test_workbench_asset_info_success(tvm):
    """
    test to get the asset information
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json={'total': 13},
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/1cbfe392-7daa-4631-aff6-d6b8e261aeac/info',
        json={},
    )
    asset = tvm.workbenches.assets()
    tvm.workbenches.asset_info(asset[0]['id'], all_fields=False)


@responses.activate
def test_workbench_assets_fields(tvm):
    """
    test to get the workbench assets and verifying their types
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json={
            'assets': [
                {
                    'id': 'b4d60aa1-a157-4ead-a23a-0a95fe8d6cb4',
                    'has_agent': False,
                    'has_plugin_results': True,
                    'created_at': '2021-06-10T11:07:45.074Z',
                    'terminated_at': None,
                    'terminated_by': None,
                    'updated_at': '2021-06-15T14:38:34.300Z',
                    'first_seen': '2021-06-10T11:07:43.000Z',
                    'last_seen': '2021-06-10T11:45:02.000Z',
                    'first_scan_time': '2021-06-10T11:07:43.000Z',
                    'last_scan_time': '2021-06-10T11:45:02.000Z',
                    'last_scan_target': '162.159.130.76',
                    'last_authenticated_scan_date': None,
                    'last_licensed_scan_date': '2021-06-10T11:45:02.000Z',
                    'last_scan_id': '9ddc6f77-d4ce-2352-b576-3fb5032d9b9e2f9714bd97fe285f',
                    'last_schedule_id': '0b855588-62dc-afc9-6b17-89e3f07a4fe49f731c78911f348a',
                    'sources': [
                        {
                            'name': 'NESSUS_SCAN',
                            'first_seen': '2021-06-10T11:07:43.000Z',
                            'last_seen': '2021-06-10T11:45:02.000Z',
                        }
                    ],
                    'tags': [],
                    'acr_score': None,
                    'acr_drivers': None,
                    'exposure_score': 522,
                    'scan_frequency': [
                        {'interval': 90, 'frequency': 5, 'licensed': False},
                        {'interval': 30, 'frequency': 5, 'licensed': False},
                    ],
                    'interfaces': [
                        {
                            'name': 'UNKNOWN',
                            'fqdn': [],
                            'mac_address': [],
                            'ipv4': ['162.159.130.76'],
                            'ipv6': [],
                        }
                    ],
                    'network_id': ['00000000-0000-0000-0000-000000000000'],
                    'ipv4': ['162.159.130.76'],
                    'ipv6': [],
                    'fqdn': [],
                    'mac_address': [],
                    'netbios_name': [],
                    'operating_system': [],
                    'system_type': [],
                    'tenable_uuid': [],
                    'hostname': [],
                    'agent_name': [],
                    'bios_uuid': [],
                    'aws_ec2_instance_id': [],
                    'aws_ec2_instance_ami_id': [],
                    'aws_owner_id': [],
                    'aws_availability_zone': [],
                    'aws_region': [],
                    'aws_vpc_id': [],
                    'aws_ec2_instance_group_name': [],
                    'aws_ec2_instance_state_name': [],
                    'aws_ec2_instance_type': [],
                    'aws_subnet_id': [],
                    'aws_ec2_product_code': [],
                    'aws_ec2_name': [],
                    'azure_vm_id': [],
                    'azure_resource_id': [],
                    'gcp_project_id': [],
                    'gcp_zone': [],
                    'gcp_instance_id': [],
                    'ssh_fingerprint': [],
                    'mcafee_epo_guid': [],
                    'mcafee_epo_agent_guid': [],
                    'qualys_asset_id': [],
                    'qualys_host_id': [],
                    'manufacturer_tpm_id': [],
                    'symantec_ep_hardware_key': [],
                    'servicenow_sysid': [],
                    'installed_software': [],
                    'bigfix_asset_id': [],
                    'security_protection_level': None,
                    'security_protections': [],
                    'container_uuid': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                    'tag_id': [],
                    'sec_ctrl_cpe': [],
                    'access_group_id': [],
                    'acr_score_value': None,
                    'exposure_score_value': 522,
                    'exposure_confidence_value': 0.25,
                }
            ],
            'total': 13,
        },
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    assets = tvm.workbenches.assets(
        all_fields=True,
        authenticated=True,
        exploitable=True,
        resolvable=True,
        severity='critical',
    )
    assert isinstance(assets, list)
    asset = assets[0]
    check(asset, 'agent_name', list)
    check(asset, 'aws_availability_zone', list)
    check(asset, 'aws_ec2_instance_ami_id', list)
    check(asset, 'aws_ec2_instance_group_name', list)
    check(asset, 'aws_ec2_instance_id', list)
    check(asset, 'aws_ec2_instance_state_name', list)
    check(asset, 'aws_ec2_instance_type', list)
    check(asset, 'aws_ec2_name', list)
    check(asset, 'aws_ec2_product_code', list)
    check(asset, 'aws_owner_id', list)
    check(asset, 'aws_region', list)
    check(asset, 'aws_subnet_id', list)
    check(asset, 'aws_vpc_id', list)
    check(asset, 'azure_resource_id', list)
    check(asset, 'azure_vm_id', list)
    check(asset, 'bios_uuid', list)
    check(asset, 'created_at', 'datetime')
    check(asset, 'first_scan_time', 'datetime', allow_none=True)
    check(asset, 'first_seen', 'datetime', allow_none=True)
    check(asset, 'fqdn', list)
    check(asset, 'gcp_instance_id', list)
    check(asset, 'gcp_project_id', list)
    check(asset, 'gcp_zone', list)
    check(asset, 'has_agent', bool)
    check(asset, 'hostname', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4', list)
    check(asset, 'ipv6', list)
    check(asset, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_scan_time', 'datetime', allow_none=True)
    check(asset, 'last_seen', 'datetime', allow_none=True)
    check(asset, 'mac_address', list)
    check(asset, 'manufacturer_tpm_id', list)
    check(asset, 'mcafee_epo_agent_guid', list)
    check(asset, 'mcafee_epo_guid', list)
    check(asset, 'netbios_name', list)
    check(asset, 'operating_system', list)
    check(asset, 'qualys_asset_id', list)
    check(asset, 'qualys_host_id', list)
    check(asset, 'servicenow_sysid', list)
    check(asset, 'sources', list)
    for source in asset['sources']:
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')
        check(source, 'name', str)
    check(asset, 'ssh_fingerprint', list)
    check(asset, 'symantec_ep_hardware_key', list)
    check(asset, 'system_type', list)
    check(asset, 'tags', list)
    check(asset, 'tenable_uuid', list)
    check(asset, 'terminated_at', 'datetime', allow_none=True)
    check(asset, 'terminated_by', str, allow_none=True)
    check(asset, 'updated_at', 'datetime')


@responses.activate
def test_workbenches_export_success(tvm):
    """
    test to export the data from vulnerability workbench
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export',
        json={'file': 244300085},
        match=[
            matchers.query_param_matcher(
                {
                    'report': 'vulnerabilities',
                    'chapter': 'vuln_by_asset',
                    'format': 'nessus',
                    'filter.search_type': 'or',
                }
            )
        ],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/244300085/status',
        json={'progress_total': '0', 'progress': '0', 'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/export/244300085/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={
            'Content-Disposition': 'attachment; filename="50d25632fe55ca90706ca33234ecaa40.nessus"'
        },
    )
    with open('example.nessus', 'wb') as fobj:
        tvm.workbenches.export(filter_type='or', fobj=fobj)


@responses.activate
def test_workbench_vulns_fields(tvm):
    """
    test to get the workbench vulnerabilities
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json=FILTERS_WORKBENCHES_VULNERABILITIES,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/vulnerabilities',
        json={
            'vulnerabilities': [
                {
                    'count': 1,
                    'plugin_family': 'CentOS Local Security Checks',
                    'plugin_id': 141584,
                    'plugin_name': 'CentOS 7 : httpd (CESA-2020:3958)',
                    'vulnerability_state': 'New',
                    'vpr_score': 6.7,
                    'accepted_count': 0,
                    'recasted_count': 0,
                    'counts_by_severity': [{'count': 1, 'value': 2}],
                    'cvss_base_score': 6.8,
                    'cvss3_base_score': 8.1,
                    'severity': 2,
                }
            ],
            'total_vulnerability_count': 2,
            'total_asset_count': 0,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'authenticated': 'True',
                    'exploitable': 'True',
                    'resolvable': 'True',
                    'severity': 'medium',
                }
            )
        ],
    )
    vulns = tvm.workbenches.vulns(
        authenticated=True, severity='medium', exploitable=True, resolvable=True
    )
    assert isinstance(vulns, list)
    each_vuln = vulns[0]
    check(each_vuln, 'accepted_count', int)
    check(each_vuln, 'counts_by_severity', list)
    for data in each_vuln['counts_by_severity']:
        check(data, 'count', int)
        check(data, 'value', int)
    check(each_vuln, 'plugin_family', str)
    check(each_vuln, 'plugin_id', int)
    check(each_vuln, 'plugin_name', str)
    check(each_vuln, 'recasted_count', int)
    check(each_vuln, 'vulnerability_state', str)


@responses.activate
def test_workbench_asset_info_success(tvm):
    """
    test to get the asset information
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets',
        json={
            'assets': [
                {
                    'id': '1cbfe392-7daa-4631-aff6-d6b8e261aeac',
                    'has_agent': False,
                    'has_plugin_results': True,
                    'created_at': '2021-06-10T11:07:45.091Z',
                    'terminated_at': None,
                    'terminated_by': None,
                    'updated_at': '2021-06-17T08:50:05.018Z',
                    'first_seen': '2021-06-10T11:07:43.000Z',
                    'last_seen': '2021-06-10T11:45:02.000Z',
                    'first_scan_time': '2021-06-10T11:07:43.000Z',
                    'last_scan_time': '2021-06-10T11:45:02.000Z',
                    'last_scan_target': '162.159.130.78',
                    'last_authenticated_scan_date': None,
                    'last_licensed_scan_date': '2021-06-10T11:45:02.000Z',
                    'last_scan_id': '9ddc6f77-d4ce-2352-b576-3fb5032d9b9e2f9714bd97fe285f',
                    'last_schedule_id': '0b855588-62dc-afc9-6b17-89e3f07a4fe49f731c78911f348a',
                    'sources': [
                        {
                            'name': 'NESSUS_SCAN',
                            'first_seen': '2021-06-10T11:07:43.000Z',
                            'last_seen': '2021-06-10T11:45:02.000Z',
                        }
                    ],
                    'tags': [],
                    'acr_score': None,
                    'acr_drivers': None,
                    'exposure_score': 549,
                    'scan_frequency': [
                        {'interval': 90, 'frequency': 7, 'licensed': False},
                        {'interval': 30, 'frequency': 7, 'licensed': False},
                    ],
                    'interfaces': [
                        {
                            'name': 'UNKNOWN',
                            'fqdn': [],
                            'mac_address': [],
                            'ipv4': ['162.159.130.78'],
                            'ipv6': [],
                        }
                    ],
                    'network_id': ['00000000-0000-0000-0000-000000000000'],
                    'ipv4': ['162.159.130.78'],
                    'ipv6': [],
                    'fqdn': [],
                    'mac_address': [],
                    'netbios_name': [],
                    'operating_system': [],
                    'system_type': [],
                    'tenable_uuid': [],
                    'hostname': [],
                    'agent_name': [],
                    'bios_uuid': [],
                    'aws_ec2_instance_id': [],
                    'aws_ec2_instance_ami_id': [],
                    'aws_owner_id': [],
                    'aws_availability_zone': [],
                    'aws_region': [],
                    'aws_vpc_id': [],
                    'aws_ec2_instance_group_name': [],
                    'aws_ec2_instance_state_name': [],
                    'aws_ec2_instance_type': [],
                    'aws_subnet_id': [],
                    'aws_ec2_product_code': [],
                    'aws_ec2_name': [],
                    'azure_vm_id': [],
                    'azure_resource_id': [],
                    'gcp_project_id': [],
                    'gcp_zone': [],
                    'gcp_instance_id': [],
                    'ssh_fingerprint': [],
                    'mcafee_epo_guid': [],
                    'mcafee_epo_agent_guid': [],
                    'qualys_asset_id': [],
                    'qualys_host_id': [],
                    'manufacturer_tpm_id': [],
                    'symantec_ep_hardware_key': [],
                    'servicenow_sysid': [],
                    'installed_software': [],
                    'bigfix_asset_id': [],
                    'security_protection_level': None,
                    'security_protections': [],
                    'container_uuid': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                    'tag_id': [],
                    'sec_ctrl_cpe': [],
                    'access_group_id': [],
                    'acr_score_value': None,
                    'exposure_score_value': 549,
                    'exposure_confidence_value': 0.25,
                }
            ],
            'total': 13,
        },
        match=[matchers.query_param_matcher({'all_fields': 'full'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/workbenches/assets/1cbfe392-7daa-4631-aff6-d6b8e261aeac/info',
        json={
            'info': {
                'time_end': '2021-06-10T11:45:02Z',
                'time_start': '2021-06-10T11:45:02Z',
                'id': '1cbfe392-7daa-4631-aff6-d6b8e261aeac',
                'uuid': '1cbfe392-7daa-4631-aff6-d6b8e261aeac',
                'operating_system': [],
                'counts': {
                    'vulnerabilities': {
                        'total': 6,
                        'severities': [
                            {'count': 54, 'level': 0, 'name': 'Info'},
                            {'count': 0, 'level': 1, 'name': 'Low'},
                        ],
                    },
                    'audits': {
                        'total': 0,
                        'statuses': [
                            {'count': 0, 'level': 1, 'name': 'Passed'},
                            {'count': 0, 'level': 2, 'name': 'Warning'},
                        ],
                    },
                },
                'has_agent': False,
                'created_at': '2021-06-10T11:07:45.091Z',
                'updated_at': '2021-06-17T08:50:05.018Z',
                'first_seen': '2021-06-10T11:07:43.000Z',
                'last_seen': '2021-06-10T11:45:02.000Z',
                'last_scan_target': '162.159.130.78',
                'last_authenticated_scan_date': None,
                'last_licensed_scan_date': '2021-06-10T11:45:02.000Z',
                'last_scan_id': '9ddc6f77-d4ce-2352-b576-3fb5032d9b9e2f9714bd97fe285f',
                'last_schedule_id': '0b855588-62dc-afc9-6b17-89e3f07a4fe49f731c78911f348a',
                'sources': [
                    {
                        'name': 'NESSUS_SCAN',
                        'first_seen': '2021-06-10T11:07:43.000Z',
                        'last_seen': '2021-06-10T11:45:02.000Z',
                    }
                ],
                'tags': [],
                'acr_score': None,
                'acr_drivers': None,
                'exposure_score': 549,
                'scan_frequency': [
                    {'interval': 90, 'frequency': 7, 'licensed': False},
                    {'interval': 30, 'frequency': 7, 'licensed': False},
                ],
                'interfaces': [
                    {
                        'name': 'UNKNOWN',
                        'fqdn': [],
                        'mac_address': [],
                        'ipv4': ['162.159.130.78'],
                        'ipv6': [],
                    }
                ],
                'ipv4': ['162.159.130.78'],
                'ipv6': [],
                'fqdn': [],
                'mac_address': [],
                'netbios_name': [],
                'system_type': [],
                'tenable_uuid': [],
                'hostname': [],
                'agent_name': [],
                'bios_uuid': [],
                'aws_ec2_instance_id': [],
                'aws_ec2_instance_ami_id': [],
                'aws_owner_id': [],
                'aws_availability_zone': [],
                'aws_region': [],
                'aws_vpc_id': [],
                'aws_ec2_instance_group_name': [],
                'aws_ec2_instance_state_name': [],
                'aws_ec2_instance_type': [],
                'aws_subnet_id': [],
                'aws_ec2_product_code': [],
                'aws_ec2_name': [],
                'azure_vm_id': [],
                'azure_resource_id': [],
                'gcp_project_id': [],
                'gcp_zone': [],
                'gcp_instance_id': [],
                'ssh_fingerprint': [],
                'mcafee_epo_guid': [],
                'mcafee_epo_agent_guid': [],
                'qualys_asset_id': [],
                'qualys_host_id': [],
                'servicenow_sysid': [],
                'installed_software': [],
                'bigfix_asset_id': [],
                'security_protection_level': None,
                'security_protections': [],
                'exposure_confidence_value': 0.25,
                'network_name': 'Default',
            }
        },
    )
    asset = tvm.workbenches.assets()
    tvm.workbenches.asset_info(asset[0]['id'], all_fields=False)
