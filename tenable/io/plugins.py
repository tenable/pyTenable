from tenable.tenable_io.base import TIOEndpoint

class PluginsAPI(TIOEndpoint):
    def families(self):
        '''
        `plugins: families <https://cloud.tenable.com/api#/resources/plugins/families>`_

        Returns:
            list: List of plugin familiy resource records.
        '''
        return self._api.get('plugins/families').json()['families']

    def family_details(self, id):
        '''
        `plugins: family-details <https://cloud.tenable.com/api#/resources/plugins/family-details>`_

        Args:
            id (int): The plugin family unique identifier.

        Returns:
            dict: 
                Returns a dictionary stating the id, name, and plugins that are
                housed within the plugin family.
        '''
        return self._api.get('plugins/families/{}'.format(
                self._check('id', id, int)
        )).json()

    def plugin_details(self, id):
            '''
            `plugins: plugin-details <https://cloud.tenable.com/api#/resources/plugins/plugin-details>`_

            Args:
                id (int): The plugin id for the requested plugin.

            Returns:
                dict:
                    A dictionary stating the id, name, family, and any other
                    relevent attributes associated to the plugin.
            '''
            return self._api.get('plugins/plugin/{}'.format(
                self._check('id', id, int))).json()
