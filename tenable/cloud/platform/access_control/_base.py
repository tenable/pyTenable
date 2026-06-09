from restfly import APIEndpoint, AsyncAPIEndpoint

from ._api import AccessControlApiAPI, AsyncAccessControlApiAPI
from ._groups import AccessControlGroupAPI, AsyncAccessControlGroupAPI
from ._permissions import AccessControlPermissionsAPI, AsyncAccessControlPermissionsAPI

# from ._users import AccessControlUserAPI, AsyncAccessControlUserAPI


class AccessControlAPI(APIEndpoint):
    #    users: AccessControlUserAPI
    groups: AccessControlGroupAPI
    permissions: AccessControlPermissionsAPI
    api: AccessControlApiAPI


class AsyncAccessControlAPI(AsyncAPIEndpoint):
    #    users: AsyncAccessControlUserAPI
    groups: AsyncAccessControlGroupAPI
    permissions: AsyncAccessControlPermissionsAPI
    api: AsyncAccessControlApiAPI
