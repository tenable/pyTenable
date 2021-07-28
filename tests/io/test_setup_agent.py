import uuid

from requests import HTTPError


class AgentSetup():
    '''
    This class is to setup agent on environment for testcases
    '''

    def setup_agent(self, api_link):
        '''
        setup fake agent
        '''
        linking_key = api_link.scanners.linking_key()

        agent_uuid = str(uuid.uuid4())
        payload = {
            'agent_uuid': agent_uuid,
            'distro': 'win-x86-64',
            'key': linking_key,
            'name': agent_uuid,
            'platform': 'WINDOWS',
            'ips': {
                "v4": ["0.0.0.0"]
            },
            'ip': "0.0.0.0"
        }

        try:
            response = api_link.post(
                'remote/agent',
                json=payload,
                headers={'ms-agent': 'token={token}'.format(token=linking_key)}).json()['token']
        except HTTPError:
            raise

        return response

    def teardown_agent(self, api_link, token):
        '''
        remove fake agent
        '''
        try:
            api_link.delete('remote/agent', headers={'MS-Agent': 'token={token}'.format(
                token=token)})
        except HTTPError:
            raise
