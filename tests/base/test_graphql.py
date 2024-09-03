'''
Base graphql Testing module.
'''
import os
import sys
import platform
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile
import pytest
import responses
from responses.registries import OrderedRegistry
from graphql import DocumentNode, parse
from tenable.version import version
from tenable.base.graphql import GraphQLIterator, GraphQLEndpoint, GraphQLSession


@pytest.fixture
def gql_session():
    return GraphQLSession(url='https://nourl',
                          api_key='something',
                          schema_validation=False,
                          )

@pytest.fixture
def gql_test_query():
    return '{ query getHeros { heros { name } } }'


def test_session_init(gql_session):
    uname = platform.uname()
    py_version = '.'.join([str(i) for i in sys.version_info][0:3])
    opsys = uname[0]
    arch = uname[-2]
    assert isinstance(gql_session, GraphQLSession)
    assert ('Integration/1.0 (unknown; unknown; Build/unknown) '
            f'pyTenable/{version} (GQL-Requests; Python/{py_version}; {opsys}/{arch})'
            ) == gql_session._client.transport.headers['User-Agent']


def test_connectionerrors():
    with pytest.raises(ConnectionError):
        GraphQLSession(url='https://nourl')
    with pytest.raises(ConnectionError):
        GraphQLSession(api_key='something')


def test_construct_query_str(gql_session, gql_test_query):
    test_query = parse(gql_test_query)
    assert test_query == gql_session.construct_query(query=gql_test_query)


def test_construct_query_stringio(gql_session, gql_test_query):
    fobj = StringIO()
    fobj.write(gql_test_query)
    fobj.seek(0)
    test_query = parse(gql_test_query)
    assert test_query == gql_session.construct_query(query=fobj)


def test_construct_query_docnode(gql_session, gql_test_query):
    test_query = parse(gql_test_query)
    assert test_query == gql_session.construct_query(query=test_query)


def test_construct_query_stored_file(gql_session, gql_test_query):
    test_query = parse(gql_test_query)
    with NamedTemporaryFile() as tfile:
        tfile.write(gql_test_query.encode('utf-8'))
        tfile.seek(0)
        tpath = Path(tfile.name)
        fname = tpath.name
        fpath = tpath.absolute().parent
        gql_session._query_folder = Path(fpath)
        assert test_query == gql_session.construct_query(stored_file=fname)


def test_construct_query_typeerror(gql_session, gql_test_query):
    with pytest.raises(TypeError):
        gql_session.construct_query()


def test_query_iterator_return(gql_session, gql_test_query):
    assert isinstance(gql_session.query(gql_test_query,
                                        iterator=GraphQLIterator,
                                        graphql_model='hero'
                                        ),
                      GraphQLIterator
                      )


def test_query_iteragtor_typeerror(gql_session, gql_test_query):
    with pytest.raises(TypeError):
        gql_session.query(gql_test_query, iterator=GraphQLIterator)


@responses.activate
def test_query_response(gql_session, gql_test_query):
    data = {'heros': [{'name': 'something'}]}
    responses.post('https://nourl/', json={'data': data})
    assert gql_session.query(gql_test_query) == data


@pytest.mark.skip(reason='No schema to mock up')
def test_validation(gql_session):
    query = ''
    assert gql_session.validate(query) == {}


@responses.activate
def test_endpoint(gql_session, gql_test_query):
    endpoint = GraphQLEndpoint(gql_session)
    assert isinstance(endpoint, GraphQLEndpoint)

    data = {'heros': [{'name': 'something'}]}
    responses.post('https://nourl/', json={'data': data})
    assert endpoint._query(gql_test_query) == data


@responses.activate(registry=OrderedRegistry)
def test_iterator_pagination(gql_session, gql_test_query):
    item = {'name': 'something'}
    responses.post('https://nourl/', json={'data': {'heros': {
        'pageInfo': {'hasNextPage': True, 'endCursor': 'something'},
        'nodes': [item for _ in range(100)]
    }}})
    responses.post('https://nourl/', json={'data': {'heros': {
        'pageInfo': {'hasNextPage': True, 'endCursor': 'something'},
        'nodes': [item for _ in range(100)]
    }}})
    responses.post('https://nourl/', json={'data': {'heros': {
        'pageInfo': {'hasNextPage': False},
        'nodes': [item for _ in range(100)]
    }}})
    iter = gql_session.query(gql_test_query,
                             iterator=GraphQLIterator,
                             graphql_model='heros'
                             )
    for i in iter:
        assert i == item
    assert iter.count == 300


@responses.activate(registry=OrderedRegistry)
def test_iterator_total_term(gql_session, gql_test_query):
    item = {'name': 'something'}
    responses.post('https://nourl/', json={'data': {'heros': {
        'pageInfo': {'hasNextPage': True, 'endCursor': 'something'},
        'nodes': [item for _ in range(100)]
    }}})
    iter = gql_session.query(gql_test_query,
                             iterator=GraphQLIterator,
                             graphql_model='heros'
                             )
    iter.total = 4
    for i in iter:
        assert i == item
    assert iter.count == 4


@responses.activate(registry=OrderedRegistry)
def test_iterator_max_page_term(gql_session, gql_test_query):
    item = {'name': 'something'}
    responses.post('https://nourl/', json={'data': {'heros': {
        'pageInfo': {'hasNextPage': True, 'endCursor': 'something'},
        'nodes': [item for _ in range(100)]
    }}})
    iter = gql_session.query(gql_test_query,
                             iterator=GraphQLIterator,
                             graphql_model='heros'
                             )
    iter.total = 200
    iter.max_pages = 1
    for i in iter:
        assert i == item
    assert iter.count == 100


@responses.activate(registry=OrderedRegistry)
def test_iterator_empty_page(gql_session, gql_test_query):
    item = {'name': 'something'}
    responses.post('https://nourl/', json={'data': {'heros': {
        'pageInfo': {'hasNextPage': True, 'endCursor': 'something'},
        'nodes': []
    }}})
    iter = gql_session.query(gql_test_query,
                             iterator=GraphQLIterator,
                             graphql_model='heros'
                             )
    iter.total = 10
    for i in iter:
        assert i == item
    assert iter.count == 0
