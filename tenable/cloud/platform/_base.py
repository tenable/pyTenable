from restfly import APIEndpoint, AsyncAPIEndpoint

from ._activity_log import ActivityLogAPI, AsyncActivityLogAPI
from ._agents import AgentsAPI, AsyncAgentsAPI
from ._connectors import AsyncConnectorsAPI, ConnectorsAPI
from ._exclusions import AsyncExclusionsAPI, ExclusionsAPI
from ._files import AsyncFilesAPI, FilesAPI
from ._filters import AsyncFiltersAPI, FiltersAPI
from ._networks import AsyncNetworksAPI, NetworksAPI
from ._permissions import AsyncPermissionsAPI, PermissionsAPI
from ._scanners import AsyncScannersAPI, ScannersAPI
from ._server import AsyncServerAPI, ServerAPI
from .access_control import AccessControlAPI, AsyncAccessControlAPI


class PlatformAPIs(APIEndpoint):
    access_control: AccessControlAPI
    activity_log: ActivityLogAPI
    agents: AgentsAPI
    connectors: ConnectorsAPI
    exclusions: ExclusionsAPI
    files: FilesAPI
    filters: FiltersAPI
    networks: NetworksAPI
    permissions: PermissionsAPI
    scanners: ScannersAPI
    server: ServerAPI


class AsyncPlatformAPIs(AsyncAPIEndpoint):
    access_control: AsyncAccessControlAPI
    activity_log: AsyncActivityLogAPI
    agents: AsyncAgentsAPI
    connectors: AsyncConnectorsAPI
    exclusions: AsyncExclusionsAPI
    files: AsyncFilesAPI
    filters: AsyncFiltersAPI
    networks: AsyncNetworksAPI
    permissions: AsyncPermissionsAPI
    scanners: AsyncScannersAPI
    server: AsyncServerAPI
