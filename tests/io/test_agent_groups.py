"""
test agent groups
"""

import time
import uuid
from unittest.mock import patch

import pytest
import responses
from responses import matchers

from tenable.errors import NotFoundError, UnexpectedValueError, ForbiddenError
from ..checker import check

FILTERS_SCANS_AGENTS = {
    'wildcard_fields': ['core_version', 'distro', 'groups'],
    'filters': [
        {
            'name': 'core_version',
            'readable_name': 'Version',
            'operators': ['eq', 'neq', 'match'],
            'control': {'readable_regex': 'X.Y.Z', 'type': 'entry', 'regex': '.*'},
        },
        {
            'name': 'status',
            'readable_name': 'Status',
            'operators': ['eq', 'neq'],
            'control': {
                'type': 'dropdown',
                'list': ['Online', 'Offline', 'Initializing'],
            },
        },
        {
            'name': 'name',
            'readable_name': 'Name',
            'operators': ['eq', 'neq', 'match'],
            'control': {'readable_regex': 'TEXT', 'type': 'entry', 'regex': '.*'},
        },
    ],
    'sort': {'sortable_fields': ['core_version', 'distro', 'ip']},
}

SCANNERS_AGENTS = {
    'agents': [
        {
            'id': 2022688,
            'uuid': 'f3800546-1813-499d-8352-57d28d58dc97',
            'name': '00fc9870f38d',
            'platform': 'LINUX',
            'distro': 'es7-x86-64',
            'ip': '172.17.0.2',
            'linked_on': 1522359489,
            'status': 'off',
        },
        {
            'id': 2012393,
            'uuid': 'f4f3c03b-f2dd-4891-befd-f5fd545209b3',
            'name': '0111b4be0d31',
            'platform': 'LINUX',
            'distro': 'es7-x86-64',
            'ip': '172.17.0.4',
            'linked_on': 1521058311,
            'status': 'off',
        },
    ],
    'pagination': {'total': 751, 'limit': 50, 'offset': 0},
}


@pytest.fixture
def agentgroup():
    """
    agent group fixture
    """
    return {
        'id': 106521,
        'uuid': '54fcb935-c022-46a5-95b8-ed6daf8647b4',
        'name': '3a7c8527-fdac-4251-8c69-39549523dd49',
        'creation_date': 1544138315,
        'last_modification_date': 1544138315,
        'timestamp': 1544138315,
        'shared': 0,
        'owner': 'system',
        'owner_id': 1,
        'owner_name': 'system',
        'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
        'user_permissions': 0,
        'agents_count': 0,
    }


def test_agentgroups_add_agent_to_group_group_id_typeerror(tvm):
    """
    test to raise the exception when type of group_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.add_agent('nope', 1)


def test_agentgroups_add_agent_to_group_agent_id_typeerror(tvm):
    """
    test to raise the exception when type of agent_id is not as defined
    """
    with pytest.raises(UnexpectedValueError):
        tvm.agent_groups.add_agent(1, 'nope')


def test_agentgroups_add_agent_to_group_mixed_ids_typeerror(tvm):
    """
    test to raise the exception when type of multiple passed ids don't match each other
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.add_agent(1, '64e1cc37-4d6a-4a36-a2d3-aca300735829', 2)


def test_agentgroups_add_agent_to_group_scanner_id_typeerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.add_agent(1, 1, scanner_id='nope')


@responses.activate
def test_agentgroups_add_agent_to_group_notfounderror(tvm):
    """
    test to add agent to group and agent not found
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agent-groups/1/agents/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'AgentGroup with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.agent_groups.add_agent(1, 1)


@responses.activate
def test_agentgroups_add_agent_to_group_standard_user_permissionerror(tvm):
    """
    test to raise the exception when standard user adds agent to group
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agent-groups/1/agents/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_groups.add_agent(1, 1)


@responses.activate
def test_agentgroups_add_agent_to_group(tvm, agentgroup, agent):
    """
    test to add single agent to the group
    """
    responses.add(
        responses.PUT, 'https://nourl/scanners/1/agent-groups/106521/agents/2022688'
    )
    tvm.agent_groups.add_agent(agentgroup['id'], agent['id'])


@responses.activate
def test_agentgroups_add_mult_agents_to_group(tvm, agentgroup):
    """
    test to add multiple agents to group
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents',
        json=SCANNERS_AGENTS,
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agent-groups/106521/agents/_bulk/add',
        json={
            'task_id': '3cbebd3c-0818-4eb8-9d06-c72b1d625ee2',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'status': 'NEW',
        },
    )
    agents = tvm.agents.list()
    task = tvm.agent_groups.add_agent(
        agentgroup['id'], agents.next()['id'], agents.next()['id']
    )
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'status', str)
    check(task, 'task_id', str)


def test_agentgroups_configure_group_id_typeerror(tvm):
    """
    test to raise the exception when type of group_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.configure('nope', 1)


def test_agentgroups_configure_name_typeerror(tvm):
    """
    test to raise the exception when type of name is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.configure(1, 1)


# @pytest.mark.vcr()
# def test_agentgroups_configure_scanner_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.agent_groups.configure(1, 1, scanner_id='nope')


@responses.activate
def test_agentgroups_configure_standard_user_permissionerror(tvm, agentgroup):
    """
    test to raise the exception when standard user tries to configure

    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agent-groups/106521',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))


@responses.activate
def test_agentgroups_configure_change_name(tvm, agentgroup):
    """
    test to configure name
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agent-groups/106521',
        json={
            'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
            'created': 1544138324470,
            'modified': 1544138325484,
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'uuid': '54fcb935-c022-46a5-95b8-ed6daf8647b4',
            'id': 106521,
            'name': '07beb326-df98-4656-b716-ee578841ce69',
            'agents_count': 0,
            'default_permissions': 16,
            'shared': 1,
            'user_permissions': 128,
            'created_in_seconds': 1544138324,
            'modified_in_seconds': 1544138325,
        },
    )
    tvm.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))


def test_agentgroups_create_name_typeerror(tvm):
    """
    test to raise the exception when type of name is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.create(True)


def test_agentgroups_create_scanner_id_typeerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.create(str(uuid.uuid4()), 'nope')


@responses.activate
def test_agentgroups_create_standard_user_permissionerror(tvm):
    """
    test to raise the exception for standard user for creating agent group
    """
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agent-groups',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_groups.create(str(uuid.uuid4()))


@responses.activate
def test_agentgroups_create_agent_group(tvm, agentgroup):
    """
    test to create agent group
    """
    responses.add(
        responses.POST, 'https://nourl/scanners/1/agent-groups', json=agentgroup
    )
    agentgroup = tvm.agent_groups.create(agentgroup['name'])
    assert isinstance(agentgroup, dict)
    check(agentgroup, 'creation_date', int)
    check(agentgroup, 'id', int)
    check(agentgroup, 'last_modification_date', int)
    check(agentgroup, 'name', str)
    check(agentgroup, 'owner', str)
    check(agentgroup, 'owner_id', int)
    check(agentgroup, 'owner_name', str)
    check(agentgroup, 'owner_uuid', 'uuid')
    check(agentgroup, 'shared', int)
    check(agentgroup, 'timestamp', int)
    check(agentgroup, 'user_permissions', int)
    check(agentgroup, 'uuid', 'uuid')


def test_agentgroups_delete_attributeerror(tvm):
    """
    test to raise the exception when no arguments are passed
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.delete()


def test_agentgroups_delete_group_id_typeerror(tvm):
    """
    test to raise the exception when type of group_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.delete('nope')


def test_agentgroups_delete_scanner_id_typerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.delete(1, scanner_id='nope')


@responses.activate
def test_agentgroups_delete_agent_group(tvm, agentgroup):
    """
    test to delete the agent group
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agent-groups/106521')
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/106521',
        json={'error': 'AgentGroup not found.'},
        status=404,
    )
    tvm.agent_groups.delete(agentgroup['id'])
    with pytest.raises(NotFoundError):
        tvm.agent_groups.details(agentgroup['id'])


def test_agentgroups_delete_agent_from_group_group_id_typeerror(tvm):
    """
    test to raise the exception when type of group_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.delete_agent('nope', 1)


def test_agentgroups_delete_agent_from_group_agent_id_typeerror(tvm):
    """
    test to raise the exception when type of agent_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.delete_agent(1, 'nope')


def test_agentgroups_delete_agent_from_group_scanner_id_typeerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.delete_agent(1, 1, scanner_id='nope')


def test_agentgroups_delete_agents_alias(tvm):
    """
    The plural spelling should preserve the existing delete-agent behavior.
    """
    agent_groups = tvm.agent_groups
    with patch.object(
        agent_groups, 'delete_agent', return_value={'task_id': 'task'}
    ) as delete_agent:
        result = agent_groups.delete_agents(42, 10, 11, scanner_id=7)

    assert result == {'task_id': 'task'}
    delete_agent.assert_called_once_with(42, 10, 11, scanner_id=7)


@responses.activate
def test_agentgroups_delete_agent_from_group_notfounderror(tvm):
    """
    test to delete agent from the group and agent is not found to delete
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanners/1/agent-groups/1/agents/1',
        json={
            'statusCode': 404,
            'error': 'Not Found',
            'message': 'AgentGroup with id 1 not found.',
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.agent_groups.delete_agent(1, 1)


@responses.activate
def test_agentgroups_delete_agent_from_group_standard_user_permissionerror(tvm):
    """
    test to raise the exception when standard user tris to delete the agent from the group
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanners/1/agent-groups/1/agents/1',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_groups.delete_agent(1, 1)


@responses.activate
def test_agentgroups_delete_agent_from_group(tvm, agent, agentgroup):
    """
    test to delete single agent from the group

    """
    responses.add(
        responses.PUT, 'https://nourl/scanners/1/agent-groups/106521/agents/2022688'
    )
    responses.add(
        responses.DELETE, 'https://nourl/scanners/1/agent-groups/106521/agents/2022688'
    )
    tvm.agent_groups.add_agent(agentgroup['id'], agent['id'])
    tvm.agent_groups.delete_agent(agentgroup['id'], agent['id'])


@responses.activate
def test_agentgroups_delete_mult_agents_from_group(tvm, agentgroup):
    """
    test to delete the multiple agents from the group
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents',
        json=SCANNERS_AGENTS,
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agent-groups/106521/agents/_bulk/add',
        json={
            'task_id': '99a62d65-a584-471d-965d-9e5d04db2f20',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'status': 'NEW',
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agent-groups/106521/agents/_bulk/remove',
        json={
            'task_id': '51c4c613-c80f-4df6-9449-f5c13ea12de5',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'status': 'NEW',
            'start_time': 1547163522852,
            'last_update_time': 1547163522852,
        },
    )
    agents = tvm.agents.list()
    alist = [agents.next()['id'], agents.next()['id']]
    tvm.agent_groups.add_agent(agentgroup['id'], *alist)
    time.sleep(1)
    task = tvm.agent_groups.delete_agent(agentgroup['id'], *alist)
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'status', str)
    check(task, 'task_id', str)


@responses.activate
def test_agentgroups_details_group_id_typeerror(tvm):
    """
    test to raise the exception when type of task_uuid is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agent_groups.details('nope')


@responses.activate
def test_agentgroups_details_scanner_id_typeerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError) as type_error:
        tvm.agent_groups.details(1, scanner_id='nope')
    assert type_error.value.args[0] == 'scanner_id is of type str.  Expected int', (
        'Invalid type validation error for scanner_id parameter is not raised by test-case.'
    )


@responses.activate
def test_agentgroups_details_agentgroup_notfounderror(tvm):
    """
    test to raise the exception when agentgroup not found
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/1',
        json={'error': 'AgentGroup not found.'},
        status=404,
        match=[matchers.query_param_matcher({'sort': 'name:asc,description:desc'})],
    )
    with pytest.raises(NotFoundError) as not_found_error:
        tvm.agent_groups.details(1, sort=(('name', 'asc'), ('description', 'desc')))
    assert 'AgentGroup not found' in not_found_error.value.msg, (
        'Invalid value validation error for group_id parameter is not raised by test-case.'
    )


@responses.activate
def test_agentgroups_details_nonexistant_group(tvm):
    """
    test to raise the exception when group doesnt exist to get its details
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/1',
        json={'error': 'AgentGroup not found.'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.agent_groups.details(1)


@responses.activate
def test_agentgroups_details_standard_user_permissionserror(tvm, agentgroup):
    """
    test to raise the exception when standard user tries to get the details of agent group
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/106521',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_groups.details(agentgroup['id'])


@responses.activate
def test_agentgroups_details_of_an_agent_group(tvm, agentgroup):
    """
    test to get the details of agent group
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/106521',
        json={
            'id': 106521,
            'uuid': '54fcb935-c022-46a5-95b8-ed6daf8647b4',
            'name': '3a7c8527-fdac-4251-8c69-39549523dd49',
            'creation_date': 1544138347,
            'last_modification_date': 1544138347,
            'timestamp': 1544138347,
            'shared': 1,
            'owner': 'system',
            'owner_id': 1,
            'owner_name': 'system',
            'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
            'user_permissions': 128,
            'agents_count': 0,
            'agents': [],
            'pagination': {
                'total': 0,
                'limit': 50,
                'offset': 0,
                'sort': [{'name': 'name', 'order': 'asc'}],
            },
        },
    )
    group = tvm.agent_groups.details(agentgroup['id'])
    check(group, 'creation_date', int)
    check(group, 'id', int)
    check(group, 'last_modification_date', int)
    check(group, 'name', str)
    check(group, 'owner', str)
    check(group, 'owner_id', int)
    check(group, 'owner_name', str)
    check(group, 'owner_uuid', 'uuid')
    check(group, 'shared', int)
    check(group, 'timestamp', int)
    check(group, 'user_permissions', int)
    check(group, 'uuid', 'uuid')
    assert group['id'] == agentgroup['id']


def test_agentgroups_task_status_group_id_typerror(tvm):
    """
    test to raise the exception when type of group id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.task_status('no', 'nope')


def test_agentgroups_task_status_task_uuid_typeerror(tvm):
    """
    test to raise the exception when type of task_uuid is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_groups.task_status(1, 1)


def test_agentgroups_task_status_task_uuid_unexpectedvalueerror(tvm):
    """
    test to raise the exception when value of task_uuid is not as defined
    """
    with pytest.raises(UnexpectedValueError):
        tvm.agent_groups.task_status(1, 'nope')


@responses.activate
def test_agentgroups_task_status(tvm, agentgroup):
    """
    test to get the task status of the agent group
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents',
        json=SCANNERS_AGENTS,
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agent-groups/106521/agents/_bulk/add',
        json={
            'task_id': '2778ad9a-a926-4bb5-9835-97cd7a3d2366',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'status': 'NEW',
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/106521/agents/_bulk/2778ad9a-a926-4bb5-9835-97cd7a3d2366',
        json={
            'task_id': '2778ad9a-a926-4bb5-9835-97cd7a3d2366',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'status': 'COMPLETED',
            'message': '2 items completed, 0 failed.',
            'start_time': 1544138352084,
            'last_update_time': 1544138352094,
            'end_time': 1544138352094,
            'total_work_units': 2,
            'total_work_units_completed': 2,
            'completion_percentage': 100.0,
        },
    )
    agents = tvm.agents.list()
    resp = tvm.agent_groups.add_agent(
        agentgroup['id'], agents.next()['id'], agents.next()['id']
    )
    task = tvm.agent_groups.task_status(agentgroup['id'], resp['task_id'])
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'last_update_time', int)
    check(task, 'start_time', int)
    check(task, 'status', str)
    check(task, 'task_id', str)


@responses.activate
def test_agentgroups_list(tvm):
    """
    test to get the agent group list
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups',
        json={
            'groups': [
                {
                    'id': 102009,
                    'uuid': '03794d05-c7f8-4627-af3a-2c643f551253',
                    'name': 'test1',
                    'creation_date': 1532117989,
                    'last_modification_date': 1532117989,
                    'timestamp': 1532117989,
                    'shared': 1,
                    'owner': 'system',
                    'owner_id': 1,
                    'owner_name': 'system',
                    'owner_uuid': '34be6452-d41b-48fe-992b-cc33fe0c4870',
                    'user_permissions': 128,
                    'agents_count': 2,
                }
            ]
        },
    )
    agentgroups = tvm.agent_groups.list()
    assert isinstance(agentgroups, list)
    for agentgroup in agentgroups:
        # check(ag, 'agents', list)
        check(agentgroup, 'creation_date', int)
        check(agentgroup, 'id', int)
        check(agentgroup, 'last_modification_date', int)
        check(agentgroup, 'name', str)
        check(agentgroup, 'owner', str)
        check(agentgroup, 'owner_id', int)
        check(agentgroup, 'owner_name', str)
        check(agentgroup, 'owner_uuid', str)
        # check(agentgroup, 'pagination', dict)
        check(agentgroup, 'shared', int)
        check(agentgroup, 'user_permissions', int)
        check(agentgroup, 'uuid', str)


@responses.activate
def test_agentgroups_details_of_an_agent_group_fields(tvm, agentgroup):
    """
    test to get the details of agent groups
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agent-groups/106521',
        json={
            'id': 106521,
            'uuid': '54fcb935-c022-46a5-95b8-ed6daf8647b4',
            'name': '3a7c8527-fdac-4251-8c69-39549523dd49',
            'creation_date': 1623834983,
            'last_modification_date': 1623834983,
            'timestamp': 1623834983,
            'shared': 1,
            'owner': 'system',
            'owner_id': 1,
            'owner_name': 'system',
            'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
            'user_permissions': 128,
            'agents_count': 0,
            'agents': [],
            'pagination': {
                'total': 0,
                'limit': 45,
                'offset': 5,
                'sort': [{'name': 'name', 'order': 'asc'}],
            },
        },
        match=[
            matchers.query_param_matcher(
                {'ft': 'or', 'w': 'match', 'wf': 'name', 'offset': '5', 'limit': '45'}
            )
        ],
    )
    group = tvm.agent_groups.details(
        agentgroup['id'],
        filter_type='or',
        limit=45,
        offset=5,
        scanner_id=1,
        # sort=(('owner_id', 'asc'), ('shared', 'asc')),
        wildcard='match',
        wildcard_fields=['name'],
    )
    check(group, 'creation_date', int)
    check(group, 'id', int)
    check(group, 'last_modification_date', int)
    check(group, 'name', str)
    check(group, 'owner', str)
    check(group, 'owner_id', int)
    check(group, 'owner_name', str)
    check(group, 'owner_uuid', 'uuid')
    check(group, 'shared', int)
    check(group, 'timestamp', int)
    check(group, 'user_permissions', int)
    check(group, 'uuid', 'uuid')
    assert group['id'] == agentgroup['id']
