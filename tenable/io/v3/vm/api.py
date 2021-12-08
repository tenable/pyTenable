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

    agent_config
    files
    plugins
    scanners
'''
from restfly.endpoint import APIEndpoint

from tenable.io.v3.vm.agent_config import AgentConfigAPI
from tenable.io.v3.vm.files import FileAPI
from tenable.io.v3.vm.plugins import PluginsAPI
from tenable.io.v3.vm.scanners import ScannersAPI


class VulnerabilityManagement(APIEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources
    under Vulnerability Management
    i.e assets, agents, scanners etc.
    '''

    @property
    def agent_config(self):
        '''
        The interface object for the
        :doc:`Agent Config APIs <agent_config>`.
        '''
        return AgentConfigAPI(self._api)

    @property
    def files(self):
        '''
        The interface object for the
        :doc:`Files API <files>`
        '''
        return FileAPI(self._api)

    @property
    def plugins(self):
        '''
        The interface object for the
        :ref:`Plugins API <plugins>`
        '''
        return PluginsAPI(self._api)

    @property
    def scanners(self):
        '''
        The interface object for the
        :doc:`Scanners API <scanners>`
        '''
        return ScannersAPI(self._api)
