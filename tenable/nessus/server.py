'''
Server
======

Methods described in this section relate to the server API.
These methods can be accessed at ``Nessus.server``.

.. rst-class:: hide-signature
.. autoclass:: ServerAPI
    :members:
'''
from typing import List, Dict, Optional
from typing_extensions import Literal
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint


class ServerAPI(APIEndpoint):
    _path = 'server'
    
    def properties(self) -> Dict:
        '''
        Retrieves the Tenable Nessus server properties.
        
        Returns:
            Dict:
                The various properties for this server.
        
        Example:
            
            >>> nessus.server.properties()
        '''
        return self._get('properties')
    
    def status(self) -> Dict:
        '''
        Retrieves the current server status.
        
        Returns:
            Dict:
                The server status
        
        Example:
            
            >>> nessus.server.status()
        '''
        return self._get('status')
    
    def restart(self,
                reason: Optional[str] = None,
                soft: Optional[bool] = None,
                unlink: Optional[bool] = None,
                when_idle: Optional[bool] = None
                ) -> None:
        '''
        Initiates a restart of this Tenable Nessus service
        
        Args:
            reason (str, optional):
                What is the reason for the restart to occur?
            soft (bool, optional):
                Should we only restart the web service (soft restart) or
                restart the whole Tenable Nessus service?
            unlink (bool, optional):
                Should the scanner be unlinked from it's upstream controller
                before restarting?
            when_idle (bool, optional):
                Should the scanner restart once there are no running scans?
        
        Example:
            
            >>> nessus.server.restart(reason='Time to restart',
            ...                       when_idle=True,
            ...                       soft=True
            ...                       )
        '''
        if soft is not None:
            soft = str(soft).lower()
        if unlink is not None:
            unlink = str(unlink).lower()
        if when_idle is not None:
            when_idle = str(when_idle).lower()
        return self._get('restart', params=dict_clean({
            'reason': reason,
            'soft': soft,
            'unlink': unlink,
            'when_idle': when_idle
        }))