'''
Repositories
============

The following methods allow for interaction into the Tenable Vulnerability Management
Container Security :devportal:`repositories <cs-v2-repositories>`
API endpoints.

Methods available on ``tio.cs.repositories``:

.. rst-class:: hide-signature
.. autoclass:: RepositoriesAPI
    :members:
'''
from typing import Optional, Dict, Union
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint
from tenable.io.cs.iterator import CSIterator


class RepositoriesAPI(APIEndpoint):
    _path = 'container-security/api/v2/repositories'
    _box = True
    _box_attrs = {'camel_killer_box': True}

    def list(self,  # noqa: PLC0103,PLR0913
             name: Optional[str] = None,
             contains: Optional[str] = None,
             offset: int = 0,
             limit: int = 1000,
             return_json: bool = False
             ) -> Union[Dict, CSIterator]:
        '''
        Returns the list of images stored within Container Security.

        :devportal:`API Documentation <container-security-v2-list-repositories>`  # noqa: E501

        Args:
            name (str, optional):
                Image name to filter on.  Filter is case-sensitive
                and enforces an exact match.
            contains (str, optional):
                Partial name to filter on.  Filter is case-sensitive.
            offset (int, optional):
                The number of records to skip before starting to return data.
            limit (int, optional):
                The number of records to return for each page of data.
            return_json (bool, optional):
                If set, then the response will instead be a Dict object instead
                of an iterable.

        Examples:

            Using the default iterable:

            >>> for repo in tio.cs.repositories.list():
            ...     print(repo)

            Getting the raw JSON response:

            >>> resp = tio.cs.repositories.list(return_json=True)
            >>> for item in resp['items']:
            ...     print(item)
        '''
        params = dict_clean({
            'offset': offset,
            'limit': limit,
            'name': name,
            'contains': contains,
        })
        if return_json:
            return self._get(params=params)
        return CSIterator(self._api,
                          _path=self._path,
                          _params=params,
                          _limit=limit,
                          _offset=offset
                          )

    def details(self, name: str) -> Dict:
        '''
        Returns the details for the specified repository.

        :devportal:`API Documentation <container-security-v2-get-repository-details>`  # noqa: E501

        Args:
            name (str):
                The repository name.

        Examples:

            >>> tio.cs.repositories.details('centos')
        '''
        return self._get(name)

    def delete(self, name: str) -> None:
        '''
        Deleted the specified repository.

        :devportal:`API Documentation <container-security-v2-delete-repository>`  # noqa: E501

        Args:
            name (str):
                The repository name.

        Examples:

            >>> tio.cs.repositories.delete('centos')
        '''
        self._delete(name)
