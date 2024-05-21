'''
Proxy
=====

Methods described in this section relate to the proxy API.
These methods can be accessed at ``Nessus.proxy``.

.. rst-class:: hide-signature
.. autoclass:: ProxyAPI
    :members:
'''
from typing import List, Dict, Optional
from typing_extensions import Literal
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint


class ProxyAPI(APIEndpoint):
    _path = 'settings/network/proxy'
    
    def edit(self, 
               proxy: Optional[str] = None,
               proxy_auth: Optional[Literal['auto',
                                            'basic',
                                            'digest',
                                            'none',
                                            'ntlm'
                                            ]] = None,
               proxy_password: Optional[str] = None,
               proxy_port: Optional[int] = None,
               proxy_username: Optional[str] = None,
               user_agent: Optional[str] = None
               ) -> None:
        '''
        Updates the proxy settings
        
        Args:
            proxy (str, optional): The proxy host
            proxy_auth (str, optional): The proxy auth method
            proxy_password (str, optional): The auth password
            proxy_port (int, optional): The proxy port
            proxy_username (str, optional): The proxy auth username
            user_agent (str, optional): The proxy user agent.
        
        Example:
        
            >>> nessus.proxy.edit(proxy='proxy.company.com',
            ...                   proxy_auth='none',
            ...                   proxy_port=3128
            ...                   )
        '''
        self._put(json=dict_clean({
            'proxy': proxy,
            'proxy_auth': proxy_auth,
            'proxy_password': proxy_password,
            'proxy_port': proxy_port,
            'proxy_username': proxy_username,
            'user_agent': user_agent
        }))
    
    def details(self) -> Dict:
        '''
        Retrieves the current proxy settings
        
        Returns:
            Dict:
                The current proxy settings 
        
        Example:
            
            >>> nessus.proxy.details()
        '''
        return self._get()