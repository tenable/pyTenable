'''
Tests for search and filter schema
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.base.schema.explore.filters import FilterSchema
from tenable.io.v3.base.schema.explore.search import SearchSchema, SortSchema

search_data = dict(
    fields=['bios_name', 'name'],
    filter=('bios_name', 'eq', 'SCCM'),
    limit=10,
    sort=[('name', 'asc'), {'property': 'bios_name', 'order': 'desc'}],
    next='sdf000dfssdSDFSDFSFE00dfsdffaf'
)
sort_data_schema = dict(property='bios_name', order='asc')


def test_search_schema():
    '''
    Test the users create schema
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

    schema = SearchSchema(context={'is_sort_with_prop': True})
    assert test_resp == schema.dump(schema.load(search_data))

    with pytest.raises(ValidationError):
        search_data['new_val'] = 'something'
        schema.load(search_data)


def test_sort_schema():
    test_resp = {'property': 'bios_name', 'order': 'asc'}
    schema = SortSchema(context={'is_sort_with_prop': True})
    data = schema.dump(schema.load(sort_data_schema))
    assert test_resp == data


def test_filter_tuple_without_condition():
    tup_data = ('bios_name', 'eq', 'SCCM')
    test_resp = {'property': 'bios_name', 'operator': 'eq', 'value': 'SCCM'}
    schema = FilterSchema()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data

    with pytest.raises(ValidationError):
        search_data['new_val'] = 'something'
        schema.load(search_data)


def test_filter_dict():
    tup_data = {'property': 'filter', 'operator': 'oper', 'value': 'value'}
    test_resp = {'operator': 'oper', 'value': 'value', 'property': 'filter'}
    schema = FilterSchema()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data


def test_filter_tuple_with_condition():
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

    with pytest.raises(ValidationError):
        data = 'something'
        schema.load(data)

    with pytest.raises(ValidationError):
        data = (
            'greater',
            ('and', ('test', 'eq', '1'), ('test', 'eq', '2')),
            'invalid',
            ('test', 'eq', 3),
        )
        schema.load(data)

    with pytest.raises(ValidationError):
        data = (
            'and',
            ('and', ('test', 'eq', '1'), ('test', 'eq', '1')),
            'and',
            ('test', 'eq', '1'),
        )
        schema.load(data)

    with pytest.raises(ValidationError):
        data = (
            'None',
            ('and', ('test', 'eq', '1'), ('test', 'eq', '1')),
            'and',
            ('test', 'eq', '1'),
        )
        schema.load(data)

    with pytest.raises(ValidationError):
        data = (
            'and',
            ('and', ('test', 'eq', None), ('test', 'eq', '1')),
            'or',
            ('test', 'eq', '1'),
        )
        schema.load(data)


def test_filter_tuple_with_condition_dict():
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
