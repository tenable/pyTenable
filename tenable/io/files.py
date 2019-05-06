'''
files
=====

The following methods allow for interaction into the Tenable.io
:devportal:`file <file>` API endpoints.

Methods available on ``tio.files``:

.. rst-class:: hide-signature
.. autoclass:: FileAPI

    .. automethod:: upload
'''
from .base import TIOEndpoint
import uuid

class FileAPI(TIOEndpoint):
    def upload(self, fobj, encrypted=False):
        '''
        Uploads a file into Tenable.io.

        :devportal:`file: upload <file-upload>`

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Tenable.io.
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
        kw = dict()
        if encrypted:
            kw['data'] = {'no_enc': int(encrypted)}
        kw['files'] = {'Filedata': fobj}

        return self._api.post('file/upload', **kw).json()['fileuploaded']