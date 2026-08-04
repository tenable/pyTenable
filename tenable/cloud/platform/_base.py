from restfly import APIEndpoint, AsyncAPIEndpoint

from ._activity_log import ActivityLogAPI, AsyncActivityLogAPI
from ._agents import AgentsAPI, AsyncAgentsAPI
from ._connectors import AsyncConnectorsAPI, ConnectorsAPI
from ._exclusions import AsyncExclusionsAPI, ExclusionsAPI
from ._filters import AsyncFiltersAPI, FiltersAPI
from .access_control import AccessControlAPI, AsyncAccessControlAPI


class PlatformAPIs(APIEndpoint):
    access_control: AccessControlAPI
    activity_log: ActivityLogAPI
    agents: AgentsAPI
    connectors: ConnectorsAPI
    exclusions: ExclusionsAPI
    filters: FiltersAPI


class AsyncPlatformAPIs(AsyncAPIEndpoint):
    access_control: AsyncAccessControlAPI
    activity_log: AsyncActivityLogAPI
    agents: AsyncAgentsAPI
    connectors: AsyncConnectorsAPI
    exclusions: AsyncExclusionsAPI
    filters: AsyncFiltersAPI
