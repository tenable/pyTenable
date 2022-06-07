'''
Vulnerability Management
========================

The following API's are available for interaction under
Vulnerability Management platform.

Methods available on ``tio.v3.vm``:


.. rst-class:: hide-signature
.. autoclass:: VulnerabilityManagement
    :members:

.. toctree::
    :hidden:
    :glob:

    assets

'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.assets.api import AssetsAPI


class VulnerabilityManagement(ExploreBaseEndpoint):
    '''
    This class will contain property for all resources
    under Vulnerability Management
    i.e assets, agents, scanners etc.
    '''

    @property
    def assets(self):
        """
        The interface object for the Assets APIs
        :doc:`Tenable.io v3 assets APIs <assets>`.
        """
        return AssetsAPI(self._api)
