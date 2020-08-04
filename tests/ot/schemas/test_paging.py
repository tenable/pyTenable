from tenable.ot.schemas.paging import (
    PaginationFilterSchema,
    PaginationOrderSchema,
    PaginationSchema
)
from marshmallow import ValidationError
import pytest


def test_pagination_filter_schema():
    '''
    Tests the PaginationFilterSchema class
    '''
    schema = PaginationFilterSchema()

    # Test the filter "loader"
    with pytest.raises(KeyError):
        schema.load_filters('something')
    schema.load_filters('assets')

    # Test that invalid filters should throw a ValidationError
    with pytest.raises(ValidationError):
        schema.load(('invalid_filter', 'eq', 'value'))

    # Test that filter rules work as expected.  we will simply spot-check here.
    schema.load(('id', 'equals', 'something'))
    schema.load(('addresses', 'contains', ['one', 'two', 'three']))

    # Test that snake_cake to camelCase works correctly:
    resp = schema.load(('first_seen', 'equals', 'something'))
    assert {'firstSeen': {'equals': 'something'}}


def test_pagination_order_schema():
    '''
    Tests the PaginationOrderSchema class
    '''
    schema = PaginationOrderSchema()

    # Assert that direction is always uppercased.
    resp = schema.load({'field': 'something', 'direction': 'asc'})
    assert resp['direction'] == 'ASC'


def test_pagination_schema():
    '''
    Tests the overreaching PaginationSchema class.
    '''
    schema = PaginationSchema()
    resp = schema.load({
        'filters': [
            ('id', 'equals', 'something'),
            ('first_seen', 'equals', 'time')
        ],
        'model': 'assets',
        'order_by': {
            'field': 'something',
            'direction': 'asc'
        },
        'offset': 0,
        'limit': 100,
        'search': 'something'
    })
    assert resp['filters']['id'] == {'equals': 'something'}
    assert resp['orderBy'] == {'field': 'something', 'direction': 'ASC'}
    assert resp['offset'] == 0
    assert resp['search'] == 'something'