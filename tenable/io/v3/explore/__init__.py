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
    Tenable.io V3 Explore APIs are deprecated. We recommend that you use the equivalent V2 APIs instead.
    '''

    @property
    def assets(self):
        """
        Tenable.io Assets V3 APIs are deprecated. We recommend that you use the equivalent V2 APIs instead.
        :doc:`Tenable.io v3 explore assets APIs <assets>`.
        """
        return AssetsAPI(self._api)

    @property
    def findings(self):
        """
        Tenable.io Findings V3 APIs are deprecated. We recommend that you use the equivalent V2 APIs instead.
        :doc:`Tenable.io v3 explore findings APIs <findings>`.
        """
        return FindingsAPI(self._api)
