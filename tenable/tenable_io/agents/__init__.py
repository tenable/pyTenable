from .config import AgentConfigAPI
from .exclusions import AgentExclusionsAPI
from .groups import AgentGroupsAPI
from tenable.base import APIEndpoint

class AgentsAPI(APIEndpoint):
    def __init__(self, api):
        APIEndpoint.__init__(self, api)

        # Now lets graft on Agent Endpoints
        self.config = AgentConfigAPI(api)
        self.exclusions = AgentExclusionsAPI(api)
        #self.groups = AgentGroupsAPI(api)