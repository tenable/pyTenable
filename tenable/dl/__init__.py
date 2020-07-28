'''
Product Downloads
=================

.. autoclass:: Downloads
    :members:
'''
from tenable.base.platform import APIPlatform
from box import BoxList
from io import BytesIO
import os, warnings


class Downloads(APIPlatform):
    '''
    The Downloads object is the primary interaction point for users to
    interface with Downloads API via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        api_token (str, optional):
            The user's API access key for Tenable.io  If an access key isn't
            specified, then the library will attempt to read the environment
            variable ``TDL_API_TOKEN`` to acquire the key.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``5``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        vendor (str, optional):
            The vendor name for the User-Agent string.
        product (str, optional):
            The product name for the User-Agent string.
        build (str, optional):
            The version or build identifier for the User-Agent string.
        timeout (int, optional):
            The connection timeout parameter informing the library how long to
            wait in seconds for a stalled response before terminating the
            connection.  If unspecified, the default is 120 seconds.

    Examples:
        Basic Example:

        >>> from tenable.dl import Downloads
        >>> dl = Downloads(api_token='API_TOKEN')

        Example with proper identification:

        >>> dl = Downloads('API_TOKEN',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')

        Example with proper identification leveraging environment variables for
        access and secret keys:

        >>> dl = Downloads(
        >>>     vendor='Company Name', product='Widget', build='1.0.0')
    '''
    _base_path = '/v1'
    _env_base = 'TDL'
    _address = 'www.tenable.com'
    _base_path = 'downloads/api/v2'

    def __init__(self, api_token=None, **kwargs):
        if not api_token:
            api_token = os.getenv('{}_API_TOKEN'.format(self._env_base))
        kwargs['api_token'] = api_token
        super(Downloads, self).__init__(**kwargs)

    def _authenticate(self, **kwargs):
        '''
        Authentication method for Downloads API
        '''
        if not kwargs.get('api_token'):
            warnings.warn('Starting an unauthenticated session')
            self._log.warning('Starting an unauthenticated session.')
        else:
            self._session.headers.update({
                'Authorization': 'Bearer {token}'.format(
                    token=kwargs.get('api_token')
                )
            })

    def list(self):
        '''
        Lists the available content pages.

        :devportal:`API Endpoint Documentation <get_pages>`

        Returns:
            :obj:`list`:
                The list of page resources.

        Examples:
            >>> pages = dl.list()
            >>> for page in pages:
            ...     pprint(page)
        '''
        return self.get('pages', box=BoxList)

    def details(self, page):
        '''
        Retrieves the specific download items for the page requested.

        :devportal:`API Endpoint Documentation <get_pages-slug>`

        Args:
            page (str): The name of the page to request.

        Returns:
            :obj:`dict`:
                The page details.

        Examples:
            >>> details = dl.details('nessus')
        '''
        return self.get('pages/{}'.format(page))

    def download(self, page, package, fobj=None):
        '''
        Retreives the requested package and downloads the file.

        :devportal:`API Endpoint Documentation <get_pages-slug-files-file>`

        Args:
            page (str): The name of the page
            package (str): The package filename
            fobj (FileObject, optional):
                The file-like object to write the package to.  If nothing is
                specified, then a BytesIO object will be used.

        Returns:
            :obj:`FileObject`:
                The binary package

        Examples:
            >>> with open('Nessus-latest.x86_64.rpm', 'wb') as pkgfile:
            ...     dl.download('nessus',
            ...         'Nessus-8.3.0-es7.x86_64.rpm', pkgfile)
        '''
        if not fobj:
            fobj = BytesIO()

        resp = self.get(
            'pages/{}/files/{}'.format(page, package), stream=True, box=False)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()

        # Lastly lets return the FileObject to the caller.
        return fobj