'''
Version3 API
============

The following sub-package allows for interaction with the Tenable.io - Version3API

Methods available on ``tio.v3``:

.. rst-class:: hide-signature
.. autoclass:: Version3API
    :members:

.. toctree::
    :hidden:
    :glob:

    explore/index
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.explore import Explore


class Version3API(APIEndpoint):
    '''
    This will contain property for all resources/app under Tenable.io - V3.
    '''

    @property
    def explore(self):
        '''
        The interface object for the
         :doc:`Tenable.io v3 explore <explore/index>`
        '''
        return Explore(self._api)
