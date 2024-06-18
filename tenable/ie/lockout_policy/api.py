'''
Lockout Policy
==============

Methods described in this section relate to the lockout policy API.
These methods can be accessed at ``TenableIE.lockout_policy``.

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
            >>> tie.lockout_policy.details()
        '''
        return self._schema.load(self._get())

    def update(self,
               **kwargs
               ) -> None:
        '''
        Update the lockout policy

        Args:
            enabled (optional, bool):
                Whether the lockout policy enabled?
            lockout_duration (optional, int):
                The time duration for which user will be locked out after
                several failed login attempts.
            failed_attempt_threshold (optional, int):
                The number of failed login attempts to trigger lockout.
            failed_attempt_period (optional, int):
                The time to wait before the login attempts count is reseted.

        Return:
            None

        Example:
            >>> tie.lockout_policy.update(enabled=True)
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        self._patch(json=payload)
