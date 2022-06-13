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
    sort = [('created', 'desc')]
    filters = ('and', ('last_observed', 'lt', '2022-04-19T18:30:00.000Z'),
               ('tags', 'eq', ['6167eae5-808a-415a-8400-f3208e5382c5']))

    iterator = api.v3.explore.assets.search_webapp(
        limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Web Applications Assets"

    iterator = api.v3.explore.assets.search_webapp(
        sort=sort, limit=200, filter=filters, return_csv=True)
    assert isinstance(iterator, CSVChunkIterator), "CSV chunk iterator is not returned in response of " \
                                                   "Explore -> Web Applications Assets with return_csv flag enabled"

    resp = api.v3.explore.assets.search_webapp(
        limit=200, sort=sort, filter=filters, return_resp=True)
    assert isinstance(resp, Response), "Response object is not returned in response of " \
                                       "Explore -> Web Applications Assets with return_resp flag enabled"

    resp = api.v3.explore.assets.search_webapp(
        limit=200, sort=sort, filter=filters, return_resp=True, return_csv=True)
    assert isinstance(resp, Response), "Response object (CSV format) is not returned in response of " \
                                       "Explore -> Web Applications Assets with return_resp flag enabled"
