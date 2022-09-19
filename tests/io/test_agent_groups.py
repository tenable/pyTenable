'''
test agent groups
'''
import time
import uuid

import pytest

from tenable.errors import NotFoundError, UnexpectedValueError, ForbiddenError
from tests.pytenable_log_handler import log_exception
from ..checker import check


@pytest.fixture
@pytest.mark.vcr()
def agentgroup(request, api):
    '''
    agent group fixture
    '''
    group = api.agent_groups.create(str(uuid.uuid4()))

    def teardown():
        try:
            api.agent_groups.delete(group['id'])
        except NotFoundError as err:
            log_exception(err)
            pass

    request.addfinalizer(teardown)
    return group


@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_group_id_typeerror(api):
    '''
    test to raise the exception when type of group_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.add_agent('nope', 1)


@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_agent_id_typeerror(api):
    '''
    test to raise the exception when type of agent_id is not as defined
    '''
    with pytest.raises(UnexpectedValueError):
        api.agent_groups.add_agent(1, 'nope')

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_mixed_ids_typeerror(api):
    '''
    test to raise the exception when type of multiple passed ids don't match each other
    '''
    with pytest.raises(TypeError):
        api.agent_groups.add_agent(1, '64e1cc37-4d6a-4a36-a2d3-aca300735829', 2)


@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_scanner_id_typeerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.add_agent(1, 1, scanner_id='nope')


@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_notfounderror(api):
    '''
    test to add agent to group and agent not found
    '''
    with pytest.raises(NotFoundError):
        api.agent_groups.add_agent(1, 1)


@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_standard_user_permissionerror(stdapi):
    '''
    test to raise the exception when standard user adds agent to group
    '''
    with pytest.raises(ForbiddenError):
        stdapi.agent_groups.add_agent(1, 1)


@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group(api, agentgroup, agent):
    '''
    test to add single agent to the group
    '''
    api.agent_groups.add_agent(agentgroup['id'], agent['id'])


@pytest.mark.vcr()
def test_agentgroups_add_mult_agents_to_group(api, agentgroup):
    '''
    test to add multiple agents to group
    '''
    agents = api.agents.list()
    task = api.agent_groups.add_agent(agentgroup['id'],
                                      agents.next()['id'],
                                      agents.next()['id']
                                      )
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'status', str)
    check(task, 'task_id', str)


@pytest.mark.vcr()
def test_agentgroups_configure_group_id_typeerror(api):
    '''
    test to raise the exception when type of group_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.configure('nope', 1)


@pytest.mark.vcr()
def test_agentgroups_configure_name_typeerror(api):
    '''
    test to raise the exception when type of name is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.configure(1, 1)


# @pytest.mark.vcr()
# def test_agentgroups_configure_scanner_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.agent_groups.configure(1, 1, scanner_id='nope')

@pytest.mark.vcr()
def test_agentgroups_configure_standard_user_permissionerror(stdapi, agentgroup):
    '''
    test to raise the exception when standard user tries to configure

    '''
    with pytest.raises(ForbiddenError):
        stdapi.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))


@pytest.mark.vcr()
def test_agentgroups_configure_change_name(api, agentgroup):
    '''
    test to configure name
    '''
    api.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))


@pytest.mark.vcr()
def test_agentgroups_create_name_typeerror(api):
    '''
    test to raise the exception when type of name is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.create(True)


@pytest.mark.vcr()
def test_agentgroups_create_scanner_id_typeerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.create(str(uuid.uuid4()), 'nope')


@pytest.mark.vcr()
def test_agentgroups_create_standard_user_permissionerror(stdapi):
    '''
    test to raise the exception for standard user for creating agent group
    '''
    with pytest.raises(ForbiddenError):
        stdapi.agent_groups.create(str(uuid.uuid4()))


@pytest.mark.vcr()
def test_agentgroups_create_agent_group(agentgroup):
    '''
    test to create agent group
    '''
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


@pytest.mark.vcr()
def test_agentgroups_delete_attributeerror(api):
    '''
    test to raise the exception when no arguments are passed
    '''
    with pytest.raises(TypeError):
        api.agent_groups.delete()


@pytest.mark.vcr()
def test_agentgroups_delete_group_id_typeerror(api):
    '''
    test to raise the exception when type of group_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.delete('nope')


@pytest.mark.vcr()
def test_agentgroups_delete_scanner_id_typerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.delete(1, scanner_id='nope')


@pytest.mark.vcr()
def test_agentgroups_delete_agent_group(api, agentgroup):
    '''
    test to delete the agent group
    '''
    api.agent_groups.delete(agentgroup['id'])
    with pytest.raises(NotFoundError):
        api.agent_groups.details(agentgroup['id'])


@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_group_id_typeerror(api):
    '''
    test to raise the exception when type of group_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent('nope', 1)


@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_agent_id_typeerror(api):
    '''
    test to raise the exception when type of agent_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent(1, 'nope')


@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_scanner_id_typeerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent(1, 1, scanner_id='nope')


@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_notfounderror(api):
    '''
    test to delete agent from the group and agent is not found to delete
    '''
    with pytest.raises(NotFoundError):
        api.agent_groups.delete_agent(1, 1)


@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_standard_user_permissionerror(stdapi):
    '''
    test to raise the exception when standard user tris to delete the agent from the group
    '''
    with pytest.raises(ForbiddenError):
        stdapi.agent_groups.delete_agent(1, 1)


@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group(api, agent, agentgroup):
    '''
    test to delete single agent from the group

    '''
    api.agent_groups.add_agent(agentgroup['id'], agent['id'])
    api.agent_groups.delete_agent(agentgroup['id'], agent['id'])


@pytest.mark.vcr()
def test_agentgroups_delete_mult_agents_from_group(api, agentgroup):
    '''
    test to delete the multiple agents from the group
    '''
    agents = api.agents.list()
    alist = [agents.next()['id'], agents.next()['id']]
    api.agent_groups.add_agent(agentgroup['id'], *alist)
    time.sleep(1)
    task = api.agent_groups.delete_agent(agentgroup['id'], *alist)
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'status', str)
    check(task, 'task_id', str)


@pytest.mark.vcr()
def test_agentgroups_details_group_id_typeerror(api):
    '''
    test to raise the exception when type of task_uuid is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.details('nope')


@pytest.mark.vcr()
def test_agentgroups_details_scanner_id_typeerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError) as type_error:
        api.agent_groups.details(1, scanner_id='nope')
    assert type_error.value.args[0] == "scanner_id is of type str.  Expected int", \
        "Invalid type validation error for scanner_id parameter is not raised by test-case."


@pytest.mark.vcr()
def test_agentgroups_details_agentgroup_notfounderror(api):
    '''
    test to raise the exception when agentgroup not found
    '''
    with pytest.raises(NotFoundError) as not_found_error:
        api.agent_groups.details(1, sort=(('name', 'asc'), ('description', 'desc')))
    assert "AgentGroup not found" in not_found_error.value.msg, \
        "Invalid value validation error for group_id parameter is not raised by test-case."


@pytest.mark.vcr()
def test_agentgroups_details_nonexistant_group(api):
    '''
    test to raise the exception when group doesnt exist to get its details
    '''
    with pytest.raises(NotFoundError):
        api.agent_groups.details(1)


@pytest.mark.vcr()
def test_agentgroups_details_standard_user_permissionserror(stdapi, agentgroup):
    '''
    test to raise the exception when standard user tries to get the details of agent group
    '''
    with pytest.raises(ForbiddenError):
        stdapi.agent_groups.details(agentgroup['id'])


@pytest.mark.vcr()
def test_agentgroups_details_of_an_agent_group(api, agentgroup):
    '''
    test to get the details of agent group
    '''
    group = api.agent_groups.details(agentgroup['id'])
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


@pytest.mark.vcr()
def test_agentgroups_task_status_group_id_typerror(api):
    '''
    test to raise the exception when type of group id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.task_status('no', 'nope')


@pytest.mark.vcr()
def test_agentgroups_task_status_task_uuid_typeerror(api):
    '''
    test to raise the exception when type of task_uuid is not as defined
    '''
    with pytest.raises(TypeError):
        api.agent_groups.task_status(1, 1)


@pytest.mark.vcr()
def test_agentgroups_task_status_task_uuid_unexpectedvalueerror(api):
    '''
    test to raise the exception when value of task_uuid is not as defined
    '''
    with pytest.raises(UnexpectedValueError):
        api.agent_groups.task_status(1, 'nope')


@pytest.mark.vcr()
def test_agentgroups_task_status(api, agentgroup):
    '''
    test to get the task status of the agent group
    '''
    agents = api.agents.list()
    resp = api.agent_groups.add_agent(agentgroup['id'],
                                      agents.next()['id'],
                                      agents.next()['id']
                                      )
    task = api.agent_groups.task_status(agentgroup['id'], resp['task_id'])
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'last_update_time', int)
    check(task, 'start_time', int)
    check(task, 'status', str)
    check(task, 'task_id', str)


@pytest.mark.vcr()
def test_agentgroups_list(api):
    '''
    test to get the agent group list
    '''
    agentgroups = api.agent_groups.list()
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


@pytest.mark.vcr()
def test_agentgroups_details_of_an_agent_group_fields(api, agentgroup):
    '''
    test to get the details of agent groups
    '''
    group = api.agent_groups.details(agentgroup['id'],
                                     filter_type='or',
                                     limit=45,
                                     offset=5,
                                     scanner_id=1,
                                     # sort=(('owner_id', 'asc'), ('shared', 'asc')),
                                     wildcard='match',
                                     wildcard_fields=['name']
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
