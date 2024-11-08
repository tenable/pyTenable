'''
APIKeys
=======

Methods described in this section relate to the APIKeys API.
These methods can be accessed at ``TenableIE.api_keys``.

.. rst-class:: hide-signature
.. autoclass:: APIKeyAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint


class APIKeyAPI(APIEndpoint):
    _path = 'api-key'

    def get(self) -> str:
        '''
        Gets the API Key of the current user.

        Examples:

            >>> tie.api_keys.get()
        '''
        return self._get(box=True).key

    def refresh(self) -> str:
        '''
        Creates or renews an API for the current user.  Will also refresh the
        API Key used in the current TenableIE session.

        Examples:

            >>> tie.api_keys.refresh()
        '''
        key = self._post(json={}, box=True).key
        self._api._key_auth(key)
        return key
