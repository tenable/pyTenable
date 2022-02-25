'''
Testing the Agents schemas
'''
from tenable.io.v3.vm.agents.schema import AgentSchema


def test_agents_schema():
    '''
    Test the agents schema with name
    '''
    schema = AgentSchema()

    # Test for schema validation for unlink method
    payload = {
        'items': [
            '57b74c0a-5d95-11ec-bf63-0242ac130002',
            '57b74e58-5d95-11ec-bf63-0242ac130002'
        ]
    }
    assert payload == schema.dump(schema.load(payload))

    # Test for schema validation for list agent from group method
    payload = {
        'filters': [('platform', 'match', ['window'])],
        'filter_type': 'and',
        'limit': 50,
        'offset': 0,
        'sort': [('name', 'asc'), ('platform', 'asc')],
        'wildcard': 'IYKKQIGOBWXUXOZIBURFENPNMGZOSWBUKVCD',
        'wildcard_fields': ['name']
    }
    res = {
        'sort': [('name', 'asc'), ('platform', 'asc')],
        'offset': 0,
        'filters': [
            {
                'value': ['window'],
                'operator': 'match',
                'field': 'platform'
            }
        ],
        'wildcard': 'IYKKQIGOBWXUXOZIBURFENPNMGZOSWBUKVCD',
        'limit': 50,
        'filter_type': 'and',
        'wildcard_fields': ['name']
    }
    assert res == schema.dump(schema.load(payload))

    # Test for schema validation for add or remove agent to network method
    payload = {
        'criteria': {
            'all_agents': True,
            'wildcard': 'sdfknskdnf',
            'filters': ['name:match:laptop'],
            'filter_type': 'and',
            'hardcoded_filters': ['core_version:lt:10.0.0']
        },
        'items': ['334b962a-ac03-4336-9ebb-a06b169576e0'],
        'not_items': ['334b962a-ac03-4336-9ebb-a06b321576e0']
    }
    assert payload == schema.dump(schema.load(payload))

    # Test for schema validation for send instruction to agent method
    payload = {
        'criteria': {
            'all_agents': True,
            'wildcard': 'sdfknskdnf',
            'filters': ['name:match:laptop'],
            'filter_type': 'and',
            'hardcoded_filters': ['core_version:lt:10.0.0']
        },
        'items': ['334b962a-ac03-4336-9ebb-a06b169576e0'],
        'not_items': ['334b962a-ac03-4336-9ebb-a06b321576e0'],
        'directive': {'type': 'restart'}
    }
    assert payload == schema.dump(schema.load(payload))
