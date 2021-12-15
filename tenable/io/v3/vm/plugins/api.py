"""
Plugins
=======

The following methods allow for interaction into the Tenable.io
:devportal:`plugins <plugins>` API endpoints.

Methods available on ``tio.v3.vm.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginsAPI
    :members:
"""
from typing import Dict, List

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class PluginsAPI(ExploreBaseEndpoint):
    """
    This will contain all methods related to plugins
    """
    _path = "api/v3/plugins"
    _conv_json = True

    def families(self) -> List:
        """
        List the available plugin families.

        :devportal:`plugins: families <plugins-families>`

        Returns:
            :obj:`list`:
                List of plugin family resource records.

        Examples:
            >>> for family in tio.plugins.families():
            ...     pprint(family)
        """
        return NotImplementedError(
            "Search and Filter functionality will be updated later."
        )

    def family_details(self, family_id: int) -> Dict:
        """
        Retrieve the details for a specific plugin family.

        :devportal:`plugins: family-details plugins-family-details>`

        Args:
            family_id:
                The plugin family unique identifier.

        Returns:
            :obj:`dict`:
                Returns a dictionary stating the id, name, and plugins that are
                housed within the plugin family.

        Examples:
            >>> family = tio.v3.vm.plugins.family_details(1)
        """
        return self._get(f"families/{family_id}")

    def plugin_details(self, plugin_id: int) -> Dict:
        """
        Retrieve the details for a specific plugin.

        :devportal:`plugins: plugin-details <plugins-plugin-details>`

        Args:
            plugin_id (int): The plugin id for the requested plugin.

        Returns:
            :obj:`dict`:
                A dictionary stating the id, name, family, and any other
                relevant attributes associated to the plugin.

        Examples:
            >>> plugin = tio.v3.vm.plugins.plugin_details(19506)
            >>> pprint(plugin)
        """
        return self._get(f"plugin/{plugin_id}")

    def search(self):
        return NotImplemented(
            "Search and Filter functionality will be updated later."
        )
