from tenable.tenable_io.agents import AgentsAPI
from tenable.base import APISession


class TenableIO(APISession):
    URL = 'https://cloud.tenable.com'
    def __init__(self, access_key, secret_key, url=None, retries=None, backoff=None):
        '''
        '''

        self._access_key = access_key
        self._secret_key = secret_key
        APISession.__init__(self, url, retries, backoff)

        # Graft on the API Components
        self.agents = AgentsAPI(self)

    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })