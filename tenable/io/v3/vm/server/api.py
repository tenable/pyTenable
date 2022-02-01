'''
Server
======

The following methods allow for interaction into the Tenable.io
:devportal:`server <server>` API endpoints.

Methods available on ``tio.v3.vm.server``:

.. rst-class:: hide-signature
.. autoclass:: ServerAPI
    :members:
'''
from typing import Dict

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class ServerAPI(ExploreBaseEndpoint):
    '''
    This class contains all the methods related to Server Endpoint.
    '''
    _path = 'api/v3/server'
    _conv_json = True

    def properties(self) -> Dict:
        '''
        Retrieves the various properties used within the Tenable.io instance.

        :devportal:`server: properties <server-properties>`

        Returns:
            :obj:`dict`:
                The server properties.

        Examples:
            >>> props = tio.v3.vm.server.properties()
            >>> pprint(props)
        '''
        return self._get('properties')

    def status(self) -> Dict:
        '''
        Retrieves the server status of the Tenable.io instance.

        :devportal:`server: status <server-status>`

        Returns:
            :obj:`dict`:
                The server status.

        Examples:
            >>> status = tio.v3.vm.server.status()
            >>> pprint(status)
        '''
        return self._get('status')
