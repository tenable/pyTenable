'''
Testing the Agent Exclusion schemas
'''
import re
from datetime import datetime, timedelta

import responses

from tenable.io.v3.vm.agent_exclusions.schema import AgentExclusionSchema

TIMEZONE_URL: str = 'https://cloud.tenable.com'


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
    timezone: str = 'Etc/UTC'
    freq: str = 'WEEKLY'
    interval: int = 1
    byweekday: list = ['MO', 'WE', 'FR']
    payload = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': s_time,
            'endtime': e_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'byweekday': byweekday
            }
        }
    }
    test_resp = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': s_time,
            'endtime': e_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'byweekday': ','.join(byweekday)
            }
        }
    }
    responses.add(
        responses.GET,
        re.compile(f'{TIMEZONE_URL}/scans/timezones'),
        json={
            "timezones": [
                {
                    "name": "Africa/Abidjan",
                    "value": "Africa/Abidjan"
                },
                {
                    "name": "Africa/Accra",
                    "value": "Africa/Accra"
                },
                {
                    "name": "Africa/Addis_Ababa",
                    "value": "Africa/Addis_Ababa"
                },
                {
                    "name": "Etc/UTC",
                    "value": "Etc/UTC"
                }
            ]
        }
    )
    schema = AgentExclusionSchema(
        context={'valid_timezone': api._tz}
    )
    assert test_resp == schema.dump(schema.load(payload))
