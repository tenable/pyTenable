'''
Mail
====

Methods described in this section relate to the mail API.
These methods can be accessed at ``Nessus.mail``.

.. rst-class:: hide-signature
.. autoclass:: MailAPI
    :members:
'''
from typing import Dict, Optional
from typing_extensions import Literal
from tenable.base.endpoint import APIEndpoint
from restfly.utils import dict_clean, dict_merge


class MailAPI(APIEndpoint):
    _path = 'settings/network/mail'
    
    def details(self) -> Dict:
        '''
        Retrieves the Tenable Nessus daemon's mail settings
        
        Returns:
            Dict:
                Dictionary of SMTP settings
                
        Example:
            
            >>> nessus.mail.details()
        '''
        return self._get()
    
    def edit(self, 
             smtp_host: Optional[str] = None,
             smtp_port: Optional[int] = None,
             smtp_enc: Optional[Literal['No Encryption', 
                                        'Use TLS if available',
                                        'Force SSL'
                                        'Force TLS'
                                        ]] = None,
             smtp_from: Optional[str] = None,
             smtp_www_host: Optional[str] = None,
             smtp_user: Optional[str] = None,
             smtp_pass: Optional[str] = None,
             smtp_auth: Optional[Literal['NONE', 
                                         'PLAIN',
                                         'LOGIN',
                                         'NTLM',
                                         'CRAM-MD5'
                                         ]] = None
             ) -> None:
        '''
        Updates the Tenable Nessus daemon's mail settings
        
        Args:
            smtp_host (str, optional): 
                DNS/IP Address of the SMTP server
            smtp_port (int, optional): 
                Port number for the SMTP service
            smtp_enc (str, optional):
                The connection encryption for the SMTP server
            smtp_from (str, optional): 
                Reply email address for email sent by the Tenable Nessus daemon
            smtp_www_host (str, optional):
                The host to use in email links
            smtp_user (str, optional):
                The username to use when authenticating to the SMTP service
            smtp_pass (str, optional):
                The password to use when authenticating to the SMTP service
            smtp_auth (str, optional): 
                The authentication type for the SMTP server
        
        Example:
        
            >>> nessus.mail.edit(smtp_user='new_user',
            ...                  smtp_pass='updated_password',
            ...                  smtp_auth='LOGIN',
            ...                  )
        '''
        current = self.details()
        updated = dict_merge(current, dict_clean({
            'smtp_host': smtp_host,
            'smtp_port': smtp_port,
            'smtp_enc': smtp_enc,
            'smtp_from': smtp_from,
            'smtp_www_host': smtp_www_host,
            'smtp_user': smtp_user,
            'smtp_pass': smtp_pass,
            'smtp_auth': smtp_auth
        }))
        self._put(json=updated)