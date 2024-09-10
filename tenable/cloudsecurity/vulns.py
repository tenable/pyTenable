"""
Vulns
=====

The following methods leverage stored queries relating to vulnerability metadata within
Cloud Security.

.. rst-class:: hide-signature
.. autoclass:: VulnsAPI
    :members:


.. autoclass:: CloudSecurityVulnIterator
    :members:
"""
from tenable.base.graphql import GraphQLEndpoint, GraphQLIterator


class VulnsAPI(GraphQLEndpoint):
    def virtualmachines(self, page_size: int = 10):
        """
        Requests virtual machine vulnerability metadata.

        Args:
            page_size (int, optional):
                How many items should be returned per page?

        Returns:
            An iterable is returned that handles paging of the data.

        Example:
            >>> for vuln in cloudsecurity.vulns.virtualmachines():
            ...     print(vuln)
        """
        return self._query(
            stored_file='vulns-virtualmachine.graphql',
            iterator=CloudSecurityVulnIterator,
            graphql_model='VirtualMachines',
            limit=page_size
        )

    def containerimages(self, page_size: int = 10):
        """
        Requests container image vulnerability metadata.

        Args:
            page_size (int, optional):
                How many items should be returned per page?

        Returns:
            An iterable is returned that handles paging of the data.

        Example:
            >>> for vuln in cloudsecurity.vulns.containerimages():
            ...     print(vuln)
        """
        return self._query(
            stored_file='vulns-containerimage.graphql',
            iterator=CloudSecurityVulnIterator,
            graphql_model='ContainerImages',
            limit=page_size
        )


class CloudSecurityVulnIterator(GraphQLIterator):
    pidx: int = 0
    sidx: int = 0
    vidx: int = 0

    def _increment_counters(self):
        self.count += 1
        self.page_count += 1
        vlen = len(self.page[self.pidx]['Software'][self.sidx]['Vulnerabilities'])
        slen = len(self.page[self.pidx]['Software'])

        self.vidx += 1
        if self.vidx >= vlen:
            self.vidx = 0
            self.sidx += 1
        if self.sidx >= slen:
            self.sidx = 0
            self.pidx += 1

    def _get_next_item(self):
        asset = self.page[self.pidx]
        software = asset['Software'][self.sidx]
        vulnerability = software['Vulnerabilities'][self.vidx]
        return {
            'Asset': {k: v for k, v in asset.items() if k != 'Software'},
            'Software': {k: v for k, v in software.items() if k != 'Vulnerabilities'},
            'Vulnerability': vulnerability
        }
