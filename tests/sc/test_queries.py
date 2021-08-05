'''
test file for testing various scenarios in security center's
queries functionality
'''
import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check


def test_queries_constructor_sort_field_typeerror(security_center):
    '''
    test queries constructor for 'sort field' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(sort_field=1, tool='1', type='1',
                                             filters=[('filtername', 'operator', 'value')])


def test_queries_constructor_description_typeerror(security_center):
    '''
    test queries constructor for 'description' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(description=1, tool='1', type='1')


def test_queries_constructor_sort_direction_typeerror(security_center):
    '''
    test queries constructor for 'sort description' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(sort_direction=1, tool='1', type='1')


def test_queries_constructor_sort_direction_unexpectedvalueerror(security_center):
    '''
    test queries constructor for 'sort direction' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.queries._constructor(sort_direction='nope', tool='1', type='1')


def test_queries_constructor_offset_typeerror(security_center):
    '''
    test queries constructor for 'offset' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(offset='one', tool='1', type='1')


def test_queries_constructor_limit_typeerror(security_center):
    '''
    test queries constructor for 'limit' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(limit='one', tool='1', type='1')


def test_queries_constructor_owner_id_typeerror(security_center):
    '''
    test queries constructor for 'owner id' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(owner_id='one', tool='1', type='1')


def test_queries_constructor_context_typeerror(security_center):
    '''
    test queries constructor for 'context' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(context=1, tool='1', type='1')


def test_queries_constructor_browse_cols_typeerror(security_center):
    '''
    test queries constructor for 'browse cols' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(browse_cols=1, tool='1', type='1')


def test_queries_constructor_browse_sort_col_typeerror(security_center):
    '''
    test queries constructor for 'browse sort col' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(browse_sort_col=1, tool='1', type='1')


def test_queries_constructor_browse_sort_dir_typeerror(security_center):
    '''
    test queries constructor for 'browse sort dir' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(browse_sort_direction=1, tool='1', type='1')


def test_queries_constructor_browse_sort_dir_unexpectedvalueerror(security_center):
    '''
    test queries constructor for 'brose sort dir' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.queries._constructor(browse_sort_direction='nope', tool='1', type='1')


def test_queries_constructor_tags_typeerror(security_center):
    '''
    test queries constructor for 'tags' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries._constructor(tags=1, tool='1', type='ticket',
                                             filters=[('filtername', 'operator', [1, 2])])


@pytest.mark.vcr()
def test_queries_constructor_success(security_center):
    '''
    test queries constructor for success
    '''
    query = security_center.queries._constructor(
        ('filtername', 'operator', 'value'),
        ('asset', 'op', 2),
        tool='vulndetails',
        type='thistype',
        tags='tag',
        sort_field='field1',
        sort_direction='asc',
        offset=0,
        limit=1000,
        owner_id=1,
        context='nothing',
        browse_cols=['something'],
        browse_sort_col='yes',
        browse_sort_direction='asc',
        query_id=1
    )
    assert isinstance(query, dict)
    assert query == {
        'tool': 'vulndetails',
        'type': 'thistype',
        'tags': 'tag',
        'filters': [{
            'filterName': 'filtername',
            'operator': 'operator',
            'value': 'value'
        }, {
            'filterName': 'asset',
            'operator': 'op',
            'value': {'id': '2'}
        }],
        'sortField': 'field1',
        'sortDir': 'ASC',
        'startOffset': 0,
        'query_id': 1,
        'endOffset': 1000,
        'ownerID': '1',
        'context': 'nothing',
        'browseColumns': 'something',
        'browseSortColumn': 'yes',
        'browseSortDirection': 'ASC'
    }


@pytest.fixture
def query(request, security_center, vcr):
    '''
    test fixture for query
    '''
    with vcr.use_cassette('test_queries_create_success'):
        query = security_center.queries.create('New Query', 'vulndetails', 'vuln',
                                               ('pluginID', '=', '19506'))

    def teardown():
        try:
            with vcr.use_cassette('test_queries_delete_success'):
                security_center.queries.delete(int(query['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return query


@pytest.mark.vcr()
def test_queries_create_success(query):
    '''
    test queries create for success
    '''
    assert isinstance(query, dict)
    check(query, 'id', str)
    check(query, 'name', str)
    check(query, 'description', str)
    check(query, 'tool', str)
    check(query, 'type', str)
    check(query, 'tags', str)
    check(query, 'context', str)
    check(query, 'browseColumns', str)
    check(query, 'browseSortColumn', str)
    check(query, 'browseSortDirection', str)
    check(query, 'createdTime', str)
    check(query, 'modifiedTime', str)
    check(query, 'status', str)
    check(query, 'filters', list)
    for filter in query['filters']:
        check(filter, 'filterName', str)
        check(filter, 'operator', str)
        check(filter, 'value', str)
    check(query, 'canManage', str)
    check(query, 'canUse', str)
    check(query, 'creator', dict)
    check(query['creator'], 'id', str)
    check(query['creator'], 'username', str)
    check(query['creator'], 'firstname', str)
    check(query['creator'], 'lastname', str)
    check(query, 'owner', dict)
    check(query['owner'], 'id', str)
    check(query['owner'], 'username', str)
    check(query['owner'], 'firstname', str)
    check(query['owner'], 'lastname', str)
    check(query, 'ownerGroup', dict)
    check(query['ownerGroup'], 'id', str)
    check(query['ownerGroup'], 'name', str)
    check(query['ownerGroup'], 'description', str)
    check(query, 'targetGroup', dict)
    check(query['targetGroup'], 'id', int)
    check(query['targetGroup'], 'name', str)
    check(query['targetGroup'], 'description', str)


@pytest.mark.vcr()
def test_queries_delete_success(security_center, query):
    '''
    test queries delete for success
    '''
    security_center.queries.delete(int(query['id']))


@pytest.mark.vcr()
def test_queries_details_success(security_center, query):
    '''
    test queries details for success
    '''
    query = security_center.queries.details(int(query['id']))
    assert isinstance(query, dict)
    check(query, 'id', str)
    check(query, 'name', str)
    check(query, 'description', str)
    check(query, 'tool', str)
    check(query, 'type', str)
    check(query, 'tags', str)
    check(query, 'context', str)
    check(query, 'browseColumns', str)
    check(query, 'browseSortColumn', str)
    check(query, 'browseSortDirection', str)
    check(query, 'createdTime', str)
    check(query, 'modifiedTime', str)
    check(query, 'status', str)
    check(query, 'filters', list)
    for filter in query['filters']:
        check(filter, 'filterName', str)
        check(filter, 'operator', str)
        check(filter, 'value', str)
    check(query, 'canManage', str)
    check(query, 'canUse', str)
    check(query, 'creator', dict)
    check(query['creator'], 'id', str)
    check(query['creator'], 'username', str)
    check(query['creator'], 'firstname', str)
    check(query['creator'], 'lastname', str)
    check(query, 'owner', dict)
    check(query['owner'], 'id', str)
    check(query['owner'], 'username', str)
    check(query['owner'], 'firstname', str)
    check(query['owner'], 'lastname', str)
    check(query, 'ownerGroup', dict)
    check(query['ownerGroup'], 'id', str)
    check(query['ownerGroup'], 'name', str)
    check(query['ownerGroup'], 'description', str)
    check(query, 'targetGroup', dict)
    check(query['targetGroup'], 'id', int)
    check(query['targetGroup'], 'name', str)
    check(query['targetGroup'], 'description', str)


@pytest.mark.vcr()
def test_queries_details_success_for_fields(security_center, query):
    '''
    test queries details success for fields
    '''
    query_output = security_center.queries.details(int(query['id']), fields=["id", "name", "description"])
    assert isinstance(query_output, dict)
    check(query_output, 'id', str)
    check(query_output, 'name', str)
    check(query_output, 'description', str)


@pytest.mark.vcr()
def test_queries_edit_success(security_center, query):
    '''
    test queries edit for success
    '''
    query = security_center.queries.edit(int(query['id']), name='Updated Name')
    assert isinstance(query, dict)
    check(query, 'id', str)
    check(query, 'name', str)
    check(query, 'description', str)
    check(query, 'tool', str)
    check(query, 'type', str)
    check(query, 'tags', str)
    check(query, 'context', str)
    check(query, 'browseColumns', str)
    check(query, 'browseSortColumn', str)
    check(query, 'browseSortDirection', str)
    check(query, 'createdTime', str)
    check(query, 'modifiedTime', str)
    check(query, 'filters', list)
    for filter in query['filters']:
        check(filter, 'filterName', str)
        check(filter, 'operator', str)
        check(filter, 'value', str)
    check(query, 'canManage', str)
    check(query, 'canUse', str)
    check(query, 'creator', dict)
    check(query['creator'], 'id', str)
    check(query['creator'], 'username', str)
    check(query['creator'], 'firstname', str)
    check(query['creator'], 'lastname', str)
    check(query, 'owner', dict)
    check(query['owner'], 'id', str)
    check(query['owner'], 'username', str)
    check(query['owner'], 'firstname', str)
    check(query['owner'], 'lastname', str)
    check(query, 'ownerGroup', dict)
    check(query['ownerGroup'], 'id', str)
    check(query['ownerGroup'], 'name', str)
    check(query['ownerGroup'], 'description', str)
    check(query, 'targetGroup', dict)
    check(query['targetGroup'], 'id', int)
    check(query['targetGroup'], 'name', str)
    check(query['targetGroup'], 'description', str)


@pytest.mark.vcr()
def test_queries_list_success(security_center, query):
    '''
    test queries list for success
    '''
    queries = security_center.queries.list()
    assert isinstance(queries, dict)
    for ltype in ['manageable', 'usable']:
        for query in queries[ltype]:
            assert isinstance(query, dict)
            check(query, 'id', str)
            check(query, 'name', str)
            check(query, 'description', str)


@pytest.mark.vcr()
def test_queries_list_success_for_fields(security_center):
    '''
    test queries list success for fields
    '''
    queries = security_center.queries.list(fields=["id", "name"])
    assert isinstance(queries, dict)
    for type in ['manageable', 'usable']:
        for query in queries[type]:
            assert isinstance(query, dict)
            check(query, 'id', str)
            check(query, 'name', str)


@pytest.mark.vcr()
def test_queries_tags_success(security_center):
    '''
    test queries tags for success
    '''
    tags = security_center.queries.tags()
    assert isinstance(tags, list)
    for tag in tags:
        assert isinstance(tag, str)


@pytest.mark.vcr()
def test_queries_share_id_typeerror(security_center):
    '''
    test queries share for id type error
    '''
    with pytest.raises(TypeError):
        security_center.queries.share('one', 1)


@pytest.mark.vcr()
def test_queries_share_group_id_typeerror(security_center):
    '''
    test queries share for 'group id' type error
    '''
    with pytest.raises(TypeError):
        security_center.queries.share(1, 'one')


@pytest.mark.vcr()
def test_queries_share_success(security_center, query, group):
    '''
    test queries share for success
    '''
    query = security_center.queries.share(int(query['id']), int(group['id']))
    assert isinstance(query, dict)
    check(query, 'id', str)
    check(query, 'name', str)
    check(query, 'description', str)
    check(query, 'tool', str)
    check(query, 'type', str)
    check(query, 'tags', str)
    check(query, 'context', str)
    check(query, 'browseColumns', str)
    check(query, 'browseSortColumn', str)
    check(query, 'browseSortDirection', str)
    check(query, 'createdTime', str)
    check(query, 'modifiedTime', str)
    check(query, 'status', str)
    check(query, 'filters', list)
    for filter in query['filters']:
        check(filter, 'filterName', str)
        check(filter, 'operator', str)
        check(filter, 'value', str)
    check(query, 'creator', dict)
    check(query['creator'], 'id', str)
    check(query['creator'], 'username', str)
    check(query['creator'], 'firstname', str)
    check(query['creator'], 'lastname', str)
    check(query, 'owner', dict)
    check(query['owner'], 'id', str)
    check(query['owner'], 'username', str)
    check(query['owner'], 'firstname', str)
    check(query['owner'], 'lastname', str)
    check(query, 'ownerGroup', dict)
    check(query['ownerGroup'], 'id', str)
    check(query['ownerGroup'], 'name', str)
    check(query['ownerGroup'], 'description', str)
    check(query, 'targetGroup', dict)
    check(query['targetGroup'], 'id', int)
    check(query['targetGroup'], 'name', str)
    check(query['targetGroup'], 'description', str)
