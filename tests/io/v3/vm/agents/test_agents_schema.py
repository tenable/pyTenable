'''
Testing the Agents schemas
'''
from tenable.io.v3.vm.agents.schema import AgentSchema


def test_agent_groups_schema_with_name():
    '''
    Test the agents schema with name
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
    schema = AgentSchema(only=['items'])
    assert test_resp == schema.dump(schema.load(payload))
