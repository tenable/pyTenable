'''
Software Update
===============

Methods described in this section relate to the software update API.
These methods can be accessed at ``Nessus.software_update``.

.. rst-class:: hide-signature
.. autoclass:: SoftwareUpdateAPI
    :members:
'''
from typing import Dict, Optional
from typing_extensions import Literal
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint


class SoftwareUpdateAPI(APIEndpoint):
    _path = 'settings/software-update'
    
    def update(self) -> None:
        '''
        Schedules a software update for all components
        
        Example:
            
            >>> nessus.software_update.update()
        '''
        self._get()
    
    def settings(self,
                 update: Literal['all', 'plugins', 'disabled'],
                 custom_host: Optional[str] = None,
                 auto_update_delay: Optional[int] = None
                 ) -> None:
        '''
        Update the software update settings
        
        Args:
            update (str): 
                What components should be updated?  Expected values are
                ``all``, ``plugins``, and ``disabled``.
            custom_host (str, optional):
                URL of the custom plugin feed host
            auto_update_delay (int, optional):
                How often should the plugin feed attempt to update (in hours)
        
        Example:
        
            >>> nessus.software_update.settings(update='all',
            ...                                 auto_update_delay=24
            ...                                 )
        '''
        self._put(json=dict_clean({
            'update': update,
            'custom_host': custom_host,
            'auto_update_delay': auto_update_delay
        }))