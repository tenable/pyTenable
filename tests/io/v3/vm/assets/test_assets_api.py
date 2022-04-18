'''
Testing the Assets endpoint
'''
import pytest
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL = 'https://cloud.tenable.com/api/v3'
ASSET_BASE_URL = f'{BASE_URL}/assets'


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    fields = ['netbios_name', 'acr_score', 'id']
    sort = [('last_seen', 'desc')]
    filters = ('last_scan_target', 'eq', '192.0.2.57')

    payload = {
        'fields': fields,
        'limit': 200,
        'sort': [{'last_seen': 'desc'}],
        'filter': {
            'property': 'last_scan_target',
            'operator': 'eq',
            'value': '192.0.2.57',
        },
    }

    api_response = {
        'assets': [
            {
                'id': '116af8c3-969d-4621-9f9f-364eeb58e3a7',
                'has_agent': False,
                'last_seen': '2018-12-31T15:00:57.000Z',
                'last_scan_target': '192.0.2.57',
                'sources': ['source_test'],
                'acr_score': 213,
                'acr_drivers': [],
                'exposure_score': 753,
                'scan_frequency': [],
                'ipv4': ['0.0.0.0'],
                'ipv6': [],
                'fqdn': ['example.test'],
                'netbios_name': ['SCCM'],
                'operating_system': ['DOS'],
                'agent_name': ['test'],
                'aws_ec2_name': ['test_aws'],
                'mac_address': ['00:00:00:00:00:00'],
            }
        ],
        'pagination': {'total': 1},
    }
    responses.add(
        responses.POST,
        f'{ASSET_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response,
    )

    iterator = api.v3.vm.assets.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.vm.assets.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.assets.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)


@responses.activate
def test_search_host(api):
    '''
    Test the search host method
    '''
    fields = ['name', 'created', 'id']
    sort = [('created', 'desc')]
    filters = ('last_observed', 'eq', '2021-12-23T11:43:44.230Z')

    payload = {
        'fields': fields,
        'limit': 200,
        'sort': [{'created': 'desc'}],
        'filter': {
            'property': 'last_observed',
            'operator': 'eq',
            'value': '2021-12-23T11:43:44.230Z',
        },
    }

    api_response = {
        'assets': [
            {
                'aws_availability_zone': 'us-east-1c',
                'aws_subnet_id': 'subnet-3533a21e',
                'ipv6_addresses': [],
                'sources': ['AWS'],
                'aws_ec2_instance_id': 'i-03985fbcdd24af13b',
                'ipv4_addresses': ['10.255.1.90', '3.91.171.121'],
                'aws_owner_id': '422820575223',
                'display_mac_address': '12:0a:cc:b0:59:3f',
                'network': {
                    'id': '00000000-0000-0000-0000-000000000000',
                    'name': 'Default',
                },
                'display_ipv4_address': '3.91.171.121',
                'first_observed': '2021-12-23T11:43:44.230Z',
                'is_deleted': False,
                'last_observed': '2021-12-23T11:43:44.230Z',
                'aws_ec2_instance_state_name': 'running',
                'id': '001b8ab9-64b8-4693-aeeb-efe1b6e433f4',
                'aws_vpc_id': 'vpc-f4fbc091',
                'mac_addresses': ['12:0a:cc:b0:59:3f'],
                'types': ['cloud', 'host'],
                'created': '2021-12-23T11:43:44.230Z',
                'aws_ec2_instance_ami_id': 'ami-0ac9f04dbde598844',
                'observation_sources': [
                    {
                        'first_observed': '2021-12-23T11:43:43.086Z',
                        'last_observed': '2022-01-07T10:53:31.429Z',
                        'name': 'AWS',
                    }
                ],
                'is_licensed': False,
                'fqdns': [
                    'ip-10-255-1-90.ec2.internal',
                    'ec2-3-91-171-121.compute-1.amazonaws.com',
                ],
                'aws_ec2_instance_group_names': [
                    'corp-accessible',
                    'managed-ops@us-east-1.eng',
                    'nginx-router-gen2@us-east-1.eng',
                ],
                'operating_systems': ['Linux'],
                'display_fqdn': 'ip-10-255-1-90.ec2.internal',
                'display_operating_system': 'Linux',
                'aws_region': 'us-east-1',
                'system_type': 'aws-ec2-instance',
                'is_public': True,
                'name': 'ip-10-255-1-90.ec2.internal',
                'aws_ec2_name': 'nginx-router-dzix4@us-east-1.eng',
                'aws_ec2_instance_type': 'c4.xlarge',
                'updated': '2022-01-07T10:53:33.391Z',
            }
        ],
        'pagination': {'total': 1},
    }
    responses.add(
        responses.POST,
        f'{ASSET_BASE_URL}/host/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response,
    )

    iterator = api.v3.vm.assets.search_host(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.vm.assets.search_host(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.assets.search_host(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)


@responses.activate
def test_delete(api):
    asset_id = '00000000-0000-0000-0000-000000000000'
    responses.add(
        responses.DELETE, url=f'{ASSET_BASE_URL}/{asset_id}', json=None
    )
    data = api.v3.vm.assets.delete(asset_id)
    assert data.status_code == 200


@responses.activate
def test_details(api):
    details_resp = {
        'ipv6_addresses': [],
        'types': ['host'],
        'sources': ['test_v3'],
        'created': '2021-11-24T13:43:56.709Z',
        'observation_sources': [
            {
                'first_observed': '2021-11-24T13:43:56.442Z',
                'last_observed': '2021-11-24T13:43:56.442Z',
                'name': 'test_v3',
            }
        ],
        'is_licensed': False,
        'ipv4_addresses': ['192.12.13.7'],
        'network': {
            'id': '00000000-0000-0000-0000-000000000000',
            'name': 'Default',
        },
        'display_ipv4_address': '192.12.13.7',
        'first_observed': '2021-11-24T13:43:56.442Z',
        'is_deleted': False,
        'last_observed': '2021-11-24T13:43:56.442Z',
        'is_public': True,
        'name': '192.12.13.7',
        'id': '0142df77-dbc4-4706-8456-b756c06ee8a2',
        'updated': '2021-11-24T13:43:56.709Z',
    }
    asset_id = '0142df77-dbc4-4706-8456-b756c06ee8a2'
    responses.add(
        responses.GET, url=f'{ASSET_BASE_URL}/{asset_id}', json=details_resp
    )
    data = api.v3.vm.assets.details(asset_id)
    assert data == details_resp


@responses.activate
def test_asset_import(api):
    source = 'example_source'
    assets = {
        'fqdn': ['example.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': 'example',
        'mac_address': ['00:00:00:00:00:00'],
    }
    resp_data = {'asset_import_job_id': '467e5338-7783-4a0d-915a-5d00584784a0'}
    responses.add(
        responses.POST, url=f'{ASSET_BASE_URL}/import', json=resp_data
    )

    data = api.v3.vm.assets.asset_import(source, assets)
    assert data == resp_data['asset_import_job_id']


@responses.activate
def test_list_import_jobs(api):
    resp_data = {
        'asset_import_jobs': [
            {
                'job_id': 'b9584671-68e6-426b-a67c-6373778b8a0a',
                'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
                'source': 'my_source',
                'batches': 1,
                'uploaded_assets': 1,
                'failed_assets': 0,
                'start_time': '2021-11-24T13:43:56.709Z',
                'last_update_time': '2021-11-24T13:43:56.709Z',
                'end_time': '2021-11-24T13:43:56.709Z',
                'status': 'COMPLETE',
                'status_message': '',
            },
            {
                'job_id': 'fb57df61-cc1c-4c2c-9a76-1f0148c1949a',
                'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
                'source': 'my_source',
                'batches': 1,
                'uploaded_assets': 1,
                'failed_assets': 0,
                'start_time': '2021-11-24T13:43:56.709Z',
                'last_update_time': '2021-11-24T13:43:56.709Z',
                'end_time': '2021-11-24T13:43:56.709Z',
                'status': 'COMPLETE',
                'status_message': '',
            },
        ]
    }
    responses.add(
        responses.GET, url=f'{ASSET_BASE_URL}/import/jobs', json=resp_data
    )

    data = api.v3.vm.assets.list_import_jobs()
    assert data == resp_data['asset_import_jobs']


@responses.activate
def test_import_job_details(api):
    job_id = 'b9584671-68e6-426b-a67c-6373778b8a0a'
    resp_data = {
        'job_id': 'b9584671-68e6-426b-a67c-6373778b8a0a',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'source': 'my_source',
        'batches': 1,
        'uploaded_assets': 1,
        'failed_assets': 0,
        'start_time': '2021-11-24T13:43:56.709Z',
        'last_update_time': '2021-11-24T13:43:56.709Z',
        'end_time': '2021-11-24T13:43:56.709Z',
        'status': 'COMPLETE',
        'status_message': '',
    }
    responses.add(
        responses.GET,
        url=f'{ASSET_BASE_URL}/import/jobs/{job_id}',
        json=resp_data,
    )

    data = api.v3.vm.assets.import_job_details(job_id)
    assert data == resp_data


@responses.activate
def test_move_assets(api):
    source = 'b9584671-68e6-426b-a67c-6373778b8a0a'
    destination = 'b7765671-68e6-426b-a67c-6373778b8a0a'
    target = ['127.0.0.1']
    resp_data = {'response': {'data': {'asset_count': 512}}}
    responses.add(responses.PATCH, url=f'{ASSET_BASE_URL}', json=resp_data)

    data = api.v3.vm.assets.move_assets(source, destination, target)
    assert data == resp_data['response']['data']['asset_count']


@responses.activate
def test_update_acr(api):
    asset = [{
        'fqdn': ['example_one.py.test'],
        'ipv4': ['192.168.1.1'],
        'netbios_name': 'example_one',
        'mac_address': ['00:00:00:00:00:00'],
        'id': '116af8c3-969d-4621-9f9f-364eeb58e3a7'
    }]
    acr_score = 10
    note = 'test'
    reason = ['Business Critical', 'In Scope For Compliance']
    payload = {
        'asset':
            [
                {'mac_address': ['00:00:00:00:00:00'],
                 'netbios_name': 'example_one',
                 'id': '116af8c3-969d-4621-9f9f-364eeb58e3a7',
                 'ipv4': ['192.168.1.1'],
                 'fqdn': ['example_one.py.test']}
            ],
        'note': 'test',
        'acr_score': 10,
        'reason': ['Business Critical', 'In Scope For Compliance']
    }
    responses.add(
        responses.PATCH,
        url=f'{ASSET_BASE_URL}',
        match=[matchers.json_params_matcher([payload])],
        status=202
    )

    resp = api.v3.vm.assets.update_acr(acr_score=acr_score,
                                    assets=asset,
                                    reason=reason,
                                    note=note)
    assert None is resp


@responses.activate
def test_bulk_delete(api):
    job_id = 'b9584671-68e6-426b-a67c-6373778b8a0a'
    import_job_resp_data = {
        'job_id': 'b9584671-68e6-426b-a67c-6373778b8a0a',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'source': 'my_source',
        'batches': 1,
        'uploaded_assets': 1,
        'failed_assets': 0,
        'start_time': '2021-11-24T13:43:56.709Z',
        'last_update_time': '2021-11-24T13:43:56.709Z',
        'end_time': '2021-11-24T13:43:56.709Z',
        'status': 'COMPLETE',
        'status_message': '',
    }

    resp_data = {
        "data": {
            "asset_count": 1
        }
    }
    resp_filter_data = {
        "hard_delete": "true",
        "query": {
            "and": [
                {
                    "or": [
                        {"field": "types", "operator": "eq", "value": "XYZ"}
                    ]
                }
            ]
        }
    }

    responses.add(
        responses.GET,
        url=f'{ASSET_BASE_URL}/import/jobs/{job_id}',
        json=import_job_resp_data,
    )

    responses.add(
        responses.POST, url=f'{ASSET_BASE_URL}/delete', json=resp_data
    )

    responses.add(
        responses.GET, url=f'{ASSET_BASE_URL}/filters/workbenches/assets', json=resp_filter_data
    )

    import_job_response = api.v3.vm.assets.import_job_details(job_id)

    bulk_delete_response = api.v3.vm.assets.bulk_delete(
        ('types', 'eq', 'XYZ'), filter_type='or'
    )
    assert isinstance(resp_data, dict)
    assert bulk_delete_response == resp_data
    assert import_job_response["uploaded_assets"] == bulk_delete_response["data"]["asset_count"]


@pytest.mark.skip(reason="Skipping this due to dependency over tag module")
@responses.activate
def test_tags(api):
    '''
    Test case for tags method
    '''
    asset_id: str = 'c712813b-ce97-4d48-b9f2-b51bfa636dd7'

    # Let's create sample response for api endpoint
    test_response: dict = {
        'tags': [
            {
                'value_id': '173c3f3c-cb25-4f35-97e8-26b83f50c38d',
                'category_name': 'location',
                'asset_id': asset_id,
                'created_at': '2018-12-31T16:29:40.606Z',
                'source': 'static',
                'value': 'Chicago',
                'created_by': '8ba8728a-04c8-4694-bdb3-c94e04ba3ccf',
                'category_id': 'e50a526c-966f-4b80-a641-6dd359b8202e',
            },
            {
                'value_id': '6c25f771-61b6-412d-8e10-1778203f14c8',
                'category_name': 'threat',
                'asset_id': asset_id,
                'created_at': '2018-12-31T16:29:40.606Z',
                'source': 'static',
                'value': 'wannacry',
                'created_by': '8ba8728a-04c8-4694-bdb3-c94e04ba3ccf',
                'category_id': 'c9f13d31-e9f7-40e6-9830-3c770e800675',
            },
        ]
    }

    # Let's register the response for api endpoint
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/tags/assets/{asset_id}/assignments',
        json=test_response,
    )

    res = api.v3.vm.assets.tags(asset_id=asset_id)

    assert isinstance(res, dict)
    for tag in res['tags']:
        assert tag['asset_id'] == asset_id


@pytest.mark.skip(reason="Skipping this due to dependency over tag module")
@responses.activate
def test_assign_tags(api):
    '''
    Test case for tags assign method
    '''
    asset_ids: list = ['60bfce80-f695-4ed0-bd47-ec9e5b2946e5']
    tag_ids: list = ['54595f6e-648c-4570-b967-9b4e6a947634']

    # Let's create sample payload for api endpoint
    payload: dict = {'action': 'add', 'assets': asset_ids, 'tags': tag_ids}

    # Let's create sample response for api endpoint
    test_response: dict = {
        'job_id': '62210d02a7056d0297f50a8ddfbd549eaef1d0bc94e1ea3fad09'
    }

    # Let's register the response to api endpoint
    responses.add(
        responses.POST,
        url=f'{BASE_URL}/tags/assets/assignments',
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response,
    )

    res = api.v3.vm.assets.assign_tags(assets=asset_ids, tags=tag_ids)

    assert isinstance(res, str)
    assert test_response['job_id'] == res
