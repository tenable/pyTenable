'''
Checker
=======

Methods described in this section relate to the checker API.
These methods can be accessed at ``TenableIE.checker``.

.. rst-class:: hide-signature
.. autoclass:: CheckerAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.checker.schema import CheckerSchema
from tenable.base.endpoint import APIEndpoint


class CheckerAPI(APIEndpoint):
    _path = 'checkers'
    _schema = CheckerSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieves the list of checkers.

        Returns:
            list:
                A list of checkers.

        Examples:

            >>> tie.checker.list()
        '''
        return self._schema.load(self._get(), many=True)

    def details(self, checker_id: str) -> Dict:
        '''
        Gets the details of the particular checker based on checker
        identifier.

        Args:
            checker_id (str): The checker instance identifier.

        Returns:
            dict:
                Details of the given ``checker_id``.

        Examples:

            >>> tie.checker.details(checker_id='1')
        '''
        return self._schema.load(self._get(f'{checker_id}'))
