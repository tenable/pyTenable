'''
Testing the Assets endpoint
'''
import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL = 'https://cloud.tenable.com/api/v3'
ASSET_BASE_URL = f'{BASE_URL}/assets'


@responses.activate
def test_search_webapp(api):
    '''
    Test the search webapp method
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
        f'{ASSET_BASE_URL}/webapp/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response,
    )

    iterator = api.v3.vm.assets.search_webapp(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.vm.assets.search_webapp(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.assets.search_webapp(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)
