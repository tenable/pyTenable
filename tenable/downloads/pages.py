'''
pages
=====

The following methods allow for interaction into the Downloads Pages API

Methods available on ``downloads.pages``:

.. rst-class:: hide-signature
.. autoclass:: PageAPI

    .. automethod:: details
    .. automethod:: download
    .. automethod:: list
'''
from tenable.base import APIEndpoint
from io import BytesIO

class PageAPI(APIEndpoint):
    def list(self):
        '''
        Lists the available content pages.

        Returns:
            list: The list of page resources.

        Examples:
            >>> pages = downloads.pages.list()
            >>> for page in pages:
            ...     pprint(page)
        '''
        return self._api.get('pages').json()

    def details(self, page):
        '''
        Retrieves the specific download items for the page requested.

        Args:
            page (str): The name of the page to request.

        Returns:
            dict: The page details.

        Examples:
            >>> details = downloads.pages.details('nessus')
        '''
        return self._api.get('pages/{}'.format(
            self._check('page', page, str))).json()

    def download(self, page, package, fobj=None):
        '''
        Retreives the requested package and downloads the file.

        Args:
            page (str): The name of the page
            package (str): The package filename
            fobj (FileObject, optional):
                The file-like object to write the package to.  If nothing is
                specified, then a BytesIO object will be used.

        Returns:
            FileObject

        Examples:
            >>> with open('Nessus-latest.x86_64.rpm', 'wb') as pkgfile:
            ...     downloads.pages.download('nessus',
            ...         'Nessus-8.3.0-es7.x86_64.rpm', pkgfile)
        '''
        if not fobj:
            fobj = BytesIO()

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._api.get('pages/{}/files/{}'.format(
            self._check('page', page, str),
            self._check('package', package, str)), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()

        # Lastly lets return the FileObject to the caller.
        return fobj