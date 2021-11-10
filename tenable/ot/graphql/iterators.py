'''
GraphQL Tenable.ot API iterator.
'''
from marshmallow.utils import EXCLUDE
from restfly.iterator import APIIterator
from tenable.ot.graphql.definitions import (
    GraphqlErrorSchema,
    GraphqlParsingError
)


class OTGraphIterator(APIIterator):
    '''
    Iterator class over Tenable.ot GraphQL connetions.
    '''

    def __init__(self, api, graph_object, **kwargs):
        self._graph_object = graph_object
        super().__init__(api, **kwargs)

    def _get_page(self):
        '''
        Retrieves the next page of data.
        '''
        graph_full_object = {
            'query': self._graph_object.query,
            'variables': self._graph_object.query_variables
        }

        resp = self._api.graphql(**graph_full_object)
        if 'error' in resp:
            errors = GraphqlErrorSchema(many=True).load(
                resp['error']['errors'], unknown=EXCLUDE)
            raise errors[0]
        if 'data' not in resp:
            raise GraphqlParsingError(
                'graphql data field was not returned but no error occurred')

        connection_object = resp['data'][self._graph_object.object_name]
        if connection_object is None:
            raise GraphqlParsingError(
                f'user requested object {self._graph_object.object_name}' +
                ' was not returned')

        self.page = self._graph_object.resp_schema().load(
            connection_object, unknown=EXCLUDE)

        self._graph_object.query_variables['startAt'] = connection_object[
            'pageInfo'].get('endCursor', None)

        return self.page
