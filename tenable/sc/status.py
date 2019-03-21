'''
status
======

The following methods allow for interaction into the Tenable.sc 
`Statuis <https://docs.tenable.com/sccv/api/Status.html>`_ API.  These API calls
are typically used to understand the current job and license statuses.

Methods available on ``sc.status``:

.. rst-class:: hide-signature
.. autoclass:: StatusAPI

    .. automethod:: status
'''
from .base import SCEndpoint

class StatusAPI(SCEndpoint):
    def status(self):
        '''
        Retreives license & status information about the Tenable.sc instance.

        Returns:
            dict: The status dictionary. 
        
        Examples:
            >>> status = sc.status.status()
        '''
        return self._api.get('status').json()['response']