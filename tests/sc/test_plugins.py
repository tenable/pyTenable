import pytest
from tenable.sc.plugins import PluginResultsIterator
from ..checker import check
from tenable.errors import UnexpectedValueError


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


def test_plugins_constructor_filter_operator_unexpected_tuple_length(sc):
    with pytest.raises(UnexpectedValueError):
        sc.plugins._constructor(filter=('name', 'something'))


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


@pytest.mark.vcr()
def test_plugins_list_success_for_json_result(sc):
    plugins = sc.plugins.list(pages=1, limit=200, json_result=True)
    assert isinstance(plugins, list)
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
    plug_in = sc.plugins.details(19506)
    assert isinstance(plug_in, dict)
    check(plug_in, 'baseScore', str, allow_none=True)
    check(plug_in, 'checkType', str)
    check(plug_in, 'copyright', str)
    check(plug_in, 'cpe', str)
    check(plug_in, 'cvssV3BaseScore', str, allow_none=True)
    check(plug_in, 'cvssV3TemporalScore', str, allow_none=True)
    check(plug_in, 'cvssV3Vector', str)
    check(plug_in, 'cvssV3VectorBF', str)
    check(plug_in, 'cvssVector', str)
    check(plug_in, 'cvssVectorBF', str)
    check(plug_in, 'dependencies', str)
    check(plug_in, 'description', str)
    check(plug_in, 'dstPort', str, allow_none=True)
    check(plug_in, 'exploitAvailable', str)
    check(plug_in, 'exploitEase', str)
    check(plug_in, 'exploitFrameworks', str)
    check(plug_in, 'family', dict)
    check(plug_in['family'], 'id', str)
    check(plug_in['family'], 'name', str)
    check(plug_in['family'], 'type', str)
    check(plug_in, 'id', str)
    check(plug_in, 'md5', str)
    check(plug_in, 'modifiedTime', str)
    check(plug_in, 'name', str)
    check(plug_in, 'patchModDate', str)
    check(plug_in, 'patchPubDate', str)
    check(plug_in, 'pluginModDate', str)
    check(plug_in, 'pluginPubDate', str)
    check(plug_in, 'protocol', str)
    check(plug_in, 'requiredPorts', str)
    check(plug_in, 'requiredUDPPorts', str)
    check(plug_in, 'riskFactor', str)
    check(plug_in, 'seeAlso', str)
    check(plug_in, 'solution', str)
    check(plug_in, 'source', str)
    check(plug_in, 'sourceFile', str)
    check(plug_in, 'srcPort', str, allow_none=True)
    check(plug_in, 'stigSeverity', str, allow_none=True)
    check(plug_in, 'synopsis', str)
    check(plug_in, 'temporalScore', str, allow_none=True)
    check(plug_in, 'type', str)
    check(plug_in, 'version', str)
    check(plug_in, 'vulnPubDate', str)
    check(plug_in, 'xrefs', str)


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
def test_plugins_family_details_success_for_fields(sc):
    family_details = sc.plugins.family_details(10, fields=['id', 'name', 'type'])
    assert isinstance(family_details, dict)
    check(family_details, 'id', str)
    check(family_details, 'name', str)
    check(family_details, 'type', str)


@pytest.mark.vcr()
def test_plugins_family_plugins_success(sc):
    plugs = sc.plugins.family_plugins(10, limit=100, pages=2)
    assert isinstance(plugs, PluginResultsIterator)
    for p in plugs:
        check(p, 'id', str)
        check(p, 'name', str)
        check(p, 'description', str)


@pytest.mark.vcr()
def test_plugins_family_plugins_success_for_json_result(sc):
    plugs = sc.plugins.family_plugins(10, limit=100, pages=1, json_result=True)
    assert isinstance(plugs, list)
    for p in plugs:
        check(p, 'id', str)
        check(p, 'name', str)
        check(p, 'description', str)


@pytest.mark.vcr()
def test_plugins_family_plugins_success_for_json_result(sc):
    plugs = sc.plugins.family_plugins(10, limit=100, pages=1, json_result=True)
    assert isinstance(plugs, list)
    for p in plugs:
        check(p, 'id', str)
        check(p, 'name', str)
        check(p, 'description', str)
