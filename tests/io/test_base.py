from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.fixture
def fitem():
    return [('distro', 'match', 'win')]

@pytest.mark.vcr()
@pytest.fixture
def fset(api):
    return api.filters.agents_filters()

def test_base_parse_filters_json(api, fitem, fset):
    assert {'filters': [{
        'filter': 'distro',
        'quality': 'match',
        'value': 'win',
    }]} == api.agents._parse_filters(fitem, fset, rtype='json')

def test_base_parse_filter_sjson(api, fitem, fset):
    assert {
        'filter.0.filter': 'distro',
        'filter.0.quality': 'match',
        'filter.0.value': 'win'
    } == api.agents._parse_filters(fitem, fset, rtype='sjson')

def test_base_parse_filter_colon(api, fitem, fset):
    assert {
        'f': ['distro:match:win']
    } == api.agents._parse_filters(fitem, fset, rtype='colon')

def test_base_parse_filter_accessgroup(api, fitem, fset):
    fitem = [(fitem[0][0], fitem[0][1], [fitem[0][2]])]
    assert {'rules': [{
        'type': 'distro',
        'operator': 'match',
        'terms': ['win',]
    }]} == api.agents._parse_filters(fitem, fset, rtype='accessgroup')