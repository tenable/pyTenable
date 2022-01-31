'''
Test cases for Agnet Config Schema
'''
from tenable.io.v3.vm.agent_config.schema import AgentConfigSchema


def test_agent_config_schema():
    '''
    Test case for agent config schema
    '''
    schema = AgentConfigSchema()

    # Schema validation if expiration is greater then one
    input_payload: dict = {
        'software_update': True,
        'auto_unlink': {
            'expiration': 1
        }
    }
    output_payload: dict = {
        'software_update': True,
        'auto_unlink': {
            'enabled': True,
            'expiration': 1
        }
    }
    res_payload = schema.dump(schema.load(input_payload))
    assert output_payload == res_payload

    # Schema validation if expiration is False or zero
    input_payload: dict = {
        'software_update': True,
        'auto_unlink': {
            'expiration': 0
        }
    }
    output_payload = {
        'software_update': True,
        'auto_unlink': {
            'enabled': False,
        }
    }
    res_payload = schema.dump(schema.load(input_payload))
    assert output_payload == res_payload
