'''
Plugin Rules
============

Methods described in this section relate to the plugin rules API.
These methods can be accessed at ``Nessus.plugin_rules``.

.. rst-class:: hide-signature
.. autoclass:: PluginRulesAPI
    :members:
'''
from typing import List, Dict, Optional
from typing_extensions import Literal
from restfly.utils import dict_clean, dict_merge
from tenable.base.endpoint import APIEndpoint
from .iterators.plugins import PluginIterator


class PluginRulesAPI(APIEndpoint):
    _path = 'plugin-rules'

    def create(self, 
               plugin_id: int,
               type: Literal['recast_critical',
                             'recast_high',
                             'recast_medium',
                             'recast_low',
                             'recast_info',
                             'exclude'
                             ],
               host: Optional[str] = None,
               date: Optional[int] = None
               ) -> None:
        '''
        Creates a new plugin rule
        
        Args:
            plugin_id (int): The plugin id to modify
            type: (str): The type of modification to perform
            host (str, optional): The host to apply this rule to
            date (int, optional): The unix date for this rule to expire
        
        Example:
        
            >>> nessus.plugin_rules.create(
            ...     plugin_id=19506,
            ...     type='exclude',
            ...     host='192.168.0.1',
            ...     date=1645164000
            ... )
        '''
        self._post(json={
            'plugin_id': str(plugin_id),
            'type': type,
            'host': host if host else '',
            'date': date
        })

    def delete(self, rule_id: int) -> None:
        '''
        Deletes a plugin rule
        
        Args:
            rule_id (int): The rule to delete
        
        Example:
            
            >>> nessus.plugin_rules.delete(1)
        '''
        self._delete(f'{rule_id}')

    def delete_many(self, rule_ids: List[int]) -> None:
        '''
        Deletes multiple plugin rules
        
        Args:
            rule_ids (list[int]): The rules to delete
        
        Example:
        
            >>> nessus.plugin_rules.delete_many([1, 2, 3])
        '''
        self._delete(json={'ids': rule_ids})

    def edit(self,
             rule_id: int,
             plugin_id: Optional[int] = None,
             type: Optional[Literal['recast_critical',
                                    'recast_high',
                                    'recast_medium',
                                    'recast_low',
                                    'recast_info',
                                    'exclude'
                                    ]] = None,
             host: Optional[str] = None,
             date: Optional[int] = None
             ) -> None:
        '''
        Creates a new plugin rule
        
        Args:
            rule_id (int): The rule to modify
            plugin_id (int, optional): The plugin id to modify
            type: (str, optional): The type of modification to perform
            host (str, optional): The host to apply this rule to
            date (int, optional): The unix date for this rule to expire
        
        Example:
        
            >>> nessus.plugin_rules.edit(1, date=1645164000)
        '''
        rule = self.details(1)
        payload = dict_merge(rule, dict_clean({
            'plugin_id': str(plugin_id),
            'type': type,
            'host': host,
            'date': date
        }))
        return self._put(f'{rule_id}', json=payload)

    def list(self) -> List[Dict]:
        '''
        Lists the plugin rules
        
        Return:
            List[Dict]:
                List of plugin rule objects
        
        Example:
            
            >>> for rule in nessus.plugin_rules.list():
            ...     print(rule)
        '''
        return self._get()['plugin_rules']

    def details(self, rule_id: int) -> Dict:
        '''
        Returns the details of a given plugin rule
        
        Args:
            rule_id (int): The plugin rule id
        
        Returns:
            Dict:
                The plugin rule object requested
            
        Example:
            
            >>> nessus.plugin_rules.details(1)
        '''
        return self._get(f'{rule_id}')
