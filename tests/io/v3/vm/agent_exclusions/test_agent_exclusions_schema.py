'''
Test cases the Agent Exclusions APIs schemas
'''
from datetime import datetime, timedelta

import pytest
import responses

from tenable.io.v3.vm.agent_exclusions.schema import AgentExclusionSchema

TIMEZONE_URL: str = 'https://cloud.tenable.com/api/v3/scans/timezones'


@responses.activate
def test_agent_exlusion_schema_with_weekly_freq(api):
    '''
    Test case for Agent Exclusion Schema with fre weekly
    '''
    name: str = 'Test Schema'
    description: str = 'Test Schema with payload'
    enabled: bool = True
    start_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    end_time: str = (
        datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    timezone: str = 'Etc/UTC'
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

    # Let's create input sample payload for schema
    payload = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval
            }
        }
    }

    # Let's create output sample payload for schema
    test_resp = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'byweekday': 'SU,MO,TU,WE,TH,FR,SA'
            }
        }
    }

    schema = AgentExclusionSchema(
        context={'timezones': api.v3.vm.scans.timezones()}
    )
    assert test_resp == schema.dump(schema.load(payload))


@responses.activate
def test_agent_exlusion_schema_with_monthly_freq(api):
    '''
    Test case for Agent Exclusion Schema with monthly freq
    '''
    name: str = 'Test Schema'
    description: str = 'Test Schema with payload'
    enabled: bool = True
    start_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    end_time: str = (
        datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    timezone: str = 'Etc/UTC'
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

    # Let's create input sample payload for schema
    payload = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval
            }
        }
    }

    # Let's create output sample payload for schema
    test_resp = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval,
                'bymonthday': datetime.today().day
            }
        }
    }

    schema = AgentExclusionSchema(
        context={'timezones': api.v3.vm.scans.timezones()}
    )
    assert test_resp == schema.dump(schema.load(payload))


@responses.activate
def test_agent_exlusion_schema_with_daily_freq(api):
    '''
    Test case for Agent Exclusion Schema with daily freq
    '''
    name: str = 'Test Schema'
    description: str = 'Test Schema with payload'
    enabled: bool = True
    start_time: str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    end_time: str = (
        datetime.utcnow() + timedelta(hours=1)
    ).strftime('%Y-%m-%d %H:%M:%S')
    timezone: str = 'Etc/UTC'
    freq: str = 'DAILY'
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

    # Let's create input sample payload for schema
    payload = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval
            }
        }
    }

    # Let's create output sample payload for schema
    test_resp = {
        'name': name,
        'description': description,
        'schedule': {
            'enabled': enabled,
            'starttime': start_time,
            'endtime': end_time,
            'timezone': timezone,
            'rrules': {
                'freq': freq,
                'interval': interval
            }
        }
    }

    schema = AgentExclusionSchema(
        context={'timezones': api.v3.vm.scans.timezones()}
    )
    assert test_resp == schema.dump(schema.load(payload))


@responses.activate
def test_agent_exlusion_schema_with_invalid_timezone(api):
    '''
    Test case for Agent Exclusion Schema with invalid timezone
    '''
    name: str = 'Test Schema'
    timezone: str = 'ABC'
    enabled: bool = False

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

    # Let's create input sample payload for schema
    payload = {
        'name': name,
        'schedule': {
            'enabled': enabled,
            'timezone': timezone,
            'rrules': {
                'freq': 'daily',
                'interval': 1
            }
        }
    }

    schema = AgentExclusionSchema(
        context={'timezones': api.v3.vm.scans.timezones()}
    )

    with pytest.raises(ValueError):
        schema.dump(schema.load(payload))
