'''
Test Agents
'''
import re
from uuid import UUID

import responses
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.base.iterators.tio_iterator import TIOIterator

BASE_URL: str = 'https://cloud.tenable.com/api/v3/agents'
AGENT_FILTER_URL = 'https://cloud.tenable.com/api/v3/definitions/scans/agents'


@responses.activate
def test_details(api):
    '''
    Test case for agents details method
    '''
    agent_id: UUID = 'd59d1f5b-f775-4061-9e36-fae22ab7518f2596d192e3cf57f8'

    # Let's create test response for api endpoint
    test_response: dict = {
        'id': agent_id,
        'name': 'DESKTOP-PSNDJQ6',
        'platform': 'WINDOWS',
        'distro': 'win-x86-64',
        'ip': '192.0.2.57',
        'last_scanned': '2022-01-18T10:36:44Z',
        'plugin_feed_id': '0',
        'linked_on': '2022-01-18T10:36:44Z',
        'status': 'off'
    }

    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/{agent_id}'),
        json=test_response
    )

    res = api.v3.vm.agents.details(agent_id)

    assert isinstance(res, dict)
    assert res['id'] == agent_id


@responses.activate
def test_list_agents_from_group(api):
    '''
    Test case for agents list_agents_from_groups method
    '''
    group_id: int = 469892
    filters: list = [('platform', 'match', ['window'])]
    filter_type: str = 'and'
    limit: int = 50
    offset: int = 0
    sort: list = [('name', 'asc')]
    wildcard: str = 'IYKKQIGOBWXUXOZIBURFENPNMGZOSWBUKVCD'
    wildcard_fields: list = ['name']

    test_response: dict = {
        'agents': [{
            'id': '96efbd47-9d96-443f-be29-2ac723dde270',
            'name': 'Codys-MacBook-Pro.local',
            'platform': 'window',
            'distro': 'macosx',
            'ip': '10.31.100.110',
            'last_scanned': '2022-01-18T10:36:44Z',
            'plugin_feed_id': '201812281741',
            'core_build': '1',
            'core_version': '7.2.1',
            'linked_on': '2022-01-18T10:36:44Z',
            'last_connect': '2022-01-18T10:36:44Z',
            'status': 'off',
            'groups': [{
                    'name': 'Agent Group A',
                    'id': 8
                },
                {
                    'name': 'Agent Group B',
                    'id': 31
                }
            ],
            'supports_remote_logs': False
        }],
        'pagination': {
            'total': 1,
            'limit': 50,
            'offset': 0,
            'sort': [{
                'name': 'name',
                'order': 'asc'
            }]
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
                },
                {
                    'name': 'status',
                    'readable_name': 'Status',
                    'operators': [
                        'eq',
                        'neq'
                    ],
                    'control': {
                        'type': 'dropdown',
                        'list': [
                            'Online',
                            'Offline',
                            'Initializing'
                        ]
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

    # let's register the response for API endpoint
    api_path = f'api/v3/agent-groups/{group_id}/agents'
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/{api_path}',
        json=test_response
    )

    res = api.v3.vm.agents.list_agents_from_group(
        group_id=group_id,
        filters=filters,
        filter_type=filter_type,
        limit=limit,
        offset=offset,
        sort=sort,
        wildcard=wildcard,
        wildcard_fields=wildcard_fields
    )

    values_list: list = []
    for item in res:
        values_list.append(item)

    assert isinstance(res, TIOIterator)
    assert len(values_list) == test_response['pagination']['total']


@responses.activate
def test_task_status(api):
    '''
    Test case for agents task_status method
    '''
    test_response: dict = {
        'task_id': '61a1320b-51e4-4244-9b34-694247384e8d',
        'container_id': 'cfdabb09-6aef-481d-b28f-aecb1c38f297',
        'status': 'COMPLETED',
        'message': 'Finished bulk unlink operation.',
        'start_time': '2022-01-18T10:36:44Z',
        'end_time': '2022-01-18T11:36:44Z',
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
def test_unlink_with_bulk_agents(api):
    '''
    Test case for agents unlink method
    '''
    test_response: dict = {
        'task_id': '7aaae2f3-544d-497f-b0f0-447d03d7cd55',
        'container_id': '3cc182bb-b8ba-4025-9e59-9a81b8a64d5a',
        'status': 'RUNNING',
        'message': 'Starting...',
        'start_time': '2022-01-18T10:36:44Z',
        'last_update_time': '2022-01-18T10:36:44Z',
        'total_work_units': 3,
        'total_work_units_completed': 0,
        'completion_percentage': 0
    }
    payload: dict = {
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


@responses.activate
def test_search(api):
    '''
    Test case for agents search method
    '''
    # Let's create sample response for API endpoint
    test_response: dict = {
        'agents': [
            {
                'distro': 'linux-distro-1',
                'ui_version': '3.3.3 (#777)',
                'ui_build': '777',
                'uuid': '00055374-39a8-4940-b296-5dc86d0f9894',
                'platform': 'Linux (linux-distro-1)',
                'network': {
                    'uuid': '00000000-0000-0000-0000-000000000000'
                },
                'mac_addrs': '02:42:ac:11:00:02',
                'aws_account_id': '007',
                'last_scanned': 1586478168315,
                'modified': 1575431183,
                'id': 2801646,
                'last_connect': 1575434652000,
                'ui_version_as_int': 30303,
                'created': 1575431183,
                'ip': '31.137.192.166',
                'aws_public_ipv4': '7.7.7.7',
                'groups': [
                    {
                        'name': 'samgroup',
                        'id': 428283
                    },
                    {
                        'name': 'samgroup2',
                        'id': 428284
                    },
                    {
                        'name': 'samgroup3',
                        'id': 428285
                    }
                ],
                'last_plugin_update': '202006131756',
                'token': 'sddfghfhjhtgsgvseveegsevgedrhrthsbrgbsfgvsgse',
                'container_uuid': 'bf80392b-646e-4a45-ba07-5670efee1b08',
                'name': '01c836ad-2263-4cfb-ae13-d5a01fcefe19',
                'aws_public_hostname': 'SEVEN',
                'aws_instance_id': '77',
                'linked_on': 1575431183139,
                'engine_version': '0.0.7',
                'status': 'off'
            },
            {
                'distro': 'distro',
                'ui_version': '6.10.9 (#123)',
                'ui_build': '123',
                'uuid': '00000000-0000-0000-0003-000000000999',
                'platform': 'platform (distro)',
                'network': {
                    'uuid': '00000000-0000-0000-0000-000000000000'
                },
                'modified': 1624572525,
                'id': 2978420,
                'ui_version_as_int': 61009,
                'created': 1624572525,
                'ip': '10.0.0.3',
                'aws_public_ipv4': '172.18.32.199',
                'token': 'sddfghfhjhtgsgvseveegsevgedrhrthsbrgbsfgvsgse',
                'container_uuid': 'bf80392b-646e-4a45-ba07-5670efee1b08',
                'name': 'sam',
                'aws_public_hostname': 'i-AWSINSTID.aws.amazon.com',
                'aws_instance_id': 'i-AWSINSTID',
                'linked_on': 1624572525967,
                'engine_version': '6.10.9',
                'status': 'off'
            }
        ],
        'pagination': {
            'next': 'nextToken',
            'total': 2
        }
    }

    fields: list = [
        'id',
        'name',
        'platform',
        'distro',
        'ip',
        'last_scanned',
        'plugin_feed_id',
        'core_build',
        'core_version',
        'linked_on',
        'last_connect',
        'status',
        'groups'
    ]

    filter: dict = {
        'and': [
            {
                'property': 'id',
                'operator': 'eq',
                'value': '655993d5-c131-46e8-a82f-957f6f894cac'
            },
            {
                'property': 'name',
                'operator': 'eq',
                'value': 'GRD-LPTP'
            }
        ]
    }

    sort: list = [('name', 'asc')]

    # Let's create sample payload for search API endpoint
    payload: dict = {
        'fields': fields,
        'filter': filter,
        'limit': 200,
        'sort': [{'name': 'asc'}]
    }

    # Let's register the mock response for search endpoint
    responses.add(
        responses.POST,
        f'{BASE_URL}/search',
        json=test_response,
        match=[responses.matchers.json_params_matcher(payload)],
    )

    iterator = api.v3.vm.agents.search(
        fields=fields,
        filter=filter,
        sort=sort,
        limit=200
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == test_response['pagination']['total']

    iterator = api.v3.vm.agents.search(
        fields=fields,
        filter=filter,
        sort=sort,
        return_csv=True
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.vm.agents.search(
        fields=fields,
        filter=filter,
        sort=sort,
        return_resp=True,
        limit=200
    )
    assert isinstance(resp, Response)


@responses.activate
def test_add_agents_to_network(api):
    '''
    Test case for Agents add_agents_to_network method
    '''
    all_agents: bool = True
    wildcard: str = 'sdfknskdnf'
    filters: list = ['name:match:laptop']
    filter_type: str = 'and'
    hardcoded_filters: list = ['core_version:lt:10.0.0']
    not_items: list = ['334b962a-ac03-4336-9ebb-a06b321576e0']

    test_response: dict = {
        'task_id': '7aaae2f3-544d-497f-b0f0-447d03d7cd55',
        'container_id': '3cc182bb-b8ba-4025-9e59-9a81b8a64d5a',
        'status': 'RUNNING',
        'message': 'Starting...',
        'start_time': '2022-01-18T10:36:44Z',
        'last_update_time': '2022-01-18T10:36:44Z',
        'total_work_units': 3,
        'total_work_units_completed': 0,
        'completion_percentage': 0
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
        }
    }

    # let's register the response for api endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/_bulk/addToNetwork'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agents.add_agents_to_network(
        '334b962a-ac03-4336-9ebb-a06b169576e0',
        all_agents=True,
        wildcard='sdfknskdnf',
        filters=['name:match:laptop'],
        filter_type='and',
        hardcoded_filters=['core_version:lt:10.0.0'],
        not_items=['334b962a-ac03-4336-9ebb-a06b321576e0']
    )

    assert isinstance(res, dict)
    assert 'task_id' in list(res.keys())


@responses.activate
def test_remove_agent_from_network(api):
    '''
    Test case for Agents remove_agent_from_network method
    '''
    all_agents: bool = True
    wildcard: str = 'sdfknskdnf'
    filters: list = ['name:match:laptop']
    filter_type: str = 'and'
    hardcoded_filters: list = ['core_version:lt:10.0.0']
    not_items: list = ['334b962a-ac03-4336-9ebb-a06b321576e0']

    test_response: dict = {
        'task_id': '7aaae2f3-544d-497f-b0f0-447d03d7cd55',
        'container_id': '3cc182bb-b8ba-4025-9e59-9a81b8a64d5a',
        'status': 'RUNNING',
        'message': 'Starting...',
        'start_time': '2022-01-18T10:36:44Z',
        'last_update_time': '2022-01-18T10:36:44Z',
        'total_work_units': 3,
        'total_work_units_completed': 0,
        'completion_percentage': 0
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
        }
    }

    # let's register the response for api endpoint
    responses.add(
        responses.POST,
        re.compile(f'{BASE_URL}/_bulk/removeFromNetwork'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agents.remove_agent_from_network(
        '334b962a-ac03-4336-9ebb-a06b169576e0',
        all_agents=True,
        wildcard='sdfknskdnf',
        filters=['name:match:laptop'],
        filter_type='and',
        hardcoded_filters=['core_version:lt:10.0.0'],
        not_items=['334b962a-ac03-4336-9ebb-a06b321576e0']
    )

    assert isinstance(res, dict)
    assert 'task_id' in list(res.keys())


@responses.activate
def test_send_instructuion_to_agent(api):
    '''
    Test case for Agents send_instructuion_to_agent method
    '''
    all_agents: bool = True
    wildcard: str = 'sdfknskdnf'
    filters: list = ['name:match:laptop']
    filter_type: str = 'and'
    hardcoded_filters: list = ['core_version:lt:10.0.0']
    not_items: list = ['334b962a-ac03-4336-9ebb-a06b321576e0']
    directive_type: str = 'restart'

    test_response: dict = {
        'task_id': '7aaae2f3-544d-497f-b0f0-447d03d7cd55',
        'container_id': '3cc182bb-b8ba-4025-9e59-9a81b8a64d5a',
        'status': 'RUNNING',
        'message': 'Starting...',
        'start_time': '2022-01-18T10:36:44Z',
        'last_update_time': '2022-01-18T10:36:44Z',
        'total_work_units': 3,
        'total_work_units_completed': 0,
        'completion_percentage': 0
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
        re.compile(f'{BASE_URL}/_bulk/directive'),
        match=[responses.matchers.json_params_matcher(payload)],
        json=test_response
    )

    res = api.v3.vm.agents.send_instructuion_to_agent(
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
