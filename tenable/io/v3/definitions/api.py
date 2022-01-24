from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.definitions.api import MSSPDefinitionsAPI
from tenable.io.v3.vm.definitions.api import VMDefinitionsAPI
from tenable.io.v3.was.definitions.api import WASDefinitionsAPI


class DefinitionsAPI(ExploreBaseEndpoint):

    @property
    def mssp(self):
        return MSSPDefinitionsAPI(self._api)

    @property
    def vm(self):
        return VMDefinitionsAPI(self._api)

    @property
    def was(self):
        return WASDefinitionsAPI(self._api)
