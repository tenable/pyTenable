'''
Tests cases  for search schema
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.base.schema.explore.filters import FilterSchema
from tenable.io.v3.base.schema.explore.search import (SearchSchema,
                                                      SearchWASSchema,
                                                      SortSchema, SortType)


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

    with pytest.raises(ValidationError):
        SEARCH_DATA['dummy_key'] = 'dummy_value'
        schema.load(SEARCH_DATA)


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

    with pytest.raises(ValidationError):
        SEARCH_DATA['dummy_key'] = 'dummy_value'
        schema.load(SEARCH_DATA)


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
