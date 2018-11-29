'''
files
=====

The following methods allow for interaction into the Tenable.sc 
`File <https://docs.tenable.com/sccv/api/File.html>`_ API.

Methods available on ``sc.feeds``:

.. rst-class:: hide-signature
.. autoclass:: FileAPI

    .. automethod:: clear
    .. automethod:: upload
'''
from .base import SCEndpoint

class FileAPI(SCEndpoint):
    def upload(self, fobj):
        '''
        Uploads a file into SecurityCenter and returns the file identifier
        to be used for subsiquent calls.

        Args:
            fobj (FileObj): The file object to upload into SecurityCenter.

        Returns:
            str: 
                The filename identifier to use for subsiquent calls in 
                Tenable.sc.
        '''
        return self.post('file/upload', files={
            'Filedata': fileobj}).json()['response']['filename']

    def clear(self, filename):
        '''
        Removes the requested file from Tenable.sc.

        Args:
            filename (str): The file identifier associated to the file.

        Returns:
            str: The file location on disk that was removed.
        '''
        return self.post('file/clear', json={
            'filename': self._check('filename', filename, str)
        }).json()['response']['filename']