from restfly import APIEndpoint, AsyncAPIEndpoint

from .access_control import AccessControlAPI, AsyncAccessControlAPI


class PlatformAPIs(APIEndpoint):
    access_control: AccessControlAPI


class AsyncPlatformAPIs(AsyncAPIEndpoint):
    access_control: AsyncAccessControlAPI
