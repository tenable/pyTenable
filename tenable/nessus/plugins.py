'''
Plugins
=======

Methods described in this section relate to the plugins API.
These methods can be accessed at ``Nessus.plugins``.

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI
    :members:
'''
from typing import List, Dict
from tenable.base.endpoint import APIEndpoint
from .iterators.plugins import PluginIterator


class PluginsAPI(APIEndpoint):
    _path = 'plugins'

    def families(self) -> List[Dict]:
        '''
        Returns the list of plugin families.

        Example:

            >>> families = nessus.plugins.families()
        '''
        return self._get('families')['families']

    def family_details(self, family_id: int) -> Dict:
        '''
        Returns the details for a given plugin family.

        Args:
            family_id (int): The id of the family to return

        Example:

            >>> family = nessus.plugins.family_details(fam_id)
        '''
        return self._get(f'families/{family_id}')

    def plugin_details(self, plugin_id: int) -> Dict:
        '''
        Returns the details for a given plugin id.

        Args:
            plugin_id (int): The id of the plugin to return

        Example:

            >>> plugin = nessus.plugins.plugin_details(19506)
        '''
        return self._get(f'plugin/{plugin_id}')

    def list(self):
        '''
        Returns an iterable to walk through each plugin.

        Example:

            >>> for plugin in nessus.plugins.list():
            ...     print(plugin)
        '''
        return PluginIterator(self._api)
