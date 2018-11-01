'''
plugins
=======

The following methods allow for interaction into the Tenable.io 
`plugins <https://cloud.tenable.com/api#/resources/plugins>`_ API endpoints.

Methods available on ``tio.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI

    .. automethod:: families
    .. automethod:: family_details
    .. automethod:: plugin_details
'''
from .base import TIOEndpoint

class PluginsAPI(TIOEndpoint):
    def families(self):
        '''
        List the available plugin families.

        `plugins: families <https://cloud.tenable.com/api#/resources/plugins/families>`_

        Returns:
            list: List of plugin familiy resource records.

        Examples:
            >>> for family in tio.plugins.families():
            ...     pprint(family)
        '''
        return self._api.get('plugins/families').json()['families']

    def family_details(self, id):
        '''
        Retrieve the details for a specific plugin family.

        `plugins: family-details <https://cloud.tenable.com/api#/resources/plugins/family-details>`_

        Args:
            id (int): The plugin family unique identifier.

        Returns:
            dict: 
                Returns a dictionary stating the id, name, and plugins that are
                housed within the plugin family.

        Examples:
            >>> family = tio.plugins.family_details(1)
        '''
        return self._api.get('plugins/families/{}'.format(
                self._check('id', id, int)
        )).json()

    def plugin_details(self, id):
            '''
            Retrieve the details for a specific plugin.

            `plugins: plugin-details <https://cloud.tenable.com/api#/resources/plugins/plugin-details>`_

            Args:
                id (int): The plugin id for the requested plugin.

            Returns:
                dict:
                    A dictionary stating the id, name, family, and any other
                    relevant attributes associated to the plugin.

            Examples:
                >>> plugin = tio.plugins.plugin_details(19506)
                >>> pprint(plugin)
            '''
            return self._api.get('plugins/plugin/{}'.format(
                self._check('id', id, int))).json()
