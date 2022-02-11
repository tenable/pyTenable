'''
Files
=====

Methods described in this section relate to the the files API.
These methods can be accessed at ``Nessus.files``.

.. rst-class:: hide-signature
.. autoclass:: FilesAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from io import BytesIO


class FilesAPI(APIEndpoint):
    _path = 'file'
    
    def upload(self, fobj: BytesIO, encrypted: bool = False) -> str:
        '''
        Uploads a file to Nessus

        Args:
            fobj (BytesIO): The file object to upload
            encrypted (bool, optional): Is the file encrypted?

        Returns:
            str: File identifier to be used in future calls.

        Example:

            >>> with open('example.txt', 'rb') as fobj:
            ...     fn = nessus.files.upload(fobj)
        '''
        return self._post('upload',
                          data={'no_enc': int(encrypted)},
                          files={'Filedata': fobj}
                          )['fileuploaded']