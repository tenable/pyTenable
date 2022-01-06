'''
Tests for search and filter schema
'''
import pytest
from marshmallow.exceptions import ValidationError

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
