'''
Test Explore -> Assets V3 API endpoints
'''

import pytest
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import CSVChunkIterator, SearchIterator


@pytest.mark.vcr()
def test_explore_assets_v3_search_was_assets(api):
    '''
    Test the search web applications assets endpoint
    '''
    tag_list = ['522b0827-1780-42c5-9f70-2e481a845b41']
    sort = [('created', 'desc')]
    filters = ('and', ('last_observed', 'lt', '2022-05-14T18:30:00.000Z'),
               ('tags', 'eq', tag_list))

    assets_iterator = api.v3.explore.assets.search_webapp(limit=200, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Web Applications Assets"

    for asset_data in assets_iterator:
        for asset_tag in asset_data['tags']:
            assert asset_tag['id'] in tag_list, \
                "Web Application Assets are not filtered as per 'tags' filter criteria."

    assets_csv_iterator = api.v3.explore.assets.search_webapp(sort=sort, limit=200, filter=filters, return_csv=True)
    assert isinstance(assets_csv_iterator, CSVChunkIterator), \
        "CSV chunk iterator is not returned in response of " \
        "Explore -> Web Applications Assets with return_csv flag enabled"

    assets_response = api.v3.explore.assets.search_webapp(limit=200, sort=sort, filter=filters, return_resp=True)
    assert isinstance(assets_response, Response), "Response object is not returned in response of " \
                                                  "Explore -> Web Applications Assets with return_resp flag enabled"

    assets_csv_response = api.v3.explore.assets.search_webapp(limit=200, sort=sort, filter=filters, return_resp=True,
                                                              return_csv=True)
    assert isinstance(assets_csv_response, Response), "Response object (CSV format) is not returned in response of " \
                                                      "Explore -> Web Applications Assets with return_resp flag enabled"


@pytest.mark.vcr()
def test_explore_assets_v3_search_host_assets(api):
    '''
    Test the search host assets endpoint
    '''
    operating_system_list = ['AIX 6.1', 'AsyncOS']
    sort = [('created', 'desc')]
    filters = ('and', ('operating_systems', 'eq', operating_system_list))

    assets_iterator = api.v3.explore.assets.search_host(limit=10, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Hosts Assets"

    for asset_data in assets_iterator:
        for asset_operating_system in asset_data['operating_systems']:
            assert asset_operating_system in operating_system_list, \
                "Host Assets are not filtered as per 'operating_systems' filter criteria."

    assets_csv_iterator = api.v3.explore.assets.search_host(sort=sort, limit=10, filter=filters, return_csv=True)
    assert isinstance(assets_csv_iterator, CSVChunkIterator), \
        "CSV chunk iterator is not returned in response of Explore -> Hosts Assets with return_csv flag enabled"

    assets_response = api.v3.explore.assets.search_host(limit=10, sort=sort, filter=filters, return_resp=True)
    assert isinstance(assets_response, Response), "Response object is not returned in response of " \
                                                  "Explore -> Hosts Assets with return_resp flag enabled"

    assets_csv_response = api.v3.explore.assets.search_host(limit=10, sort=sort, filter=filters, return_resp=True,
                                                            return_csv=True)
    assert isinstance(assets_csv_response, Response), "Response object (CSV format) is not returned in response of " \
                                                      "Explore -> Hosts Assets with return_resp flag enabled"


@pytest.mark.vcr()
def test_explore_assets_v3_search_cloud_resource_assets(api):
    '''
    Test the search cloud resource assets endpoint
    '''
    asset_name_list = ['CSTest', 'CSTest-ip']
    region_list = ['CSTest_group']
    sort = [('updated', 'desc')]
    filters = ('and', ('name', 'eq', asset_name_list), ('cloud.runtime.region', 'eq', region_list))

    assets_iterator = api.v3.explore.assets.search_cloud_resource(limit=5, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Cloud Resources Assets"

    for asset_data in assets_iterator:
        assert asset_data['name'] in asset_name_list, \
            "Cloud Resource Assets are not filtered as per 'name' filter criteria."
        assert asset_data['cloud']['runtime']['region'] in region_list, \
            "Cloud Resource Assets are not filtered as per 'region' filter criteria."

    assets_csv_iterator = api.v3.explore.assets.search_cloud_resource(sort=sort, limit=5, filter=filters,
                                                                      return_csv=True)
    assert isinstance(assets_csv_iterator, CSVChunkIterator), \
        "CSV chunk iterator is not returned in response of " \
        "Explore -> Cloud Resources Assets with return_csv flag enabled"

    assets_response = api.v3.explore.assets.search_cloud_resource(limit=5, sort=sort, filter=filters, return_resp=True)
    assert isinstance(assets_response, Response), "Response object is not returned in response of " \
                                                  "Explore -> Cloud Resources Assets with return_resp flag enabled"

    assets_csv_response = api.v3.explore.assets.search_cloud_resource(limit=5, sort=sort, filter=filters,
                                                                      return_resp=True, return_csv=True)
    assert isinstance(assets_csv_response, Response), "Response object (CSV format) is not returned in response of " \
                                                      "Explore -> Cloud Resources Assets with return_resp flag enabled"


@pytest.mark.vcr()
def test_explore_assets_v3_search_all_assets(api):
    '''
    Test the search all the assets endpoint
    '''
    operating_system_list = ['linux*']
    source_list = ['AWS']
    asset_type_request_list = ['host', 'webapp', 'cloud_resource']
    asset_type_response_list = ['host', 'webapp', 'cloud']
    sort = [('last_observed', 'desc')]
    filters = ('and', ('operating_systems', 'wc', operating_system_list), ('sources', 'eq', source_list),
               ('types', 'eq', asset_type_request_list))

    assets_iterator = api.v3.explore.assets.search_all(limit=50, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> All Assets"

    for asset_data in assets_iterator:
        for asset_operating_system in asset_data['operating_systems']:
            assert asset_operating_system.lower() in operating_system_list[0].lower(), \
                "All Assets are not filtered as per 'operating_systems' filter criteria."

        for asset_source in asset_data['sources']:
            assert asset_source in source_list, \
                "All Assets are not filtered as per 'sources' filter criteria."

        for asset_type in asset_data['types']:
            assert asset_type in asset_type_response_list, \
                "All Assets are not filtered as per 'types' filter criteria."

    assets_csv_iterator = api.v3.explore.assets.search_all(sort=sort, limit=50, filter=filters,
                                                           return_csv=True)
    assert isinstance(assets_csv_iterator, CSVChunkIterator), \
        "CSV chunk iterator is not returned in response of Explore -> All Assets with return_csv flag enabled"

    assets_response = api.v3.explore.assets.search_all(limit=50, sort=sort, filter=filters, return_resp=True)
    assert isinstance(assets_response, Response), "Response object is not returned in response of " \
                                                  "Explore -> All Assets with return_resp flag enabled"

    assets_csv_response = api.v3.explore.assets.search_all(limit=50, sort=sort, filter=filters,
                                                           return_resp=True, return_csv=True)
    assert isinstance(assets_csv_response, Response), "Response object (CSV format) is not returned in response of " \
                                                      "Explore -> All Assets with return_resp flag enabled"
