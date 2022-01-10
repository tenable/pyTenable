'''
Test cases the Agent Exclusions APIs schemas
'''
from datetime import datetime, timedelta

import responses

from tenable.io.v3.vm.agent_exclusions.schema import AgentExclusionSchema


@responses.activate
def test_agent_exlusion_schema(api):
    '''
    Test case for Agent Exclusion Schema
    '''
    name: str = 'Test Schema'
    description: str = 'Test Schema with payload'
    enabled: bool = True
    s_time: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    e_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')
    freq: str = 'WEEKLY'
    interval: int = 1
    byweekday: list = ['MO', 'WE', 'FR']

    # Let's create input sample payload for schema
    payload = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': s_time,
            'endtime': e_time,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'byweekday': byweekday
            }
        }
    }

    # Let's create output sample payload for schema
    test_resp = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': s_time,
            'endtime': e_time,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'byweekday': ','.join(byweekday)
            }
        }
    }

    schema = AgentExclusionSchema()
    assert test_resp == schema.dump(schema.load(payload))
