'''
test tags
'''
import uuid
import pytest
from tests.checker import check, single
from tenable.errors import UnexpectedValueError, NotFoundError
from tenable.io.tags import TagsIterator

@pytest.fixture
@pytest.mark.vcr()
def tagvalue(request, api):
    '''
    Fixture to create tag value
    '''
    tag = api.tags.create('Example', 'Test')
    def teardown():
        '''
        cleanup function to delete tag value
        '''
        try:
            api.tags.delete(tag['uuid'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return tag

@pytest.fixture
@pytest.mark.vcr()
def tagcat(request, api):
    '''
    Fixture to create tag category
    '''
    tag = api.tags.create_category('Example3')
    def teardown():
        '''
        cleanup function to delete tag category
        '''
        try:
            api.tags.delete_category(tag['uuid'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return tag

@pytest.mark.vcr()
def test_tags_create_category_typeerror(api):
    '''
    test to raise exception when type of category param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create(1, '')

@pytest.mark.vcr()
def test_tags_create_value_typerror(api):
    '''
    test to raise exception when type of value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', 1)

@pytest.mark.vcr()
def test_tags_create_value_description_typerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', description=1)

@pytest.mark.vcr()
def test_tags_create_value_category_description_typeerror(api):
    '''
    test to raise exception when type of category_description
    param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create('', '', category_description=1)

@pytest.mark.vcr()
def test_tags_create_success(api, tagvalue):
    '''
    test to create tag value.
    '''
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
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create_category(1)

@pytest.mark.vcr()
def test_tags_create_category_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.create_category('', description=1)

@pytest.mark.vcr()
def test_tags_create_category_success(api, tagcat):
    '''
    test to create tag category.
    '''
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
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.delete(1)

@pytest.mark.vcr()
def test_tags_delete_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.delete('1')

@pytest.mark.vcr()
def test_tags_delete_success(api, tagvalue):
    '''
    test to delete tag value.
    '''
    api.tags.delete(tagvalue['uuid'])

@pytest.mark.vcr()
def test_tags_delete_bulk_typeerror(api, tagvalue):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.delete(tagvalue['uuid'], 1)

@pytest.mark.vcr()
def test_tags_delete_bulk_unexpectedvalueerror(api, tagvalue):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.delete(tagvalue['uuid'], 'nope')

@pytest.mark.vcr()
def test_tags_delete_bulk_success(api):
    '''
    test to delete multiple tags .
    '''
    tag1 = api.tags.create('Example', 'Test1')
    tag2 = api.tags.create('Example', 'Test2')
    api.tags.delete(tag1['uuid'], tag2['uuid'])

@pytest.mark.vcr()
def test_tags_delete_category_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.delete_category(1)

@pytest.mark.vcr()
def test_tags_delete_category_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.delete_category('1')

@pytest.mark.vcr()
def test_tags_delete_category_success(api, tagcat):
    '''
    test to delete tag category.
    '''
    api.tags.delete_category(tagcat['uuid'])

@pytest.mark.vcr()
def test_tags_details_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.details(1)

@pytest.mark.vcr()
def test_tags_details_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.details('1')

@pytest.mark.vcr()
def test_tags_details_success(api, tagvalue):
    '''
    test to get details for a specific tag category/value pair.
    '''
    details = api.tags.details(tagvalue['uuid'])
    assert isinstance(details, dict)
    check(details, 'uuid', 'uuid')
    check(details, 'created_at', 'datetime')
    check(details, 'created_by', str)
    check(details, 'updated_at', 'datetime')
    check(details, 'updated_by', str)
    check(details, 'category_uuid', 'uuid')
    check(details, 'value', str)
    check(details, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(details, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_details_category_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.details_category(1)

@pytest.mark.vcr()
def test_tags_details_category_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.details_category('1')

@pytest.mark.vcr()
def test_tags_details_category_success(api, tagcat):
    '''
    test to get details for a specific tag category.
    '''
    details = api.tags.details_category(tagcat['uuid'])
    assert isinstance(details, dict)
    check(details, 'uuid', 'uuid')
    check(details, 'created_at', 'datetime')
    check(details, 'created_by', str)
    check(details, 'updated_at', 'datetime')
    check(details, 'updated_by', str)
    check(details, 'name', str)
    #check(t, 'description', str, allow_none=True)
    check(details, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_edit_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(1)

@pytest.mark.vcr()
def test_tags_edit_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_value_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.edit('1')

@pytest.mark.vcr()
def test_tags_edit_value_typeerror(api):
    '''
    test to raise exception when type of value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), value=1)

@pytest.mark.vcr()
def test_tags_edit_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit(uuid.uuid4(), description=1)

@pytest.mark.vcr()
def test_tags_edit_success(api, tagvalue):
    '''
    test to edit tag category/value pair information.
    '''
    resp = api.tags.edit(tagvalue['uuid'], value='Edited')
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'category_uuid', 'uuid')
    check(resp, 'value', str)
    check(resp, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(resp, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)
    assert resp['value'] == 'Edited'

@pytest.mark.vcr()
def test_tags_edit_category_uuid_typeerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit_category(1)

@pytest.mark.vcr()
def test_tags_edit_category_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when type of tag_category_uuid param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.edit_category('1')

@pytest.mark.vcr()
def test_tags_edit_category_value_typeerror(api):
    '''
    test to raise exception when type of value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), value=1)

@pytest.mark.vcr()
def test_tags_edit_category_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.edit_category(uuid.uuid4(), description=1)

@pytest.mark.vcr()
def test_tags_edit_category_success(api, tagcat):
    '''
    test to edit tag category information.
    '''
    resp = api.tags.edit_category(tagcat['uuid'], name='Edited')
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'name', str)
    #check(t, 'description', str, allow_none=True)
    check(resp, 'reserved', bool)
    assert resp['name'] == 'Edited'

def test_tags_list_constructor_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, True, None)

def test_tags_list_constructor_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, 'nadda', None)

def test_tags_list_constructor_filter_type_success(api):
    '''
    test to check filter_type param in tags_list_constructor method.
    '''
    resp = api.tags._tag_list_constructor([],
        api.tags._filterset_tags, 'and', None)
    assert resp['ft'] == 'AND'

def test_tags_list_constructor_sort_typeerror(api):
    '''
    test to raise exception when type of sort param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, None, 1)

def test_tags_list_constructor_sort_unexpectedvalueerror(api):
    '''
    test to raise exception when sort param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags._tag_list_constructor([],
            api.tags._filterset_tags, None, (('something_else'),))

def test_tags_list_constructor_sort_success(api):
    '''
    test to check sort param in tags_list_constructor method.
    '''
    resp = api.tags._tag_list_constructor([],
        api.tags._filterset_tags, None, (('value','asc'),))
    assert resp['sort'] == 'value:asc'

def test_tags_list_constructor_filter_success(api):
    '''
    test to check filter param in tags_list_constructor method.
    '''
    resp = api.tags._tag_list_constructor([
        ('value', 'eq', 'Test')
    ], api.tags._filterset_tags, None, None)
    assert resp['f'] == ['value:eq:Test']

@pytest.mark.vcr()
def test_tags_list_success(api, tagvalue):
    '''
    test to get list of tags.
    '''
    tags = api.tags.list()
    assert isinstance(tags, TagsIterator)
    resp = tags.next()
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'category_uuid', 'uuid')
    check(resp, 'value', str)
    check(resp, 'type', str)
    #check(t, 'description', str, allow_none=True)
    check(resp, 'category_name', str)
    #check(t, 'category_description', str, allow_none=True)

@pytest.mark.vcr()
def test_tags_list_category_success(api, tagcat):
    '''
    test to list of tag categories.
    '''
    tags = api.tags.list_categories()
    assert isinstance(tags, TagsIterator)
    resp = tags.next()
    check(resp, 'uuid', 'uuid')
    check(resp, 'created_at', 'datetime')
    check(resp, 'created_by', str)
    check(resp, 'updated_at', 'datetime')
    check(resp, 'updated_by', str)
    check(resp, 'name', str)
    #check(t, 'description', str, allow_none=True)
    #check(t, 'reserved', bool)

@pytest.mark.vcr()
def test_tags_list_date_failure(api):
    '''
    test to raise exception when value of filter tuple does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.list(('updated_at', 'eq', 'something_else'))

@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_list(api):
    '''
    test to raise exception when type of asset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign(1, [])

@pytest.mark.vcr()
def test_tags_assign_assets_typeerror_entity(api):
    '''
    test to raise exception when type of asset param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign([1,], [])

@pytest.mark.vcr()
def test_tags_assign_assets_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when asset param value does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.assign(['something'], [])

@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_list(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign([], 1)

@pytest.mark.vcr()
def test_tags_assign_tags_typeerror_entity(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.assign([], [1, ])

@pytest.mark.vcr()
def test_tags_assign_tags_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when tags param value does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.assign([], ['something', ])

@pytest.mark.vcr()
def test_tags_assign_success(api, tagvalue):
    '''
    test to assign tags to assets.
    '''
    assets = api.assets.list()
    resp = api.tags.assign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)

@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_list(api):
    '''
    test to raise exception when type of asstes param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign(1, [])

@pytest.mark.vcr()
def test_tags_unassign_assets_typeerror_entity(api):
    '''
    test to raise exception when type of assets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign([1,], [])

@pytest.mark.vcr()
def test_tags_unassign_assets_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when assets param value does not match the expected.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign(['something'], [])

@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_list(api):
    '''
    test to unassign tags from assets.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign([], 1)

@pytest.mark.vcr()
def test_tags_unassign_tags_typeerror_entity(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.tags.unassign([], [1, ])

@pytest.mark.vcr()
def test_tags_unassign_tags_unexpectedvalueerror_entity(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.tags.unassign([], ['something', ])

@pytest.mark.vcr()
def test_tags_unassign_success(api, tagvalue):
    '''
    test to raise exception when tags param value does not match the expected.
    '''
    assets = api.assets.list()
    resp = api.tags.unassign([a['id'] for a in assets], [tagvalue['uuid']])
    single(resp, str)
