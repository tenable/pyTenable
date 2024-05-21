'''
Container Security
==================

The following sub-package allows for interaction with the Tenable Vulnerability Management
Container Security APIs.

.. rst-class:: hide-signature
.. autoclass:: ContainerSecurity
    :members:

.. toctree::
    :hidden:
    :glob:

    images
    reports
    repositories
'''
from tenable.base.endpoint import APIEndpoint


from tenable.io.cs.images import ImagesAPI
from tenable.io.cs.reports import ReportsAPI
from tenable.io.cs.repositories import RepositoriesAPI


class ContainerSecurity(APIEndpoint):
    @property
    def images(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Container Security Images APIs <images>`.
        '''
        return ImagesAPI(self._api)

    @property
    def reports(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Container Security Reports APIs <reports>`.
        '''
        return ReportsAPI(self._api)

    @property
    def repositories(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Container Security Repository APIs <repositories>`.
        '''
        return RepositoriesAPI(self._api)
