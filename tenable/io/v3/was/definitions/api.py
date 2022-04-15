from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class WASDefinitionsAPI(ExploreBaseEndpoint):

    _conv_json = True

    def configurations(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def folders(self):
        '''
        Example
        >>> tio.definitions.was.folders()
        '''
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def plugins(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def vulnerabilities(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def scan_vulnerabilities(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def scans(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def templates(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def user_templates(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')
