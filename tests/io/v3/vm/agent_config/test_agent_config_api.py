'''
Test cases for Agent Config
'''

import responses

BASE_URL = 'https://cloud.tenable.com/api/v3/agents/config'


@responses.activate
def test_agent_config_details(api):
    '''
    Test agent_config details endpoint
    '''
    # Let's create mock response for details endpoint
    test_response = {
        'software_update': False,
        'auto_unlink': {
            'enabled': True,
            'expiration': 20
        }
    }

    # Let's register the response for details endpoint
    responses.add(
        responses.GET,
        BASE_URL,
        json=test_response
    )

    res = api.v3.vm.agent_config.details()

    assert isinstance(res, dict)


@responses.activate
def test_agent_config_edit(api):
    '''
    Test agent_config edit endpoint
    '''
    auto_link: int = 1
    software_update: bool = True

    # Let's create sample response for edit endpoint
    test_response: dict = {
        'software_update': software_update,
        'auto_unlink': {
            'enabled': True,
            'expiration': auto_link
        }
    }

    # Let's create sample payload for edit endpoint
    payload: dict = {
        'software_update': software_update,
        'auto_unlink': {
            'enabled': True,
            'expiration': auto_link
        }
    }

    # Let's register the response for edit endpoint
    responses.add(
        responses.PUT,
        BASE_URL,
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agent_config.edit(
        auto_unlink=auto_link,
        software_update=software_update
    )

    assert isinstance(res, dict)
