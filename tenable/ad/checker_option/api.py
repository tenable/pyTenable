'''
Checker Option
==============

Methods described in this section relate to the the checker option API.
These methods can be accessed at ``TenableAD.checker_option``.

.. rst-class:: hide-signature
.. autoclass:: CheckerOptionAPI
    :members:
'''
from typing import List, Dict
from restfly.utils import dict_clean
from tenable.ad.checker_option.schema import CheckerOptionSchema
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
            staged (optional, str):
                ???
            per_page (optional, str):
                ???
            page (optional, str):
                ???

        Returns:
            list:
                List of checker options.

        Examples:

            >>> tad.checker_option.list(
            ...     profile_id='9',
            ...     checker_id='1',
            ...     staged='1',
            ...     per_page='5',
            ...     page='1')

        '''
        params = self._schema.dump(self._schema.load(
            dict_clean({
                'perPage': kwargs.get('per_page'),
                'page': kwargs.get('page'),
                'staged': kwargs.get('staged')
            })))
        return self._schema.load(
            self._api.get(
                f'profiles/{profile_id}/checkers/{checker_id}/checker-options',
                params=params), many=True)

    def create(self,
               profile_id: str,
               checker_id: str,
               codename: str,
               value: str,
               value_type: str,
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
                ???
            value (str):
                ???
            value_type (str):
                ???
            directory_id (optional, int):
                The directory instance identifier.

        Returns:
            list:
                Created checker option instance.

        Examples:

            >>> tad.checker_option.create(
            ...     profile_id='9',
            ...     checker_id='2',
            ...     codename='codename',
            ...     value='false',
            ...     value_type='boolean'
            ...     directory_id=3)
        '''
        payload = [
            self._schema.dump(self._schema.load(
                dict_clean({
                    'directoryId': kwargs.get('directory_id'),
                    'codename': codename,
                    'value': value,
                    'valueType': value_type,
                })
            ))
        ]
        return self._schema.load(
            self._api.post(
                f'profiles/{profile_id}/checkers/{checker_id}/checker-options',
                json=payload), many=True)
