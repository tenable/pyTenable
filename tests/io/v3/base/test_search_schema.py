'''
Tests for search and filter schema
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.base.schema.explore.filters import FilterSchema
from tenable.io.v3.base.schema.explore.search import (SearchSchema, SortSchema, SearchWASSchema,
                                                      SortType)
from tests.io.v3.base.search_objects import (NEGATIVE_FILTER_SCHEMA,
                                             NEGATIVE_SEARCH_SCHEMA,
                                             NEGATIVE_SORT_SCHEMA)

SEARCH_DATA = dict(
    fields=['bios_name', 'name'],
    filter=('bios_name', 'eq', 'SCCM'),
    limit=10,
    sort=[('name', 'asc'), ('bios_name', 'desc')],
    next='sdf000dfssdSDFSDFSFE00dfsdffaf'
)

SEARCH_DATA_WAS = dict(
    fields=['bios_name', 'name'],
    filter=('bios_name', 'eq', 'SCCM'),
    limit=10,
    offset=0,
    num_pages=1,
    sort=[('name', 'asc'), ('bios_name', 'desc')],
)

SORT_DATA_SCHEMA = dict(property='bios_name', order='asc')


def test_search_schema():
    '''
    Test the search schema with default values
    '''
    test_resp = {
        'limit': 10,
        'fields': ['bios_name', 'name'],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    }

    schema = SearchSchema(context={'sort_type': SortType.property_based})
    assert test_resp == schema.dump(schema.load(SEARCH_DATA))


def test_search_schema_was():
    '''
    Test the search schema with default values for was api
    '''
    test_resp = {
        'limit': 10,
        'fields': ['bios_name', 'name'],
        'offset': 0,
        'num_pages': 1,
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    }

    schema = SearchWASSchema(context={'sort_type': SortType.property_based})
    assert test_resp == schema.dump(schema.load(SEARCH_DATA_WAS))


def test_search_schema_invalid_limit():
    '''
    Test the search schema with invalid limit value
    '''
    search_schema = {
        'limit': 'abc',
        'fields': ['bios_name', 'name'],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [('name', 'asc'), ('bios_name', 'desc')],
    }

    schema = SearchSchema(context={'sort_type': SortType.property_based})

    with pytest.raises(ValidationError):
        schema.load(search_schema)


def test_search_schema_invalid_limit_was():
    '''
    Test the search schema with invalid limit value for was api
    '''
    search_schema = {
        'limit': 'abc',
        'fields': ['bios_name', 'name'],
        'offset': 0,
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [('name', 'asc'), ('bios_name', 'desc')],
    }

    schema = SearchWASSchema(context={'sort_type': SortType.property_based})

    with pytest.raises(ValidationError):
        schema.load(search_schema)


@pytest.mark.parametrize("test_input", NEGATIVE_SEARCH_SCHEMA)
def test_search_negative(test_input):
    '''
    Test negative cases for search schema
    '''
    schema = SearchSchema(context={'sort_type': SortType.property_based})
    with pytest.raises(ValidationError):
        schema.load(test_input)


def test_sort_schema():
    '''
    Test Sort Schema with no sort type
    '''
    test_resp = {'bios_name': 'asc'}
    schema = SortSchema()
    data = schema.dump(schema.load(SORT_DATA_SCHEMA))
    assert test_resp == data


def test_sort_schema_default():
    '''
    Test Sort Schema with default sort type
    '''
    test_resp = {'bios_name': 'asc'}
    schema = SortSchema(context={'sort_type': SortType.default})
    data = schema.dump(schema.load(SORT_DATA_SCHEMA))
    assert test_resp == data


def test_sort_schema_property_based():
    '''
    Test Sort Schema with property_based sort type
    '''
    test_resp = {'property': 'bios_name', 'order': 'asc'}
    schema = SortSchema(context={'sort_type': SortType.property_based})
    data = schema.dump(schema.load(SORT_DATA_SCHEMA))
    assert test_resp == data


def test_sort_schema_name_based():
    '''
    Test Sort Schema with name_based sort type
    '''
    test_resp = {'name': 'bios_name', 'order': 'asc'}
    schema = SortSchema(context={'sort_type': SortType.name_based})
    data = schema.dump(schema.load(SORT_DATA_SCHEMA))
    assert test_resp == data


@pytest.mark.parametrize("test_input", NEGATIVE_SORT_SCHEMA)
def test_sort_negative(test_input):
    '''
    Test negative cases for sort schema
    '''
    schema = SortSchema(context={'sort_type': SortType.property_based})
    with pytest.raises(ValidationError):
        schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_FILTER_SCHEMA)
def test_filter_negative(test_input):
    '''
    Test negative cases for filter schema
    '''
    schema = FilterSchema()
    with pytest.raises(ValidationError):
        schema.load(test_input)


def test_filter_tuple_without_condition():
    '''
    Test Filter with tuple
    '''
    tup_data = ('bios_name', 'eq', 'SCCM')
    test_resp = {'property': 'bios_name', 'operator': 'eq', 'value': 'SCCM'}
    schema = FilterSchema()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data


def test_filter_dict():
    '''
    Test Filter with dict
    '''
    tup_data = {'property': 'filter', 'operator': 'oper', 'value': 'value'}
    test_resp = {'operator': 'oper', 'value': 'value', 'property': 'filter'}
    schema = FilterSchema()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data


def test_filter_tuple_with_condition():
    '''
    Test Filter with tuple and condition
    '''
    tup_data = (
        'or',
        ('and', ('test', 'eq', '1'), ('test', 'eq', '2')),
        'and',
        ('test', 'eq', 3),
    )
    test_resp = {
        'or': [
            {
                'and': [
                    {'operator': 'eq', 'value': '1', 'property': 'test'},
                    {'operator': 'eq', 'value': '2', 'property': 'test'},
                ]
            }
        ],
        'and': [{'operator': 'eq', 'value': 3, 'property': 'test'}],
    }
    schema = FilterSchema()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data


def test_filter_dict_with_condition_dict():
    '''
    Test Filter with dict and condition
    '''
    data = {
        'or': [
            {
                'and': [
                    {'value': '1', 'operator': 'oper', 'property': '1'},
                    {'value': '2', 'operator': 'oper', 'property': '2'},
                ]
            }
        ],
        'and': [{'value': '3', 'operator': 'oper', 'property': '3'}],
    }
    test_resp = {
        'and': [{'operator': 'oper', 'property': '3', 'value': '3'}],
        'or': [
            {
                'and': [
                    {'operator': 'oper', 'property': '1', 'value': '1'},
                    {'operator': 'oper', 'property': '2', 'value': '2'},
                ]
            }
        ],
    }
    schema = FilterSchema()
    assert test_resp == schema.dump(schema.load(data))
