from .base import CSEndpoint

class RegistryAPI(CSEndpoint):
    def repos(self, limit=None, offset=None):
        '''
        `container-security-repositories: list-repositories <https://cloud.tenable.com/api#/resources/container-security-repositories/list-repositories>`_

        Args:
            offset (int, optional): Number of items to skip before returning.
            limit (int, optional): Maximum number of items to return.

        Returns:
            dict: Dictionary containing the list of items requested.
        '''
        payload = dict()

        if limit:
            payload['limit'] = self._check('limit', limit, int)
        if offset:
            payload['offset'] = self._check('offset', offset, int)

        return self._api.get('v1/repositories', params=payload).json()['items']

    def images(self, repo_id, limit=None, offset=None):
        '''
        `container-security-repositories: list-images <https://cloud.tenable.com/api#/resources/container-security-repositories/list-images>`_

        Args:
            repo_id (int): The unique identifier for the repository.
            offset (int, optional): Number of items to skip before returning.
            limit (int, optional): Maximum number of items to return.

        Returns:
            dict: Dictionary containing the list of items requested.
        '''
        payload = dict()

        if limit:
            payload['limit'] = self._check('limit', limit, int)
        if offset:
            payload['offset'] = self._check('offset', offset, int)

        return self._api.get('v1/repositories/{}/images'.format(
            self._check('repo_id', repo_id, int)), params=payload).json()['items']