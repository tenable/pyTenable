'''
Score
=====

Methods described in this section relate to the score API.
These methods can be accessed at ``TenableIE.score``.

.. rst-class:: hide-signature
.. autoclass:: ScoreAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.score.schema import ScoreSchema
from tenable.base.endpoint import APIEndpoint


class ScoreAPI(APIEndpoint):
    _schema = ScoreSchema()

    def list(self,
             profile_id: str,
             **kwargs
             ) -> List[Dict]:
        '''
        Get the list of directories score by profile.

        Args:
            Option-1:
                profile_id (str):
                    The profile instance identifier.
                directory_ids (optional, List(int)):
                    The list of directory_ids.
                checker_ids (optional, List(int)):
                    The list of checker_ids.
                reason_ids (optional, List(int)):
                    The list of reason_ids.

            Option-2:
                profile_id (str):
                    The profile instance identifier.
                directory_ids (optional, str):
                    The directory_id instance identifier.
                checker_ids (optional, str):
                    The checker_id instance identifier.
                reason_ids (optional, str):
                    The reason_id instance identifier.

        Returns:
            list:
                List of scores of different directories in the instance.

        Examples:

            With single directory_ids, checker_ids, reason_ids

            >>> tie.score.list(profile_id='1',
            ...     directory_ids='3',
            ...     checker_ids='1',
            ...     reason_ids='1')

            With multiple directory_ids, checker_ids, reason_ids

            >>> tie.score.list(profile_id='1',
            ...     directory_ids=[1, 2, 3],
            ...     checker_ids=[1, 2, 3],
            ...     reason_ids=[1, 2, 3])
        '''
        param = self._schema.dump(self._schema.load({
            'directoryIds': kwargs.get('directory_ids'),
            'checkerIds': kwargs.get('checker_ids'),
            'reasonIds': kwargs.get('reason_ids')
        }))
        return self._schema.load(self._api.get(f'profiles/{profile_id}/scores',
                                               params=param), many=True)
