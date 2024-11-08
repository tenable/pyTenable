'''
Checker Option
==============

Methods described in this section relate to the checker option API.
These methods can be accessed at ``TenableIE.checker_option``.

.. rst-class:: hide-signature
.. autoclass:: CheckerOptionAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.checker_option.schema import CheckerOptionSchema
from tenable.base.endpoint import APIEndpoint


class CheckerOptionAPI(APIEndpoint):
    _schema = CheckerOptionSchema()

    def list(self,
             profile_id: str,
             checker_id: str,
             **kwargs
             ) -> List[Dict]:
        '''
        Retrieves the list of checker-options.

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            staged (optional, bool):
                Get only the checker-options that are staged. Accepted
                values are ``True`` and ``False``. Added checker options
                are first staged until the profile is commited. The staged
                profile options are not activated and don't affect
                yet the IOE and the exposure detection.

        Returns:
            list:
                List of checker options.

        Examples:
            >>> tie.checker_option.list(
            ...     profile_id='9',
            ...     checker_id='1',
            ...     staged=True
            ...     )
        '''
        params = self._schema.dump(self._schema.load(kwargs, partial=True))
        return self._schema.load(
            self._api.get(
                f'profiles/{profile_id}/checkers/{checker_id}/checker-options',
                params=params), many=True)

    def create(self,
               profile_id: str,
               checker_id: str,
               **kwargs
               ) -> List[Dict]:
        '''
        Creates the new checker-option.

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            codename (str):
                The codename of the checker option.
            value (str):
                The value of the checker option.
            value_type (str):
                The type of the checker option. Accepted values are:
                ``string``, ``regex``, ``float``, ``integer``, ``boolean``,
                ``date``, ``object``, ``array/string``, ``array/regex``,
                ``array/integer``, ``array/boolean``, ``array/select``,
                ``array/object``.
            directory_id (optional, int):
                The directory instance identifier.

        Returns:
            list:
                Created checker option instance.

        Examples:
            >>> tie.checker_option.create(
            ...     profile_id='9',
            ...     checker_id='2',
            ...     codename='codename',
            ...     value='false',
            ...     value_type='boolean'
            ...     directory_id=3
            ...     )
        '''
        payload = [self._schema.dump(self._schema.load(kwargs))]
        return self._schema.load(
            self._api.post(
                f'profiles/{profile_id}/checkers/{checker_id}/checker-options',
                json=payload), many=True)
