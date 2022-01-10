'''
test plugins
'''
import re
from uuid import UUID

import pytest
import responses

BASE_URL = 'https://cloud.tenable.com/api/v3/agent-groups'


@responses.activate
def test_add_agent_with_single_agent_id(api):
    '''
    Test case for add_agent method with sigle agent id
    '''
    group_id: UUID = '2b2db604-5d92-11ec-bf63-0242ac130002'
    agent_id: UUID = '3f8eed68-5d95-11ec-bf63-0242ac130002'
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/{group_id}/agents/{agent_id}')
    )
    res = api.v3.vm.agent_groups.add_agent(group_id, agent_id)
    assert res is None


@responses.activate
def test_add_agent_with_multiple_agent_id(api):
    '''
    Test case for add_agent method with multiple agent id
    '''
    group_id: UUID = '2b2db604-5d92-11ec-bf63-0242ac130002'
    payload = {
        'items': [
            i for i in (
                '57b74c0a-5d95-11ec-bf63-0242ac130002',
                '57b74e58-5d95-11ec-bf63-0242ac130002',
                '57b74f66-5d95-11ec-bf63-0242ac130002'
            )
        ]
    }
    test_response = {
        'task_id': '07a665f4-6e09-444b-b9ce-ed5ccf5c193b',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'NEW',
        'message': 'Beginning bulk addToGroup operation'
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/{group_id}/agents/_bulk/add'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.agent_groups.add_agent(
        group_id,
        '57b74c0a-5d95-11ec-bf63-0242ac130002',
        '57b74e58-5d95-11ec-bf63-0242ac130002',
        '57b74f66-5d95-11ec-bf63-0242ac130002'
    )
    assert isinstance(res, dict)
    assert 'container_id' in list(res.keys())
    assert 'task_id' in list(res.keys())


@responses.activate
def test_configure(api):
    '''
    Test case for configure method
    '''
    group_id: UUID = 'e069b272-ed76-487a-8cf9-1c32836698b7'
    name: str = 'test name 2'
    payload = {'name': name}
    test_response = {
        'agent_groups': [
            {
                'owner_id': '2e3a71fc-2442-4024-9fee-085cc61750cb',
                'created': 1595001140400,
                'modified': 1595001217809,
                'container_id': 'd6c3e937-4467-4171-92d8-debf5ef3c917',
                'id': 'e069b272-ed76-487a-8cf9-1c32836698b7',
                'name': name,
                'agents_count': 0,
                'default_permissions': 16,
                'shared': 1,
                'user_permissions': 128,
                'created_in_seconds': 1595001140,
                'modified_in_seconds': 1595001217
            }
        ]
    }
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/{group_id}'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.agent_groups.configure(group_id, name)
    assert isinstance(res, dict)
    assert res['agent_groups'][0]['name'] == name


@responses.activate
def test_create(api):
    '''
    Test case for create method
    '''
    name: str = 'test'
    test_response: dict = {
        'agent_groups': [
            {
                'id': 'ef62870e-fe2f-4ba9-98b7-43d3a53ffe85',
                'name': name,
                'creation_date': 1635756224,
                'last_modification_date': 1635756224,
                'timestamp': 1635756224,
                'shared': 1,
                'owner': {
                    'name': 'system',
                    'id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e'
                },
                'user_permissions': 128,
                'agents_count': 0
            }
        ]
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}'),
        match=[responses.matchers.json_params_matcher({'name': name})],
        json=test_response
    )
    res = api.v3.vm.agent_groups.create(name)
    assert isinstance(res, dict)
    assert res['agent_groups'][0]['name'] == name


@responses.activate
def test_delete(api):
    '''
    Test case for delete method
    '''
    group_id: UUID = 'e069b272-ed76-487a-8cf9-1c32836698b7'
    responses.add(
        responses.DELETE,
        re.compile(f'{BASE_URL}/{group_id}'),
        status=200
    )
    res = api.v3.vm.agent_groups.delete(group_id)
    assert res is None


@responses.activate
def test_delete_agent_with_single_agent_id(api):
    '''
    Test case for delete_agent method
    '''
    group_id: UUID = '2b2db604-5d92-11ec-bf63-0242ac130002'
    agent_id: UUID = '3f8eed68-5d95-11ec-bf63-0242ac130002'
    responses.add(
        responses.DELETE,
        re.compile(f'{BASE_URL}/{group_id}/agents/{agent_id}')
    )
    res = api.v3.vm.agent_groups.delete_agent(group_id, agent_id)
    assert res is None


@responses.activate
def test_delete_agent_with_multiple_agent_id(api):
    '''
    Test case for delete_agent method
    '''
    group_id: UUID = 'fs252fdg-4b7c-4d2b-99a1-dvsdsv4242vf'
    payload = {
        'items': [
            i for i in (
                '57b74c0a-5d95-11ec-bf63-0242ac130002',
                '57b74e58-5d95-11ec-bf63-0242ac130002',
                '57b74f66-5d95-11ec-bf63-0242ac130002'
            )
        ]
    }
    test_response = {
        'task_id': 'c26d637e-8533-411b-920c-5f49faeb270d',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'NEW',
        'message': 'Beginning bulk removeFromGroup operation'
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/{group_id}/agents/_bulk/remove'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.agent_groups.delete_agent(
        group_id,
        '57b74c0a-5d95-11ec-bf63-0242ac130002',
        '57b74e58-5d95-11ec-bf63-0242ac130002',
        '57b74f66-5d95-11ec-bf63-0242ac130002'
    )
    assert isinstance(res, dict)
    assert 'container_id' in list(res.keys())
    assert 'task_id' in list(res.keys())


@responses.activate
def test_task_status(api):
    '''
    Test case for task_status method
    '''
    group_id: UUID = 'fs252fdg-4b7c-4d2b-99a1-dvsdsv4242vf'
    task_id: UUID = '02683e5e-4b7c-4d2b-99a1-cde1ea0940d9'
    test_response = {
        'task_id': '02683e5e-4b7c-4d2b-99a1-cde1ea0940d9',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'COMPLETED',
        'message': 'Finished bulk addToGroup operation.',
        'start_time': 1638807034721,
        'end_time': 1638807034730,
        'total_work_units_completed': 0
    }
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/{group_id}/agents/_bulk/{task_id}'),
        json=test_response
    )
    res = api.v3.vm.agent_groups.task_status(group_id, task_id)
    assert isinstance(res, dict)
    assert 'container_id' in list(res.keys())
    assert 'task_id' in list(res.keys())


@responses.activate
def test_details(api):
    '''
    Test case for details method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.agent_groups.details()


@responses.activate
def test_search(api):
    '''
    Test case for search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.agent_groups.search()
