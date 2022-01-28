from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class MSSPDefinitionsAPI(ExploreBaseEndpoint):

    def accounts(self):
        return self._get('/api/v3/definitions/mssp/accounts')

    def logos(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')
