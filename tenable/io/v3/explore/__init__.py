'''
Explore
=======

The following API's are available for interaction under Explore platform.

Methods available on ``tio.v3.explore``:


.. rst-class:: hide-signature
.. autoclass:: Explore
    :members:

.. toctree::
    :hidden:
    :glob:

    assets
    findings

'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.explore.assets.api import AssetsAPI
from tenable.io.v3.explore.findings.api import FindingsAPI


class Explore(ExploreBaseEndpoint):
    '''
    This class will contain property for all resources under Explore  i.e. assets, findings etc.
    '''

    @property
    def assets(self):
        """
        The interface object for the Assets APIs
        :doc:`Tenable.io v3 explore assets APIs <assets>`.
        """
        return AssetsAPI(self._api)

    @property
    def findings(self):
        """
        The interface object for the Findings APIs
        :doc:`Tenable.io v3 explore findings APIs <findings>`.
        """
        return FindingsAPI(self._api)
