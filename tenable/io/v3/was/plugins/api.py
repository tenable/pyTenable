'''
Plugins
=======

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 plugins <was-v2-plugins>` API.

Methods available on ``tio.v3.was.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI
    :members:
'''
from typing import Dict

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class PluginsAPI(ExploreBaseEndpoint):
    _path = 'api/v3/was/plugins'
    _conv_json = True

    def details(self, id: int) -> Dict:
        '''
        Returns details for the specified Tenable.io
        Web Application Scanning plugin.

        :devportal:`was plugins: plugin details <was-v2-plugins-details>`

        Args:
            id (int):
                The ID of a Tenable.io Web Application Scanning plugin.

        Returns:
            :obj:`dict`:
                The resource record of the was plugin.

        Examples:
            >>> plugin = tio.v3.was.plugins.details(1)
        '''
        return self._get(f'{id}')

    def search(self, **kwargs):
        raise NotImplementedError(
            'Search and Filter functionality will be updated later.'
        )
