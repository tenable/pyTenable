'''
Test cases agent groups API
'''
import re
from uuid import UUID

import responses
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

BASE_URL = 'https://cloud.tenable.com/api/v3/agent-groups'
AGENT_FILTER_URL = 'https://cloud.tenable.com/api/v3/definitions/scans/agents'


@responses.activate
def test_add_agent_with_single_agent_id(api):
    '''
    Test case for agent groups add_agent method with sigle agent id
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
    Test case for agent groups add_agent method with multiple agent id
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
    Test case for agent groups configure method
    '''
    group_id: UUID = 'e069b272-ed76-487a-8cf9-1c32836698b7'
    name: str = 'test name 2'
    payload = {'name': name}
    test_response = {
        'id': group_id,
        'name': name,
        'creation_date': '2022-01-31T06:18:45Z',
        'last_modification_date': '2022-01-31T06:18:45Z',
        'timestamp': '2022-01-31T06:18:45Z',
        'shared': 0,
        'owner': {
            'owner_id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            'owner_name': 'system'
        },
        'user_permissions': 0,
        'agents_count': 0
    }
    responses.add(
        responses.PUT,
        re.compile(f'{BASE_URL}/{group_id}'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )
    res = api.v3.vm.agent_groups.configure(group_id, name)
    assert isinstance(res, dict)
    assert res['name'] == name


@responses.activate
def test_create(api):
    '''
    Test case for agent groups create method
    '''
    name: str = 'Agent Group 1'
    test_response: dict = {
        'id': 'd1bdf0b4-f31d-4147-af83-9d528c86ea66',
        'name': name,
        'creation_date': '2022-01-31T06:18:45Z',
        'last_modification_date': '2022-01-31T06:18:45Z',
        'timestamp': '2022-01-31T06:18:45Z',
        'shared': 0,
        'owner': {
            'owner_id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
            'owner_name': 'system'
        },
        'user_permissions': 0,
        'agents_count': 0
    }
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}'),
        match=[responses.matchers.json_params_matcher({'name': name})],
        json=test_response
    )
    res = api.v3.vm.agent_groups.create(name)
    assert isinstance(res, dict)
    assert res['name'] == name


@responses.activate
def test_delete(api):
    '''
    Test case for agent groups delete method
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
    Test case for agent groups delete_agent method
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
    Test case for agent groups delete_agent method
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
    Test case for agent groups task_status method
    '''
    group_id: UUID = 'fs252fdg-4b7c-4d2b-99a1-dvsdsv4242vf'
    task_id: UUID = '02683e5e-4b7c-4d2b-99a1-cde1ea0940d9'
    test_response = {
        'task_id': '02683e5e-4b7c-4d2b-99a1-cde1ea0940d9',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'COMPLETED',
        'message': 'Finished bulk addToGroup operation.',
        'start_time': '2022-01-31T06:18:45Z',
        'end_time': '2022-01-31T06:19:45Z',
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
    Test case for agent groups details method
    '''
    group_id: UUID = 'ea81c0e9-a041-45d6-a654-80570d6bee97'
    filters: tuple = ('platform', 'match', ['window'])
    filter_type: str = 'and'
    limit: int = 50
    offset: int = 0
    sort: list = [('name', 'asc')]
    wildcard: str = 'IYKKQIGOBWXUXOZIBURFENPNMGZOSWBUKVCD'
    wildcard_fields: list = ['name']

    test_response: dict = {
        'id': group_id,
        'name': 'Western Region',
        'creation_date': '2022-01-31T06:18:45Z',
        'last_modification_date': '2022-01-31T06:18:45Z',
        'timestamp': '2022-01-31T06:18:45Z',
        'shared': 1,
        'owner': {
            'name': 'system',
            'id': '1bd703af-b2aa-4a82-ad8d-b883381a873f'
        },
        'user_permissions': 128,
        'agents_count': 0,
        'agents': [],
        'pagination': {
            'total': 0,
            'limit': 50,
            'offset': 0,
            'sort': [
                {
                    'name': 'name',
                    'order': 'asc'
                }
            ]
        }
    }

    # Let's register the response for agents filter endpoint
    responses.add(
        responses.GET,
        f'{AGENT_FILTER_URL}',
        json={
            'wildcard_fields': [
                'core_version',
                'distro',
                'groups',
                'ip',
                'name',
                'platform',
                'status'
            ],
            'filters': [
                {
                    'name': 'platform',
                    'readable_name': 'Platform',
                    'operators': [
                        'eq',
                        'neq',
                        'match',
                        'nmatch'
                    ],
                    'control': {
                        'readable_regex': 'Platform Name (e.g. Linux)',
                        'type': 'entry',
                        'regex': '.*'
                    }
                }
            ],
            'sort': {
                'sortable_fields': [
                    'core_version',
                    'distro',
                    'ip',
                    'last_connect',
                    'last_scanned',
                    'name',
                    'platform',
                    'plugin_feed_id'
                ]
            }
        }
    )

    responses.add(
        responses.GET,
        f'{BASE_URL}/{group_id}',
        json=test_response
    )

    res = api.v3.vm.agent_groups.details(
        group_id,
        filters,
        filter_type=filter_type,
        limit=limit,
        offset=offset,
        sort=sort,
        wildcard=wildcard,
        wildcard_fields=wildcard_fields
    )
    assert isinstance(res, dict)
    assert res['id'] == group_id


@responses.activate
def test_search(api):
    '''
    Test case for agent groups search method
    '''
    test_response: dict = {
        'agent_groups': [
            {
                'id': '801cc413-bae9-4b84-b53c-f4b86056b9fd',
                'name': 'test-007',
                'creation_date': '2022-01-06T17:19:52Z',
                'last_modification_date': '2022-01-06T17:19:52Z',
                'timestamp': '2022-01-06T17:19:52Z',
                'shared': 0,
                'owner': {
                    'owner_id': '3bfcfb11-6c12-405b-b7ba-bbc705cd2a6e',
                    'owner_name': 'system'
                },
                'user_permissions': 0,
                'agents_count': 1
            }
        ],
        'pagination': {
            'next': 'nextToken',
            'total': 1
        }
    }

    fields: list = [
        'name',
        'id',
        'created',
        'modified',
        'owner_id',
        'agents_count'
    ]

    filter = {
        'and': [{
            'property': 'modified',
            'operator': 'date-eq',
            'value': '2021-06-25T15:19:24Z'
        }]
    }

    sort = [('name', 'asc')]

    # Let's create sample payload for search exclusion endpoint
    payload = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'name': 'asc'}],
    }

    # Let's register the mock response for search endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}/search',
        json=test_response,
        match=[responses.matchers.json_params_matcher(payload)],
    )

    iterator = api.v3.vm.agent_groups.search(
        fields=fields, filter=filter, sort=sort, limit=200
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == test_response['pagination']['total']

    iterator = api.v3.vm.agent_groups.search(
        fields=fields, filter=filter, sort=sort, return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.agent_groups.search(
        fields=fields, filter=filter, sort=sort, return_resp=True, limit=200
    )
    assert isinstance(resp, Response)


@responses.activate
def test_send_instruction_to_agents_in_group(api):
    '''
    Test case for agent groups send_instruction_to_agents_in_group method
    '''
    group_id: UUID = 'ea81c0e9-a041-45d6-a654-80570d6bee97'
    all_agents: bool = True
    wildcard: str = 'sdfknskdnf'
    filters: list = ['name:match:laptop']
    filter_type: str = 'and'
    hardcoded_filters: list = ['core_version:lt:10.0.0']
    not_items: list = ['334b962a-ac03-4336-9ebb-a06b321576e0']
    directive_type: str = 'restart'

    test_response: dict = {
        "task_id": "7aaae2f3-544d-497f-b0f0-447d03d7cd55",
        "container_id": "3cc182bb-b8ba-4025-9e59-9a81b8a64d5a",
        "status": "RUNNING",
        "message": "Starting...",
        "start_time": '2022-01-18T10:36:44Z',
        "last_update_time": '2022-01-18T10:36:44Z',
        "total_work_units": 3,
        "total_work_units_completed": 0,
        "completion_percentage": 0
    }

    payload: dict = {
        'items': [
            '334b962a-ac03-4336-9ebb-a06b169576e0'
        ],
        'not_items': not_items,
        'criteria': {
            'all_agents': all_agents,
            'filters': filters,
            'hardcoded_filters': hardcoded_filters,
            'wildcard': wildcard,
            'filter_type': filter_type
        },
        'directive': {
            'type': directive_type
        }
    }

    # let's register the response for api endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/{group_id}/agents/_bulk/directive'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agent_groups.send_instruction_to_agents_in_group(
        group_id,
        '334b962a-ac03-4336-9ebb-a06b169576e0',
        directive_type='restart',
        all_agents=True,
        wildcard='sdfknskdnf',
        filters=['name:match:laptop'],
        filter_type='and',
        hardcoded_filters=['core_version:lt:10.0.0'],
        not_items=['334b962a-ac03-4336-9ebb-a06b321576e0']
    )

    assert isinstance(res, dict)
    assert 'task_id' in list(res.keys())
