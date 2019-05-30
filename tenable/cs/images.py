'''
images
======

The images methods allow interaction into ContainerSecurity 
image API.

Methods available on ``cs.images``:

.. rst-class:: hide-signature
.. autoclass:: ImageAPI

    .. automethod:: delete
    .. automethod:: details
    .. automethod:: list
'''
from .base import CSEndpoint, CSIterator

class ImageIterator(CSIterator):
    def _get_data(self):
        query = self._query
        query['offset'] = self._offset
        query['limit'] = self._limit
        return self._api.get('images', params=query).json()


class ImageAPI(CSEndpoint):
    def list(self, **kw):
        '''
        Retrieves the list of images stores in ContainerSecurity.

        Args:
            has_malware (bool, optional):
                Limits images to only those that either have or don't have malware.
            image_id (str, optional):
                Limits the reponse to images with the specified image id.
            name (str, optional):
                Limits the response to images with the specified name.
            limit (int, optional): 
                The number of items to return for each page.  The default if
                not specified is 50.
            offset (int, optional):
                The number of records to skip before returning results.  The
                default if not specified is 0.
            os (str, optional):
                Limits the response to images that have the specified base
                operating system.
            repository (str, optional):
                Limits the response to images within the specified repository.
            score_operator (str, optional):
                The operator for the score threshold.  Must be a either ``eq``,
                ``lt``, or ``gt``.
            score_value (int, optional):
                The value for the score threshold. Must be an integer between
                0 and 10.
            tag (str, optional):
                Limits the response to images with the specified tag.

        Returns:
            ImageIterator: an iterator handling the pagination of the response.

        Examples:
            >>> for image in cs.images.list():
            ...     pprint(image)
        '''
        query = dict()
        
        if 'has_malware' in kw:
            query['hasMalware'] = self._check(
                'has_malware', kw['has_malware'], bool)
        if 'image_id' in kw:
            query['dockerImageId'] = self._check(
                'image_id', kw['image_id'], str)
        if 'name' in kw:
            query['name'] = self._check('name', kw['name'], str)
        if 'os' in kw:
            query['os'] = self._check('os', kw['os'], str)
        if 'repository' in kw:
            query['repo'] = self._check('repository', kw['repository'], str)
        if 'score_value' in kw:
            query['score'] = self._check(
                'score_value', kw['score_value'], int)
        if 'score_operator' in kw:
            query['scoreOperator'] = self._check(
                'score_operator', kw['score_operator'], str, 
                choices=['EQ', 'LT', 'GT'],
                case='upper')
        if 'tag' in kw:
            query['tag'] = self._check('tag', kw['tag'], str)

        return ImageIterator(self._api,
            _limit=self._check(
                'limit', kw['limit'], int) if 'limit' in kw else 50,
            _offset=self._check(
                'offset', kw['offset'], int) if 'offset' in kw else 0,
            _pages_total=self._check(
                'pages', kw['pages'], int) if 'pages' in kw else None,
            _query=query)

    def details(self, repository, image, tag):
        '''
        Returns the details of a specified image.

        Args:
            repository (str): 
                The name of the repository that the image resides within.
            image (str):
                The image name.
            tag (str):
                The specific tag of the image to pull.

        Returns:
            dict: The image resource record.

        Examples:
            >>> image = cs.images.details('library', 'apache', 'latest')
        '''

        return self._api.get('images/{}/{}/{}'.format(
            self._check('repository', repository, str),
            self._check('image', image, str),
            self._check('tag', tag, str)
        )).json()

    def delete(self, repository, image, tag):
        '''
        Removes the specified image from ContainerSecurity

        Args:
            repository (str): 
                The name of the repository that the image resides within.
            image (str):
                The image name.
            tag (str):
                The specific tag of the image to pull.

        Returns:
            dict: The image resource record.

        Examples:
            >>> cs.images.delete('library', 'apache', 'latest')
        '''

        return self._api.delete('images/{}/{}/{}'.format(
            self._check('repository', repository, str),
            self._check('image', image, str),
            self._check('tag', tag, str)
        ))