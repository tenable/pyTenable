'''
Test cases for Agent Config Schema
'''
import pytest

from tenable.io.v3.vm.agent_config.schema import (AgentsConfigSchema,
                                                  AutoLinkSchema)
from tests.io.v3.vm.agent_config.objects import (NEGATIVE_AGENT_CONFIG_SCHEMA,
                                                 NEGATIVE_AUTO_LINK_SCHEMA)

agent_config_schema = AgentsConfigSchema()


def test_agent_config_schema():
    '''
    Test case for agent config schema
    '''

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
    res_payload = agent_config_schema.dump(
        agent_config_schema.load(input_payload)
    )
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
    res_payload = agent_config_schema.dump(
        agent_config_schema.load(input_payload)
    )
    assert output_payload == res_payload


@pytest.mark.parametrize("test_input", NEGATIVE_AUTO_LINK_SCHEMA)
def test_auto_link_schema_negative(test_input):
    auto_link_schema = AutoLinkSchema()
    with pytest.raises(Exception):
        auto_link_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_AGENT_CONFIG_SCHEMA)
def test_agent_config_schema_negative(test_input):
    with pytest.raises(Exception):
        agent_config_schema.load(test_input)
