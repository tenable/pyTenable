'''
.. autoclass:: Downloads
.. automodule:: tenable.downloads.pages

Raw HTTP Calls
==============

Even though the ``Downloads`` object pythonizes the downloads API for
you, there may still bee the occasional need to make raw HTTP calls to the
Downloads portal API.  The methods listed below aren't run through any
naturalization by the library aside from the response code checking.  These
methods effectively route directly into the requests session.  The responses
will be Response objects from the ``requests`` library.  In all cases, the path
is appended to the base ``url`` parameter that the ``Downloads`` object was
instantiated with.

Example:

.. code-block:: python

   resp = downloads.get('pages')

.. py:module:: tenable.downloads
.. rst-class:: hide-signature
.. autoclass:: Downloads

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
from tenable.base import APISession
from .pages import PageAPI

class Downloads(APISession):
    '''
    The Downloads object is the primary interaction point for users to
    interface with downloads API via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        api_key (str, optional):
            The user's API access key for the Downloads API.
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://www.tenable.com/downloads/api/v2``
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        ua_identity (str, optional):
            An application identifier to be added into the User-Agent string
            for the purposes of application identification.

    Examples:
        >>> from tenable.downloads import Downloads
        >>> downloads = Downloads({DL_API_KEY})
    '''
    _url = 'https://www.tenable.com/downloads/api/v2'

    def __init__(self, api_key, url=None, retries=None,
                 backoff=None, ua_identity=None, session=None, proxies=None,
                 vendor=None, product=None, build=None):
        self._api_key = api_key
        super(Downloads, self).__init__(url,
            retries=retries,
            backoff=backoff,
            ua_identity=ua_identity,
            session=session,
            proxies=proxies,
            vendor=vendor,
            product=product,
            build=build)

    def _build_session(self, session):
        '''
        Build the session and add the API Keys into the session
        '''
        super(Downloads, self)._build_session(session)
        self._session.trust_env = False
        self._session.headers.update({
            'Authorization': 'Bearer {}'.format(self._api_key)})

    @property
    def pages(self):
        return PageAPI(self)