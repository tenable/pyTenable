from restfly import APIEndpoint, AsyncAPIEndpoint

from ._assets import AssetsAPI, AsyncAssetsAPI
from ._plugins import AsyncPluginsAPI, PluginsAPI


class VMAPIs(APIEndpoint):
    assets: AssetsAPI
    plugins: PluginsAPI


class AsyncVMAPIs(AsyncAPIEndpoint):
    assets: AsyncAssetsAPI
    plugins: AsyncPluginsAPI
