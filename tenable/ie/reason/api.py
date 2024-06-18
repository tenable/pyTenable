'''
Reason
======
Methods described in this section relate to the reason API.
These methods can be accessed at ``TenableIE.reason``.

.. rst-class:: hide-signature
.. autoclass:: ReasonAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.reason.schema import ReasonSchema
from tenable.base.endpoint import APIEndpoint


class ReasonAPI(APIEndpoint):
    _schema = ReasonSchema()
    _path = 'reasons'

    def list(self) -> List[Dict]:
        '''
        Retrieves the list of reason instances.

        Returns:
            list:
                The list of reason instances.

        Examples:
            >>> tie.reason.list()
        '''
        return self._schema.load(self._get(), many=True)

    def details(self, reason_id: str) -> Dict:
        '''
        Retrieves the details of the reason based on reason_id

        Args:
            reason_id (str):
                The reason instance identifier.

        Returns:
            dict:
                Details of the reason object .

        Examples:
            >>> tie.reason.details(reason_id='1')
        '''
        return self._schema.load(self._get(f'{reason_id}'))

    def list_by_checker(self,
                        profile_id: str,
                        checker_id: str
                        ) -> List[Dict]:
        '''
        Retrieves the details of the reason based on profile_id and checker_id.

        Args:
            profile_id (str):
                The profile instance identifier
            checker_id (str):
                The checker instance identifier

        Returns:
            list:
                Details of the reason object.

        Examples:
            >>> tie.reason.list_by_checker(
            ...     profile_id='1',
            ...     checker_id='1'
            ...     )
        '''
        return self._schema.load(self._api.get(
            f'profiles/{profile_id}/checkers/{checker_id}/reasons'),
            many=True)

    def list_by_directory_and_event(self,
                                    profile_id: str,
                                    infrastructure_id: str,
                                    directory_id: str,
                                    event_id: str
                                    ) -> List[Dict]:
        '''
        Retrieves the details of the reason object based on profile_id,
        directory_id and event_id.

        Args:
            profile_id (str):
                The profile instance identifier.
            infrastructure_id (str):
                The infrastructure instance identifier.
            directory_id (str):
                The directory instance identifier.
            event_id (str):
                The event instance identifier.

        Returns:
            list:
                Details of the reason object.

        Examples:
            >>> tie.reason.list_by_directory_and_event(
            ...     profile_id='1',
            ...     infrastructure_id='1',
            ...     directory_id='1',
            ...     event_id='1'
            ...     )
        '''
        return self._schema.load(self._api.get(
            f'profiles/{profile_id}/infrastructures/{infrastructure_id}'
            f'/directories/{directory_id}/events/{event_id}/reasons'),
            many=True)
