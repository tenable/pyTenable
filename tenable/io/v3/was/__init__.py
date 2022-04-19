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
    configurations
    definitions
    folders
    plugins
    scans
    templates
    user_templates
    vulnerabilities
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.was.attachments.api import AttachmentsAPI
from tenable.io.v3.was.configurations.api import ConfigurationsAPI
from tenable.io.v3.was.folders.api import FoldersAPI
from tenable.io.v3.was.plugins.api import PluginsAPI
from tenable.io.v3.was.scans.api import ScansAPI
from tenable.io.v3.was.vulnerabilities.api import VulnerabilityAPI
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
        :doc:`Tenable.IO v3 Attachments APIs <attachments>`
        '''
        return AttachmentsAPI(self._api)

    @property
    def configurations(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Configurations APIs <configurations>`
        '''
        return ConfigurationsAPI(self._api)

    @property
    def folders(self):
        '''
        The interface object for the
        :doc:`Tenable.IO v3 Folders APIs <folders>`
        '''
        return FoldersAPI(self._api)

    @property
    def plugins(self):
        '''
        The interface object for the
        :doc:`Tenable.IO v3 Plugins APIs <plugins>`
        '''
        return PluginsAPI(self._api)

    @property
    def scans(self):
        '''
        The interface object for the
        :doc:`Tenable.IO v3 Scans APIs <scans>`
        '''
        return ScansAPI(self._api)

    @property
    def vulnerabilities(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 WAS Vulnerabilities APIs <vulnerabilities>`
        '''
        return VulnerabilityAPI(self._api)

    @property
    def templates(self):
        '''
        The interface object for the
        :doc:`Tenable.IO v3 Templates APIs <templates>`
        '''
        return TemplatesAPI(self._api)

    @property
    def user_templates(self):
        '''
        The interface object for the
        :doc:`Tenable.IO v3 User-Templates APIs <user_templates>`
        '''
        return UserTemplatesAPI(self._api)
