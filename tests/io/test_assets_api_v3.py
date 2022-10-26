'''
Test Explore -> Assets V3 API endpoints
'''

import pytest
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import CSVChunkIterator, SearchIterator


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
