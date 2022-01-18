'''
Testing the Assets endpoint
'''
import pytest
import responses

from tenable.io.v3.base.iterators.explore_iterator import CSVChunkIterator

ASSET_BASE_URL = r'https://cloud.tenable.com/api/v3/assets'

REQUESTDATA = dict(
    fields=['test1', 'test2'],
    filter=('netbios_name', 'eq', 'SCCM'),
    limit=10,
    sort=[('name', 'asc')],
    return_csv=True
)


def test_search(api):
    csv_iterator = api.v3.assets.search(
        **REQUESTDATA
    )
    assert isinstance(csv_iterator, CSVChunkIterator)


@responses.activate
def test_delete(api):
    asset_id = '00000000-0000-0000-0000-000000000000'
    responses.add(
        responses.DELETE,
        url=f'{ASSET_BASE_URL}/{asset_id}',
        json=None
    )
    data = api.v3.assets.delete(asset_id)
    assert data.status_code == 200


@responses.activate
def test_details(api):
    details_resp = {'ipv6_addresses': [], 'types': ['host'],
                    'sources': ['test_v3'],
                    'created': '2021-11-24T13:43:56.709Z',
                    'observation_sources': [
                        {'first_observed': '2021-11-24T13:43:56.442Z',
                         'last_observed': '2021-11-24T13:43:56.442Z',
                         'name': 'test_v3'}], 'is_licensed': False,
                    'ipv4_addresses': ['192.12.13.7'],
                    'network': {'id': '00000000-0000-0000-0000-000000000000',
                                'name': 'Default'},
                    'display_ipv4_address': '192.12.13.7',
                    'first_observed': '2021-11-24T13:43:56.442Z',
                    'is_deleted': False,
                    'last_observed': '2021-11-24T13:43:56.442Z',
                    'is_public': True, 'name': '192.12.13.7',
                    'id': '0142df77-dbc4-4706-8456-b756c06ee8a2',
                    'updated': '2021-11-24T13:43:56.709Z'}
    asset_id = '0142df77-dbc4-4706-8456-b756c06ee8a2'
    responses.add(
        responses.GET,
        url=f'{ASSET_BASE_URL}/{asset_id}',
        json=details_resp
    )
    data = api.v3.assets.details(asset_id)
    assert data == details_resp


@responses.activate
def test_asset_import(api):
    source = 'example_source'
    assets = {
        'fqdn': ['example.py.test'],
        'ipv4': ['192.168.254.1'],
        'netbios_name': 'example',
        'mac_address': ['00:00:00:00:00:00']
    }
    resp_data = {
        'asset_import_job_uuid': '467e5338-7783-4a0d-915a-5d00584784a0'
    }
    responses.add(
        responses.POST,
        url=f'{ASSET_BASE_URL}/import',
        json=resp_data
    )

    data = api.v3.assets.asset_import(source, assets)
    assert data == resp_data['asset_import_job_uuid']


@responses.activate
def test_list_import_jobs(api):
    resp_data = {'asset_import_jobs': [
        {
            'job_id': 'b9584671-68e6-426b-a67c-6373778b8a0a',
            'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
            'source': 'my_source',
            'batches': 1,
            'uploaded_assets': 1,
            'failed_assets': 0,
            'start_time': 1637000199986,
            'last_update_time': 1637000201930,
            'end_time': 1637000201930,
            'status': 'COMPLETE',
            'status_message': ""
        },
        {
            'job_id': 'fb57df61-cc1c-4c2c-9a76-1f0148c1949a',
            'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
            'source': 'my_source',
            'batches': 1,
            'uploaded_assets': 1,
            'failed_assets': 0,
            'start_time': 1637000271655,
            'last_update_time': 1637000272765,
            'end_time': 1637000272765,
            'status': 'COMPLETE',
            'status_message': ""
        },
    ]}
    responses.add(
        responses.GET,
        url=f'{ASSET_BASE_URL}/import/jobs',
        json=resp_data
    )

    data = api.v3.assets.list_import_jobs()
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
        'start_time': 1637000199986,
        'last_update_time': 1637000201930,
        'end_time': 1637000201930,
        'status': 'COMPLETE',
        'status_message': ""
    }
    responses.add(
        responses.GET,
        url=f'{ASSET_BASE_URL}/import/jobs/{job_id}',
        json=resp_data
    )

    data = api.v3.assets.import_job_details(job_id)
    assert data == resp_data


@responses.activate
def test_move_assets(api):
    source = 'b9584671-68e6-426b-a67c-6373778b8a0a'
    destination = 'b7584671-68e6-426b-a67c-6373778b8a0a'
    target = ['127.0.0.1']
    resp_data = {
        'response': {
            'data': {
                'asset_count': 512
            }
        }
    }
    responses.add(
        responses.PATCH,
        url=f'{ASSET_BASE_URL}',
        json=resp_data
    )

    data = api.v3.assets.move_assets(source, destination, target)
    assert data == resp_data['response']['data']['asset_count']


def test_update_acr(api):
    with pytest.raises(NotImplementedError):
        api.v3.assets.update_acr([{}])


def test_bulk_delete(api):
    with pytest.raises(NotImplementedError):
        api.v3.assets.bulk_delete(
            ('host.hostname', 'match', 'asset.com'), filter_type='or')


def test_tags(api):
    with pytest.raises(NotImplementedError):
        api.v3.assets.tags('00000000-0000-0000-0000-000000000000')


def test_assign_tags(api):
    with pytest.raises(NotImplementedError):
        api.v3.assets.assign_tags('add',
                                  ['00000000-0000-0000-0000-000000000000'],
                                  ['00000000-0000-0000-0000-000000000000'])
