from tenable.tenable_io.agent_config import AgentConfigAPI
from tenable.tenable_io.agent_exclusions import AgentExclusionsAPI
from tenable.base import APISession

class TenableIO(APISession):
    URL = 'https://cloud.tenable.com'
    def __init__(access_key, secret_key, url=None, retries=None, backoff=None):
        '''
        '''
        self._access_key = access_key
        self._secret_key = secret_key
        APISession.__init__(self, url, retries, backoff)

        # Graft on the API Components
        self.agent_config = AgentConfigAPI(self)
        self.agent_exclusions = AgentExclusionsAPI(self)

    def build_session(self):
        '''
        '''
        APISession.build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })