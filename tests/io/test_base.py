'''
test base
'''
import pytest

@pytest.fixture
def fitem():
    '''
    fixture to returns list of filters in user defined filters format
    '''
    return [('distro', 'match', 'win')]

@pytest.mark.vcr()
@pytest.fixture
def fset(api):
    '''
    fixture to returns list of agents filters
    '''
    return api.filters.agents_filters()

def test_base_parse_filters_json(api, fitem, fset):
    '''
    test to parse filters with rtype as json
    '''
    assert {'filters': [{
        'filter': 'distro',
        'quality': 'match',
        'value': 'win',
    }]} == api.agents._parse_filters(fitem, fset, rtype='json')

def test_base_parse_filter_sjson(api, fitem, fset):
    '''
    test to parse filters with rtype as sjson
    '''
    assert {
        'filter.0.filter': 'distro',
        'filter.0.quality': 'match',
        'filter.0.value': 'win'
    } == api.agents._parse_filters(fitem, fset, rtype='sjson')

def test_base_parse_filter_colon(api, fitem, fset):
    '''
    test to parse filters with rtype as colon
    '''
    assert {
        'f': ['distro:match:win']
    } == api.agents._parse_filters(fitem, fset, rtype='colon')

def test_base_parse_filter_accessgroup(api, fitem, fset):
    '''
    test to parse filters with rtype as accessgroup
    '''
    fitem = [(fitem[0][0], fitem[0][1], [fitem[0][2]])]
    assert {'rules': [{
        'type': 'distro',
        'operator': 'match',
        'terms': ['win',]
    }]} == api.agents._parse_filters(fitem, fset, rtype='accessgroup')

def test_base_parse_filter_assets(api, fitem, fset):
    '''
    test to parse filters with rtype as assets
    '''
    fitem = [(fitem[0][0], fitem[0][1], [fitem[0][2]])]
    assert {'asset': [{
        'field': 'distro',
        'operator': 'match',
        'value': 'win'
    }]} == api.agents._parse_filters(fitem, fset, rtype='assets')
