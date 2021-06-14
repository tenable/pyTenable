'''
test filters
'''
import pytest
from tests.checker import check

@pytest.mark.vcr()
def test_agent_filters(api):
    '''
    test to get agent filters
    '''
    filters = api.filters.agents_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_workbench_vuln_filters(api):
    '''
    test to get workbench vulnerabilities filters
    '''
    filters = api.filters.workbench_vuln_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_workbench_asset_filters(api):
    '''
    test to get workbench asset filters
    '''
    filters = api.filters.workbench_asset_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_scan_filters(api):
    '''
    test to get scan filters
    '''
    filters = api.filters.scan_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_access_group_asset_rules_filters(api):
    '''
    test to get access group asset rules filters
    '''
    filters = api.filters.access_group_asset_rules_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_access_group_filters(api):
    '''
    test to get access group filters
    '''
    filters = api.filters.access_group_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_access_group_asset_rules_filters_v2(api):
    '''
    test to get access group asset rules filters v2
    '''
    filters = api.filters.access_group_asset_rules_filters_v2()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

@pytest.mark.vcr()
def test_access_group_filters_v2(api):
    '''
    test to get access group filters v2
    '''
    filters = api.filters.access_group_filters_v2()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data ], 'choices', list, allow_none=True)
        check(filters[data ], 'operators', list)
        check(filters[data ], 'pattern', str, allow_none=True)
        
@pytest.mark.vcr()
def test_asset_tag_filters(api):
    '''
    test to get asset tag filters
    '''
    filters = api.filters.asset_tag_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)

