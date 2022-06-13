'''
Tests cases for filter schema for V3 endpoints
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.base.schema.explore.filters import FilterSchemaV3

SEARCH_DATA = dict(
    fields=['bios_name', 'name'],
    filter=('bios_name', 'eq', 'SCCM'),
    limit=10,
    sort=[('name', 'asc'), ('bios_name', 'desc')],
    next='sdf000dfssdSDFSDFSFE00dfsdffaf'
)


@pytest.mark.vcr()
def test_filter_tuple_without_condition_v3():
    '''
    Test Filter with tuple
    '''
    tup_data = ('bios_name', 'eq', 'SCCM')
    test_resp = {'property': 'bios_name', 'operator': 'eq', 'value': 'SCCM'}
    schema = FilterSchemaV3()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data

    with pytest.raises(ValidationError):
        SEARCH_DATA['dummy_key'] = 'dummy_value'
        schema.load(SEARCH_DATA)


@pytest.mark.vcr()
def test_filter_dict_v3():
    '''
    Test Filter with dict
    '''
    tup_data = {'property': 'filter', 'operator': 'oper', 'value': 'value'}
    test_resp = {'operator': 'oper', 'value': 'value', 'property': 'filter'}
    schema = FilterSchemaV3()
    data = schema.dump(schema.load(tup_data))

    assert test_resp == data


@pytest.mark.vcr()
def test_filter_tuple_with_condition_b3():
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
    schema = FilterSchemaV3()
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


@pytest.mark.vcr()
def test_filter_dict_with_condition_dict_v3():
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
    schema = FilterSchemaV3()
    assert test_resp == schema.dump(schema.load(data))
