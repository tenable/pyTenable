"""
Vulns
=====

The following methods leverage stored queries relating to vulnerability metadata within
Cloud Security.

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:


.. autoclass:: CloudSecurityVulnIterator
    :members:
"""
from tenable.base.graphql import GraphQLEndpoint, GraphQLIterator


class FindingsAPI(GraphQLEndpoint):
    def get(
        self,
        page_size: int = 100,
        search: str | None = None,
        sort: list[dict[str, str]] | None = None,
        after: str | None = None,
    ):
        """
        Requests virtual machine vulnerability metadata.

        Args:
            page_size: The number of items to return per page.
            search: A search string to filter the results.
            sort: Sortable parameters to order the results by.
            after: A cursor to start the results from.

        Returns:
            An iterable is returned that handles paging of the data.

        Example:
            >>> for finding in otsecurity.findings.get():
            ...     print(finding)
        """
        variables = {"startAt": after}
        if search:
            variables["search"] = search
        if sort:
            variables["sort"] = sort
        return self._query(
            stored_file='findings.graphql',
            iterator=GraphQLIterator,
            graphql_model='findings',
            startAt=after,
            variables=variables,
        )
