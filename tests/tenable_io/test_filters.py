from .fixtures import *
from tenable.errors import *

def test_agent_filters(api):
    filters = api.filters.agents_filters()
    assert isinstance(filters, dict)

def test_workbench_vuln_filters(api):
    filters = api.filters.workbench_vuln_filters()
    assert isinstance(filters, dict)

def test_workbench_asset_filters(api):
    filters = api.filters.workbench_asset_filters()
    assert isinstance(filters, dict)

def test_scan_filters(api):
    filters = api.filters.scan_filters()
    assert isinstance(filters, dict)