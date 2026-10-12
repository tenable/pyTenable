"""
test file for testing various scenarios in security center's
queries functionality
"""

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError
from ..checker import check


def test_queries_constructor_sort_field_typeerror(tsc):
    """
    test queries constructor for 'sort field' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(
            sort_field=1,
            tool='1',
            type='1',
            filters=[('filtername', 'operator', 'value')],
        )


def test_queries_constructor_description_typeerror(tsc):
    """
    test queries constructor for 'description' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(description=1, tool='1', type='1')


def test_queries_constructor_sort_direction_typeerror(tsc):
    """
    test queries constructor for 'sort description' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(sort_direction=1, tool='1', type='1')


def test_queries_constructor_sort_direction_unexpectedvalueerror(tsc):
    """
    test queries constructor for 'sort direction' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.queries._constructor(sort_direction='nope', tool='1', type='1')


def test_queries_constructor_offset_typeerror(tsc):
    """
    test queries constructor for 'offset' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(offset='one', tool='1', type='1')


def test_queries_constructor_limit_typeerror(tsc):
    """
    test queries constructor for 'limit' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(limit='one', tool='1', type='1')


def test_queries_constructor_owner_id_typeerror(tsc):
    """
    test queries constructor for 'owner id' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(owner_id='one', tool='1', type='1')


def test_queries_constructor_context_typeerror(tsc):
    """
    test queries constructor for 'context' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(context=1, tool='1', type='1')


def test_queries_constructor_browse_cols_typeerror(tsc):
    """
    test queries constructor for 'browse cols' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(browse_cols=1, tool='1', type='1')


def test_queries_constructor_browse_sort_col_typeerror(tsc):
    """
    test queries constructor for 'browse sort col' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(browse_sort_col=1, tool='1', type='1')


def test_queries_constructor_browse_sort_dir_typeerror(tsc):
    """
    test queries constructor for 'browse sort dir' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(browse_sort_direction=1, tool='1', type='1')


def test_queries_constructor_browse_sort_dir_unexpectedvalueerror(tsc):
    """
    test queries constructor for 'brose sort dir' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.queries._constructor(browse_sort_direction='nope', tool='1', type='1')


def test_queries_constructor_tags_typeerror(tsc):
    """
    test queries constructor for 'tags' type error
    """
    with pytest.raises(TypeError):
        tsc.queries._constructor(
            tags=1,
            tool='1',
            type='ticket',
            filters=[('filtername', 'operator', [1, 2])],
        )


@responses.activate
def test_queries_constructor_success(tsc):
    """
    test queries constructor for success
    """
    responses.get(
        'https://nourl/rest/query/1',
        json={
            'type': 'regular',
            'response': {},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1556816692,
        },
        match=[matchers.query_param_matcher({'fields': 'filters'})],
    )
    query = tsc.queries._constructor(
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
        query_id=1,
    )
    assert isinstance(query, dict)
    assert query == {
        'tool': 'vulndetails',
        'type': 'thistype',
        'tags': 'tag',
        'filters': [
            {'filterName': 'filtername', 'operator': 'operator', 'value': 'value'},
            {'filterName': 'asset', 'operator': 'op', 'value': {'id': '2'}},
        ],
        'sortField': 'field1',
        'sortDir': 'ASC',
        'startOffset': 0,
        'query_id': 1,
        'endOffset': 1000,
        'ownerID': '1',
        'context': 'nothing',
        'browseColumns': 'something',
        'browseSortColumn': 'yes',
        'browseSortDirection': 'ASC',
    }


@pytest.fixture
def query():
    """
    test fixture for query
    """
    return {
        'id': '740',
        'name': 'New Query',
        'description': '',
        'tool': 'vulndetails',
        'type': 'vuln',
        'tags': '',
        'context': '',
        'browseColumns': '',
        'browseSortColumn': '',
        'browseSortDirection': 'ASC',
        'createdTime': '1556816689',
        'modifiedTime': '1556816689',
        'status': '0',
        'filters': [],
        'groups': [],
        'canUse': 'true',
        'canManage': 'true',
        'creator': {
            'id': '2',
            'username': 'api',
            'firstname': 'api',
            'lastname': 'user',
        },
        'owner': {'id': '2', 'username': 'api', 'firstname': 'api', 'lastname': 'user'},
        'ownerGroup': {
            'id': '0',
            'name': 'Full Access',
            'description': 'Full Access group',
        },
        'targetGroup': {'id': -1, 'name': '', 'description': ''},
    }


@responses.activate
def test_queries_create_success(tsc):
    """
    test queries create for success
    """
    responses.post(
        'https://nourl/rest/query',
        json={
            'type': 'regular',
            'response': {
                'id': '740',
                'name': 'New Query',
                'description': '',
                'tool': 'vulndetails',
                'type': 'vuln',
                'tags': '',
                'context': '',
                'browseColumns': '',
                'browseSortColumn': '',
                'browseSortDirection': 'ASC',
                'createdTime': '1556816689',
                'modifiedTime': '1556816689',
                'status': '0',
                'filters': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1556816688,
        },
    )
    query = tsc.queries.create(
        'New Query', 'vulndetails', 'vuln', ('pluginID', '=', '19506')
    )
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


@responses.activate
def test_queries_delete_success(tsc, query):
    """
    test queries delete for success
    """
    responses.delete(
        'https://nourl/rest/query/740',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1556816689,
        },
    )
    tsc.queries.delete(int(query['id']))


@responses.activate
def test_queries_details_success(tsc, query):
    """
    test queries details for success
    """
    responses.get(
        'https://nourl/rest/query/740',
        json={
            'type': 'regular',
            'response': {
                'id': '742',
                'name': 'New Query',
                'description': '',
                'tool': 'vulndetails',
                'type': 'vuln',
                'tags': '',
                'context': '',
                'browseColumns': '',
                'browseSortColumn': '',
                'browseSortDirection': 'ASC',
                'createdTime': '1556816692',
                'modifiedTime': '1556816692',
                'status': '0',
                'filters': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1556816692,
        },
    )
    query = tsc.queries.details(int(query['id']))
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


@responses.activate
def test_queries_details_success_for_fields(tsc, query):
    """
    test queries details success for fields
    """
    responses.get(
        'https://nourl/rest/query/740',
        json={
            'type': 'regular',
            'response': {'id': '742', 'name': 'New Query', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1556816692,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    query_output = tsc.queries.details(
        int(query['id']), fields=['id', 'name', 'description']
    )
    assert isinstance(query_output, dict)
    check(query_output, 'id', str)
    check(query_output, 'name', str)
    check(query_output, 'description', str)


@responses.activate
def test_queries_edit_success(tsc, query):
    """
    test queries edit for success
    """
    responses.patch(
        'https://nourl/rest/query/740',
        json={
            'type': 'regular',
            'response': {
                'id': '746',
                'name': 'Updated Name',
                'description': '',
                'tool': 'vulndetails',
                'type': 'vuln',
                'tags': '',
                'context': '',
                'browseColumns': '',
                'browseSortColumn': '',
                'browseSortDirection': 'ASC',
                'createdTime': '1556819920',
                'modifiedTime': '1556819920',
                'status': 0,
                'filters': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1556819920,
        },
    )
    query = tsc.queries.edit(int(query['id']), name='Updated Name')
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


@responses.activate
def test_queries_list_success(tsc, query):
    """
    test queries list for success
    """
    responses.get(
        'https://nourl/rest/query',
        json={
            'type': 'regular',
            'response': {
                'usable': [],
                'manageable': [
                    {
                        'id': '744',
                        'name': 'New Query',
                        'description': '',
                        'tool': 'vulndetails',
                        'type': 'vuln',
                        'tags': '',
                        'context': '',
                        'browseColumns': '',
                        'browseSortColumn': '',
                        'browseSortDirection': 'ASC',
                        'createdTime': '1556816695',
                        'modifiedTime': '1556816695',
                        'status': '0',
                        'canUse': 'true',
                        'canManage': 'true',
                    }
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1556816696,
        },
    )
    queries = tsc.queries.list()
    assert isinstance(queries, dict)
    for ltype in ['manageable', 'usable']:
        for query in queries[ltype]:
            assert isinstance(query, dict)
            check(query, 'id', str)
            check(query, 'name', str)
            check(query, 'description', str)


@responses.activate
def test_queries_list_success_for_fields(tsc):
    """
    test queries list success for fields
    """
    responses.get(
        'https://nourl/rest/query',
        json={
            'type': 'regular',
            'response': {
                'usable': [{'id': '744', 'name': 'New Query', 'description': ''}],
                'manageable': [{'id': '744', 'name': 'New Query', 'description': ''}],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1556816696,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name'})],
    )
    queries = tsc.queries.list(fields=['id', 'name'])
    assert isinstance(queries, dict)
    for type in ['manageable', 'usable']:
        for query in queries[type]:
            assert isinstance(query, dict)
            check(query, 'id', str)
            check(query, 'name', str)


@responses.activate
def test_queries_tags_success(tsc):
    """
    test queries tags for success
    """
    responses.get(
        'https://nourl/rest/query/tag',
        json={
            'type': 'regular',
            'response': [],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1556816697,
        },
    )
    tags = tsc.queries.tags()
    assert isinstance(tags, list)
    for tag in tags:
        assert isinstance(tag, str)


def test_queries_share_id_typeerror(tsc):
    """
    test queries share for id type error
    """
    with pytest.raises(TypeError):
        tsc.queries.share('one', 1)


def test_queries_share_group_id_typeerror(tsc):
    """
    test queries share for 'group id' type error
    """
    with pytest.raises(TypeError):
        tsc.queries.share(1, 'one')


@responses.activate
def test_queries_share_success(tsc, query, group):
    """
    test queries share for success
    """
    responses.post(
        'https://nourl/rest/query/740/share',
        json={
            'type': 'regular',
            'response': {
                'id': '745',
                'name': 'New Query',
                'description': '',
                'tool': 'vulndetails',
                'type': 'vuln',
                'tags': '',
                'context': '',
                'browseColumns': '',
                'browseSortColumn': '',
                'browseSortDirection': 'ASC',
                'createdTime': '1556816698',
                'modifiedTime': '1556816698',
                'status': '0',
                'filters': [],
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'targetGroup': {'id': -1, 'name': '', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1556816698,
        },
    )
    query = tsc.queries.share(int(query['id']), int(group['id']))
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
