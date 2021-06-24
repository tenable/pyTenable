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

@pytest.mark.vcr()
def test_use_cache_true_filters(api):
    '''
    test to raise the exception use_cache filter is normalized
    '''
    filters = getattr(api.filters, '_use_cache')\
        ('rules', 'access-groups/rules/filters', 'rules', True)
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)



@pytest.mark.vcr()
def test_use_cache_false_filters(api):
    '''
    test to raise the exception use_cache filter is not normalized
    '''
    filters = getattr(api.filters, '_use_cache')\
        ('rules', 'access-groups/rules/filters', 'rules', False)
    assert isinstance(filters, list)
    for data in enumerate(filters):
        check(data[1], 'operators', list, allow_none=True)
        check(data[1], 'name', str, allow_none=True)
        check(data[1], 'readable_name', str, allow_none=True)
        check(data[1], 'control', dict, allow_none=True)

@pytest.mark.vcr()
def test_filters_credentials_false_filters(api):
    '''
    test to raise the exception when the credentials filter is not normalized
    '''
    filters = api.filters.credentials_filters(normalize=False)
    assert isinstance(filters, list)
    for data in enumerate(filters):
        check(data[1], 'name', str, allow_none=True)
        check(data[1], 'readable_name', str, allow_none=True)
        check(data[1], 'operators', list, allow_none=True)
        check(data[1], 'control', dict, allow_none=True)