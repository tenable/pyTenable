'''
Testing the search iterators for V3 endpoints
'''
import pytest

from tenable.io.v3.base.iterators.explore_iterator import SearchIterator

ASSET_DATA = [
    {'types': ['webapp'], 'is_deleted': False, 'sources': ['WAS'], 'ssl_tls_enabled': False,
     'created': '2022-01-25T15:19:17.224Z', 'name': 'target9.pubtarg.bananas.com', 'is_licensed': False,
     'id': '0f19a1a4-d1df-4f8a-a2ec-9cd5f4f3f3c5', 'updated': '2022-01-25T15:21:29.692Z',
     'tags': [{'id': '6167eae5-808a-415a-8400-f3208e5382c5', 'category': 'ABCD', 'value': 'tag111', 'type': 'static'}]},
    {'types': ['webapp'], 'sources': ['WAS'], 'last_licensed_scan_time': '2022-01-25T15:17:50.322Z',
     'created': '2021-10-28T13:47:40.801Z', 'ipv4_addresses': ['44.241.194.21'],
     'homepage_screenshot_url': 'https://cloud.tenable.com/was/v2/attachments/54fd0e88-7377-4755-8e9b-7b944f671de9',
     'tags': [{'id': '6167eae5-808a-415a-8400-f3208e5382c5', 'category': 'ABCD', 'value': 'tag111', 'type': 'static'}],
     'display_ipv4_address': '44.241.194.21', 'first_observed': '2021-10-28T13:47:40.694Z',
     'display_operating_system': 'Linux Kernel 3.10 on CentOS Linux release 7', 'ssl_tls_enabled': False,
     'last_observed': '2022-01-25T15:17:50.322Z', 'name': 'target1.pubtarg.tenablesecurity.com',
     'id': '8a148a61-7f5f-4730-8ac0-ebcebcbd6a4d', 'updated': '2022-01-25T15:22:22.966Z'}

]


@pytest.mark.vcr()
def test_search_iterator_v3(api):
    '''
    Test for search iterator
    '''
    search_iterator = SearchIterator(
        api=api,
        _resource='assets',
        _path='api/v3/assets/search',
        _payload={
            "limit": 1,
            "filter": {
                "and": [
                    {
                        "operator": "eq",
                        "property": "tags",
                        "value": [
                            "6167eae5-808a-415a-8400-f3208e5382c5"
                        ]
                    },
                    {
                        "operator": "eq",
                        "property": "types",
                        "value": "webapp"
                    },
                    {
                        "operator": "neq",
                        "property": "types",
                        "value": "host"
                    }
                ]
            }
        }
    )
    assert ASSET_DATA.__contains__(next(search_iterator))
    assert ASSET_DATA.__contains__(next(search_iterator))

    with pytest.raises(StopIteration):
        next(search_iterator)
