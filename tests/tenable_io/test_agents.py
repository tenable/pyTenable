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
        api.agents.list(sort=(1, 'asc'))

def test_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.list(sort=('uuid', 1))

def test_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agents.list(sort=('uuid', 'nope'))

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

### 
### Need mock agents to test further
###

def test_get_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.get(scanner_id='nope')

def test_get_agent_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agents.get('nope')

### 
### Need mock agents to test further
###