from copy import copy
from datetime import date

from restfly import APIEndpoint, APIIterator, AsyncAPIEndpoint, AsyncAPIIterator

from .models.plugins import (
    Plugin,
    PluginDetails,
    PluginFamily,
    PluginFamilyDetails,
    PluginFamilyListParams,
    PluginFamilyListResponse,
    PluginFamilyNameRequest,
    PluginListParams,
    PluginListResponse,
)


class PluginIterator(APIIterator):
    api: "PluginsAPI"
    page: list[Plugin]
    params: PluginListParams

    def _get_page(self) -> None:
        params = copy(self.params)
        params.page = self.num_pages + 1
        resp = self.api._get_plugins(params=params)
        self.total = resp.total_count
        self.page = resp.data.plugin_details


class AsyncPluginIterator(AsyncAPIIterator):
    api: "AsyncPluginsAPI"
    page: list[Plugin]
    params: PluginListParams

    async def _get_page(self) -> None:
        params = copy(self.params)
        params.page = self.num_pages + 1
        resp = await self.api._get_plugins(params=params)
        self.total = resp.total_count
        self.page = resp.data.plugin_details


class PluginsAPI(APIEndpoint):
    _path = "/plugins"

    def _get_plugins(self, *, params: PluginListParams) -> PluginListResponse:
        return self._get("/plugin", params=params, response_model=PluginListResponse)

    def get(
        self,
        *,
        last_updated: date | str | None = None,
        size: int = 1000,
    ) -> PluginIterator:
        """
        Returns an iterator of the Tenable plugins, sorted by plugin id.

        Args:
            last_updated:
                Only return plugins updated after this date.  Note that VPR updates
                are not taken into account.  To filter on VPR updates, use a date of
                `1970-01-01` and filter on the `vpr.updated` attribute.
            size: The number of plugins to return per page.  Maximum is 10,000.

        Returns:
            Iterator supporting pagination of the plugin data.

        Example:
            >>> for plugin in cloud.vm.plugins.get(last_updated="2025-01-01"):
            ...     print(plugin.id, plugin.name)
        """
        params = PluginListParams.model_validate(
            {"last_updated": last_updated, "size": size}
        )
        return PluginIterator(self._client, api=self, params=params)

    def details(self, plugin_id: int) -> PluginDetails:
        """
        Returns the details for the specified plugin.

        Args:
            plugin_id: The id of the plugin.

        Returns:
            Requested plugin details object.

        Example:
            >>> cloud.vm.plugins.details(19506)
        """
        return self._get(f"/plugin/{int(plugin_id)}", response_model=PluginDetails)

    def families(self, *, all: bool | None = None) -> list[PluginFamily]:
        """
        Returns the list of plugin families.

        Args:
            all:
                Include the plugin families hidden within the UI, such as
                "Port Scanners".

        Returns:
            List of plugin family objects.

        Example:
            >>> cloud.vm.plugins.families(all=True)
        """
        resp = self._get(
            "/families",
            params=PluginFamilyListParams(all=all),
            response_model=PluginFamilyListResponse,
        )
        return resp.families

    def family_details(self, family: int | str) -> PluginFamilyDetails:
        """
        Returns the details and the plugins of the specified plugin family.

        Args:
            family:
                The plugin family id.  If a string is passed, it's used as the plugin
                family name instead.

        Returns:
            Requested plugin family details object.

        Example:
            Retrieve a family by id:

            >>> cloud.vm.plugins.family_details(1)

            Retrieve a family by name:

            >>> cloud.vm.plugins.family_details("Red Hat Local Security Checks")
        """
        if isinstance(family, str):
            return self._post(
                "/families/_byName",
                json=PluginFamilyNameRequest(name=family),
                response_model=PluginFamilyDetails,
            )
        return self._get(f"/families/{int(family)}", response_model=PluginFamilyDetails)


class AsyncPluginsAPI(AsyncAPIEndpoint):
    _path = "/plugins"

    async def _get_plugins(self, *, params: PluginListParams) -> PluginListResponse:
        return await self._get(
            "/plugin", params=params, response_model=PluginListResponse
        )

    async def get(
        self,
        *,
        last_updated: date | str | None = None,
        size: int = 1000,
    ) -> AsyncPluginIterator:
        """
        Returns an iterator of the Tenable plugins, sorted by plugin id.

        Args:
            last_updated:
                Only return plugins updated after this date.  Note that VPR updates
                are not taken into account.  To filter on VPR updates, use a date of
                `1970-01-01` and filter on the `vpr.updated` attribute.
            size: The number of plugins to return per page.  Maximum is 10,000.

        Returns:
            Iterator supporting pagination of the plugin data.

        Example:
            >>> async for plugin in await cloud.vm.plugins.get():
            ...     print(plugin.id, plugin.name)
        """
        params = PluginListParams.model_validate(
            {"last_updated": last_updated, "size": size}
        )
        return AsyncPluginIterator(self._client, api=self, params=params)

    async def details(self, plugin_id: int) -> PluginDetails:
        """
        Returns the details for the specified plugin.

        Args:
            plugin_id: The id of the plugin.

        Returns:
            Requested plugin details object.

        Example:
            >>> await cloud.vm.plugins.details(19506)
        """
        return await self._get(
            f"/plugin/{int(plugin_id)}", response_model=PluginDetails
        )

    async def families(self, *, all: bool | None = None) -> list[PluginFamily]:
        """
        Returns the list of plugin families.

        Args:
            all:
                Include the plugin families hidden within the UI, such as
                "Port Scanners".

        Returns:
            List of plugin family objects.

        Example:
            >>> await cloud.vm.plugins.families(all=True)
        """
        resp = await self._get(
            "/families",
            params=PluginFamilyListParams(all=all),
            response_model=PluginFamilyListResponse,
        )
        return resp.families

    async def family_details(self, family: int | str) -> PluginFamilyDetails:
        """
        Returns the details and the plugins of the specified plugin family.

        Args:
            family:
                The plugin family id.  If a string is passed, it's used as the plugin
                family name instead.

        Returns:
            Requested plugin family details object.

        Example:
            Retrieve a family by id:

            >>> await cloud.vm.plugins.family_details(1)

            Retrieve a family by name:

            >>> await cloud.vm.plugins.family_details("Red Hat Local Security Checks")
        """
        if isinstance(family, str):
            return await self._post(
                "/families/_byName",
                json=PluginFamilyNameRequest(name=family),
                response_model=PluginFamilyDetails,
            )
        return await self._get(
            f"/families/{int(family)}", response_model=PluginFamilyDetails
        )
