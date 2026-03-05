"""
Assets
======

The following methods leverage stored queries relating to asset metadata within
Cloud Security.

.. rst-class:: hide-signature
.. autoclass:: AssetsAPI
    :members:
"""

from tenable.base.graphql import GraphQLEndpoint

from .iterator import OTSecurityIterator


class AssetsAPI(GraphQLEndpoint):
    def list(self, page_size: int = 10) -> OTSecurityIterator:
        """
        Requests compute asset metadata.

        Args:
            page_size (int, optional):
                How many items should be returned per page?

        Returns:
            An iterable is returned that handles paging of the data.

        Example:
            >>> for asset in otsecurity.assets.list():
            ...     print(asset)
        """
        return self._query(
            stored_file='assets-compute.graphql',
            iterator=OTSecurityIterator,
            graphql_model='Entities',
            limit=page_size,
        )

    def get(self, id) -> None:
        """ """
