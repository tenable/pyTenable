"""
Assets
======

The following methods leverage stored queries relating to asset metadata within
Cloud Security.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:


.. autoclass:: CloudSecurityAssetIterator
    :members:
"""
from tenable.base.graphql import GraphQLEndpoint, GraphQLIterator


class CloudSecurityAssetIterator(GraphQLIterator):
    pass


class AssetsAPI(GraphQLEndpoint):
    def compute(self, page_size: int = 10) -> CloudSecurityAssetIterator:
        """
        Requests compute asset metadata.

        Args:
            page_size (int, optional):
                How many items should be returned per page?

        Returns:
            An iterable is returned that handles paging of the data.

        Example:
            >>> for asset in cloudsecurity.assets.compute():
            ...     print(asset)
        """
        return self._query(
            stored_file='assets-compute.graphql',
            iterator=CloudSecurityAssetIterator,
            graphql_model='Entities',
            limit=page_size
        )

    def container(self, page_size: int = 10):
        """
        Requests container asset metadata.

        Args:
            page_size (int, optional):
                How many items should be returned per page?

        Returns:
            An iterable is returned that handles paging of the data.

        Example:
            >>> for asset in cloudsecurity.assets.container():
            ...     print(asset)
        """
        return self._query(
            stored_file='assets-container.graphql',
            iterator=CloudSecurityAssetIterator,
            graphql_model='Entities',
            limit=page_size
        )
