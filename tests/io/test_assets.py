"""
test assets
"""

import uuid

import pytest
import responses

from tenable.errors import ForbiddenError, UnexpectedValueError
from tests.checker import check, single

FILTERS_WORKBENCHES_ASSETS = {
    'filters': [
        {
            'control': {
                'readable_regex': 'e.g. 192.168.0.1, 10.0.0.0/24, 201.15.99.100-201.15.99.199',
                'type': 'entry',
                'regex': '^(\\s*((?=\\d+\\.\\d+\\.\\d+\\.\\d+(?:\\/|-|\\s*,|$))(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})(?:(?:\\/(?:3[0-2]|[12]+\\d|[1-9]))|((?:-(?=\\d+\\.\\d+\\.\\d+\\.\\d+)(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.?){4})|(?:\\s*,(?:\\s*)))?)+)+$',
            },
            'name': 'ipv4',
            'operators': ['eq'],
            'readable_name': 'IPv4 Address',
        },
        {
            'control': {
                'readable_regex': 'e.g. Windows',
                'type': 'entry',
                'regex': '.*',
            },
            'name': 'operating_system',
            'operators': ['eq', 'neq', 'match'],
            'readable_name': 'Operating System',
        },
    ]
}


@responses.activate
def test_assets_list(tvm):
    """
    test to get list of assets
    """
    responses.add(
        responses.GET,
        'https://nourl/assets',
        json={
            'assets': [
                {
                    'id': 'b666e9f5-fde7-4cd8-9c07-12c19246b616',
                    'has_agent': False,
                    'last_seen': '2018-03-29T21:43:12.000Z',
                    'sources': [
                        {
                            'first_seen': '2018-03-14T20:43:03.000Z',
                            'last_seen': '2018-03-29T21:41:38.000Z',
                            'name': 'PVS',
                        }
                    ],
                    'ipv4': ['192.168.15.104'],
                    'ipv6': [],
                    'fqdn': ['docker.demo.io'],
                    'netbios_name': [],
                    'operating_system': [
                        'Linux Kernel 4.8.0-53-generic on Ubuntu 16.04'
                    ],
                    'aws_ec2_name': [],
                    'mac_address': [],
                }
            ],
            'total': 242,
        },
    )
    assets = tvm.assets.list()
    assert isinstance(assets, list)
    resp = assets[0]
    check(resp, 'aws_ec2_name', list)
    check(resp, 'fqdn', list)
    check(resp, 'has_agent', bool)
    check(resp, 'id', 'uuid')
    check(resp, 'ipv4', list)
    check(resp, 'ipv6', list)
    check(resp, 'last_seen', 'datetime')
    check(resp, 'mac_address', list)
    check(resp, 'netbios_name', list)
    check(resp, 'operating_system', list)
    check(resp, 'sources', list)
    for source in resp['sources']:
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')
        check(source, 'name', str)


def test_assets_import_assets_typeerror(tvm):
    """
    test to raise exception when type of assets param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.assets.asset_import('pytest', 1)


def test_assets_import_source_typeerror(tvm):
    """
    test to raise exception when type of source param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.assets.asset_import(
            1,
            {
                'fqdn': ['example.py.test'],
                'ipv4': ['192.168.254.1'],
                'netbios_name': '',
                'mac_address': [],
            },
        )


@responses.activate
def test_assets_import_standard_user_permissionerror(tvm):
    """
    test to raise exception when standard user try to import asset.
    """
    responses.add(
        responses.POST,
        'https://nourl/import/assets',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.assets.asset_import(
            'pytest',
            {
                'fqdn': ['example.py.test'],
                'ipv4': ['192.168.254.1'],
                'netbios_name': '',
                'mac_address': [],
            },
        )


@responses.activate
def test_assets_import(tvm):
    """
    test to import asset
    """
    responses.add(
        responses.POST,
        'https://nourl/import/assets',
        json={'asset_import_job_uuid': '5c667763-5589-4b3b-83cb-9d806efba1c4'},
    )
    resp = tvm.assets.asset_import(
        'pytest',
        {
            'fqdn': ['example.py.test'],
            'ipv4': ['192.168.254.1'],
            'netbios_name': '',
            'mac_address': [],
        },
    )
    single(resp, 'uuid')


@responses.activate
def test_assets_import_jobs(tvm):
    """
    test to get list of asset import jobs
    """
    responses.add(
        responses.GET,
        'https://nourl/import/asset-jobs',
        json={
            'asset_import_jobs': [
                {
                    'job_id': '855f118f-4f94-43fe-b461-2e7dfc68853b',
                    'container_id': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
                    'source': 'pytest',
                    'batches': 1,
                    'uploaded_assets': 1,
                    'failed_assets': 0,
                    'start_time': 1521170133233,
                    'last_update_time': 1521170133471,
                    'end_time': 1521170133471,
                    'status': 'COMPLETE',
                    'status_message': '',
                }
            ]
        },
    )
    jobs = tvm.assets.list_import_jobs()
    assert isinstance(jobs, list)
    for i in jobs:
        check(i, 'batches', int)
        check(i, 'container_id', 'uuid')
        check(i, 'end_time', int)
        check(i, 'failed_assets', int)
        check(i, 'job_id', 'uuid')
        check(i, 'last_update_time', int)
        check(i, 'source', str)
        check(i, 'start_time', int)
        check(i, 'status', str)
        check(i, 'status_message', str)
        check(i, 'uploaded_assets', int)


@responses.activate
def test_assets_import_job_info(tvm):
    """
    test to get the details about a specific asset import job
    """
    responses.add(
        responses.GET,
        'https://nourl/import/asset-jobs',
        json={
            'asset_import_jobs': [
                {
                    'job_id': '855f118f-4f94-43fe-b461-2e7dfc68853b',
                    'container_id': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
                    'source': 'pytest',
                    'batches': 1,
                    'uploaded_assets': 1,
                    'failed_assets': 0,
                    'start_time': 1521170133233,
                    'last_update_time': 1521170133471,
                    'end_time': 1521170133471,
                    'status': 'COMPLETE',
                    'status_message': '',
                }
            ]
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/import/asset-jobs/855f118f-4f94-43fe-b461-2e7dfc68853b',
        json={
            'job_id': '855f118f-4f94-43fe-b461-2e7dfc68853b',
            'container_id': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'source': 'pytest',
            'batches': 1,
            'uploaded_assets': 1,
            'failed_assets': 0,
            'start_time': 1521170133233,
            'last_update_time': 1521170133471,
            'end_time': 1521170133471,
            'status': 'COMPLETE',
            'status_message': '',
        },
    )
    jobs = tvm.assets.list_import_jobs()
    if len(jobs) > 0:
        job = tvm.assets.import_job_details(jobs[0]['job_id'])
        check(job, 'batches', int)
        check(job, 'container_id', 'uuid')
        check(job, 'end_time', int)
        check(job, 'failed_assets', int)
        check(job, 'job_id', 'uuid')
        check(job, 'last_update_time', int)
        check(job, 'source', str)
        check(job, 'start_time', int)
        check(job, 'status', str)
        check(job, 'status_message', str)
        check(job, 'uploaded_assets', int)
        assert job['job_id'] == jobs[0]['job_id']


@pytest.mark.skip("We don't want to actually delete an asset")
def test_workbenches_asset_delete_success(tvm):
    """
    test to delete the asset
    """
    asset = tvm.workbenches.assets()[0]
    tvm.workbenches.asset_delete(asset['id'])


def test_assign_tags(tvm):
    """
    test to raise exception when action param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.assets.assign_tags('foo', [], [])


def test_assets_move_assets_source_typeerror(tvm):
    """
    test to raise exception when type of source param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.assets.move_assets(1, str(uuid.uuid4()), ['127.0.0.1'])


def test_assets_move_assets_source_unexpectedvalueerror(tvm):
    """
    test to raise exception when source param value does not match the pattern.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.assets.move_assets('nope', str(uuid.uuid4()), ['127.0.0.1'])


def test_assets_move_assets_destination_typeerror(tvm):
    """
    test to raise exception when type of destination param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.assets.move_assets(str(uuid.uuid4()), 1, ['127.0.0.1'])


def test_assets_move_assets_destination_unexpectedvalueerror(tvm):
    """
    test to raise exception when destination param value does not match the pattern.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.assets.move_assets(str(uuid.uuid4()), 'nope', ['127.0.0.1'])


def test_assets_move_assets_target_typeerror(tvm):
    """
    test to raise exception when type of target param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.assets.move_assets(str(uuid.uuid4()), str(uuid.uuid4()), 1)


@pytest.mark.xfail(raises=AssertionError, reason='asset import job not completed')
@responses.activate
def test_assets_move_assets_success(tvm, network):
    """
    test to move assets from the specified network to another network
    """
    responses.add(
        responses.POST,
        'https://nourl/import/assets',
        json={'asset_import_job_uuid': '6382a3de-89b6-4347-a339-57fc6697bc87'},
    )
    responses.add(
        responses.GET,
        'https://nourl/import/asset-jobs',
        json={'asset_import_jobs': []},
    )
    responses.add(
        responses.POST,
        'https://nourl/api/v2/assets/bulk-jobs/move-to-network',
        json={'response': {'data': {'asset_count': 0}}},
        status=202,
    )
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.POST,
        'https://nourl/api/v2/assets/bulk-jobs/delete',
        json={'response': {'data': {'asset_count': 0}}},
        status=202,
    )
    ip_addr = '192.168.254.1'

    # import asset
    job_id = tvm.assets.asset_import(
        'pytest',
        {
            'fqdn': ['example.py.test'],
            'ipv4': [ip_addr],
            'netbios_name': '',
            'mac_address': [],
        },
    )

    # wait for asset to import
    iterate = True
    iterate_count = 0
    while iterate:
        # time.sleep(5)
        job = tvm.assets.list_import_jobs()
        asset = [data['status'] for data in job if job_id in data['job_id']]
        iterate_count = iterate_count + 1

        # break iteration
        if iterate_count == 5 or (len(asset) == 1 and asset[0] == 'COMPLETE'):
            break

    # move asset to new network
    # time.sleep(45)
    resp = tvm.assets.move_assets(
        '00000000-0000-0000-0000-000000000000', network['uuid'], ['192.168.254.1']
    )

    # remove imported asset
    tvm.assets.bulk_delete(('ipv4', 'eq', ip_addr))

    check(resp['response']['data'], 'asset_count', int)
    assert resp['response']['data']['asset_count'] == 1


def test_assets_bulk_delete_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.assets.bulk_delete(filter_type=1)


def test_assets_bulk_delete_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.assets.bulk_delete(filter_type='NOT')


@responses.activate
def test_assets_bulk_delete_bad_filter(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    with pytest.raises(UnexpectedValueError):
        tvm.assets.bulk_delete(('operating_system', 'contains', 'Linux'))


@pytest.mark.xfail(raises=AssertionError, reason='asset import job not completed')
@responses.activate
def test_assets_bulk_delete_success(tvm):
    """
    test to delete multiple assets
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json=FILTERS_WORKBENCHES_ASSETS,
    )
    responses.add(
        responses.POST,
        'https://nourl/import/assets',
        json={'asset_import_job_uuid': '796bde6d-46ca-4e0f-9fe9-9927ee2d9ef4'},
    )
    responses.add(
        responses.POST,
        'https://nourl/import/assets',
        json={'asset_import_job_uuid': '6ff80486-59ac-4c39-964c-920d9b408949'},
    )
    responses.add(
        responses.GET,
        'https://nourl/import/asset-jobs',
        json={
            'asset_import_jobs': [
                {
                    'job_id': '9d5bfb53-5746-4343-8900-725f0ccd0ee1',
                    'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                    'source': 'pytest',
                    'batches': 1,
                    'uploaded_assets': 1,
                    'failed_assets': 0,
                    'start_time': 1620129139511,
                    'last_update_time': 1620129140091,
                    'end_time': 1620129140091,
                    'status': 'COMPLETE',
                    'status_message': '',
                }
            ]
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/api/v2/assets/bulk-jobs/delete',
        json={'response': {'data': {'asset_count': 0}}},
        status=202,
    )
    ip_addr = '192.168.254.2'

    # import assets
    first_asset = tvm.assets.asset_import(
        'pytest',
        {
            'fqdn': ['example1.py.test'],
            'ipv4': [ip_addr],
            'netbios_name': '',
            'mac_address': [],
        },
    )
    second_asset = tvm.assets.asset_import(
        'pytest',
        {
            'fqdn': ['example2.py.test'],
            'ipv4': [ip_addr],
            'netbios_name': '',
            'mac_address': [],
        },
    )

    # wait for asset to import
    iterate = True
    iterate_count = 0
    while iterate:
        # time.sleep(5)
        job = tvm.assets.list_import_jobs()
        asset = [
            data['status']
            for data in job
            if first_asset in data['job_id'] or second_asset in data['job_id']
        ]
        iterate_count = iterate_count + 1

        # break iteration
        if iterate_count == 5 or (
            len(asset) == 2 and len(set(asset)) == 1 and asset[0] == 'COMPLETE'
        ):
            break

    # remove imported asset
    # time.sleep(45)
    resp = tvm.assets.bulk_delete(('ipv4', 'eq', ip_addr))
    check(resp['response']['data'], 'asset_count', int)
    assert resp['response']['data']['asset_count'] == 2


@responses.activate
def test_assets_details_success_fields(tvm):
    """
    test to check the details of the assets and their types
    """
    responses.add(
        responses.GET,
        'https://nourl/assets',
        json={
            'assets': [
                {
                    'id': '864502e0-4b55-4a3b-994d-4017075b89ad',
                    'has_agent': False,
                    'last_seen': '2021-06-10T11:45:02.000Z',
                    'last_scan_target': '162.159.130.79',
                    'acr_score': None,
                    'acr_drivers': None,
                    'exposure_score': 551,
                    'security_protection_level': None,
                    'exposure_confidence_value': 0.25,
                }
            ],
            'total': 13,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/assets/864502e0-4b55-4a3b-994d-4017075b89ad',
        json={
            'id': '864502e0-4b55-4a3b-994d-4017075b89ad',
            'has_agent': False,
            'created_at': '2021-06-10T11:07:45.061Z',
            'updated_at': '2021-06-16T07:48:09.167Z',
            'first_seen': '2021-06-10T11:07:43.000Z',
            'last_seen': '2021-06-10T11:45:02.000Z',
            'last_scan_target': '162.159.130.79',
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
            'exposure_score': 551,
            'scan_frequency': [],
            'interfaces': [
                {
                    'name': 'UNKNOWN',
                    'fqdn': [],
                    'mac_address': [],
                    'ipv4': ['162.159.130.79'],
                    'ipv6': [],
                }
            ],
            'network_id': ['00000000-0000-0000-0000-000000000000'],
            'ipv4': ['162.159.130.79'],
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
            'servicenow_sysid': [],
            'installed_software': [],
            'bigfix_asset_id': [],
            'security_protection_level': None,
            'security_protections': [],
            'exposure_confidence_value': 0.25,
        },
    )
    asset = tvm.assets.list()
    asset_id = [i.get('id') for i in asset][0]
    resp = tvm.assets.details(asset_id)
    assert isinstance(resp, dict)
    check(resp, 'id', 'uuid')
    check(resp, 'has_agent', bool)
    check(resp, 'created_at', 'datetime')
    check(resp, 'updated_at', 'datetime')
    check(resp, 'first_seen', 'datetime')
    check(resp, 'last_seen', 'datetime')
    check(resp, 'last_scan_target', str, allow_none=True)
    check(resp, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(resp, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(resp, 'last_scan_id', str, allow_none=True)
    check(resp, 'last_schedule_id', str, allow_none=True)
    check(resp, 'sources', list)

    for source in resp['sources']:
        check(source, 'name', str)
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')

    check(resp, 'tags', list)

    for tag in resp['tags']:
        check(tag, 'tag_uuid', 'uuid')
        check(tag, 'tag_key', str)
        check(tag, 'tag_value', str)
        check(tag, 'added_by', 'uuid')
        check(tag, 'added_at', 'datetime')

    check(resp, 'acr_score', int, allow_none=True)
    check(resp, 'exposure_score', int, allow_none=True)
    check(resp, 'acr_drivers', list, allow_none=True)
    check(resp, 'scan_frequency', list, allow_none=True)
    check(resp, 'interfaces', list)

    for interface in resp['interfaces']:
        check(interface, 'name', str)
        check(interface, 'fqdn', list)
        check(interface, 'mac_address', list)
        check(interface, 'ipv4', list)
        check(interface, 'ipv6', list)

    check(resp, 'network_id', list)
    check(resp, 'ipv4', list)
    check(resp, 'ipv6', list)
    check(resp, 'fqdn', list)
    check(resp, 'mac_address', list)
    check(resp, 'netbios_name', list)
    check(resp, 'operating_system', list)
    check(resp, 'system_type', list)
    check(resp, 'tenable_uuid', list)
    check(resp, 'hostname', list)
    check(resp, 'agent_name', list)
    check(resp, 'bios_uuid', list)
    check(resp, 'gcp_zone', list)
    check(resp, 'gcp_project_id', list)
    check(resp, 'azure_resource_id', list)
    check(resp, 'azure_vm_id', list)
    check(resp, 'aws_ec2_name', list)
    check(resp, 'aws_ec2_product_code', list)
    check(resp, 'aws_subnet_id', list)
    check(resp, 'aws_ec2_instance_type', list)
    check(resp, 'aws_ec2_instance_state_name', list)
    check(resp, 'aws_ec2_instance_group_name', list)
    check(resp, 'aws_region', list)
    check(resp, 'aws_availability_zone', list)
    check(resp, 'aws_owner_id', list)
    check(resp, 'aws_ec2_instance_ami_id', list)
    check(resp, 'aws_ec2_instance_id', list)
    check(resp, 'bigfix_asset_id', list)
    check(resp, 'installed_software', list)
    check(resp, 'servicenow_sysid', list)
    check(resp, 'qualys_host_id', list)
    check(resp, 'qualys_asset_id', list)
    check(resp, 'mcafee_epo_agent_guid', list)
    check(resp, 'mcafee_epo_guid', list)
    check(resp, 'ssh_fingerprint', list)
    check(resp, 'gcp_instance_id', list)
    check(resp, 'security_protections', list)
    check(resp, 'exposure_confidence_value', float, allow_none=True)


@responses.activate
def test_update_acr(tvm):
    """
    Test case to check update acr happens.
    """
    responses.add(
        responses.POST, 'https://nourl/api/v2/assets/bulk-jobs/acr', status=202
    )

    status_code = tvm.assets.update_acr(
        ['de2e56a2-6a0e-4757-8d00-e9ad635f6231'], ['Other'], 1, 'something'
    )
    assert status_code == 202
