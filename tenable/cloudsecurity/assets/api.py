from tenable.base.graphql import GraphQLEndpoint
from .iterator import CloudSecurityAssetIterator


class AssetsAPI(GraphQLEndpoint):
    def compute(self, page_size: int = 10):
        return self._query(
            stored_file='assets-compute.graphql',
            iterator=CloudSecurityAssetIterator,
            graphql_model='Entities',
            limit=page_size
        )

    def container(self, page_size: int = 10):
        return self._query(
            stored_file='assets-container.graphql',
            iterator=CloudSecurityAssetIterator,
            graphql_model='Entities',
            limit=page_size
        )
