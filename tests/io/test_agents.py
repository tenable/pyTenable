from .fixtures import *
from tenable.errors import *

def test_list_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(scanner_id='nope')

def test_list_offset_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(offset='nope')

def test_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(limit='nope')

def test_list_sort_field_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(sort=((1, 'asc'),))

def test_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(sort=(('uuid', 1),))

def test_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agents.list(sort=(('uuid', 'nope'),))

def test_list_filter_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list((1, 'match', 'win'))

def test_list_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(('distro', 1, 'win'))

def test_list_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(('distro', 'match', 1))

def test_list_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(filter_type=1)

def test_list_wildcard_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(wildcard=1)

def test_list_wildcard_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(wildcard_fields='nope')

def test_list_standard_users_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agents.list()

def test_list(api):
    count = 0
    agents = api.agents.list()
    for i in agents:
        count += 1
        check(i, 'distro', str)
        check(i, 'id', int)
        check(i, 'ip', str)
        check(i, 'linked_on', int)
        check(i, 'name', str)
        check(i, 'platform', str)
        check(i, 'status', str)
        check(i, 'uuid', 'uuid')
    assert count == agents.total

def test_details_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.details(scanner_id='nope')

def test_details_agent_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.details('nope')

def test_details_agent_details(api, agent):
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