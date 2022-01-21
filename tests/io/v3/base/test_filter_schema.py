'''
Tests cases for filter schema
'''
import pytest
import responses
from marshmallow.exceptions import ValidationError

from tenable.io.v3.base.schema.explore.filters import (FilterSchema,
                                                       ParseFilterSchema)

SEARCH_DATA = dict(
    fields=['bios_name', 'name'],
    filter=('bios_name', 'eq', 'SCCM'),
    limit=10,
    sort=[('name', 'asc'), ('bios_name', 'desc')],
    next='sdf000dfssdSDFSDFSFE00dfsdffaf'
)

ASSET_TAG_FILTER_ENDPOINT: str = 'https://cloud.tenable.com'


def test_filter_tuple_without_condition():
    '''
    Test Filter with tuple
    '''
    tup_data = ('bios_name', 'eq', 'SCCM')
    test_resp = {'property': 'bios_name', 'operator': 'eq', 'value': 'SCCM'}
    schema = FilterSchema()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data

    with pytest.raises(ValidationError):
        SEARCH_DATA['dummy_key'] = 'dummy_value'
        schema.load(SEARCH_DATA)


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


def test_parse_filter_schema(api):
    '''
    Test case for parse filter schema
    '''
    # Let's create test response
    filters_dict: dict = {
        'field': 'field_1',
        'operator': 'oper_1',
        'value': ['value_1', 'value_2']
    }

    schema = ParseFilterSchema()

    assert filters_dict == schema.dump(schema.load(filters_dict))


@responses.activate
def test_parse_filter_schema_with_populate_filter(api):
    '''
    Test case for parse filter schema
    '''
    # Let's create test response
    filters_dict: dict = {
        'field': 'field_1',
        'operator': 'oper_1',
        'value': ['value_1', 'value_2']
    }

    # Let's register the response for filter API endpoint
    # Let's register the response for asset tag filter endpoint
    responses.add(
        responses.GET,
        f'{ASSET_TAG_FILTER_ENDPOINT}/api/v3/definitions/tags/assets/filters',
        json={
            'filters': [
                {
                    "name": "field_1",
                    "operators": [
                        "oper_1",
                        "oper_2"
                    ]
                }
            ]
        }
    )

    ParseFilterSchema.populate_filters(
        api, path='api/v3/definitions/tags/assets/filters'
    )

    schema = ParseFilterSchema()

    assert filters_dict == schema.dump(schema.load(filters_dict))


@responses.activate
def test_parse_filter_schema_with_validation_error(api):
    '''
    Test case for parse filter schema
    '''
    # Let's create test response
    filters_dict: dict = {
        'field': 'field_2',
        'operator': 'oper_3',
        'value': ['value_1', 'value_2']
    }

    # Let's register the response for filter API endpoint
    # Let's register the response for asset tag filter endpoint
    responses.add(
        responses.GET,
        f'{ASSET_TAG_FILTER_ENDPOINT}/api/v3/definitions/tags/assets/filters',
        json={
            'filters': [
                {
                    "name": "field_1",
                    "operators": [
                        "oper_1",
                        "oper_2"
                    ]
                }
            ]
        }
    )

    ParseFilterSchema.populate_filters(
        api, path='api/v3/definitions/tags/assets/filters'
    )

    schema = ParseFilterSchema()
    with pytest.raises(ValidationError):
        schema.load(filters_dict)
