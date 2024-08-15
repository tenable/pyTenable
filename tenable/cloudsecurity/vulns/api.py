from tenable.base.graphql import GraphQLEndpoint
from .iterator import CloudSecurityVulnIterator


class VulnsAPI(GraphQLEndpoint):
    def virtualmachines(self, page_size: int = 10):
        return self._query(
            stored_file='vulns-virtualmachine.graphql',
            iterator=CloudSecurityVulnIterator,
            graphql_model='VirtualMachines',
            limit=page_size
        )

    def containerimages(self, page_size: int = 10):
        return self._query(
            stored_file='vulns-containerimage.graphql',
            iterator=CloudSecurityVulnIterator,
            graphql_model='ContainerImages',
            limit=page_size
        )
