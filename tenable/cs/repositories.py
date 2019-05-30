'''
repositories
============

The repositories methods allow interaction into ContainerSecurity
repositories API.

Methods available on ``cs.repositories``:

.. rst-class:: hide-signature
.. autoclass:: RepositoryAPI

    .. automethod:: delete
    .. automethod:: details
    .. automethod:: list
'''
from .base import CSEndpoint, CSIterator

class RepositoryIterator(CSIterator):
    def _get_data(self):
        query = self._query
        query['offset'] = self._offset
        query['limit'] = self._limit
        return self._api.get('repositories', params=query).json()


class RepositoryAPI(CSEndpoint):
    def list(self, **kw):
        '''
        Retrieves a list of repositories configured within ContainerSecurity.

        Args:
            contains (str, optional):
                limit the response to only repositories with the specified
                string within their name.
            image (str, optional):
                limit the response to only repositories containing the image
                name.
            limit (int, optional):
                How many records should be returned within each page of data?
                If nothing is specified, then the default is 50.
            offset (int, optional):
                At what offset do we start returning the data?  If nothing is
                specified, then the default is 0.
            pages (int, optional):
                How many pages

        Returns:
            RepositoryIterator:
                an iterator handling the pagination of the response.

        Examples:
            >>> for repository in cs.repository.list():
            ...     pprint(repository)
        '''
        query = dict()

        if 'contains' in kw:
            query['nameContains'] = self._check('contains', kw['contains'], str)
        if 'image' in kw:
            query['imageName'] = self._check('image', kw['image'], str)

        return RepositoryIterator(self._api,
            _limit=self._check(
                'limit', kw['limit'], int) if 'limit' in kw else 50,
            _offset=self._check(
                'offset', kw['offset'], int) if 'offset' in kw else 0,
            _pages_total=self._check(
                'pages', kw['pages'], int) if 'pages' in kw else None,
            _query=query)

    def details(self, name):
        '''
        Retrieves the list of images for the specified repository.

        Args:
            name (str): The name of the repository.

        Returns:
            list: List of image resources.

        Examples:
            >>> for image in cs.repository.details('library'):
            ...     pprint(image)
        '''
        return self._api.get('repositories/{}'.format(
            self._check('name', name, str))).json()

    def delete(self, name):
        '''
        Removes the specified repository.

        Args:
            name (str): The name of the repository to delete.

        Returns:
            None

        Examples:
            >>> cs.repository.delete('library')
        '''
        self._api.delete('repositories/{}'.format(
            self._check('name', name, str)))