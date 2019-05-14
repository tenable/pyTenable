'''
status
======

The following methods allow for interaction into the Tenable.sc
:sc-api:`Status <Status.html>` API.  These API calls are typically used to
understand the current job and license statuses.

Methods available on ``sc.status``:

.. rst-class:: hide-signature
.. autoclass:: StatusAPI

    .. automethod:: status
'''
from .base import SCEndpoint

class StatusAPI(SCEndpoint):
    def status(self):
        '''
        Retrieves license & status information about the Tenable.sc instance.

        :sc-api:`status: status <Status.html#StatusRESTReference-/status>`

        Returns:
            :obj:`dict`:
                The status dictionary.

        Examples:
            >>> status = sc.status.status()
        '''
        return self._api.get('status').json()['response']