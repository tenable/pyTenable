'''
test agents
'''
import pytest
from tenable.errors import UnexpectedValueError
from ..checker import check


@pytest.mark.vcr()
def test_agents_list_scanner_id_typeerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(scanner_id='nope')


@pytest.mark.vcr()
def test_agents_list_offset_typeerror(api):
    '''
    test to raise the exception when type of offset is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(offset='nope')


@pytest.mark.vcr()
def test_agents_list_limit_typeerror(api):
    '''
    test to raise the exception when type of limit is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(limit='nope')


@pytest.mark.vcr()
def test_agents_list_sort_field_typeerror(api):
    '''
    test to raise the exception when type of sort field is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(sort=((1, 'asc'),))


@pytest.mark.vcr()
def test_agents_list_sort_direction_typeerror(api):
    '''
    test to raise the exception when type of sort direction is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(sort=(('uuid', 1),))


@pytest.mark.vcr()
def test_agents_list_sort_direction_unexpectedvalue(api):
    '''
    test to raise the exception when value of sort direction is not as defined
    '''
    with pytest.raises(UnexpectedValueError):
        api.agents.list(sort=(('uuid', 'nope'),))


@pytest.mark.vcr()
def test_agents_list_filter_name_typeerror(api):
    '''
    test to raise the exception when type of filter name is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list((1, 'match', 'win'))


@pytest.mark.vcr()
def test_agents_list_filter_operator_typeerror(api):
    '''
    test to raise the exception when type of filter operator is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(('distro', 1, 'win'))


@pytest.mark.vcr()
def test_agents_list_filter_value_typeerror(api):
    '''
    test to raise the exception when type of filter value is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(('distro', 'match', 1))


@pytest.mark.vcr()
def test_agents_list_filter_type_typeerror(api):
    '''
    test to raise the exception when type of filter type is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(filter_type=1)


@pytest.mark.vcr()
def test_agents_list_wildcard_typeerror(api):
    '''
    test to raise the exception when type of wildcard is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(wildcard=1)


@pytest.mark.vcr()
def test_agents_list_wildcard_fields_typeerror(api):
    '''
    test to raise the exception when type of wildcard fields is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.list(wildcard_fields='nope')


@pytest.mark.vcr()
def test_agents_list(api):
    '''
    test to get the agents list
    '''
    count = 0
    agents = api.agents.list()
    for agent in agents:
        count += 1
        check(agent, 'distro', str)
        check(agent, 'id', int)
        check(agent, 'ip', str)
        check(agent, 'linked_on', int)
        check(agent, 'name', str)
        check(agent, 'platform', str)
        check(agent, 'status', str)
        check(agent, 'uuid', 'uuid')
    assert count == agents.total


@pytest.mark.vcr()
def test_agents_details_scanner_id_typeerror(api):
    '''
    test to raise the exception when type of scanner_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.details(scanner_id='nope')


@pytest.mark.vcr()
def test_agents_details_agent_id_typeerror(api):
    '''
    test to raise the exception when type of agent_id is not as defined
    '''
    with pytest.raises(TypeError):
        api.agents.details('nope')


@pytest.mark.vcr()
def test_agents_details_agent_details(api, agent):
    '''
    test to get the agent details
    '''
    resp = api.agents.details(agent['id'])
    check(resp, 'distro', str)
    check(resp, 'id', int)
    check(resp, 'ip', str)
    check(resp, 'linked_on', int)
    check(resp, 'name', str)
    check(resp, 'platform', str)
    check(resp, 'status', str)
    check(resp, 'uuid', 'uuid')
    assert resp['id'] == agent['id']


# Add tests for singular & bulk agent deletion.
# att tests for task_status.
@pytest.mark.vcr()
def test_agents_list_fields(api):
    '''
    test to get the agent list
    '''
    count = 0
    agents = api.agents.list(
        filter_type='or',
        limit=45,
        offset=5,
        wildcard='match',
        wildcard_fields=['name'])
    for agent in agents:
        count += 1
        check(agent, 'distro', str)
        check(agent, 'id', int)
        check(agent, 'ip', str)
        check(agent, 'linked_on', int)
        check(agent, 'name', str)
        check(agent, 'platform', str)
        check(agent, 'status', str)
        check(agent, 'uuid', 'uuid')
    assert count == agents.total
