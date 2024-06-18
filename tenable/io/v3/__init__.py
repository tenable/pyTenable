"""
Version3 API
============

The following sub-package allows for interaction with the Tenable Vulnerability Management - Version3API

Methods available on ``tio.v3``:

.. rst-class:: hide-signature
.. autoclass:: Version3API
    :members:

.. toctree::
    :hidden:
    :glob:

    access_control
"""
import warnings
from tenable.base.endpoint import APIEndpoint
from tenable.io.access_control import AccessControlAPI


class Version3API(APIEndpoint):
    """
    This will contain property for all resources/app under Tenable Vulnerability Management - V3.
    """

    @property
    def access_control(self):
        """
        The interface object for the
         :doc:`Tenable Vulnerability Management v3 access control <access_control>`
        """
        warnings.warn('This Method is deprecated and will be removed in a'
                      'later release, please switch to using the'
                      '`access_control` method on the base TVM Object instead',
                      DeprecationWarning,
                      stacklevel=2
                      )
        return AccessControlAPI(self._api)
