from restfly import APIEndpoint, AsyncAPIEndpoint

from ._assets import AssetsAPI, AsyncAssetsAPI


class VMAPIs(APIEndpoint):
    assets: AssetsAPI


class AsyncVMAPIs(AsyncAPIEndpoint):
    assets: AsyncAssetsAPI
