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
    templates
    user_templates
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.was.attachments.api import AttachmentsAPI
from tenable.io.v3.was.folders.api import FoldersAPI
from tenable.io.v3.was.scans.api import ScansAPI
from tenable.io.v3.was.templates.api import TemplatesAPI
from tenable.io.v3.was.user_templates.api import UserTemplatesAPI


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

    @property
    def templates(self):
        '''
        The interface object for the
        :doc:`Templates API <templates>`
        '''
        return TemplatesAPI(self._api)

    @property
    def user_templates(self):
        '''
        The interface object for the
        :doc:`User-Templates API <user_templates>`
        '''
        return UserTemplatesAPI(self._api)
