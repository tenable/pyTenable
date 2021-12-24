'''
Test Agents
'''
import re
from uuid import UUID

import pytest
import responses

BASE_URL = 'https://cloud.tenable.com/api/v3/agents'


@responses.activate
def test_details(api):
    '''
    Test case for agents details method
    '''
    test_response = {
        'id': 'd59d1f5b-f775-4061-9e36-fae22ab7518f2596d192e3cf57f8',
        'name': 'DESKTOP-PSNDJQ6',
        'platform': 'WINDOWS',
        'distro': 'win-x86-64',
        'ip': '192.0.2.57',
        'last_scanned': 1477011651,
        'plugin_feed_id': '0',
        'linked_on': 1468619962,
        'status': 'off',
        'groups': [
            {
                'name': 'CodyAgents', 'id': 8
            },
            {
                'name': 'Agent Group A', 'id': 3316
            }
        ]
    }
    agent_id: UUID = 'd59d1f5b-f775-4061-9e36-fae22ab7518f2596d192e3cf57f8'
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/{agent_id}'),
        json=test_response
    )
    res = api.v3.vm.agents.details(agent_id)
    assert isinstance(res, dict)
    assert 'id' in list(res.keys())
    assert res['id'] == agent_id


@responses.activate
def test_list_agents_from_group(api):
    '''
    Test case for agents list_agents_from_group method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.agents.list_agents_from_group()


@responses.activate
def test_task_status(api):
    '''
    Test case for agents task_status method
    '''
    test_response = {
        'task_id': '61a1320b-51e4-4244-9b34-694247384e8d',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'COMPLETED',
        'message': 'Finished bulk unlink operation.',
        'start_time': 1638963662426,
        'end_time': 1638963662492,
        'total_work_units_completed': 0
    }
    task_id: UUID = '61a1320b-51e4-4244-9b34-694247384e8d'
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/_bulk/{task_id}'),
        json=test_response
    )
    res = api.v3.vm.agents.task_status(task_id)
    assert isinstance(res, dict)
    assert 'task_id' in list(res.keys())
    assert res['task_id'] == task_id


@responses.activate
def test_search(api):
    '''
    Test case for agents search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.agents.search()


@responses.activate
def test_unlink_with_singuler_agent(api):
    '''
    Test case for agents unlink method
    '''
    agent_id: UUID = '61a1320b-51e4-4244-9b34-694247384e8d'
    responses.add(
        responses.DELETE,
        re.compile(f'{BASE_URL}/{agent_id}')
    )
    res = api.v3.vm.agents.unlink(agent_id)
    assert res is None


@responses.activate
def test_unlink_with_multiple_agents(api):
    '''
    Test case for agents unlink method
    '''
    test_response = {
        'task_id': '61a1320b-51e4-4244-9b34-694247384e8d',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'NEW',
        'message': 'Beginning bulk unlink operation'
    }
    payload = {
        'items': [
            i for i in (
                '31b25934-5da2-11ec-bf63-0242ac130002',
                '31b25b78-5da2-11ec-bf63-0242ac130002',
                '31b25c7c-5da2-11ec-bf63-0242ac130002'
            )
        ]
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/_bulk/unlink'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.agents.unlink(
        '31b25934-5da2-11ec-bf63-0242ac130002',
        '31b25b78-5da2-11ec-bf63-0242ac130002',
        '31b25c7c-5da2-11ec-bf63-0242ac130002'
    )
    assert isinstance(res, dict)
    assert 'task_id' in list(res.keys())
