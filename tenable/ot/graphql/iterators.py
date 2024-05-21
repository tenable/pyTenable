"""
GraphQL Tenable OT Security API iterator.
"""
import json
import typing
from typing import Type

from marshmallow.utils import EXCLUDE
from restfly.iterator import APIIterator

from tenable.ot.graphql.definitions import (
    GraphqlErrorSchema,
    GraphqlParsingError,
    GraphObject,
    NodesSchema,
)

if typing.TYPE_CHECKING:
    from tenable.ot.session import TenableOT


class OTGraphIterator(APIIterator):
    """
    Iterator class over Tenable OT Security GraphQL connections.
    """

    def __init__(
        self,
        api: "Type[TenableOT]",
        graph_object: GraphObject,
        **kwargs,
    ):
        self._graph_object = graph_object
        self.api = api
        super().__init__(
            api=api,
            **kwargs,
        )

    def _get_page(self) -> Type[NodesSchema]:
        """
        Retrieves the next page of data.
        """
        graph_full_object = {
            "query": self._graph_object.query,
            "variables": json.dumps(self._graph_object.query_variables),
        }
        graphql_response_object = self._perform_request(graph_full_object)

        self.page = self._graph_object.resp_schema().load(
            graphql_response_object, unknown=EXCLUDE
        )
        if graphql_response_object.get("pageInfo"):
            self._graph_object.query_variables["startAt"] = graphql_response_object[
                "pageInfo"
            ].get("endCursor", None)

        return self.page

    def _perform_request(
        self,
        graph_full_object: dict,
    ) -> dict:
        resp = self.api.graphql(**graph_full_object)
        if "error" in resp:
            errors = GraphqlErrorSchema(many=True).load(
                resp["error"].get("errors", None), unknown=EXCLUDE
            )
            raise errors[0]
        if "data" not in resp:
            raise GraphqlParsingError(
                "graphql data field was not returned but no error occurred"
            )

        graphql_response_object = resp["data"][self._graph_object.object_name]
        if graphql_response_object is None:
            raise GraphqlParsingError(
                f"user requested object {self._graph_object.object_name} was not returned"
            )

        return graphql_response_object
