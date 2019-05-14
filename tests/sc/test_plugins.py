from tenable.sc.plugins import PluginResultsIterator
from tenable.errors import *
from ..checker import check, single
import pytest, os

def test_plugins_constructor_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(fields=1)

def test_plugins_constructor_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(fields=[1])

def test_plugins_constructor_filter_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(filter=1)

def test_plugins_constructor_filter_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(filter=(1, 'eq', 'something'))

def test_plugins_constructor_filter_operator_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(filter=('name', 1, 'something'))

def test_plugins_constructor_filter_operator_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.plugins._constructor(filter=('name', 'something', 'something'))

def test_plugins_constructor_filter_value_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(filter=('name', 'eq', 1))

def test_plugins_constructor_sort_field_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(sort_field=1)

def test_plugins_constructor_sort_direction_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(sort_direction=1)

def test_plugins_constructor_sort_direction_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.plugins._constructor(sort_direction='no')

def test_plugins_constructor_since_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(since='no')

def test_plugins_constructor_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(type=1)

def test_plugins_constructor_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.plugins._constructor(type='nope')

def test_plugins_constructor_offset_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(offset='nope')

def test_plugins_constructor_limit_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins._constructor(limit='nope')

def test_plugins_constructor(sc):
    resp = sc.plugins._constructor(fields=['one', 'two'],
        filter=('name', 'eq', 'value'),
        sort_field='name',
        sort_direction='asc',
        since=0,
        type='all',
        offset=0,
        limit=200,
        pages=1,
        json_result=True)
    assert resp == {
        'fields': 'one,two',
        'filterField': 'name',
        'op': 'eq',
        'value': 'value',
        'sortField': 'name',
        'sortDirection': 'ASC',
        'since': 0,
        'type': 'all',
        'startOffset': 0,
        'endOffset': 200
    }

@pytest.mark.vcr()
def test_plugins_list_success(sc):
    plugins = sc.plugins.list(pages=2, limit=200)
    assert isinstance(plugins, PluginResultsIterator)
    for plugin in plugins:
        assert isinstance(plugin, dict)
        check(plugin, 'id', str)
        check(plugin, 'name', str)
        check(plugin, 'description', str)

def test_plugins_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins.details('one')

def test_plugins_details_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins.details(19506, fields=1)

def test_plugins_details_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.plugins.details(19506, fields=[1])

@pytest.mark.vcr()
def test_plugins_details_success(sc):
    p = sc.plugins.details(19506)
    assert isinstance(p, dict)
    check(p, 'baseScore', str, allow_none=True)
    check(p, 'checkType', str)
    check(p, 'copyright', str)
    check(p, 'cpe', str)
    check(p, 'cvssV3BaseScore', str, allow_none=True)
    check(p, 'cvssV3TemporalScore', str, allow_none=True)
    check(p, 'cvssV3Vector', str)
    check(p, 'cvssV3VectorBF', str)
    check(p, 'cvssVector', str)
    check(p, 'cvssVectorBF', str)
    check(p, 'dependencies', str)
    check(p, 'description', str)
    check(p, 'dstPort', str, allow_none=True)
    check(p, 'exploitAvailable', str)
    check(p, 'exploitEase', str)
    check(p, 'exploitFrameworks', str)
    check(p, 'family', dict)
    check(p['family'], 'id', str)
    check(p['family'], 'name', str)
    check(p['family'], 'type', str)
    check(p, 'id', str)
    check(p, 'md5', str)
    check(p, 'modifiedTime', str)
    check(p, 'name', str)
    check(p, 'patchModDate', str)
    check(p, 'patchPubDate', str)
    check(p, 'pluginModDate', str)
    check(p, 'pluginPubDate', str)
    check(p, 'protocol', str)
    check(p, 'requiredPorts', str)
    check(p, 'requiredUDPPorts', str)
    check(p, 'riskFactor', str)
    check(p, 'seeAlso', str)
    check(p, 'solution', str)
    check(p, 'source', str)
    check(p, 'sourceFile', str)
    check(p, 'srcPort', str, allow_none=True)
    check(p, 'stigSeverity', str, allow_none=True)
    check(p, 'synopsis', str)
    check(p, 'temporalScore', str, allow_none=True)
    check(p, 'type', str)
    check(p, 'version', str)
    check(p, 'vulnPubDate', str)
    check(p, 'xrefs', str)

@pytest.mark.vcr()
def test_plugins_family_list_success(sc):
    f = sc.plugins.family_list()
    assert isinstance(f, list)
    for i in f:
        check(i, 'id', str)
        check(i, 'name', str)

@pytest.mark.vcr()
def test_plugins_family_details_success(sc):
    f = sc.plugins.family_details(10)
    assert isinstance(f, dict)
    check(f, 'id', str)
    check(f, 'name', str)
    check(f, 'type', str)
    check(f, 'plugins', list)
    check(f, 'count', int)

@pytest.mark.vcr()
def test_plugins_family_plugins_success(sc):
    plugs = sc.plugins.family_plugins(10, limit=100, pages=2)
    assert isinstance(plugs, PluginResultsIterator)
    for p in plugs:
        check(p, 'id', str)
        check(p, 'name', str)
        check(p, 'description', str)