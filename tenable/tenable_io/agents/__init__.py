from .config import AgentConfigAPI
from .exclusions import AgentExclusionsAPI
from .groups import AgentGroupsAPI
from tenable.base import APIEndpoint

class AgentsAPI(APIEndpoint):
    def __init__(self, parent):
        APIEndpoint.__init__(self, parent)

        # Now lets graft on Agent Endpoints
        self.config = AgentConfigAPI(parent)
        self.exclusions = AgentExclusionsAPI(parent)
        #self.groups = AgentGroupsAPI(parent)