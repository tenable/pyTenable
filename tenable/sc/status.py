'''
Status
======

The following methods allow for interaction into the Tenable Security Center
:sc-api:`Status <Status.htm>` API.  These API calls are typically used to
understand the current job and license statuses.

Methods available on ``sc.status``:

.. rst-class:: hide-signature
.. autoclass:: StatusAPI
    :members:
'''
from .base import SCEndpoint

class StatusAPI(SCEndpoint):
    def status(self):
        '''
        Retrieves license & status information about the Tenable Security Center instance.

        :sc-api:`status: status <Status.htm#StatusRESTReference-/status>`

        Returns:
            :obj:`dict`:
                The status dictionary.

        Examples:
            >>> status = sc.status.status()
        '''
        return self._api.get('status').json()['response']
