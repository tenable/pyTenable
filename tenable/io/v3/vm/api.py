'''
API's under Vulnerability Management
'''
from restfly.endpoint import APIEndpoint

from .scanners import ScannersAPI


class VulnerabilityManagement(APIEndpoint):  # noqa: PLR0904
    """
    This class will contain property for all resources
    under Vulnerability Management
    i.e assets, agents, scanners etc.
    """

    @property
    def scanners(self):
        return ScannersAPI(self._api)
