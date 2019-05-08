from tenable.errors import *
from ..checker import check
import pytest, os

def test_queries_constructor_sort_field_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(sort_field=1, tool='1', type='1')

def test_queries_constructor_sort_direction_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(sort_direction=1, tool='1', type='1')

def test_queries_constructor_sort_direction_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.queries._constructor(sort_direction='nope', tool='1', type='1')

def test_queries_constructor_offset_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(offset='one', tool='1', type='1')

def test_queries_constructor_limit_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(limit='one', tool='1', type='1')

def test_queries_constructor_owner_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(owner_id='one', tool='1', type='1')

def test_queries_constructor_context_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(context=1, tool='1', type='1')

def test_queries_constructor_browse_cols_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(browse_cols=1, tool='1', type='1')

def test_queries_constructor_browse_sort_col_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(browse_sort_col=1, tool='1', type='1')

def test_queries_constructor_browse_sort_dir_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(browse_sort_direction=1, tool='1', type='1')

def test_queries_constructor_browse_sort_dir_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.queries._constructor(browse_sort_direction='nope', tool='1', type='1')

def test_queries_constructor_tags_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries._constructor(tags=1, tool='1', type='1')

def test_queries_constructor_success(sc):
    query = sc.queries._constructor(
        ('filtername', 'operator', 'value'),
        ('f2', 'op', 'val'),
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
        browse_sort_direction='asc'
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
            'filterName': 'f2',
            'operator': 'op',
            'value': 'val'
        }],
        'sortField': 'field1',
        'sortDir': 'ASC',
        'startOffset': 0,
        'endOffset': 1000,
        'ownerID': '1',
        'context': 'nothing',
        'browseColumns': 'something',
        'browseSortColumn': 'yes',
        'browseSortDirection': 'ASC'
    }

@pytest.fixture
def query(request, sc, vcr):
    with vcr.use_cassette('test_queries_create_success'):
        q = sc.queries.create('New Query', 'vulndetails', 'vuln',
            ('pluginID', '=', '19506'))
    def teardown():
        try:
            with vcr.use_cassette('test_queries_delete_success'):
                sc.queries.delete(int(q['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return q

@pytest.mark.vcr()
def test_queries_create_success(sc, query):
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
    for i in query['filters']:
        check(i, 'filterName', str)
        check(i, 'operator', str)
        check(i, 'value', str)
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
def test_queries_delete_success(sc, query):
    sc.queries.delete(int(query['id']))

@pytest.mark.vcr()
def test_queries_details_success(sc, query):
    q = sc.queries.details(int(query['id']))
    assert isinstance(q, dict)
    check(q, 'id', str)
    check(q, 'name', str)
    check(q, 'description', str)
    check(q, 'tool', str)
    check(q, 'type', str)
    check(q, 'tags', str)
    check(q, 'context', str)
    check(q, 'browseColumns', str)
    check(q, 'browseSortColumn', str)
    check(q, 'browseSortDirection', str)
    check(q, 'createdTime', str)
    check(q, 'modifiedTime', str)
    check(q, 'status', str)
    check(q, 'filters', list)
    for i in q['filters']:
        check(i, 'filterName', str)
        check(i, 'operator', str)
        check(i, 'value', str)
    check(q, 'canManage', str)
    check(q, 'canUse', str)
    check(q, 'creator', dict)
    check(q['creator'], 'id', str)
    check(q['creator'], 'username', str)
    check(q['creator'], 'firstname', str)
    check(q['creator'], 'lastname', str)
    check(q, 'owner', dict)
    check(q['owner'], 'id', str)
    check(q['owner'], 'username', str)
    check(q['owner'], 'firstname', str)
    check(q['owner'], 'lastname', str)
    check(q, 'ownerGroup', dict)
    check(q['ownerGroup'], 'id', str)
    check(q['ownerGroup'], 'name', str)
    check(q['ownerGroup'], 'description', str)
    check(q, 'targetGroup', dict)
    check(q['targetGroup'], 'id', int)
    check(q['targetGroup'], 'name', str)
    check(q['targetGroup'], 'description', str)

@pytest.mark.vcr()
def test_queries_edit_success(sc, query):
    q = sc.queries.edit(int(query['id']), name='Updated Name')
    assert isinstance(q, dict)
    check(q, 'id', str)
    check(q, 'name', str)
    check(q, 'description', str)
    check(q, 'tool', str)
    check(q, 'type', str)
    check(q, 'tags', str)
    check(q, 'context', str)
    check(q, 'browseColumns', str)
    check(q, 'browseSortColumn', str)
    check(q, 'browseSortDirection', str)
    check(q, 'createdTime', str)
    check(q, 'modifiedTime', str)
    check(q, 'filters', list)
    for i in q['filters']:
        check(i, 'filterName', str)
        check(i, 'operator', str)
        check(i, 'value', str)
    check(q, 'canManage', str)
    check(q, 'canUse', str)
    check(q, 'creator', dict)
    check(q['creator'], 'id', str)
    check(q['creator'], 'username', str)
    check(q['creator'], 'firstname', str)
    check(q['creator'], 'lastname', str)
    check(q, 'owner', dict)
    check(q['owner'], 'id', str)
    check(q['owner'], 'username', str)
    check(q['owner'], 'firstname', str)
    check(q['owner'], 'lastname', str)
    check(q, 'ownerGroup', dict)
    check(q['ownerGroup'], 'id', str)
    check(q['ownerGroup'], 'name', str)
    check(q['ownerGroup'], 'description', str)
    check(q, 'targetGroup', dict)
    check(q['targetGroup'], 'id', int)
    check(q['targetGroup'], 'name', str)
    check(q['targetGroup'], 'description', str)

@pytest.mark.vcr()
def test_queries_list_success(sc, query):
    queries = sc.queries.list()
    assert isinstance(queries, dict)
    for ltype in ['manageable', 'usable']:
        for q in queries[ltype]:
            assert isinstance(q, dict)
            check(q, 'id', str)
            check(q, 'name', str)
            check(q, 'description', str)

@pytest.mark.vcr()
def test_queries_tags_success(sc):
    tags = sc.queries.tags()
    assert isinstance(tags, list)
    for i in tags:
        assert isinstance(i, str)

@pytest.mark.vcr()
def test_queries_share_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries.share('one', 1)

@pytest.mark.vcr()
def test_queries_share_group_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.queries.share(1, 'one')

@pytest.mark.vcr()
def test_queries_share_success(sc, query, group):
    q = sc.queries.share(int(query['id']), int(group['id']))
    assert isinstance(q, dict)
    check(q, 'id', str)
    check(q, 'name', str)
    check(q, 'description', str)
    check(q, 'tool', str)
    check(q, 'type', str)
    check(q, 'tags', str)
    check(q, 'context', str)
    check(q, 'browseColumns', str)
    check(q, 'browseSortColumn', str)
    check(q, 'browseSortDirection', str)
    check(q, 'createdTime', str)
    check(q, 'modifiedTime', str)
    check(q, 'status', str)
    check(q, 'filters', list)
    for i in q['filters']:
        check(i, 'filterName', str)
        check(i, 'operator', str)
        check(i, 'value', str)
    check(q, 'creator', dict)
    check(q['creator'], 'id', str)
    check(q['creator'], 'username', str)
    check(q['creator'], 'firstname', str)
    check(q['creator'], 'lastname', str)
    check(q, 'owner', dict)
    check(q['owner'], 'id', str)
    check(q['owner'], 'username', str)
    check(q['owner'], 'firstname', str)
    check(q['owner'], 'lastname', str)
    check(q, 'ownerGroup', dict)
    check(q['ownerGroup'], 'id', str)
    check(q['ownerGroup'], 'name', str)
    check(q['ownerGroup'], 'description', str)
    check(q, 'targetGroup', dict)
    check(q['targetGroup'], 'id', int)
    check(q['targetGroup'], 'name', str)
    check(q['targetGroup'], 'description', str)