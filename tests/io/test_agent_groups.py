from tenable.errors import *
from ..checker import check, single
import uuid, time, pytest

@pytest.fixture
@pytest.mark.vcr()
def agentgroup(request, api):
    group = api.agent_groups.create(str(uuid.uuid4()))
    def teardown():
        try:
            api.agent_groups.delete(group['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return group

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.add_agent('nope', 1)

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_agent_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.add_agent(1, 'nope')

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.add_agent(1, 1, scanner_id='nope')

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.agent_groups.add_agent(1, 1)

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.add_agent(1, 1)

@pytest.mark.vcr()
def test_agentgroups_add_agent_to_group(api, agentgroup, agent):
    api.agent_groups.add_agent(agentgroup['id'], agent['id'])

@pytest.mark.vcr()
def test_agentgroups_add_mult_agents_to_group(api, agentgroup):
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
    with pytest.raises(TypeError):
        api.agent_groups.configure('nope', 1)

@pytest.mark.vcr()
def test_agentgroups_configure_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.configure(1, 1)

@pytest.mark.vcr()
def test_agentgroups_configure_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.configure(1, 1, scanner_id='nope')

@pytest.mark.vcr()
def test_agentgroups_configure_standard_user_permissionerror(stdapi, agentgroup):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))

@pytest.mark.vcr()
def test_agentgroups_configure_change_name(api, agentgroup):
    api.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))

@pytest.mark.vcr()
def test_agentgroups_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.create(True)

@pytest.mark.vcr()
def test_agentgroups_create_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.create(str(uuid.uuid4()), 'nope')

@pytest.mark.vcr()
def test_agentgroups_create_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.create(str(uuid.uuid4()))

@pytest.mark.vcr()
def test_agentgroups_create_agent_group(api, agentgroup):
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
    with pytest.raises(TypeError):
        api.agent_groups.delete()

@pytest.mark.vcr()
def test_agentgroups_delete_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete('nope')

@pytest.mark.vcr()
def test_agentgroups_delete_scanner_id_typerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete(1, scanner_id='nope')

@pytest.mark.vcr()
def test_agentgroups_delete_agent_group(api, agentgroup):
    api.agent_groups.delete(agentgroup['id'])
    with pytest.raises(NotFoundError):
        api.agent_groups.details(agentgroup['id'])

@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent('nope', 1)

@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_agent_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent(1, 'nope')

@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent(1, 1, scanner_id='nope')

@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.agent_groups.delete_agent(1, 1)

@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.delete_agent(1, 1)

@pytest.mark.vcr()
def test_agentgroups_delete_agent_from_group(api, agent, agentgroup):
    api.agent_groups.add_agent(agentgroup['id'], agent['id'])
    api.agent_groups.delete_agent(agentgroup['id'], agent['id'])

@pytest.mark.vcr()
def test_agentgroups_delete_mult_agents_from_group(api, agentgroup):
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
    with pytest.raises(TypeError):
        api.agent_groups.details('nope')

@pytest.mark.vcr()
def test_agentgroups_details_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.details(1, scanner_id='nope')

@pytest.mark.vcr()
def test_agentgroups_details_nonexistant_group(api):
    with pytest.raises(NotFoundError):
        api.agent_groups.details(1)

@pytest.mark.vcr()
def test_agentgroups_details_standard_user_permissionserror(stdapi, agentgroup):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.details(agentgroup['id'])

@pytest.mark.vcr()
def test_agentgroups_details_of_an_agent_group(api, agentgroup):
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
    with pytest.raises(TypeError):
        api.agent_groups.task_status('no', 'nope')

@pytest.mark.vcr()
def test_agentgroups_task_status_task_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.task_status(1, 1)

@pytest.mark.vcr()
def test_agentgroups_task_status_task_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_groups.task_status(1, 'nope')

@pytest.mark.vcr()
def test_agentgroups_task_status(api, agentgroup):
    agents = api.agents.list()
    t1 = api.agent_groups.add_agent(agentgroup['id'], 
        agents.next()['id'],
        agents.next()['id']
    )
    task = api.agent_groups.task_status(agentgroup['id'], t1['task_id'])
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'last_update_time', int)
    check(task, 'start_time', int)
    check(task, 'status', str)
    check(task, 'task_id', str)

@pytest.mark.vcr()
def test_agentgroups_list(api):
    agentgroups = api.agent_groups.list()
    assert isinstance(agentgroups, list)
    for ag in agentgroups:
        # check(ag, 'agents', list)
        check(ag, 'creation_date', int)
        check(ag, 'id', int)
        check(ag, 'last_modification_date', int)
        check(ag, 'name', str)
        check(ag, 'owner', str)
        check(ag, 'owner_id', int)
        check(ag, 'owner_name', str)
        check(ag, 'owner_uuid', str)
        # check(ag, 'pagination', dict)
        check(ag, 'shared', int)
        check(ag, 'user_permissions', int)
        check(ag, 'uuid', str)
