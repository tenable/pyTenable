from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class WASDefinitionsAPI(ExploreBaseEndpoint):

    def folders(self):
        '''
        Example
        >>> tio.definitions.was.folders()
        '''
        raise NotImplementedError()
