'''
Lockout Policy
=============

Methods described in this section relate to the lockout policy API.
These methods can be accessed at ``TenableAD.lockout_policy``.

.. rst-class:: hide-signature
.. autoclass:: LockoutPolicyAPI
    :members:
'''
from typing import Dict
from tenable.base.endpoint import APIEndpoint
from .schema import LockoutPolicySchema


class LockoutPolicyAPI(APIEndpoint):
    _path = 'lockout-policy'
    _schema = LockoutPolicySchema()

    def details(self) -> Dict:
        '''
        Get the lockout policy

        Returns:
            dict:
                The lockout policy object

        Examples:
            >>> tad.lockout_policy.details()
        '''
        return self._schema.load(self._get())

    def update(self,
               **kwargs
               ) -> None:
        '''
        Update the lockout policy

        Args:
            enabled (optional, bool):
                ???
            lockout_duration (optional, int):
                ???
            failed_attempt_threshold (optional, int):
                ???
            failed_attempt_period (optional, int):
                ???

        Return:
            None

        Example:
            >>> tad.lockout_policy.update(enabled=True)
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        self._patch(json=payload)
