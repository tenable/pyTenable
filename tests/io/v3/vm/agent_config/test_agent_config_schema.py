'''
Test cases for Agnet Config Schema
'''
from tenable.io.v3.vm.agent_config.schema import AgentConfigSchema


def test_agent_config_schema():
    '''
    Test case for agent config schema
    '''
    payload: dict = {
        'software_update': True,
        'auto_unlink': {
            'enabled': True,
            'expiration': 1
        }
    }

    schema = AgentConfigSchema()

    assert payload == schema.dump(schema.load(payload))
