from restfly import APIEndpoint, AsyncAPIEndpoint

from ._activity_log import ActivityLogAPI, AsyncActivityLogAPI
from .access_control import AccessControlAPI, AsyncAccessControlAPI


class PlatformAPIs(APIEndpoint):
    access_control: AccessControlAPI
    activity_log: ActivityLogAPI


class AsyncPlatformAPIs(AsyncAPIEndpoint):
    access_control: AsyncAccessControlAPI
    activity_log: AsyncActivityLogAPI
