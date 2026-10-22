from restfly import APIEndpoint, AsyncAPIEndpoint

from ._assets import AssetsAPI, AsyncAssetsAPI
from ._plugins import AsyncPluginsAPI, PluginsAPI
from ._remediation import AsyncRemediationAPI, RemediationAPI


class VMAPIs(APIEndpoint):
    assets: AssetsAPI
    plugins: PluginsAPI
    remediation: RemediationAPI


class AsyncVMAPIs(AsyncAPIEndpoint):
    assets: AsyncAssetsAPI
    plugins: AsyncPluginsAPI
    remediation: AsyncRemediationAPI
