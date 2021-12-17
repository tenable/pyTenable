'''
Files
=====

The following methods allow for interaction into the Tenable.io
:devportal:`file <file>` API endpoints.

Methods available on ``tio.v3.vm.files``:

.. rst-class:: hide-signature
.. autoclass:: FileAPI
    :members:
'''
from typing import BinaryIO

from tenable.base.endpoint import APIEndpoint


class FileAPI(APIEndpoint):

    _path = 'api/v3/file'
    _conv_json = True

    def upload(self, fobj: BinaryIO, encrypted: bool = False) -> str:
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
            >>> with open('scan_targets.txt') as fobj:
            ...     file_id = tio.v3.vm.files.upload(fobj)
        '''

        # We will attempt to discover the name of the file stored within the
        # file object.  If none exists however, we will generate a random
        # uuid string to use instead.
        kw = dict()
        if encrypted:
            kw['data'] = {'no_enc': int(encrypted)}
        kw['files'] = {'Filedata': fobj}

        return self._post('upload', **kw)['fileuploaded']
