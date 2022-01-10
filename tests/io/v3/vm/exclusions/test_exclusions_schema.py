'''
Test cases the Exclusions APIs schemas
'''
from datetime import datetime, timedelta

import responses

from tenable.io.v3.vm.exclusions.schema import ExclusionSchema


@responses.activate
def test_exlusion_schema(api):
    '''
    Test case for Exclusion Schema
    '''
    name: str = 'Test Schema'
    members: list = ['127.0.0.1']
    description: str = 'Test Schema with payload'
    network_id: str = '00000000-0000-0000-0000-000000000000'
    enabled: bool = True
    s_time: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    e_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%dT%H:%M:%SZ')
    freq: str = 'WEEKLY'
    interval: int = 1
    byweekday: list = ['MO', 'WE', 'FR']

    # Let's create sample input payload
    input_payload = {
        'name': name,
        'members': members,
        'description': description,
        'network_id': network_id,
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

    # Let's create sample output payload
    output_payload = {
        'name': name,
        'members': ''.join(members),
        'description': description,
        'network_id': network_id,
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

    schema = ExclusionSchema()
    assert output_payload == schema.dump(schema.load(input_payload))
