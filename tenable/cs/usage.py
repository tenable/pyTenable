'''
usage
=====

The usage methods allow interaction into ContainerSecurity 
usage API.

Methods available on ``cs.usage``:

.. rst-class:: hide-signature
.. autoclass:: UsageAPI

    .. automethod:: stats
'''
from .base import CSEndpoint

class UsageAPI(CSEndpoint):
    def stats(self):
        '''
        Returns the usage statistics for ContainerSecurity

        Returns:
            dict: The usage statistics information.

        Examples:
            >>> stats = cs.usage.stats()
        '''
        return self._api.get('organization-stats').json()