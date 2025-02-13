"""
test class for testing various scenarios in security center plugins
functionality
"""

import pytest

from tenable.errors import UnexpectedValueError
from tenable.sc.plugins import PluginResultsIterator

from ..checker import check


def test_plugins_constructor_fields_typeerror(security_center):
    """
    test plugins constructor for fields type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(fields=1)


def test_plugins_constructor_field_item_typeerror(security_center):
    """
    test plugins constructor for 'fields item' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(fields=[1])


def test_plugins_constructor_filter_typeerror(security_center):
    """
    test plugins constructor for filter type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filter=1)


def test_plugins_constructor_filter_name_typeerror(security_center):
    """
    test plugins constructor for 'filter name' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filter=(1, 'eq', 'something'))


def test_plugins_constructor_filter_operator_typeerror(security_center):
    """
    test plugins constructor for 'filter operator' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filter=('name', 1, 'something'))


def test_plugins_constructor_filter_operator_unexpectedvalueerror(security_center):
    """
    test plugins constructor for 'filter operator' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.plugins._constructor(filter=('name', 'something', 'something'))


def test_plugins_constructor_filter_operator_unexpected_tuple_length(security_center):
    """
    test plugins constructor for 'filter operator tuple length'
    unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.plugins._constructor(filter=('name', 'something'))


def test_plugins_constructor_filter_value_typeerror(security_center):
    """
    test plugins constructor for 'filter value' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filter=('name', 'eq', 1))


def test_plugins_constructor_sort_field_typeerror(security_center):
    """
    test plugins constructor for 'sor field' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(sort_field=1)


def test_plugins_constructor_sort_direction_typeerror(security_center):
    """
    test plugins constructor for 'sort direction' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(sort_direction=1)


def test_plugins_constructor_sort_direction_unexpectedvalueerror(security_center):
    """
    test plugins constructor for 'sor direction' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.plugins._constructor(sort_direction='no')


def test_plugins_constructor_since_typeerror(security_center):
    """
    test plugins constructor for since type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(since='no')


def test_plugins_constructor_type_typeerror(security_center):
    """
    test plugins constructor for type type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(type=1)


def test_plugins_constructor_type_unexpectedvalueerror(security_center):
    """
    test plugins constructor for type unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        security_center.plugins._constructor(type='nope')


def test_plugins_constructor_offset_typeerror(security_center):
    """
    test plugins constructor for offset type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(offset='nope')


def test_plugins_constructor_limit_typeerror(security_center):
    """
    test plugins constructor for limit type error
    """
    with pytest.raises(TypeError):
        security_center.plugins._constructor(limit='nope')


def test_plugins_constructor_filters_errors(security_center):
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filters='nope')
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filters=['one'])
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filters=[(1, 1, 1)])
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filters=[('name', 1, 1)])
    with pytest.raises(TypeError):
        security_center.plugins._constructor(filters=[('name', 'eq', 1)])
    with pytest.raises(UnexpectedValueError):
        security_center.plugins._constructor(filters=[('name', 'something', 'value')])


def test_plugins_constructor_filters_success(security_center):
    assert security_center.plugins._constructor(filters=[('name', 'eq', 'value')]) == {
        'filters': '[{"filterField": "name", "filterOperator": "eq", "filterString": "value"}]'
    }


def test_plugins_constructor(security_center):
    """
    test plugins constructor for success
    """
    resp = security_center.plugins._constructor(
        fields=['one', 'two'],
        filter=('name', 'eq', 'value'),
        sort_field='name',
        sort_direction='asc',
        since=0,
        type='all',
        offset=0,
        limit=200,
        pages=1,
        json_result=True,
    )
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
        'endOffset': 200,
    }


@pytest.mark.vcr()
def test_plugins_list_success(security_center):
    """
    test plugins list for success
    """
    plugins = security_center.plugins.list(pages=2, limit=200)
    assert isinstance(plugins, PluginResultsIterator)
    for plugin in plugins:
        assert isinstance(plugin, dict)
        check(plugin, 'id', str)
        check(plugin, 'name', str)
        check(plugin, 'description', str)


@pytest.mark.vcr()
def test_plugins_list_success_for_json_result(security_center):
    """
    test plugins list success for json result
    """
    plugins = security_center.plugins.list(pages=1, limit=200, json_result=True)
    assert isinstance(plugins, list)
    for plugin in plugins:
        assert isinstance(plugin, dict)
        check(plugin, 'id', str)
        check(plugin, 'name', str)
        check(plugin, 'description', str)


def test_plugins_details_id_typeerror(security_center):
    """
    test plugins details for id type error
    """
    with pytest.raises(TypeError):
        security_center.plugins.details('one')


def test_plugins_details_fields_typeerror(security_center):
    """
    test plugins details for fields type error
    """
    with pytest.raises(TypeError):
        security_center.plugins.details(19506, fields=1)


def test_plugins_details_field_item_typeerror(security_center):
    """
    test plugins details for 'fields item' type error
    """
    with pytest.raises(TypeError):
        security_center.plugins.details(19506, fields=[1])


@pytest.mark.vcr()
def test_plugins_details_success(security_center):
    """
    test plugins details for success
    """
    plug_in = security_center.plugins.details(19506)
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
def test_plugins_family_list_success(security_center):
    """
    test plugins family list for success
    """
    families = security_center.plugins.family_list()
    assert isinstance(families, list)
    for family in families:
        check(family, 'id', str)
        check(family, 'name', str)


@pytest.mark.vcr()
def test_plugins_family_details_success(security_center):
    """
    test plugins family details for success
    """
    family_details = security_center.plugins.family_details(10)
    assert isinstance(family_details, dict)
    check(family_details, 'id', str)
    check(family_details, 'name', str)
    check(family_details, 'type', str)
    check(family_details, 'plugins', list)
    check(family_details, 'count', int)


@pytest.mark.vcr()
def test_plugins_family_details_success_for_fields(security_center):
    """
    test plugins family details success for fields
    """
    family_details = security_center.plugins.family_details(
        10, fields=['id', 'name', 'type']
    )
    assert isinstance(family_details, dict)
    check(family_details, 'id', str)
    check(family_details, 'name', str)
    check(family_details, 'type', str)


@pytest.mark.vcr()
def test_plugins_family_plugins_success(security_center):
    """
    test plugins family plugins success
    """
    plugs = security_center.plugins.family_plugins(10, limit=100, pages=2)
    assert isinstance(plugs, PluginResultsIterator)
    for plugin in plugs:
        check(plugin, 'id', str)
        check(plugin, 'name', str)
        check(plugin, 'description', str)


@pytest.mark.vcr()
def test_plugins_family_plugins_success_for_json_result(security_center):
    """
    test plugins family plugins success for json result
    """
    plugs = security_center.plugins.family_plugins(
        10, limit=100, pages=1, json_result=True
    )
    assert isinstance(plugs, list)
    for plugin in plugs:
        check(plugin, 'id', str)
        check(plugin, 'name', str)
        check(plugin, 'description', str)
