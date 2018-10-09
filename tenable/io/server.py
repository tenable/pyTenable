from tenable.tenable_io.base import TIOEndpoint

class ServerAPI(TIOEndpoint):
    def properties(self):
        '''
        `server: properties <https://cloud.tenable.com/api#/resources/server/properties>`_

        Returns:
            dict: The server properties.
        '''
        return self._api.get('server/properties').json()

    def status(self):
        '''
        `server: status <https://cloud.tenable.com/api#/resources/server/status>`_

        Returns:
            dict: The server status.
        '''
        return self._api.get('server/status').json()