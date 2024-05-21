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
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .base import SCEndpoint

class FileAPI(SCEndpoint):
    _path = 'file'
    _box = True

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
        encoder = MultipartEncoder({'Filedata': ('filedata', fobj)})
        return self._post('upload',
                          data=encoder,
                          headers={'Content-Type': encoder.content_type}
                          ).response.filename

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
        return self._post('clear',
                          json={'filename': filename}
                          ).response.filename
