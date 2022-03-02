'''
Tokens
======

Methods described in this section relate to the the tokens API.
These methods can be accessed at ``Nessus.tokens``.

.. rst-class:: hide-signature
.. autoclass:: TokensAPI
    :members:
'''
from io import BytesIO
from typing import List, Dict, Optional, Callable
from typing_extensions import Literal
from requests import Response
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint


class TokensAPI(APIEndpoint):
    _path = 'tokens'
    
    def status(self, token: str) -> Dict:
        '''
        Retrieves the status of the specified token
        
        Args:
            token (str): The token to check the status of
        
        Returns:
            Dict:
                The status response
        
        Example:
            
            >>> nessus.tokens.status('1234567890')
        '''
        return self._get(f'{token}/status')
    
    def download(self, 
                 token: str, 
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
        Downloads the specified token download
        
        Args:
            token (str): The token to download
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
        
        Example:
            
            >>> with open('file.ext', 'wb') as fobj:
            ...     nessus.tokens.download('1234567890', fobj=fobj)
        '''
        resp = self._get(f'{token}/download', stream=True)
        return self._api.files._download(response=resp,
                                         fobj=fobj,
                                         chunk_size=chunk_size,
                                         stream_hook=stream_hook,
                                         hook_kwargs=hook_kwargs
                                         )
        