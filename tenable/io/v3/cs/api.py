'''
Container Security
==================

The following sub-package allows for interaction with the Tenable.io
Container Security APIs.

.. rst-class:: hide-signature
.. autoclass:: ContainerSecurity
    :members:

.. toctree::
    :hidden:
    :glob:

    reports
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.cs.reports import ReportsAPI


class ContainerSecurity(APIEndpoint):
    @property
    def reports(self):
        '''
        The interface object for the
        :doc:`Tenable.io Container Security Reports APIs <reports>`.
        '''
        return ReportsAPI(self._api)
