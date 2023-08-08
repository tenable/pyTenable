'''
Files
=====

The following methods allow for interaction into the Tenable Security Center
:sc-api:`File <File.htm>` API.

Methods available on ``sc.files``:

.. rst-class:: hide-signature
.. autoclass:: FileAPI
    :members:
'''
from .base import SCEndpoint

class FileAPI(SCEndpoint):
    def upload(self, fobj):
        '''
        Uploads a file into SecurityCenter and returns the file identifier
        to be used for subsequent calls.

        :sc-api:`file: upload <File.htm#FileRESTReference-/file/upload>`

        Args:
            fobj (FileObj): The file object to upload into SecurityCenter.

        Returns:
            :obj:`str`:
                The filename identifier to use for subsequent calls in
                Tenable Security Center.
        '''
        return self._api.post('file/upload', files={
            'Filedata': fobj}).json()['response']['filename']

    def clear(self, filename):
        '''
        Removes the requested file from Tenable Security Center.

        :sc-api:`file: clear <File.htm#FileRESTReference-/file/clear>`

        Args:
            filename (str): The file identifier associated to the file.

        Returns:
            :obj:`str`:
                The file location on disk that was removed.
        '''
        return self._api.post('file/clear', json={
            'filename': self._check('filename', filename, str)
        }).json()['response']['filename']
