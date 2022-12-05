import pytest
import responses

from tenable.ot.graphql.definitions import GraphqlParsingError, GraphqlError


@responses.activate
def test_perform_request_errors(fixture_ot):
    """
    Tests the assets Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "error": {
                "errors": [
                    {
                        "message": "whoopsy",
                        "path": ["/graphql"],
                    }
                ]
            }
        },
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
