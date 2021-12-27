'''
Web Application Scanning
========================

The following API's are available for interaction under Web Application
Scanning

Methods available on ``tio.v3.was``:


.. rst-class:: hide-signature
.. autoclass:: WebApplicationScanning
    :members:

.. toctree::
    :hidden:
    :glob:

    attachments
    folders
    scans
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.was.attachments.api import AttachmentsAPI
from tenable.io.v3.was.folders.api import FoldersAPI
from tenable.io.v3.was.scans.api import ScansAPI


class WebApplicationScanning(ExploreBaseEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources under Web Application
    Scanning i.e plugins, scans, folders etc.
    '''

    @property
    def attachments(self):
        '''
        The interface object for the
        :doc:`Attachments API <attachments>`
        '''
        return AttachmentsAPI(self._api)

    @property
    def folders(self):
        '''
        The interface object for the
        :doc:`Folders API <folders>`
        '''
        return FoldersAPI(self._api)

    @property
    def scans(self):
        '''
        The interface object for the
        :doc:`Scans API <scans>`
        '''
        return ScansAPI(self._api)
