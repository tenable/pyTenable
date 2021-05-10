from tenable.errors import *
from ..checker import check, single
import pytest, uuid

@pytest.mark.vcr()
def test_access_groups_v2_list_offset_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(offset='nope')

@pytest.mark.vcr()
def test_access_groups_v2_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(limit='nope')

@pytest.mark.vcr()
def test_access_groups_v2_list_sort_field_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(sort=((1, 'asc'),))

@pytest.mark.vcr()
def test_access_groups_v2_list_sort_direction_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(sort=(('uuid', 1),))

@pytest.mark.vcr()
def test_access_groups_v2_list_sort_direction_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.access_groups_v2.list(sort=(('uuid', 'nope'),))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_name_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list((1, 'match', 'win'))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(('name', 1, 'win'))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(('name', 'match', 1))

@pytest.mark.vcr()
def test_access_groups_v2_list_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(filter_type=1)

@pytest.mark.vcr()
def test_access_groups_v2_list_wildcard_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(wildcard=1)

@pytest.mark.vcr()
def test_access_groups_v2_list_wildcard_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.access_groups_v2.list(wildcard_fields='nope')

@pytest.mark.vcr()
def test_access_groups_v2_list(api):
    count = 0
    access_groups = api.access_groups_v2.list()
    for i in access_groups:
        count += 1
        assert isinstance(i, dict)
        check(i, 'created_at', 'datetime')
        check(i, 'updated_at', 'datetime')
        check(i, 'id', 'uuid')
        check(i, 'name', str)
        check(i, 'all_assets', bool)
        check(i, 'version', int)
        check(i, 'status', str)
        check(i, 'access_group_type', str)
        #check(i, 'created_by_uuid', 'uuid') # Will not return for default group
        #check(i, 'updated_by_uuid', 'uuid') # Will not return for default group
        check(i, 'created_by_name', str)
        check(i, 'updated_by_name', str)
        check(i, 'processing_percent_complete', int)
    assert count == access_groups.total
