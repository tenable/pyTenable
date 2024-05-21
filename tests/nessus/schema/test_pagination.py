import pytest
from tenable.nessus.schema.pagination import FilterSchema, ListSchema


def test_filter_schema_dict():
    filter = {'filter': 'name', 'quality': 'eq', 'value': 'something'}
    schema = FilterSchema()
    assert schema.dump(schema.load(filter)) == filter


def test_filter_schema_tuple():
    filter_out = {'filter': 'name', 'quality': 'eq', 'value': 'something'}
    filter_tpl = ('name', 'eq', 'something')
    schema = FilterSchema()
    assert schema.dump(schema.load(filter_tpl)) == filter_out


def test_list_schema():
    schema = ListSchema()
    test = {
        'limit': 10,
        'offset': 0,
        'sort_by': 'something',
        'sort_order': 'DESC',
        'search_type': 'AND',
        'filters': [('something', 'eq', 'value'),
                    {'filter': 'a', 'quality': 'eq', 'value': 's2'}
                    ]
    }
    resp = schema.dump(schema.load(test))
    assert resp['limit'] == 10
    assert resp['offset'] == 0
    assert resp['sort_by'] == 'something'
    assert resp['sort_order'] == 'desc'
    assert resp['filter.search_type'] == 'and'
    assert resp['filter.0.filter'] == 'something'
    assert resp['filter.0.quality'] == 'eq'
    assert resp['filter.0.value'] == 'value'
    assert resp['filter.1.filter'] == 'a'
    assert resp['filter.1.quality'] == 'eq'
    assert resp['filter.1.value'] == 's2'
