"""
test agent exclusions
"""

import uuid
from datetime import datetime as dtime
from datetime import timedelta, timezone

import pytest
import responses

from tenable.errors import ForbiddenError, NotFoundError, UnexpectedValueError

from ..checker import check

SCANS_TIMEZONES = {
    'timezones': [
        {'name': 'Africa/Abidjan', 'value': 'Africa/Abidjan'},
        {'name': 'Etc/UTC', 'value': 'Etc/UTC'},
    ]
}


@pytest.fixture
def agentexclusion():
    """
    agent exclusion fixture
    """
    return {
        'schedule': {
            'endtime': '2018-12-07 00:17:41',
            'enabled': True,
            'rrules': {'freq': 'ONETIME', 'interval': 1},
            'timezone': 'Etc/UTC',
            'starttime': '2018-12-06 23:17:41',
        },
        'last_modification_date': 1544138262,
        'creation_date': 1544138262,
        'description': None,
        'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
        'id': 6418,
    }


def test_agentexclusions_create_no_times(tvm):
    """
    test to create the exclusion
    """
    with pytest.raises(AttributeError):
        tvm.agent_exclusions.create(str(uuid.uuid4()))


@responses.activate
def test_agentexclusions_create_scanner_id_typeerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    scanner_id is not passed as defined
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            scanner_id='nope',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_name_typeerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    name is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            1.02,
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_starttime_typerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    starttime is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            start_time='fail',
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_endtime_typerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    endtime is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()), start_time=dtime.now(timezone.utc), end_time='nope'
        )


@responses.activate
def test_agentexclusions_create_timezone_typerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    timezone is not passed as defined
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            timezone=1,
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_agentexclusions_create_timezone_unexpectedvalue(tvm):
    """
    test to raise the exception while creating the exclusion when value of
    timezone is not passed as defined
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            timezone='not a real timezone',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_description_typeerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    description is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            description=True,
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_frequency_typeerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    frequency is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            frequency=True,
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_frequency_unexpectedvalue(tvm):
    """
    test to raise the exception while creating the exclusion when value of
    frequency is not passed as defined
    """
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            frequency='nope',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_interval_typeerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    interval is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            interval='nope',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_weekdays_typerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    weekdays is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            weekdays='nope',
            frequency='weekly',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_weekdays_unexpectedvalue(tvm):
    """
    test to raise the exception while creating the exclusion when value of
    weekdays is not passed as defined
    """
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            weekdays=['MO', 'TU', 'nope'],
            frequency='weekly',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_dayofmonth_typeerror(tvm):
    """
    test to raise the exception while creating the exclusion when type of
    day of month is not passed as defined
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            day_of_month='nope',
            frequency='monthly',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


def test_agentexclusions_create_dayofmonth_unexpectedvalue(tvm):
    """
    test to raise the exception while creating the exclusion when value of
    day of month is not passed as defined
    """
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            day_of_month=0,
            frequency='monthly',
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_agentexclusions_create_onetime_exclusion(tvm):
    """
    test to create one time exclusion
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': '5469a60b-9b32-467f-a1d1-f0de78155e54',
            'uuid': '5bef020c-1032-4511-a228-64394c208a3c',
            'creation_date': 1615977274,
            'last_modification_date': 1615977274,
            'id': 105596,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 10:34:33',
                'endtime': '2021-03-17 11:34:33',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105596')
    resp = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
    )
    assert isinstance(resp, dict)
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_create_daily_exclusion(tvm):
    """
    test to create daily exclusion
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': 'f5c3ca6e-bafe-4066-b112-4545652baa1c',
            'uuid': 'ca23d313-b01f-42be-8c35-1042f4a01f7d',
            'creation_date': 1615977267,
            'last_modification_date': 1615977267,
            'id': 105595,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 10:34:26',
                'endtime': '2021-03-17 11:34:26',
                'enabled': True,
                'rrules': {'freq': 'DAILY', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105595')
    resp = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        frequency='daily',
    )
    assert isinstance(resp, dict)
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_create_weekly_exclusion(tvm):
    """
    test to create weekly exclusion

    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': 'e9036fec-3394-4c2f-b774-1728aa4f4e7c',
            'uuid': 'c1f90585-ecd9-42f7-97d8-ded55e8c66aa',
            'creation_date': 1615977260,
            'last_modification_date': 1615977260,
            'id': 105594,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 10:34:19',
                'endtime': '2021-03-17 11:34:19',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': '1', 'byweekday': 'MO,WE,FR'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105594')
    resp = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        frequency='weekly',
        weekdays=['mo', 'we', 'fr'],
    )
    assert isinstance(resp, dict)
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule']['rrules'], 'byweekday', str)
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_create_monthly_exclusion(tvm):
    """
    test to create monthly exclusion
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': '265b2cc0-400c-49de-a938-643b943284e9',
            'uuid': 'b33a07c7-3fdf-4c4b-aff8-753fb5308a1d',
            'creation_date': 1615977251,
            'last_modification_date': 1615977251,
            'id': 105593,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 10:34:10',
                'endtime': '2021-03-17 11:34:10',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': '1', 'bymonthday': '15'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105593')
    resp = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        frequency='monthly',
        day_of_month=15,
    )
    assert isinstance(resp, dict)
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule']['rrules'], 'bymonthday', str)
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_create_yearly_exclusion(tvm):
    """
    test to create yearly exclusion
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': '1f581a91-2696-45bd-950c-75fc12086c5f',
            'uuid': 'cfd55d08-eae1-4da4-97c9-78a99cb84eac',
            'creation_date': 1615977244,
            'last_modification_date': 1615977244,
            'id': 105592,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 10:34:03',
                'endtime': '2021-03-17 11:34:03',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105592')
    resp = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        frequency='yearly',
    )
    assert isinstance(resp, dict)
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_create_enabled_false_exclusion(tvm):
    """
    test to create exclusion when it is disabled
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': '9b379792-82a6-4dc7-995b-31d3d95594ae',
            'uuid': 'd81fafc7-94cb-4cb9-9d60-2e813ecffa10',
            'creation_date': 1615967509,
            'last_modification_date': 1615967509,
            'id': 105578,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 07:51:43',
                'endtime': '2021-03-17 08:51:43',
                'enabled': False,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105578')
    resp = tvm.agent_exclusions.create(str(uuid.uuid4()), enabled=False)
    assert isinstance(resp, dict)
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    assert resp['schedule']['enabled'] is False
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_create_standard_users_cant_create(tvm):
    """
    test to raise the exception when user try to create the exclusion
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_exclusions.create(
            str(uuid.uuid4()),
            start_time=dtime.now(timezone.utc),
            end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_agentexclusions_delete_notfounderror(tvm):
    """
    test to raise the exception when id not found to perform the deletion
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanners/1/agents/exclusions/123',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.agent_exclusions.delete(123)


@responses.activate
def test_agentexclusions_delete_exclusion(tvm, agentexclusion):
    """
    test to delete the agent exclusion
    """
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/6418')
    tvm.agent_exclusions.delete(agentexclusion['id'])


@responses.activate
def test_agentexclusions_delete_standard_user_fail(tvm, agentexclusion):
    """
    test to raise the exception when failed to delete the agent exclusion
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_exclusions.delete(agentexclusion['id'])


def test_agentexclusions_edit_no_exclusion_id_typeerror(tvm):
    """
    test to raise the exception when nothing is passed
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit()


def test_agentexclusions_edit_exclusion_id_typeerror(tvm):
    """
    test to raise the exception when expected type of exclusion_id is not passed
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit('nope')


def test_agentexclusions_edit_scanner_id_typeerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of scanner_id is not passed
    """
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], scanner_id='nope')


@responses.activate
def test_agentexclusions_edit_name_typeerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of name is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138797,
            'creation_date': 1544138797,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], name=1.02)


@responses.activate
def test_agentexclusions_edit_starttime_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of starttime is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138800,
            'creation_date': 1544138800,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], start_time='nope')


@responses.activate
def test_agentexclusions_edit_timezone_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of timezone is not passed
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138803,
            'creation_date': 1544138803,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], timezone=1)


@responses.activate
def test_agentexclusions_edit_timezone_unexpectedvalue(tvm, agentexclusion):
    """
    test to raise the exception when expected value of timezone is not passed
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138806,
            'creation_date': 1544138806,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.edit(agentexclusion['id'], timezone='nope')


@responses.activate
def test_agentexclusions_edit_description_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of description is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138809,
            'creation_date': 1544138809,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], description=1)


@responses.activate
def test_agentexclusions_edit_frequency_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of frequency is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138812,
            'creation_date': 1544138812,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], frequency=1)


@responses.activate
def test_agentexclusions_edit_frequency_unexpectedvalue(tvm, agentexclusion):
    """
    test to raise the exception when expected value of frequency is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138815,
            'creation_date': 1544138815,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.edit(agentexclusion['id'], frequency='nope')


@responses.activate
def test_agentexclusions_edit_interval_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of interval is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138818,
            'creation_date': 1544138818,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(agentexclusion['id'], interval='nope')


@responses.activate
def test_agentexclusions_edit_weekdays_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of weekdays is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': 'c1d01a51-60e2-48bc-b246-06e0a74bcfb7',
            'creation_date': 1615977186,
            'last_modification_date': 1615977186,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(
            agentexclusion['id'], frequency='weekly', weekdays='nope'
        )


@responses.activate
def test_agentexclusions_edit_weekdays_unexpectedvalue(tvm, agentexclusion):
    """
    test to raise the exception when expected value of weekdays is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '76614448-5492-4599-b4f8-ada40c39566f',
            'creation_date': 1615977194,
            'last_modification_date': 1615977194,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.edit(
            agentexclusion['id'], frequency='weekly', weekdays=['MO', 'WE', 'nope']
        )


@responses.activate
def test_agentexclusions_edit_dayofmonth_typerror(tvm, agentexclusion):
    """
    test to raise the exception when expected type of day of month is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': 'af438b56-7279-4beb-8c8a-ffbd8e7ea62a',
            'creation_date': 1615977202,
            'last_modification_date': 1615977202,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    with pytest.raises(TypeError):
        tvm.agent_exclusions.edit(
            agentexclusion['id'], frequency='monthly', day_of_month='nope'
        )


@responses.activate
def test_agentexclusions_edit_dayofmonth_unexpectedvalue(tvm, agentexclusion):
    """
    test to raise the exception when expected value of day of month is not passed
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': 'b9101b77-a625-484a-9c45-a5f6a5a2a561',
            'creation_date': 1615977210,
            'last_modification_date': 1615977210,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.agent_exclusions.edit(
            agentexclusion['id'], frequency='monthly', day_of_month=0
        )


@responses.activate
def test_agentexclusions_edit_standard_user_permission_error(tvm, agentexclusion):
    """
    test to raise the exception when there is no permission to edit the agent exclusion
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_exclusions.edit(agentexclusion['id'], name=str(uuid.uuid4()))


@responses.activate
def test_agentexclusions_edit_success(tvm, agentexclusion):
    """
    test to edit the exclusion
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138307,
            'creation_date': 1544138307,
            'description': None,
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'id': 6418,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:17:41',
            },
            'last_modification_date': 1544138309,
            'creation_date': 1544138307,
            'description': None,
            'name': 'c7ce3bc7-e74f-4e96-8bba-4ce9c123c5e3',
            'id': 6418,
        },
    )
    tvm.agent_exclusions.edit(agentexclusion['id'], name=str(uuid.uuid4()))


@responses.activate
def test_agentexclusions_edit_freq_onetime_to_daily(tvm, agentexclusion):
    """
    test to edit the exclusion by enabling exclusion daily
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '3f066aa3-60eb-4a77-836e-79f2363badaf',
            'creation_date': 1615969541,
            'last_modification_date': 1615969541,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '9833ad85-2692-43c4-a4ab-5037f0364613',
            'uuid': '3f066aa3-60eb-4a77-836e-79f2363badaf',
            'creation_date': 1615969541,
            'last_modification_date': 1615969543,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'DAILY', 'interval': '2'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'], name=str(uuid.uuid4()), frequency='daily', interval=2
    )

    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'DAILY'
    assert resp['schedule']['rrules']['interval'] == '2'


@responses.activate
def test_agentexclusions_edit_enable_exclusion(tvm):
    """
    test to check the exclusion by enabling exclusion

    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': '413bca99-daa4-404c-86e1-fb40ceaabdbe',
            'uuid': '3cdd5883-9d3b-4e5d-9e44-3f0229c75b90',
            'creation_date': 1615969553,
            'last_modification_date': 1615969553,
            'id': 105580,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:25:52',
                'endtime': '2021-03-17 09:25:52',
                'enabled': False,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/105580',
        json={
            'description': '',
            'name': '413bca99-daa4-404c-86e1-fb40ceaabdbe',
            'uuid': '3cdd5883-9d3b-4e5d-9e44-3f0229c75b90',
            'creation_date': 1615969553,
            'last_modification_date': 1615969553,
            'id': 105580,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:25:52',
                'endtime': '2021-03-17 09:25:52',
                'enabled': False,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/105580',
        json={
            'description': '',
            'name': '413bca99-daa4-404c-86e1-fb40ceaabdbe',
            'uuid': '3cdd5883-9d3b-4e5d-9e44-3f0229c75b90',
            'creation_date': 1615969553,
            'last_modification_date': 1615969555,
            'id': 105580,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:25:53',
                'endtime': '2021-03-17 09:25:53',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105580')
    agentexclusion = tvm.agent_exclusions.create(str(uuid.uuid4()), enabled=False)
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'],
        enabled=True,
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
    )
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    assert resp['schedule']['enabled'] is True
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_edit_onetime_to_weekly_valdefault(tvm, agentexclusion):
    """
    test to check the exclusion weekly
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '3359a34e-e380-4e0a-ba6a-530d38346bc1',
            'creation_date': 1615969563,
            'last_modification_date': 1615969563,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '3359a34e-e380-4e0a-ba6a-530d38346bc1',
            'creation_date': 1615969563,
            'last_modification_date': 1615969565,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': '1',
                    'byweekday': 'SU,MO,TU,WE,TH,FR,SA',
                },
                'timezone': 'Etc/UTC',
            },
        },
    )
    resp = tvm.agent_exclusions.edit(agentexclusion['id'], frequency='Weekly')
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    assert resp['schedule']['rrules']['byweekday'] == 'SU,MO,TU,WE,TH,FR,SA'


@responses.activate
def test_agentexclusions_edit_onetime_to_weekly_valassigned(tvm, agentexclusion):
    """
    test to check the exclusion weekly

    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '2a250f41-620e-4bab-a156-b449c6c53b97',
            'creation_date': 1615969573,
            'last_modification_date': 1615969573,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '2a250f41-620e-4bab-a156-b449c6c53b97',
            'creation_date': 1615969573,
            'last_modification_date': 1615969575,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': '1', 'byweekday': 'MO,TU'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'], frequency='Weekly', weekdays=['MO', 'TU']
    )
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    assert resp['schedule']['rrules']['byweekday'] == 'MO,TU'


@responses.activate
def test_agentexclusions_edit_onetime_to_weekly_valavailable(tvm):
    """
    test to check the exclusion weekly

    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': 'e68b5c71-c3ba-4c3a-ac0e-ab53bbe2f1fe',
            'uuid': 'bb5b2562-2d07-47cc-9d58-3fbf9910457b',
            'creation_date': 1615969583,
            'last_modification_date': 1615969583,
            'id': 105583,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:26:22',
                'endtime': '2021-03-17 09:26:22',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': '1', 'byweekday': 'TU,WE'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/105583',
        json={
            'description': '',
            'name': 'e68b5c71-c3ba-4c3a-ac0e-ab53bbe2f1fe',
            'uuid': 'bb5b2562-2d07-47cc-9d58-3fbf9910457b',
            'creation_date': 1615969583,
            'last_modification_date': 1615969583,
            'id': 105583,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:26:22',
                'endtime': '2021-03-17 09:26:22',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': '1', 'byweekday': 'TU,WE'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/105583',
        json={
            'description': '',
            'name': 'f83a538d-d4e4-4ec8-a114-e4a3d48774f0',
            'uuid': 'bb5b2562-2d07-47cc-9d58-3fbf9910457b',
            'creation_date': 1615969583,
            'last_modification_date': 1615969585,
            'id': 105583,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:26:22',
                'endtime': '2021-03-17 09:26:22',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': '1', 'byweekday': 'TU,WE'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    agentexclusion = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        frequency='Weekly',
        weekdays=['TU', 'WE'],
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
    )
    resp = tvm.agent_exclusions.edit(agentexclusion['id'], name=str(uuid.uuid4()))
    check(resp, 'id', int)
    check(resp, 'name', str)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'last_modification_date', int)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    assert resp['schedule']['rrules']['byweekday'] == 'TU,WE'


@responses.activate
def test_agentexclusions_edit_freq_onetime_to_monthly_valddefault(tvm, agentexclusion):
    """
    test to check the exclusion monthly

    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': 'fa1dfd07-469c-46ec-8295-eee600bfb46a',
            'creation_date': 1615969593,
            'last_modification_date': 1615969593,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': 'bc721cb9-833e-4d2d-ae2c-c191febaf338',
            'uuid': 'fa1dfd07-469c-46ec-8295-eee600bfb46a',
            'creation_date': 1615969593,
            'last_modification_date': 1615969595,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': '2', 'bymonthday': '17'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'], name=str(uuid.uuid4()), frequency='monthly', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == '2'


@responses.activate
def test_agentexclusions_edit_freq_onetime_to_monthly_valassigned(tvm, agentexclusion):
    """
    test to check the exclusion monthly

    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '67fc7cb4-bc76-47d6-b44f-690b395ab8a2',
            'creation_date': 1615969603,
            'last_modification_date': 1615969603,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '5675ab88-c3bf-46d5-85c0-caadaf9e6665',
            'uuid': '67fc7cb4-bc76-47d6-b44f-690b395ab8a2',
            'creation_date': 1615969603,
            'last_modification_date': 1615969605,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': '2', 'bymonthday': '8'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'],
        name=str(uuid.uuid4()),
        frequency='monthly',
        interval=2,
        day_of_month=8,
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == '2'
    assert resp['schedule']['rrules']['bymonthday'] == '8'


@responses.activate
def test_agentexclusions_edit_freq_onetime_to_monthly_valavailable(tvm):
    """
    test to check the exclusion monthly

    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'description': '',
            'name': 'b73f3f9f-7a6e-4855-af02-e08405fb2a04',
            'uuid': '21520f04-785f-45b0-9e9a-674b8b7a09a6',
            'creation_date': 1615969732,
            'last_modification_date': 1615969732,
            'id': 105586,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:28:52',
                'endtime': '2021-03-17 09:28:52',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': '1', 'bymonthday': '8'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/105586',
        json={
            'description': '',
            'name': 'b73f3f9f-7a6e-4855-af02-e08405fb2a04',
            'uuid': '21520f04-785f-45b0-9e9a-674b8b7a09a6',
            'creation_date': 1615969732,
            'last_modification_date': 1615969732,
            'id': 105586,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:28:52',
                'endtime': '2021-03-17 09:28:52',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': '1', 'bymonthday': '8'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/105586',
        json={
            'description': '',
            'name': 'b73f3f9f-7a6e-4855-af02-e08405fb2a04',
            'uuid': '21520f04-785f-45b0-9e9a-674b8b7a09a6',
            'creation_date': 1615969732,
            'last_modification_date': 1615969734,
            'id': 105586,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2021-03-17 08:28:52',
                'endtime': '2021-03-17 09:28:52',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': '2', 'bymonthday': '8'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scanners/1/agents/exclusions/105586')
    agentexclusion = tvm.agent_exclusions.create(
        str(uuid.uuid4()),
        start_time=dtime.now(timezone.utc),
        end_time=dtime.now(timezone.utc) + timedelta(hours=1),
        frequency='monthly',
        day_of_month=8,
    )
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'], frequency='monthly', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == '2'
    assert resp['schedule']['rrules']['bymonthday'] == '8'
    tvm.agent_exclusions.delete(resp['id'])


@responses.activate
def test_agentexclusions_edit_freq_onetime_to_yearly(tvm, agentexclusion):
    """
    test to check the exclusion yearly
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': '7af0a062-4e74-4272-a595-d591d60cfff7',
            'uuid': '077a6332-7977-4a5b-865b-05321b370596',
            'creation_date': 1615969751,
            'last_modification_date': 1615969751,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': '1'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/exclusions/6418',
        json={
            'description': '',
            'name': 'e2daa349-2546-41b2-92fc-2140d2f3d4d1',
            'uuid': '077a6332-7977-4a5b-865b-05321b370596',
            'creation_date': 1615969751,
            'last_modification_date': 1615969753,
            'id': 6418,
            'core_updates_blocked': True,
            'schedule': {
                'starttime': '2018-12-06 23:17:41',
                'endtime': '2018-12-07 00:17:41',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': '2'},
                'timezone': 'Etc/UTC',
            },
        },
    )
    resp = tvm.agent_exclusions.edit(
        agentexclusion['id'], name=str(uuid.uuid4()), frequency='yearly', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', str)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'YEARLY'
    assert resp['schedule']['rrules']['interval'] == '2'


@responses.activate
def test_agentexclusions_list_blackouts(tvm):
    """
    test to list the blackouts
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/exclusions',
        json={
            'exclusions': [
                {
                    'schedule': {
                        'endtime': '2018-10-15 22:41:28',
                        'enabled': True,
                        'rrules': {'freq': 'MONTHLY', 'interval': 1, 'bymonthday': 15},
                        'timezone': 'Etc/UTC',
                        'starttime': '2018-10-15 21:41:28',
                    },
                    'last_modification_date': 1539639689,
                    'creation_date': 1539639689,
                    'description': None,
                    'name': '006f3653-f108-41ec-b770-4e13ce53ef0a',
                    'id': 4210,
                }
            ]
        },
    )
    items = tvm.agent_exclusions.list()
    assert isinstance(items, list)
