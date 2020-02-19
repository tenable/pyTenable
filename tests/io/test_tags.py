from ..checker import check, single
from tenable.errors import *
from tenable.io.tags import TagsIterator
import uuid, pytest

@pytest.fixture
@pytest.mark.vcr()
def tagvalue(request, api):
    tag = api.tags.create('Example', 'Test')
    def teardown():
        try:
            api.tags.delete(tag['uuid'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return tag

@pytest.fixture
@pytest.mark.vcr()
def tagcat(request, api):
    tag = api.tags.create_category('Example3')
    def teardown():
        try:
            api.tags.delete_category(tag['uuid'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return tag

@pytest.mark.vcr()
def test_tags_create_category_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create(1, '')

@pytest.mark.vcr()
def test_tags_create_value_typerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', 1)

@pytest.mark.vcr()
def test_tags_create_description_typerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', description=1)

@pytest.mark.vcr()
def test_tags_create_category_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create('', '', category_description=1)

@pytest.mark.vcr()
def test_tags_create_success(api, tagvalue):
    assert isinstance(tagvalue, dict)
    check(tagvalue, 'uuid', 'uuid')
    check(tagvalue, 'created_at', 'datetime')
    check(tagvalue, 'updated_at', 'datetime')
    check(tagvalue, 'updated_by', str)
    check(tagvalue, 'category_uuid', 'uuid')
    check(tagvalue, 'value', str)
    #check(tagvalue, 'description', str, allow_none=True)
    #check(tagvalue, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_create_category_name_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create_category(1)

@pytest.mark.vcr()
def test_tags_create_category_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.create_category('', description=1)

@pytest.mark.vcr()
def test_tags_create_category_success(api, tagcat):
    assert isinstance(tagcat, dict)
    check(tagcat, 'uuid', 'uuid')
    check(tagcat, 'created_at', 'datetime')
    check(tagcat, 'updated_at', 'datetime')
    check(tagcat, 'updated_by', str)
    check(tagcat, 'name', str)
    #check(tagcat, 'description', str, allow_none=True)
    check(tagcat, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_delete_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.delete(1)

@pytest.mark.vcr()
def test_tags_delete_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.delete('1')

@pytest.mark.vcr()
def test_tags_delete_success(api, tagvalue):
    api.tags.delete(tagvalue['uuid'])

@pytest.mark.vcr()
def test_tags_delete_category_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.delete_category(1)

@pytest.mark.vcr()
def test_tags_delete_category_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.delete_category('1')

@pytest.mark.vcr()
def test_tags_delete_category_success(api, tagcat):
    api.tags.delete_category(tagcat['uuid'])

@pytest.mark.vcr()
def test_tags_details_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.details(1)

@pytest.mark.vcr()
def test_tags_details_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.details('1')

@pytest.mark.vcr()
def test_tags_details_success(api, tagvalue):
    t = api.tags.details(tagvalue['uuid'])
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'category_uuid', 'uuid')
    check(t, 'value', str)
    check(t, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_details_category_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.details_category(1)

@pytest.mark.vcr()
def test_tags_details_category_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.details_category('1')

@pytest.mark.vcr()
def test_tags_details_category_success(api, tagcat):
    t = api.tags.details_category(tagcat['uuid'])
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'name', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_edit_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit(1)

@pytest.mark.vcr()
def test_tags_edit_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.edit('1')

@pytest.mark.vcr()
def test_tags_edit_value_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), value=1)

@pytest.mark.vcr()
def test_tags_edit_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), description=1)

@pytest.mark.vcr()
def test_tags_edit_success(api, tagvalue):
    t = api.tags.edit(tagvalue['uuid'], value='Edited')
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'category_uuid', 'uuid')
    check(t, 'value', str)
    check(t, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)
    assert t['value'] == 'Edited'

@pytest.mark.vcr()
def test_tags_edit_category_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit_category(1)

@pytest.mark.vcr()
def test_tags_edit_category_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.edit_category('1')

@pytest.mark.vcr()
def test_tags_edit_category_value_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), value=1)

@pytest.mark.vcr()
def test_tags_edit_category_description_typeerror(api):
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), description=1)

@pytest.mark.vcr()
def test_tags_edit_category_success(api, tagcat):
    t = api.tags.edit_category(tagcat['uuid'], name='Edited')
    assert isinstance(t, dict)
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'name', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'reserved', bool)
    assert t['name'] == 'Edited'

def test_tags_list_constructor_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, True, None)

def test_tags_list_constructor_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, 'nadda', None)

def test_tags_list_constructor_filter_type_success(api):
    resp = api.tags._tag_list_constructor([],
        api.tags._filterset_tags, 'and', None)
    assert resp['ft'] == 'AND'

def test_tags_list_constructor_sort_typeerror(api):
    with pytest.raises(TypeError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, None, 1)

def test_tags_list_constructor_sort_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, None, 'something_else')

def test_tags_list_constructor_sort_success(api):
    resp = api.tags._tag_list_constructor([],
        api.tags._filterset_tags, None, 'value')
    assert resp['sort'] == 'value'

def test_tags_list_constructor_filter_success(api):
    resp = api.tags._tag_list_constructor([
        ('value', 'eq', 'Test')
    ], api.tags._filterset_tags, None, None)
    assert resp['f'] == ['value:eq:Test']

@pytest.mark.vcr()
def test_tags_list_success(api, tagvalue):
    tags = api.tags.list()
    assert isinstance(tags, TagsIterator)
    t = tags.next()
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'category_uuid', 'uuid')
    check(t, 'value', str)
    check(t, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(t, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_list_category_success(api, tagcat):
    tags = api.tags.list_categories()
    assert isinstance(tags, TagsIterator)
    t = tags.next()
    check(t, 'uuid', 'uuid')
    check(t, 'created_at', 'datetime')
    check(t, 'created_by', str)
    check(t, 'updated_at', 'datetime')
    check(t, 'updated_by', str)
    check(t, 'name', str)
    #check(t, 'description', str, allow_none=True)
    #check(t, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_list_date_failure(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.list(('updated_at', 'eq', 'something_else'))

@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.assign(1, [])

@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.assign([1,], [])

@pytest.mark.vcr()
def test_tags_assign_assets_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.assign(['something'], [])

@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.assign([], 1)

@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.assign([], [1, ])

@pytest.mark.vcr()
def test_tags_assign_tags_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.assign([], ['something', ])

@pytest.mark.vcr()
def test_tags_assign_success(api, tagvalue):
    assets = api.assets.list()
    resp = api.tags.assign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)

@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.unassign(1, [])

@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.unassign([1,], [])

@pytest.mark.vcr()
def test_tags_unassign_assets_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign(['something'], [])

@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_list(api):
    with pytest.raises(TypeError):
        api.tags.unassign([], 1)

@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_entity(api):
    with pytest.raises(TypeError):
        api.tags.unassign([], [1, ])

@pytest.mark.vcr()
def test_tags_unassign_tags_unexpectedvalueerror_entity(api):
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign([], ['something', ])

@pytest.mark.vcr()
def test_tags_unassign_success(api, tagvalue):
    assets = api.assets.list()
    resp = api.tags.unassign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)