'''
Test cases for AgentGroups schemas
'''
from tenable.io.v3.vm.agent_groups.schema import AgentGroupSchema


def test_agent_groups_schema():
    '''
    Test the agent_groups schema with name
    '''
    schema = AgentGroupSchema()

    # Test for schema validation for create/configure agent method
    payload = {
        'name': 'Sample Agent Groups'
    }
    assert payload == schema.dump(schema.load(payload))

    # Test for schema validation for add/delete_agents method
    payload = {
        'items': [
            '57b74c0a-5d95-11ec-bf63-0242ac130002',
            '57b74e58-5d95-11ec-bf63-0242ac130002'
        ]
    }
    assert payload == schema.dump(schema.load(payload))

    # Test for schema validation for details method
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

    # Test for schema validation for send_instruction_to_agents_in_group method
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
