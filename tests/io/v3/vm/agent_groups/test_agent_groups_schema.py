'''
Testing the AgentGroups schemas
'''
from tenable.io.v3.vm.agent_groups.schema import AgentGroupSchema


def test_agent_groups_schema_with_name():
    '''
    Test the agent_groups schema with name
    '''
    name: str = 'sample name'
    payload = {
        'name': name
    }
    test_resp = {
        'name': name
    }
    schema = AgentGroupSchema()
    assert test_resp == schema.dump(schema.load(payload))


def test_agent_groups_schema_with_agent_ids():
    '''
    Test the agent_groups schema with agent_ids
    '''
    payload = {
        'items': [
            '57b74c0a-5d95-11ec-bf63-0242ac130002',
            '57b74e58-5d95-11ec-bf63-0242ac130002',
            '57b74f66-5d95-11ec-bf63-0242ac130002'
        ]
    }
    test_resp = {
        'items': [
            '57b74c0a-5d95-11ec-bf63-0242ac130002',
            '57b74e58-5d95-11ec-bf63-0242ac130002',
            '57b74f66-5d95-11ec-bf63-0242ac130002'
        ]
    }
    schema = AgentGroupSchema()
    assert test_resp == schema.dump(schema.load(payload))
