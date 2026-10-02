import json

import pytest
import responses

from tenable.ot.exports import queries
from tenable.ot.exports.iterator import OTExportsIterator

GRAPHQL_URL = 'https://localhost/graphql'
ASSET_PAGE = {
    'data': {
        'assets': {
            'pageInfo': {'endCursor': None},
            'count': 1,
            'nodes': [{'id': 'asset-1', 'name': 'PLC-1'}],
        }
    }
}


def _body(call):
    return json.loads(call.request.body)


@responses.activate
def test_exports_assets_return_json(fixture_ot):
    """
    return_json must post the query to the GraphQL endpoint and return the page.
    """
    rsp = responses.post(GRAPHQL_URL, json=ASSET_PAGE)
    resp = fixture_ot.exports.assets(return_json=True, limit=10)
    assert resp == ASSET_PAGE
    body = _body(rsp.calls[0])
    assert body['query'] == queries.ASSETS
    assert body['variables']['limit'] == 10


@responses.activate
def test_exports_assets_iterator(fixture_ot):
    responses.post(GRAPHQL_URL, json=ASSET_PAGE)
    assets = fixture_ot.exports.assets()
    assert isinstance(assets, OTExportsIterator)
    assert list(assets) == ASSET_PAGE['data']['assets']['nodes']


@pytest.mark.parametrize('filter_type', ['And', 'Or'])
@responses.activate
def test_exports_assets_filter_type(fixture_ot, filter_type):
    """
    Multiple filters must be combined with the requested operator.
    """
    rsp = responses.post(GRAPHQL_URL, json=ASSET_PAGE)
    filters = [
        {'op': 'Equal', 'field': 'type', 'values': 'PlcType'},
        {'op': 'Equal', 'field': 'vendor', 'values': 'Example'},
    ]
    fixture_ot.exports.assets(
        filters=filters, filter_type=filter_type, return_json=True
    )
    query_filter = _body(rsp.calls[0])['variables']['filter']
    assert query_filter['op'] == filter_type
    assert filters[0] in query_filter['expressions']
    assert filters[1] in query_filter['expressions']
