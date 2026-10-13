"""
test exclusions
"""

import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest
import responses

from tenable.errors import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    UnexpectedValueError,
)
from tests.checker import check

SCANS_TIMEZONES = {
    'timezones': [
        {'name': 'Africa/Abidjan', 'value': 'Africa/Abidjan'},
        {'name': 'Etc/UTC', 'value': 'Etc/UTC'},
    ]
}


@pytest.fixture(name='exclusion')
def fixture_exclusion():
    """
    Fixture to create exclusion
    """
    return {
        'schedule': {
            'endtime': '2018-12-07 00:19:41',
            'enabled': True,
            'rrules': {'freq': 'ONETIME', 'interval': 1},
            'timezone': 'Etc/UTC',
            'starttime': '2018-12-06 23:19:41',
        },
        'last_modification_date': 1544138382,
        'creation_date': 1544138382,
        'members': '127.0.0.1',
        'description': None,
        'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
        'id': 5412,
    }


@responses.activate
def test_exclusions_create_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            1,
            ['127.0.0.1'],
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_exclusions_create_members_typeerror(tvm):
    """
    test to raise exception when type of members param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4),
            '127.0.0.1',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_start_time_typeerror(tvm):
    """
    test to raise exception when type of start_time param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4),
            ['127.0.0.1'],
            start_time='now',
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_end_time_typeerror(tvm):
    """
    test to raise exception when type of end_time param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4),
            ['127.0.0.1'],
            start_time=datetime.now(timezone.utc),
            end_time='later',
        )


@responses.activate
def test_exclusions_create_timezone_typeerror(tvm):
    """
    test to raise exception when type of timezone param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            timezone=1,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_exclusions_create_timezone_unexpectedvalue(tvm):
    """
    test to raise exception when timezone param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            timezone='the zone of time',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_exclusions_create_description_typeerror(tvm):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            description=1,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_frequency_typeerror(tvm):
    """
    test to raise exception when type of frequency param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            frequency=1,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_frequency_unexpectedvalue(tvm):
    """
    test to raise exception when frequency param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            frequency='nope',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_interval_typeerror(tvm):
    """
    test to raise exception when type of interval param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            interval='nope',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_weekdays_typeerror(tvm):
    """
    test to raise exception when type of weekdays param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            weekdays='nope',
            frequency='weekly',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_weekdays_unexpectedvalue(tvm):
    """
    test to raise exception when weekdays param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            weekdays=['MO', 'WE', 'nope'],
            frequency='weekly',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_day_of_month_typeerror(tvm):
    """
    test to raise exception when type of day_of_month param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            day_of_month='nope',
            frequency='monthly',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_day_of_month_unexpectedvalue(tvm):
    """
    test to raise exception when day_of_month param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            day_of_month=82,
            frequency='monthly',
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


def test_exclusions_create_enabled_typeerror(tvm):
    """
    test to raise exception when type of enabled param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled='yup')


@responses.activate
def test_exclusions_create_standard_user_permissionerror(tvm):
    """
    test to raise exception when standard_user tries to create exclusion.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        )


@responses.activate
def test_exclusions_create_with_selected_network_unexpectedvalueerror(tvm):
    """
    test to raise exception when network_id param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
            network_id='nope',
        )


@responses.activate
def test_exclusions_create_with_selected_network_typeerror(tvm):
    """
    test to raise exception when type of network_id param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
            network_id=1,
        )


@responses.activate
def test_exclusions_create_with_selected_network_notfounderror(tvm):
    """
    test to raise exception when network_id not found.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'error': '{"error":"Network with uuid 00000000-0000-0000-0000-100000000001 does not exist"}'
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.exclusions.create(
            str(uuid.uuid4()),
            ['127.0.0.1'],
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
            network_id='00000000-0000-0000-0000-100000000001',
        )


@responses.activate
def test_exclusions_create_onetime_exclusion(tvm):
    """
    test to create exclusion with frequency onetime
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:36',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:36',
            },
            'last_modification_date': 1544138377,
            'creation_date': 1544138377,
            'members': '127.0.0.1',
            'description': None,
            'name': '514b8ad4-3cb6-4242-9d49-049d3991d159',
            'id': 5407,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/5407')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_daily_exclusion(tvm):
    """
    test to create exclusion with frequency daily
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:38',
                'enabled': True,
                'rrules': {'freq': 'DAILY', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:38',
            },
            'last_modification_date': 1544138378,
            'creation_date': 1544138378,
            'members': '127.0.0.1',
            'description': None,
            'name': 'dd178a18-13f0-4ed9-a840-1c7e54d658df',
            'id': 5408,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/5408')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='daily',
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_weekly_exclusion(tvm):
    """
    test to create exclusion with frequency weekly
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:39',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': 1, 'byweekday': 'MO,WE,FR'},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:39',
            },
            'last_modification_date': 1544138379,
            'creation_date': 1544138379,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e3c1c048-a585-49c0-baaf-fd8d021e90b6',
            'id': 5409,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/5409')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='weekly',
        weekdays=['mo', 'we', 'fr'],
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'byweekday', str)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_monthly_exclusion(tvm):
    """
    test to create exclusion with frequency monthly
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:39',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 1, 'bymonthday': 15},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:39',
            },
            'last_modification_date': 1544138380,
            'creation_date': 1544138380,
            'members': '127.0.0.1',
            'description': None,
            'name': 'c232e128-e259-482e-83ef-9afaf14366be',
            'id': 5410,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/5410')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='monthly',
        day_of_month=15,
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'bymonthday', int)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_yearly_exclusion(tvm):
    """
    test to create exclusion with frequency yearly
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:40',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:40',
            },
            'last_modification_date': 1544138381,
            'creation_date': 1544138381,
            'members': '127.0.0.1',
            'description': None,
            'name': '491a36a8-ba27-4638-8d64-78e48d9d2f22',
            'id': 5411,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/5411')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='yearly',
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_enabled_false_exclusion(tvm):
    """
    test to create exclusion with enabled param as false
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614938517,
            'creation_date': 1614938517,
            'members': '127.0.0.1',
            'description': '',
            'name': 'bcd29ea6-c26f-4d8e-8471-8f798b423d80',
            'id': 13,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/13')
    resp = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    assert resp['schedule']['enabled'] is False
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_with_selected_network_exclusion(tvm, network):
    """
    test to create exclusion and apply to user defined network_id
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2021-03-03 14:29:58',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-03 13:29:58',
            },
            'network_id': '58ac2d96-81aa-472c-a418-74fcc6082049',
            'last_modification_date': 1614778200,
            'creation_date': 1614778200,
            'members': '127.0.0.1',
            'description': '',
            'name': 'b6e89aad-78e6-4d67-b070-6e208459039f',
            'id': 2,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/2',
        json={
            'schedule': {
                'endtime': '2021-03-03 14:29:58',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-03 13:29:58',
            },
            'network_id': '58ac2d96-81aa-472c-a418-74fcc6082049',
            'last_modification_date': 1614778200,
            'creation_date': 1614778200,
            'members': '127.0.0.1',
            'description': '',
            'name': 'b6e89aad-78e6-4d67-b070-6e208459039f',
            'id': 2,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/2')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='yearly',
        network_id=network['uuid'],
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'network_id', 'uuid')
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    details = tvm.exclusions.details(resp['id'])
    assert details['network_id'] == network['uuid']
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_create_with_default_network_exclusion(tvm):
    """
    test to create exclusion with default network_id
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2021-03-03 14:31:40',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-03 13:31:40',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614778301,
            'creation_date': 1614778301,
            'members': '127.0.0.1',
            'description': '',
            'name': '65ffdf2f-f965-4c94-9080-74b37d05b896',
            'id': 7,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/7',
        json={
            'schedule': {
                'endtime': '2021-03-03 14:31:40',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-03 13:31:40',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614778301,
            'creation_date': 1614778301,
            'members': '127.0.0.1',
            'description': '',
            'name': '65ffdf2f-f965-4c94-9080-74b37d05b896',
            'id': 7,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/7')
    resp = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='yearly',
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'network_id', 'uuid')
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    details = tvm.exclusions.details(resp['id'])
    assert details['network_id'] == '00000000-0000-0000-0000-000000000000'
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_delete_notfounderror(tvm):
    """
    test to raise exception when exclusion_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/exclusions/999999',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.exclusions.delete(999999)


@responses.activate
def test_exclusions_delete_exclusion(tvm, exclusion):
    """
    test to delete exclusion
    """
    responses.add(responses.DELETE, 'https://nourl/exclusions/5412')
    tvm.exclusions.delete(exclusion['id'])


@responses.activate
def test_exclusions_delete_standard_user_fail(tvm, exclusion):
    """
    test to raise exception when standard user try to delete exclusion.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/exclusions/5412',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.exclusions.delete(exclusion['id'])


@responses.activate
def test_exclusions_edit_members_typeerror(tvm, exclusion):
    """
    test to raise exception when type of members param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138837,
            'creation_date': 1544138837,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], members='192.168.0.1')


@responses.activate
def test_exclusions_edit_name_typeerror(tvm, exclusion):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138838,
            'creation_date': 1544138838,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], name=1.02)


@responses.activate
def test_exclusions_edit_starttime_typerror(tvm, exclusion):
    """
    test to raise exception when type of start time param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138840,
            'creation_date': 1544138840,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], start_time='nope')


@responses.activate
def test_exclusions_edit_timezone_typerror(tvm, exclusion):
    """
    test to raise exception when type of timezone param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138841,
            'creation_date': 1544138841,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], timezone=1)


@responses.activate
def test_exclusions_edit_timezone_unexpectedvalue(tvm, exclusion):
    """
    test to raise exception when timezone param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138842,
            'creation_date': 1544138842,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.edit(exclusion['id'], timezone='nope')


@responses.activate
def test_exclusions_edit_description_typerror(tvm, exclusion):
    """
    test to raise exception when type of description param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138843,
            'creation_date': 1544138843,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], description=1)


@responses.activate
def test_exclusions_edit_frequency_typerror(tvm, exclusion):
    """
    test to raise exception when type of frequency param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138844,
            'creation_date': 1544138844,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], frequency=1)


@responses.activate
def test_exclusions_edit_frequency_unexpectedvalue(tvm, exclusion):
    """
    test to raise exception when frequency param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138845,
            'creation_date': 1544138845,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.edit(exclusion['id'], frequency='nope')


@responses.activate
def test_exclusions_edit_interval_typerror(tvm, exclusion):
    """
    test to raise exception when type of interval param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138846,
            'creation_date': 1544138846,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], interval='nope')


@responses.activate
def test_exclusions_edit_weekdays_typerror(tvm, exclusion):
    """
    test to raise exception when type of weekdays param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614979479,
            'creation_date': 1614979479,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], frequency='Weekly', weekdays='nope')


@responses.activate
def test_exclusions_edit_weekdays_unexpectedvalue(tvm, exclusion):
    """
    test to raise exception when weekdays param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614979487,
            'creation_date': 1614979487,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.edit(
            exclusion['id'], frequency='Weekly', weekdays=['MO', 'WE', 'nope']
        )


@responses.activate
def test_exclusions_edit_dayofmonth_typerror(tvm, exclusion):
    """
    test to raise exception when type of day_of_month param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614979494,
            'creation_date': 1614979494,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], frequency='monthly', day_of_month='nope')


@responses.activate
def test_exclusions_edit_dayofmonth_unexpectedvalue(tvm, exclusion):
    """
    test to raise exception when day_of_month param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614979500,
            'creation_date': 1614979500,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.edit(exclusion['id'], frequency='monthly', day_of_month=0)


@responses.activate
def test_exclusions_edit_standard_user_permission_error(tvm, exclusion):
    """
    test to raise exception when standard user try to edit exclusion.
    """
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))


@responses.activate
def test_exclusions_edit_network_select_notfounderror(tvm, exclusion):
    """
    test to raise exception when user provided network_id not found.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614778225,
            'creation_date': 1614778225,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'error': '{"error":"Network with uuid 00000000-0000-0000-0000-100000000001 does not exist"}'
        },
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.exclusions.edit(
            exclusion['id'], network_id='00000000-0000-0000-0000-100000000001'
        )


@responses.activate
def test_exclusions_edit_network_select_unexpectedvalueerror(tvm, exclusion):
    """
    test to raise exception when network_id param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614778242,
            'creation_date': 1614778242,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(UnexpectedValueError):
        tvm.exclusions.edit(exclusion['id'], network_id='nope')


@responses.activate
def test_exclusions_edit_network_select_typeerror(tvm, exclusion):
    """
    test to raise exception when type of network_id param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614778256,
            'creation_date': 1614778256,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    with pytest.raises(TypeError):
        tvm.exclusions.edit(exclusion['id'], network_id=1)


@responses.activate
def test_exclusions_edit_success(tvm, exclusion):
    """
    test to edit exclusion name
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138401,
            'creation_date': 1544138401,
            'members': '127.0.0.1',
            'description': None,
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'last_modification_date': 1544138402,
            'creation_date': 1544138401,
            'members': '127.0.0.1',
            'description': None,
            'name': '7af4d35f-ed56-49aa-a39c-abb79aff05b0',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)


@responses.activate
def test_exclusions_edit_network_success(tvm, exclusion, network):
    """
    test to edit exclusion network
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614778269,
            'creation_date': 1614778269,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '58ac2d96-81aa-472c-a418-74fcc6082049',
            'last_modification_date': 1614778272,
            'creation_date': 1614778269,
            'members': '127.0.0.1',
            'description': '',
            'name': 'f485edff-c59e-4eee-8461-e1dcf48913e5',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), network_id=network['uuid']
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'network_id', 'uuid')
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['network_id'] == network['uuid']


@responses.activate
def test_exclusions_edit_freq_onetime_to_daily(tvm, exclusion):
    """
    test to edit exclusion frequency from onetime to daily
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614978556,
            'creation_date': 1614978556,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'DAILY', 'interval': 2},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614978558,
            'creation_date': 1614978556,
            'members': '127.0.0.1',
            'description': '',
            'name': '0cb428a1-ed14-4768-98eb-436195a3608b',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='daily', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'DAILY'
    assert resp['schedule']['rrules']['interval'] == 2


@responses.activate
def test_exclusions_edit_freq_onetime_to_weekly_valdefault(tvm, exclusion):
    """
    test to edit exclusion frequency from onetime to weekly
    and assign default value to weekdays param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115057,
            'creation_date': 1615115057,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': 2,
                    'byweekday': 'SU,MO,TU,WE,TH,FR,SA',
                },
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115059,
            'creation_date': 1615115057,
            'members': '127.0.0.1',
            'description': '',
            'name': 'acce4990-9fda-447d-a43f-6afbb3b5054a',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='weekly', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'WEEKLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['byweekday'] == 'SU,MO,TU,WE,TH,FR,SA'


@responses.activate
def test_exclusions_edit_freq_onetime_to_weekly_valassigned(tvm, exclusion):
    """
    test to edit exclusion frequency from onetime to weekly
    and assign user defined value to weekdays param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115161,
            'creation_date': 1615115161,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': 2, 'byweekday': 'TH,FR'},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115163,
            'creation_date': 1615115161,
            'members': '127.0.0.1',
            'description': '',
            'name': '00ee9854-e85d-41f7-af71-702c6f9e3342',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'],
        name=str(uuid.uuid4()),
        frequency='weekly',
        interval=2,
        weekdays=['TH', 'FR'],
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'WEEKLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['byweekday'] == 'TH,FR'


@responses.activate
def test_exclusions_edit_freq_onetime_to_weekly_valavailable(tvm):
    """
    test to edit weekly exclusion and assign existing weekdays values to weekdays param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:50:34',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': 1, 'byweekday': 'TH,FR'},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:50:34',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614977436,
            'creation_date': 1614977436,
            'members': '127.0.0.1',
            'description': '',
            'name': '00517893-09e6-46e4-a081-b20736223a3d',
            'id': 48,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/48',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:50:34',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': 1, 'byweekday': 'TH,FR'},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:50:34',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614977436,
            'creation_date': 1614977436,
            'members': '127.0.0.1',
            'description': '',
            'name': '00517893-09e6-46e4-a081-b20736223a3d',
            'id': 48,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/48',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:50:34',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': 2, 'byweekday': 'TH,FR'},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:50:34',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614977438,
            'creation_date': 1614977436,
            'members': '127.0.0.1',
            'description': '',
            'name': '00517893-09e6-46e4-a081-b20736223a3d',
            'id': 48,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/48')
    exclusion = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='weekly',
        weekdays=['TH', 'FR'],
    )
    resp = tvm.exclusions.edit(exclusion['id'], frequency='weekly', interval=2)
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'WEEKLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['byweekday'] == 'TH,FR'
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_enable_false_to_weekly_valdefault(tvm):
    """
    test to enable exclusion and assign frequency as weekly and weekdays as default
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614978142,
            'creation_date': 1614978142,
            'members': '127.0.0.1',
            'description': '',
            'name': '45c6b9d7-bf9f-4b48-81b9-6c23e0a3477d',
            'id': 54,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/54',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614978142,
            'creation_date': 1614978142,
            'members': '127.0.0.1',
            'description': '',
            'name': '45c6b9d7-bf9f-4b48-81b9-6c23e0a3477d',
            'id': 54,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/54',
        json={
            'schedule': {
                'endtime': '2021-03-05 22:02:22',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': 2,
                    'byweekday': 'SU,MO,TU,WE,TH,FR,SA',
                },
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 21:02:22',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614978145,
            'creation_date': 1614978142,
            'members': '127.0.0.1',
            'description': '',
            'name': '45c6b9d7-bf9f-4b48-81b9-6c23e0a3477d',
            'id': 54,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/54')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='weekly',
        interval=2,
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'WEEKLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['byweekday'] == 'SU,MO,TU,WE,TH,FR,SA'
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_enable_false_to_weekly_valassigned(tvm):
    """
    test to enable exclusion and assign frequency as weekly and weekdays as defined
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976984,
            'creation_date': 1614976984,
            'members': '127.0.0.1',
            'description': '',
            'name': '7899b7d0-88ef-44e4-b192-2fad5ff46549',
            'id': 44,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/44',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976984,
            'creation_date': 1614976984,
            'members': '127.0.0.1',
            'description': '',
            'name': '7899b7d0-88ef-44e4-b192-2fad5ff46549',
            'id': 44,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/44',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:43:05',
                'enabled': True,
                'rrules': {'freq': 'WEEKLY', 'interval': 2, 'byweekday': 'TH,FR'},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:43:05',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976988,
            'creation_date': 1614976984,
            'members': '127.0.0.1',
            'description': '',
            'name': '7899b7d0-88ef-44e4-b192-2fad5ff46549',
            'id': 44,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/44')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='weekly',
        interval=2,
        weekdays=['TH', 'FR'],
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'WEEKLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['byweekday'] == 'TH,FR'
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_freq_onetime_to_monthly_valddefault(tvm, exclusion):
    """
    test to edit exclusion frequency from onetime to monthly
    and assign default value to day_of_month param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115545,
            'creation_date': 1615115545,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 2, 'bymonthday': 7},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115548,
            'creation_date': 1615115545,
            'members': '127.0.0.1',
            'description': '',
            'name': '41e71207-93f4-438f-99d0-728646e32c04',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='monthly', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == 2


@responses.activate
def test_exclusions_edit_freq_onetime_to_monthly_valassigned(tvm, exclusion):
    """
    test to edit exclusion frequency from onetime to monthly
    and assign user defined value to day_of_month param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976497,
            'creation_date': 1614976497,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 2, 'bymonthday': 8},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976499,
            'creation_date': 1614976497,
            'members': '127.0.0.1',
            'description': '',
            'name': 'f502621b-72b5-4fc8-b6a7-846ec9da5853',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'],
        name=str(uuid.uuid4()),
        frequency='monthly',
        interval=2,
        day_of_month=8,
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['bymonthday'] == 8


@responses.activate
def test_exclusions_edit_freq_onetime_to_monthly_valavailable(tvm):
    """
    test to edit exclusion and assign existing day_of_month value to day_of_month param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:35:00',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 1, 'bymonthday': 8},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:35:00',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976502,
            'creation_date': 1614976502,
            'members': '127.0.0.1',
            'description': '',
            'name': '3a543f0b-fc5b-4728-818a-cdd64211f9cd',
            'id': 38,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/38',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:35:00',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 1, 'bymonthday': 8},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:35:00',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976502,
            'creation_date': 1614976502,
            'members': '127.0.0.1',
            'description': '',
            'name': '3a543f0b-fc5b-4728-818a-cdd64211f9cd',
            'id': 38,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/38',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:35:00',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 2, 'bymonthday': 8},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:35:00',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976504,
            'creation_date': 1614976502,
            'members': '127.0.0.1',
            'description': '',
            'name': '3a543f0b-fc5b-4728-818a-cdd64211f9cd',
            'id': 38,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/38')
    exclusion = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='monthly',
        day_of_month=8,
    )
    resp = tvm.exclusions.edit(exclusion['id'], frequency='monthly', interval=2)
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['bymonthday'] == 8
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_enable_false_to_monthly_valdefault(tvm):
    """
    test to enable exclusion and assign frequency as monthly and day_of_month as default
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115621,
            'creation_date': 1615115621,
            'members': '127.0.0.1',
            'description': '',
            'name': 'b7564389-71c3-4e24-b88e-cc79c67e180d',
            'id': 66,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/66',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115621,
            'creation_date': 1615115621,
            'members': '127.0.0.1',
            'description': '',
            'name': 'b7564389-71c3-4e24-b88e-cc79c67e180d',
            'id': 66,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/66',
        json={
            'schedule': {
                'endtime': '2021-03-07 12:13:41',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 2, 'bymonthday': 7},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-07 11:13:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615115624,
            'creation_date': 1615115621,
            'members': '127.0.0.1',
            'description': '',
            'name': 'b7564389-71c3-4e24-b88e-cc79c67e180d',
            'id': 66,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/66')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='monthly',
        interval=2,
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == 2
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_enable_false_to_monthly_valassigned(tvm):
    """
    test to enable exclusion and assign frequency as monthly and day_of_month as defined
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976792,
            'creation_date': 1614976792,
            'members': '127.0.0.1',
            'description': '',
            'name': '583ffd7d-00ea-4b8f-a8c7-04c96ba0f5e4',
            'id': 43,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/43',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976792,
            'creation_date': 1614976792,
            'members': '127.0.0.1',
            'description': '',
            'name': '583ffd7d-00ea-4b8f-a8c7-04c96ba0f5e4',
            'id': 43,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/43',
        json={
            'schedule': {
                'endtime': '2021-03-05 21:39:52',
                'enabled': True,
                'rrules': {'freq': 'MONTHLY', 'interval': 2, 'bymonthday': 8},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 20:39:52',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976796,
            'creation_date': 1614976792,
            'members': '127.0.0.1',
            'description': '',
            'name': '583ffd7d-00ea-4b8f-a8c7-04c96ba0f5e4',
            'id': 43,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/43')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        frequency='monthly',
        interval=2,
        day_of_month=8,
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'MONTHLY'
    assert resp['schedule']['rrules']['interval'] == 2
    assert resp['schedule']['rrules']['bymonthday'] == 8
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_freq_onetime_to_yearly(tvm, exclusion):
    """
    test to edit exclusion frequency from onetime to yearly
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976517,
            'creation_date': 1614976517,
            'members': '127.0.0.1',
            'description': '',
            'name': 'e55e8062-8042-49d8-9769-38bb8036d152',
            'id': 5412,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/5412',
        json={
            'schedule': {
                'endtime': '2018-12-07 00:19:41',
                'enabled': True,
                'rrules': {'freq': 'YEARLY', 'interval': 2},
                'timezone': 'Etc/UTC',
                'starttime': '2018-12-06 23:19:41',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614976520,
            'creation_date': 1614976517,
            'members': '127.0.0.1',
            'description': '',
            'name': '118b333d-ed9a-4ade-9033-2c414432d934',
            'id': 5412,
        },
    )
    resp = tvm.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='yearly', interval=2
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['freq'] == 'YEARLY'
    assert resp['schedule']['rrules']['interval'] == 2


@responses.activate
def test_exclusions_edit_enable_true_exclusion(tvm):
    """
    test to enable exclusion
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614938509,
            'creation_date': 1614938509,
            'members': '127.0.0.1',
            'description': '',
            'name': 'f7de5147-253a-4c04-b4c7-4c9cb1bb7d06',
            'id': 12,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/12',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614938509,
            'creation_date': 1614938509,
            'members': '127.0.0.1',
            'description': '',
            'name': 'f7de5147-253a-4c04-b4c7-4c9cb1bb7d06',
            'id': 12,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/12',
        json={
            'schedule': {
                'endtime': '2021-03-05 11:01:49',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-05 10:01:49',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614938513,
            'creation_date': 1614938509,
            'members': '127.0.0.1',
            'description': '',
            'name': 'f7de5147-253a-4c04-b4c7-4c9cb1bb7d06',
            'id': 12,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/12')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_interval_exclusion_valdefault(tvm):
    """
    test to enable exclusion and assign default interval value
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892612,
            'creation_date': 1615892612,
            'members': '127.0.0.1',
            'description': '',
            'name': '0eac52a6-548d-458d-9551-6fd1a356c259',
            'id': 67,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/67',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892612,
            'creation_date': 1615892612,
            'members': '127.0.0.1',
            'description': '',
            'name': '0eac52a6-548d-458d-9551-6fd1a356c259',
            'id': 67,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/67',
        json={
            'schedule': {
                'endtime': '2021-03-16 12:03:33',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 1},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-16 11:03:33',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892615,
            'creation_date': 1615892612,
            'members': '127.0.0.1',
            'description': '',
            'name': '0eac52a6-548d-458d-9551-6fd1a356c259',
            'id': 67,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/67')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['interval'] == 1
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_interval_exclusion_valassigned(tvm):
    """
    test to enable exclusion and assign defined interval value
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892626,
            'creation_date': 1615892626,
            'members': '127.0.0.1',
            'description': '',
            'name': 'ef7fba6d-f513-47ca-9f20-ae8d28f088cb',
            'id': 68,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/68',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892626,
            'creation_date': 1615892626,
            'members': '127.0.0.1',
            'description': '',
            'name': 'ef7fba6d-f513-47ca-9f20-ae8d28f088cb',
            'id': 68,
        },
    )
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/68',
        json={
            'schedule': {
                'endtime': '2021-03-16 12:03:46',
                'enabled': True,
                'rrules': {'freq': 'ONETIME', 'interval': 3},
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-16 11:03:46',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892629,
            'creation_date': 1615892626,
            'members': '127.0.0.1',
            'description': '',
            'name': 'ef7fba6d-f513-47ca-9f20-ae8d28f088cb',
            'id': 68,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/68')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(
        exclusion['id'],
        enabled=True,
        interval=3,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['interval'] == 3
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_interval_exclusion_valavailable(tvm):
    """
    test to edit exclusion and assign existing interval value
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': '2021-03-16 12:03:59',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': 2,
                    'byweekday': 'SU,MO,TU,WE,TH,FR,SA',
                },
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-16 11:03:59',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892641,
            'creation_date': 1615892641,
            'members': '127.0.0.1',
            'description': '',
            'name': 'ad0e4d5e-4bb9-4bb9-acce-4530036e9b01',
            'id': 69,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/69',
        json={
            'schedule': {
                'endtime': '2021-03-16 12:03:59',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': 2,
                    'byweekday': 'SU,MO,TU,WE,TH,FR,SA',
                },
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-16 11:03:59',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892641,
            'creation_date': 1615892641,
            'members': '127.0.0.1',
            'description': '',
            'name': 'ad0e4d5e-4bb9-4bb9-acce-4530036e9b01',
            'id': 69,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/69',
        json={
            'schedule': {
                'endtime': '2021-03-16 12:03:59',
                'enabled': True,
                'rrules': {
                    'freq': 'WEEKLY',
                    'interval': 2,
                    'byweekday': 'SU,MO,TU,WE,TH,FR,SA',
                },
                'timezone': 'Etc/UTC',
                'starttime': '2021-03-16 11:03:59',
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1615892643,
            'creation_date': 1615892641,
            'members': '127.0.0.1',
            'description': '',
            'name': 'ad0e4d5e-4bb9-4bb9-acce-4530036e9b01',
            'id': 69,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/69')
    exclusion = tvm.exclusions.create(
        str(uuid.uuid4()),
        ['127.0.0.1'],
        enabled=True,
        frequency='Weekly',
        interval=2,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    resp = tvm.exclusions.edit(exclusion['id'])
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    check(resp['schedule'], 'endtime', 'datetime')
    check(resp['schedule'], 'rrules', dict)
    check(resp['schedule']['rrules'], 'freq', str)
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule'], 'starttime', 'datetime')
    check(resp['schedule'], 'timezone', str)
    assert resp['schedule']['rrules']['interval'] == 2
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_edit_enabled_false_exclusion(tvm):
    """
    test to edit enabled false exclusion
    """
    responses.add(
        responses.POST,
        'https://nourl/exclusions',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614977237,
            'creation_date': 1614977237,
            'members': '127.0.0.1',
            'description': '',
            'name': '4d830cda-4a1b-4b9c-a96c-27d8929c40e2',
            'id': 45,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/exclusions/45',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614977237,
            'creation_date': 1614977237,
            'members': '127.0.0.1',
            'description': '',
            'name': '4d830cda-4a1b-4b9c-a96c-27d8929c40e2',
            'id': 45,
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/exclusions/45',
        json={
            'schedule': {
                'endtime': None,
                'enabled': False,
                'rrules': None,
                'timezone': None,
                'starttime': None,
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_modification_date': 1614977240,
            'creation_date': 1614977237,
            'members': '127.0.0.2',
            'description': '',
            'name': '4d830cda-4a1b-4b9c-a96c-27d8929c40e2',
            'id': 45,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/exclusions/45')
    exclusion = tvm.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = tvm.exclusions.edit(exclusion['id'], members=['127.0.0.2'])
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    tvm.exclusions.delete(resp['id'])


@responses.activate
def test_exclusions_list(tvm):
    """
    test to list exclusions
    """
    responses.add(responses.GET, 'https://nourl/exclusions', json={'exclusions': []})
    items = tvm.exclusions.list()
    assert isinstance(items, list)
    for exclusion in items:
        check(exclusion, 'description', str, allow_none=True)
        check(exclusion, 'id', int)
        check(exclusion, 'last_modification_date', int)
        check(exclusion, 'members', str)
        check(exclusion, 'name', str)
        check(exclusion, 'schedule', dict)
        check(exclusion['schedule'], 'enabled', bool)
        if exclusion['schedule']['enabled'] is True:
            check(exclusion['schedule'], 'endtime', 'datetime')
            check(exclusion['schedule'], 'rrules', dict)
            check(exclusion['schedule']['rrules'], 'freq', str)
            check(exclusion['schedule']['rrules'], 'interval', int)
            check(exclusion['schedule'], 'starttime', 'datetime')
            check(exclusion['schedule'], 'timezone', str)


@responses.activate
def test_exclusion_import_exclusion(tvm):
    """
    test to import exclusion from file
    """
    responses.add(
        responses.POST,
        'https://nourl/file/upload',
        json={'fileuploaded': 'exclusion-c3563adf-2a06-45e1-85c9-081fe9e683c4.csv'},
    )
    responses.add(responses.POST, 'https://nourl/exclusions/import')
    header = 'id,name,description,members,creation_date,last_modification_date'
    data = '1,"Test-Exclusion","test","127.0.0.1",1617703622,1617789521'

    # create path and dynamic filename
    filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'test_files',
        'exclusion-' + str(uuid.uuid4()) + '.csv',
    )

    # creating file for import
    with open(filename, 'w') as csvfile:
        csvfile.write(header)
        csvfile.write('\n')
        csvfile.write(data)

    # import created file using API call
    try:
        with open(filename, 'r') as fobj:
            tvm.exclusions.exclusions_import(fobj)
    except BadRequestError:
        raise
    finally:
        # remove created file
        os.remove(filename)
