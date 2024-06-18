'''
Preference
=============

Methods described in this section relate to the preferences API.
These methods can be accessed at ``TenableIE.preference``.

.. rst-class:: hide-signature
.. autoclass:: PreferenceAPI
    :members:
'''
from typing import Dict
from tenable.base.endpoint import APIEndpoint
from .schema import PreferenceSchema


class PreferenceAPI(APIEndpoint):
    _path = 'preferences'
    _schema = PreferenceSchema()

    def details(self) -> Dict:
        '''
        Get the user's preferences

        Returns:
            dict:
                The user's preferences object

        Examples:
            >>> tie.preference.details()
        '''
        return self._schema.load(self._get())

    def update(self,
               **kwargs
               ) -> Dict:
        '''
        Update the user's preferences

        Args:
            language (optional, str):
                The language of product for the current user.
            preferred_profile_id (optional, int):
                The profile identifier to use after login for the current user.

        Return:
            The user's preferences object

        Example:
            >>> tie.preference.update(
            ...     language='en',
            ...     preferred_profile_id=1
            ... )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(self._patch(json=payload))
