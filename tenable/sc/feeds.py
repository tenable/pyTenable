'''
feeds
=====

The following methods allow for interaction into the Tenable.sc 
`Feed <https://docs.tenable.com/sccv/api/Feed.html>`_ API.

Methods available on ``sc.feeds``:

.. rst-class:: hide-signature
.. autoclass:: FeedAPI

    .. automethod:: process
    .. automethod:: status
    .. automethod:: update
'''
from .base import SCEndpoint

class FeedAPI(SCEndpoint):
    def status(self, feed_type=None):
        '''
        Returns the status of either a specific feed type (if requested) or all
        of the feed types if nothing is specifically asked.

        + `SC Feed <https://docs.tenable.com/sccv/api/Feed.html>`_
        + `SC Feed-Type <https://docs.tenable.com/sccv/api/Feed.html#FeedRESTReference-FeedGETType>`_

        Args:
            feed_type (str, optional): 
                The feed type to specifically return.  Valid types are `active`,
                `passive`, `lce`, `sc`, or `all`.

        Returns:
            dict: 
                If no specific feed type is specified, then a dictionary with
                each type listed with a sub-dictionary detailing the status is
                returned.  If a specific feed type is requested, then only the
                status information for that feed type is returned.

        Examples:
            Getting all of the feed types returned:

            >>> status = sc.feed.status()

            Getting the feed status for a specific type (e.g. `active`).

            >>> status = sc.feed.status('active')
        '''
        self._check('feed_type', feed_type, str, choices=[
            'active', 'passive', 'lce', 'sc', 'all'])

        if not feed_type:
            return self._api.get('feed').json()['response']
        else:
            return self._api.get('feed/{}'.format(feed_type)).json()['response']

    def update(self, feed_type=None):
        '''
        Initiates an on-line feed update based on the specified feed_type.  If
        no feed type is specified, then it will default to initiating an update
        for all feed types.

        + `SC Feed Update <https://docs.tenable.com/sccv/api/Feed.html#FeedRESTReference-FeedUpdatePOSTType>`_

        Args:
            feed_type (str, optional);
                The feed type to specifically return.  Valid types are `active`,
                `passive`, `lce`, `sc`, or `all`.

        Returns:
            None: Update successfully requested.
        '''
        self._api.post('feed/{}/update'.format(
            self._check('feed_type', feed_type, str, default='all', choices=[
                'active', 'passive', 'lce', 'sc', 'all'])), json={})

    def process(self, feed_type, fobj):
        '''
        Initiates an off-line feed update based on the specified feed_type using
        the file object passed as the update file.

        + `SC Feed Process <https://docs.tenable.com/sccv/api/Feed.html#FeedRESTReference-FeedUpdatePOSTProcess>`_

        Args:
            feed_type (str);
                The feed type to specifically return.  Valid types are `active`,
                `passive`, `lce`, `sc`, or `all`.
            fobj (FileObject):
                The file object to upload into SecurityCenter and use as the
                update package.

        Returns:
            None: Update successfully requested.

        Examples:
            updating the active plugins:

            >>> with open('sc-plugins-diff.tar.gz', 'rb') as plugfile:
            ...     sc.feed.process('active', plugfile)
        '''
        filename = self._api.files.upload(fobj)

        self._api.post('feed/{}/update'.format(
            self._check('feed_type', feed_type, str, choices=[
                'active', 'passive', 'lce', 'sc'])), 
            json={'filename': filename})
