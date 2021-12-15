'''
test agent config
'''
import re

import responses

BASE_URL = 'https://cloud.tenable.com/api/v3/agents'


@responses.activate
def test_agent_config_details(api):
    '''
    Test agent_config details endpoint
    '''
    test_response = {
        'auto_unlink': {'enabled': True, 'expiration': 20},
        'software_update': False
    }
    agent_id: int = 1
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/{agent_id}/config'),
        json=test_response
    )
    res = api.v3.vm.agent_config.details(agent_id=agent_id)
    assert isinstance(res, dict)


@responses.activate
def test_agent_config_edit(api):
    '''
    Test agent_config edit endpoint
    '''
    test_response = {
        'auto_unlink': {'enabled': True, 'expiration': 20},
        'software_update': False
    }
    agent_id: int = 20
    payload = {
        'software_update': False,
        'auto_unlink': {'enabled': True, 'expiration': 20}
    }
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/{agent_id}/config'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.agent_config.edit(
        auto_unlink=20,
        software_update=False,
        agent_id=agent_id
    )
    assert isinstance(res, dict)
