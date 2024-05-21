'''
Images
======

The following methods allow for interaction into the Tenable Vulnerability Management
Container Security :devportal:`images <cs-v2-images>` API endpoints.

Methods available on ``tio.cs.images``:

.. rst-class:: hide-signature
.. autoclass:: ImagesAPI
    :members:
'''
from typing_extensions import Literal
from typing import Optional, Dict, Union
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint
from tenable.io.cs.iterator import CSIterator


class ImagesAPI(APIEndpoint):
    _path = 'container-security/api/v2/images'
    _box = True
    _box_attrs = {'camel_killer_box': True}

    def list(self,  # noqa: PLC0103,PLR0913
             name: Optional[str] = None,
             repo: Optional[str] = None,
             tag: Optional[str] = None,
             has_malware: Optional[bool] = None,
             score: Optional[int] = None,
             score_operator: Optional[Literal['EQ', 'GT', 'LT']] = None,
             os: Optional[str] = None,
             offset: int = 0,
             limit: int = 1000,
             return_json: bool = False
             ) -> Union[Dict, CSIterator]:
        '''
        Returns the list of images stored within Container Security.

        :devportal:`API Documentation <container-security-v2-list-images>`

        Args:
            name (str, optional):
                Image name to filter on.  Filter is case-sensitive
                and enforces an exact match.
            repo (str, optional):
                Repository name to filter on.  Filter is case-sensitive
                and enforces an exact match.
            tag (str, optional):
                Tag to filter on.  Filter is case-sensitive and enforces
                an exact match.
            has_malware (bool, optional):
                Specifies whether to return only images with malware
                associated to them.
            score (int, optional):
                The score value to filter on.
            score_operator (str, optional):
                The score operator to use with the score value.  Supported
                operations are ``EQ`` (equal), ``GT`` (greater-than), and
                ``LT`` (less-than).
            os (str, optional):
                The operating system to filter on.  Filter is case-sensitive
                and enforces an exact match.
            offset (int, optional):
                The number of records to skip before starting to return data.
            limit (int, optional):
                The number of records to return for each page of data.
            return_json (bool, optional):
                If set, then the response will instead be a Dict object instead
                of an iterable.

        Examples:

            Using the default iterable:

            >>> for image in tio.cs.images.list():
            ...     print(image)

            Getting the raw JSON response:

            >>> resp = tio.cs.images.list(return_json=True)
            >>> for item in resp['items']:
            ...     print(item)
        '''
        params = dict_clean({
            'offset': offset,
            'limit': limit,
            'name': name,
            'repo': repo,
            'tag': tag,
            'hasMalware': has_malware,
            'score': score,
            'scoreOperator': score_operator,
            'os': os
        })
        if return_json:
            return self._get(params=params)
        return CSIterator(self._api,
                          _path=self._path,
                          _params=params,
                          _limit=limit,
                          _offset=offset
                          )

    def details(self, repository: str, image: str, tag: str) -> Dict:
        '''
        Returns the details for the specified image.

        :devportal:`API Documentation <container-security-v2-get-image-details>`  # noqa: E501

        Args:
            repository (str):
                The repository name.
            image (str):
                The image name.
            tag (str):
                The tag name.

        Examples:

            >>> tio.cs.images.details('centos', '7', 'latest')
        '''
        return self._get(f'{repository}/{image}/{tag}')

    def delete(self, repository: str, image: str, tag: str) -> None:
        '''
        Deleted the specified image.

        :devportal:`API Documentation <container-security-v2-delete-image>`

        Args:
            repository (str):
                The repository name.
            image (str):
                The image name.
            tag (str):
                The tag name.

        Examples:

            >>> tio.cs.images.delete('centos', '7', 'latest')
        '''
        self._delete(f'{repository}/{image}/{tag}')
