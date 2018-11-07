from .fixtures import *
from tenable.errors import *

def test_agent_filters(api):
    filters = api.filters.agents_filters()
    assert isinstance(filters, dict)
    for f in filters:
        check(filters[f], 'choices', list, allow_none=True)
        check(filters[f], 'operators', list)
        check(filters[f], 'pattern', str, allow_none=True)

def test_workbench_vuln_filters(api):
    filters = api.filters.workbench_vuln_filters()
    assert isinstance(filters, dict)
    for f in filters:
        check(filters[f], 'choices', list, allow_none=True)
        check(filters[f], 'operators', list)
        check(filters[f], 'pattern', str, allow_none=True)

def test_workbench_asset_filters(api):
    filters = api.filters.workbench_asset_filters()
    assert isinstance(filters, dict)
    for f in filters:
        check(filters[f], 'choices', list, allow_none=True)
        check(filters[f], 'operators', list)
        check(filters[f], 'pattern', str, allow_none=True)

def test_scan_filters(api):
    filters = api.filters.scan_filters()
    assert isinstance(filters, dict)
    for f in filters:
        check(filters[f], 'choices', list, allow_none=True)
        check(filters[f], 'operators', list)
        check(filters[f], 'pattern', str, allow_none=True)
