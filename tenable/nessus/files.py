'''
Files
=====

Methods described in this section relate to the files API.
These methods can be accessed at ``Nessus.files``.

.. rst-class:: hide-signature
.. autoclass:: FilesAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from typing import Optional, Callable, Dict
from requests import Response
from io import BytesIO


class FilesAPI(APIEndpoint):
    _path = 'file'
    
    def upload(self, fobj: BytesIO, encrypted: bool = False) -> str:
        '''
        Uploads a file to Tenable Nessus

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
    
    def _download(self, 
                  response: Response, 
                  fobj: Optional[BytesIO] = None,
                  chunk_size: int = 1024,
                  stream_hook: Optional[Callable[[Response, 
                                                  BytesIO, 
                                                  int
                                                  ], BytesIO
                                                 ]] = None,
                  hook_kwargs: Optional[Dict] = None
                  ) -> BytesIO:
        '''
        File download manager for Tenable Nessus
        
        Args:
            response (Response): The Response object to work on
            fobj (BytesIO, optional): 
                The file object to write to. If unspecified, an in-memory
                object will be created and returned
            chunk_size (int, optional):
                The chunk size to use when writing to the file object.  The
                default is unspecified is ``1024`` bytes.
            stream_hook (Callable[Response, BytesIO, int], optional):
                If specified, the output will be passed to the stream hook
                instead of processing ourselves.
            hook_kwargs (Dict, optional):
                Any additional keyword arguments that should be passed on to
                the stream hook.
        
        Returns:
            BytesIO:
                The file object
        '''
        def base_hook(resp: Response, 
                      fobj: BytesIO, 
                      chunk_size: int, 
                      **kwargs
                      ):
            ''' Default stream hook '''
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    fobj.write(chunk)
        
        # Set the default attributes values if nothing was passed to them
        if fobj is None:
            fobj = BytesIO()
        if hook_kwargs is None:
            hook_kwargs = {}
        if stream_hook is None:
            stream_hook = base_hook
        
        # Call the stream hook with the Response object passed to us
        stream_hook(response, fobj, chunk_size, **hook_kwargs)
        
        # seek the file back to the beginning, close the response, and return
        # the file object to the caller
        fobj.seek(0)
        response.close()
        return fobj