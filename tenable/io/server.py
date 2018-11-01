'''
server
======

The following methods allow for interaction into the Tenable.io 
`server <https://cloud.tenable.com/api#/resources/server>`_ API endpoints.

Methods available on ``tio.server``:

.. rst-class:: hide-signature
.. autoclass:: ServerAPI

    .. automethod:: properties
    .. automethod:: status
'''
from .base import TIOEndpoint

class ServerAPI(TIOEndpoint):
    def properties(self):
        '''
        Retrieves the various properties used within the Tenable.io instance.

        `server: properties <https://cloud.tenable.com/api#/resources/server/properties>`_

        Returns:
            dict: The server properties.

        Examples:
            >>> props = tio.server.properties()
            >>> pprint(props)
        '''
        return self._api.get('server/properties').json()

    def status(self):
        '''
        Retrieves the server status of the Tenable.io instance.

        `server: status <https://cloud.tenable.com/api#/resources/server/status>`_

        Returns:
            dict: The server status.

        Examples:
            >>> status = tio.server.status()
            >>> pprint(status)
        '''
        return self._api.get('server/status').json()