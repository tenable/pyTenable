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
    is_licensed = False
    sort = [('created', 'desc')]
    filters = ('and', ('is_licensed', 'eq', is_licensed))

    assets_iterator = api.v3.explore.assets.search_webapp(limit=200, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Web Applications Assets"

    for asset_data in assets_iterator:
        assert asset_data['is_licensed'] == is_licensed, \
            "Web Application Assets are not filtered as per 'is_licensed' filter criteria."

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
    is_licensed = False
    sort = [('created', 'desc')]
    filters = ('and', ('is_licensed', 'eq', is_licensed))

    assets_iterator = api.v3.explore.assets.search_host(limit=10, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Hosts Assets"

    for asset_data in assets_iterator:
        assert asset_data['is_licensed'] == is_licensed, \
            "Host Assets are not filtered as per 'is_licensed' filter criteria."

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
    is_licensed = False
    sort = [('updated', 'desc')]
    filters = ('and', ('is_licensed', 'eq', is_licensed))

    assets_iterator = api.v3.explore.assets.search_cloud_resource(limit=5, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Cloud Resources Assets"

    for asset_data in assets_iterator:
        assert asset_data['is_licensed'] == is_licensed, \
            "Cloud Resource Assets are not filtered as per 'is_licensed' filter criteria."

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
    is_licensed = False

    asset_type_list = ['host', 'webapp', 'cloud_resource']
    sort = [('last_observed', 'desc')]
    filters = ('and', ('is_licensed', 'eq', is_licensed), ('types', 'eq', asset_type_list))

    assets_iterator = api.v3.explore.assets.search_all(limit=50, sort=sort, filter=filters)
    assert isinstance(assets_iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> All Assets"

    for asset_data in assets_iterator:
        assert asset_data['is_licensed'] == is_licensed, \
            "All Assets are not filtered as per 'is_licensed' filter criteria."

        for asset_type in asset_data['types']:
            assert asset_type in asset_type_list, \
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
