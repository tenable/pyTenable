import pytest
import responses

from tenable.ot.graphql.definitions import GraphqlParsingError, GraphqlError


@pytest.mark.parametrize(
    "resp_json",
    [
        pytest.param(
            {
                "error": {
                    "errors": [
                        {
                            "message": 'Variable "$sort" of required type "[AssetSortParams!]!" was not provided.',  # noqa: E501
                            "locations": [{"line": 1, "column": 64}],
                            "extensions": {"code": "BAD_USER_INPUT"},
                        }
                    ]
                }
            },
            id="error_dict",
        ),
        pytest.param(
            {
                "errors": [
                    {
                        "message": "Syntax Error: Expected Name, found <EOF>.",
                        "locations": [{"line": 23, "column": 1}],
                        "extensions": {"code": "GRAPHQL_PARSE_FAILED"},
                    }
                ]
            },
            id="errors_list_single",
        ),
        pytest.param(
            {
                "errors": [
                    {
                        "message": "request to http://127.0.0.1:8083/v1/assets/osinfo failed, reason: connect EADDRNOTAVAIL 127.0.0.1:8083 - Local (127.0.0.1:0)",  # noqa: E501
                        "locations": [{"line": 46, "column": 7}],
                        "path": ["assets", "nodes", 0, "osDetails"],
                        "extensions": {
                            "code": "INTERNAL_SERVER_ERROR",
                            "exception": {
                                "message": "request to http://127.0.0.1:8083/v1/assets/osinfo failed, reason: connect EADDRNOTAVAIL 127.0.0.1:8083 - Local (127.0.0.1:0)",  # noqa: E501
                                "type": "system",
                                "errno": "EADDRNOTAVAIL",
                                "code": "EADDRNOTAVAIL",
                            },
                        },
                    },
                    {
                        "message": "request to http://127.0.0.1:8083/v1/assets/osinfo failed, reason: connect EADDRNOTAVAIL 127.0.0.1:8083 - Local (127.0.0.1:0)",  # noqa: E501
                        "locations": [{"line": 46, "column": 7}],
                        "path": ["assets", "nodes", 1, "osDetails"],
                        "extensions": {
                            "code": "INTERNAL_SERVER_ERROR",
                            "exception": {
                                "message": "request to http://127.0.0.1:8083/v1/assets/osinfo failed, reason: connect EADDRNOTAVAIL 127.0.0.1:8083 - Local (127.0.0.1:0)",  # noqa: E501
                                "type": "system",
                                "errno": "EADDRNOTAVAIL",
                                "code": "EADDRNOTAVAIL",
                            },
                        },
                    },
                ],
                "data": None,
            },
            id="errors_list_multiple_with_data_none",
        ),
    ],
)
@responses.activate
def test_perform_request_errors(fixture_ot, resp_json):
    """
    Tests the assets Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json=resp_json,
    )
    with pytest.raises(GraphqlError):
        resp = fixture_ot.assets.list().next()


@responses.activate
def test_perform_request_no_data(fixture_ot):
    """
    Tests the assets Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={},
    )
    with pytest.raises(GraphqlParsingError) as e:
        resp = fixture_ot.assets.list().next()
    print(e.value)


@responses.activate
def test_perform_request_none_data(fixture_ot):
    """
    Tests the assets Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "assets": None,
            }
        },
    )
    with pytest.raises(GraphqlParsingError) as e:
        resp = fixture_ot.assets.list().next()
    print(e.value)


@responses.activate
def test_get_page_pageinfo(fixture_ot):
    """
    Tests the assets Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjE5OQ=="},
        },
    )
    with pytest.raises(GraphqlParsingError) as e:
        resp = fixture_ot.assets.list().next()
    print(e.value)
