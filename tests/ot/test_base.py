"""
test base
"""
import responses

from tenable.ot.assets import AssetsAPI
from tenable.ot.graphql.definitions import (
    Extension,
    GraphqlError,
    GraphqlErrorSchema,
    Location,
)
from tenable.ot.schema.base import NodesList


def test_ot_interfaces(fixture_ot):
    """
    Testing that the right interfaces are returned.
    """
    assert isinstance(fixture_ot.assets, AssetsAPI)


@responses.activate
def test_graphql_direct_api(fixture_ot):
    """
    Test the graph api method.
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "asset": {
                    "id": "something",
                    "type": "EngType",
                    "name": "Eng. Station #40",
                    "criticality": "HighCriticality",
                    "location": None,
                }
            }
        },
    )
    resp = fixture_ot.graphql(
        variables={"asset": "something"},
        query="""
            query getAssetDetails($asset: ID!) {
                asset(id: $asset) {
                    id
                    type
                    name
                    criticality
                    location
                }
            }
        """,
    )
    assert resp["data"]["asset"]["id"] == "something"
    assert resp["data"]["asset"]["type"] == "EngType"
    assert resp["data"]["asset"]["name"] == "Eng. Station #40"
    assert resp["data"]["asset"]["criticality"] == "HighCriticality"
    assert resp["data"]["asset"]["location"] is None


def test_graphql_error_parsing():
    """
    Test GraphQL single error parsing.
    """
    raw_err = {
        "message": "Test error",
        "locations": [{"line": 4, "column": 7}],
        "path": ["asset"],
        "extensions": {"code": "GRAPHQL_VALIDATION_FAILED"},
    }

    expected_err = GraphqlError(
        message="Test error",
        locations=[Location(line=4, column=7)],
        path=["asset"],
        extensions=Extension(code="GRAPHQL_VALIDATION_FAILED"),
    )

    parsed_err = GraphqlErrorSchema().load(raw_err)
    assert parsed_err == expected_err
    print(expected_err)


def test_node_iterator():
    items = NodesList(
        nodes=[
            "a",
            "b",
            "c",
        ]
    )
    assert ["a", "b", "c"] == [item for item in items]
