'''
Test cases the Exclusions APIs schemas
'''
from datetime import datetime, timedelta

import pytest
import responses

from tenable.io.v3.vm.exclusions.schema import ExclusionSchema

TIMEZONE_URL: str = 'https://cloud.tenable.com/scans/timezones'


@responses.activate
def test_exclusion_schema_with_weekly_freq(api):
    '''
    Test case for Exclusion Schema for weekly freq
    '''
    name: str = 'Test Schema'
    members: list = ['127.0.0.1']
    description: str = 'Test Schema with payload'
    network_id: str = '00000000-0000-0000-0000-000000000000'
    enabled: bool = True
    s_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    e_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    freq: str = 'WEEKLY'
    interval: int = 1

    # Let's register the response for timezone API
    responses.add(
        responses.GET,
        TIMEZONE_URL,
        json={
            'timezones': [
                {
                    'name': 'Africa/Addis_Ababa',
                    'value': 'Africa/Addis_Ababa'
                },
                {
                    'name': 'Etc/UTC',
                    'value': 'Etc/UTC'
                }
            ]
        }
    )
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
                'interval': interval
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
                'byweekday': 'SU,MO,TU,WE,TH,FR,SA'
            }
        }
    }

    schema = ExclusionSchema(
        context={'timezones': api._tz}
    )
    assert output_payload == schema.dump(schema.load(input_payload))


@responses.activate
def test_exclusion_schema_with_monthly_freq(api):
    '''
    Test case for Exclusion Schema for monthly freq
    '''
    name: str = 'Test Schema'
    members: list = ['127.0.0.1']
    description: str = 'Test Schema with payload'
    network_id: str = '00000000-0000-0000-0000-000000000000'
    enabled: bool = True
    s_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    e_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    freq: str = 'MONTHLY'
    interval: int = 1

    # Let's register the response for timezone API
    responses.add(
        responses.GET,
        TIMEZONE_URL,
        json={
            'timezones': [
                {
                    'name': 'Africa/Addis_Ababa',
                    'value': 'Africa/Addis_Ababa'
                },
                {
                    'name': 'Etc/UTC',
                    'value': 'Etc/UTC'
                }
            ]
        }
    )
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
                'interval': interval
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
                'bymonthday': datetime.today().day
            }
        }
    }

    schema = ExclusionSchema(
        context={'timezones': api._tz}
    )
    assert output_payload == schema.dump(schema.load(input_payload))


@responses.activate
def test_exclusion_schema_with_onetime_freq(api):
    '''
    Test case for Exclusion Schema for onetime freq
    '''
    name: str = 'Test Schema'
    members: list = ['127.0.0.1']
    description: str = 'Test Schema with payload'
    network_id: str = '00000000-0000-0000-0000-000000000000'
    enabled: bool = True
    s_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    e_time: str = (
            datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    freq: str = 'ONETIME'
    interval: int = 1

    # Let's register the response for timezone API
    responses.add(
        responses.GET,
        TIMEZONE_URL,
        json={
            'timezones': [
                {
                    'name': 'Africa/Addis_Ababa',
                    'value': 'Africa/Addis_Ababa'
                },
                {
                    'name': 'Etc/UTC',
                    'value': 'Etc/UTC'
                }
            ]
        }
    )
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
                'interval': interval
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
                'interval': interval
            }
        }
    }

    schema = ExclusionSchema(
        context={'timezones': api._tz}
    )
    assert output_payload == schema.dump(schema.load(input_payload))


@responses.activate
def test_exclusion_schema_with_invalid_field(api):
    '''
    Test case for Exclusion Schema for onetime freq
    '''
    # Let's register the response for timezone API
    responses.add(
        responses.GET,
        TIMEZONE_URL,
        json={
            'timezones': [
                {
                    'name': 'Africa/Addis_Ababa',
                    'value': 'Africa/Addis_Ababa'
                },
                {
                    'name': 'Etc/UTC',
                    'value': 'Etc/UTC'
                }
            ]
        }
    )
    schema = ExclusionSchema(
        context={'timezones': api._tz}
    )

    # Test with invalid timezone field
    with pytest.raises(ValueError):
        schema.dump(schema.load(
            {
                'schedule': {
                    'endtime': '2022-01-09 16:44:32',
                    'enabled': True,
                    'rrules': {
                        'freq': 'ONETIME',
                        'interval': 2
                    },
                    'timezone': 'Invalid',
                    'starttime': '2022-01-09 15:44:32'
                },
                'network_id': '00000000-0000-0000-0000-000000000000',
                'members': '127.0.0.1',
                'name': 'Weekly Exclusion'
            }
        ))

    # Test with missing starttime field
    with pytest.raises(ValueError):
        schema.dump(schema.load(
            {
                'schedule': {
                    'endtime': '2022-01-09 16:44:32',
                    'enabled': True,
                    'rrules': {
                        'freq': 'ONETIME',
                        'interval': 2
                    },
                    'timezone': 'Ect/UTC'
                },
                'network_id': '00000000-0000-0000-0000-000000000000',
                'members': '127.0.0.1',
                'name': 'Weekly Exclusion'
            }
        ))

    # Test with missing endtime field
    with pytest.raises(ValueError):
        schema.dump(schema.load(
            {
                'schedule': {
                    'enabled': True,
                    'rrules': {
                        'freq': 'ONETIME',
                        'interval': 2
                    },
                    'timezone': 'Ect/UTC',
                    'starttime': '2022-01-09 15:44:32'
                },
                'network_id': '00000000-0000-0000-0000-000000000000',
                'members': '127.0.0.1',
                'name': 'Weekly Exclusion'
            }
        ))
