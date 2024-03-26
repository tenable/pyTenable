'''
Files
=====

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`file <file>` API endpoints.

Methods available on ``tio.files``:

.. rst-class:: hide-signature
.. autoclass:: FileAPI
    :members:
'''
from typing import BinaryIO
from .base import TIOEndpoint
import uuid

class FileAPI(TIOEndpoint):

    def upload(self, fobj: BinaryIO, encrypted: bool = False):
        '''
        Uploads a file into Tenable Vulnerability Management.

        :devportal:`file: upload <file-upload>`

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Tenable Vulnerability Management.
            encrypted (bool, optional):
                If the file is encrypted, set the flag to True.

        Returns:
            :obj:`str`:
                The fileuploaded attribute

        Examples:
            >>> with open('file.txt') as fobj:
            ...     file_id = tio.files.upload(fobj)
        '''

        # We will attempt to discover the name of the file stored within the
        # file object.  If none exists however, we will generate a random
        # uuid string to use instead.
        params = dict()
        if encrypted:
            params['no_enc'] = int(encrypted)
        kw = {'files': {'Filedata': fobj}}

        return self._api.post('file/upload', **kw, params=params).json()['fileuploaded']
