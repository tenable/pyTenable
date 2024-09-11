import pytest
import responses
from responses.registries import OrderedRegistry
from responses.matchers import json_params_matcher, query_param_matcher
from tenable.asm import TenableASM


@responses.activate(registry=OrderedRegistry)
def test_asm_inventory_list():
    test_item = {'id': 123456}
    responses.post(
        'https://nourl/api/1.0/inventory',
        json={'assets': [test_item for _ in range(1000)], 'total': 2005, 'stats': {}},
        match=[
            query_param_matcher({
                'columns': 'id,name',
                'inventory': 'false',
                'sortorder': 'true',
                'sortby': 'id',
                'after': '0000000000',
                'limit': 1000,
            }),
            json_params_matcher([
                {'column': 'id', 'type': 'equals', 'value': 'something'}
            ])
        ]
    )
    responses.post(
        'https://nourl/api/1.0/inventory',
        json={'assets': [test_item for _ in range(1000)], 'total': 2005, 'stats': {}},
        match=[
            query_param_matcher({
                'columns': 'id,name',
                'inventory': 'false',
                'sortorder': 'true',
                'sortby': 'id',
                'after': '123456',
                'limit': 1000,
            }),
            json_params_matcher([
                {'column': 'id', 'type': 'equals', 'value': 'something'}
            ])
        ]
    )
    responses.post(
        'https://nourl/api/1.0/inventory',
        json={'assets': [test_item for _ in range(5)], 'total': 2005, 'stats': {}},
        match=[
            query_param_matcher({
                'columns': 'id,name',
                'inventory': 'false',
                'sortorder': 'true',
                'sortby': 'id',
                'after': '123456',
                'limit': 1000,
            }),
            json_params_matcher([
                {'column': 'id', 'type': 'equals', 'value': 'something'}
            ])
        ]
    )
    asm = TenableASM(url='https://nourl', api_key='12345')
    items = asm.inventory.list(
        ('id', 'equals', 'something'),
        columns=['id', 'name'],
        sort_field='id'
    )
    for item in items:
        assert dict(item) == test_item
    assert items.count == 2005
