'''
test exclusions
'''
import os
import uuid
from datetime import datetime, timedelta
import pytest
from tenable.errors import NotFoundError, UnexpectedValueError, PermissionError
from tests.checker import check
from tests.io.test_networks import fixture_network

@pytest.fixture(name='exclusion')
@pytest.mark.vcr()
def fixture_exclusion(request, api):
    '''
    Fixture to create exclusion
    '''
    excl = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))
    def teardown():
        '''
        cleanup function to delete exclusion
        '''
        try:
            api.exclusions.delete(excl['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return excl

@pytest.mark.vcr()
def test_exclusions_create_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(1, ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_members_typeerror(api):
    '''
    test to raise exception when type of members param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), '127.0.0.1',
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_start_time_typeerror(api):
    '''
    test to raise exception when type of start_time param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), ['127.0.0.1'],
            start_time='now',
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_end_time_typeerror(api):
    '''
    test to raise exception when type of end_time param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time='later')

@pytest.mark.vcr()
def test_exclusions_create_timezone_typeerror(api):
    '''
    test to raise exception when type of timezone param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            timezone=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_timezone_unexpectedvalue(api):
    '''
    test to raise exception when timezone param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            timezone='the zone of time',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_description_typeerror(api):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            description=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_frequency_typeerror(api):
    '''
    test to raise exception when type of frequency param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            frequency=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_frequency_unexpectedvalue(api):
    '''
    test to raise exception when frequency param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            frequency='nope',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_interval_typeerror(api):
    '''
    test to raise exception when type of interval param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            interval='nope',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_weekdays_typeerror(api):
    '''
    test to raise exception when type of weekdays param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            weekdays='nope',
            frequency='weekly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_weekdays_unexpectedvalue(api):
    '''
    test to raise exception when weekdays param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            weekdays=['MO', 'WE', 'nope'],
            frequency='weekly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_day_of_month_typeerror(api):
    '''
    test to raise exception when type of day_of_month param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            day_of_month='nope',
            frequency='monthly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_day_of_month_unexpectedvalue(api):
    '''
    test to raise exception when day_of_month param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            day_of_month=82,
            frequency='monthly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_enabled_typeerror(api):
    '''
    test to raise exception when type of enabled param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled='yup')

@pytest.mark.vcr()
def test_exclusions_create_standard_user_permissionerror(stdapi):
    '''
    test to raise exception when standard_user tries to create exclusion.
    '''
    with pytest.raises(PermissionError):
        stdapi.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_unexpectedvalueerror(api):
    '''
    test to raise exception when network_id param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1),
            network_id='nope')

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_typeerror(api):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1),
            network_id=1)

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_notfounderror(api):
    '''
    test to raise exception when network_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1),
            network_id='00000000-0000-0000-0000-100000000001')

@pytest.mark.vcr()
def test_exclusions_create_onetime_exclusion(api):
    '''
    test to create exclusion with frequency onetime
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_daily_exclusion(api):
    '''
    test to create exclusion with frequency daily
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='daily')
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_weekly_exclusion(api):
    '''
    test to create exclusion with frequency weekly
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='weekly',
        weekdays=['mo', 'we', 'fr'])
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_monthly_exclusion(api):
    '''
    test to create exclusion with frequency monthly
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='monthly',
        day_of_month=15)
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_yearly_exclusion(api):
    '''
    test to create exclusion with frequency yearly
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='yearly')
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_enabled_false_exclusion(api):
    '''
    test to create exclusion with enabled param as false
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    assert resp['schedule']['enabled'] is False
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_exclusion(api, network):
    '''
    test to create exclusion and apply to user defined network_id
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='yearly',
        network_id=network['uuid'])
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
    details = api.exclusions.details(resp['id'])
    assert details['network_id'] == network['uuid']
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_with_default_network_exclusion(api):
    '''
    test to create exclusion with default network_id
    '''
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='yearly')
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
    details = api.exclusions.details(resp['id'])
    assert details['network_id'] == '00000000-0000-0000-0000-000000000000'
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_delete_notfounderror(api):
    '''
    test to raise exception when exclusion_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.exclusions.delete(999999)

@pytest.mark.vcr()
def test_exclusions_delete_exclusion(api, exclusion):
    '''
    test to delete exclusion
    '''
    api.exclusions.delete(exclusion['id'])

@pytest.mark.vcr()
def test_exclusions_delete_standard_user_fail(stdapi, exclusion):
    '''
    test to raise exception when standard user try to delete exclusion.
    '''
    with pytest.raises(PermissionError):
        stdapi.exclusions.delete(exclusion['id'])

@pytest.mark.vcr()
def test_exclusions_edit_no_exclusion_id_typeerror(api):
    '''
    test to raise exception when exclusion_id is not provided.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit()

@pytest.mark.vcr()
def test_exclusions_edit_exclusion_id_typeerror(api):
    '''
    test to raise exception when type of exclusion_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit('nope')

@pytest.mark.vcr()
def test_exclusions_edit_members_typeerror(api, exclusion):
    '''
    test to raise exception when type of members param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], members='192.168.0.1')

@pytest.mark.vcr()
def test_exclusions_edit_name_typeerror(api, exclusion):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], name=1.02)

@pytest.mark.vcr()
def test_exclusions_edit_starttime_typerror(api, exclusion):
    '''
    test to raise exception when type of start time param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], start_time='nope')

@pytest.mark.vcr()
def test_exclusions_edit_timezone_typerror(api, exclusion):
    '''
    test to raise exception when type of timezone param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], timezone=1)

@pytest.mark.vcr()
def test_exclusions_edit_timezone_unexpectedvalue(api, exclusion):
    '''
    test to raise exception when timezone param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], timezone='nope')

@pytest.mark.vcr()
def test_exclusions_edit_description_typerror(api, exclusion):
    '''
    test to raise exception when type of description param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], description=1)

@pytest.mark.vcr()
def test_exclusions_edit_frequency_typerror(api, exclusion):
    '''
    test to raise exception when type of frequency param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency=1)

@pytest.mark.vcr()
def test_exclusions_edit_frequency_unexpectedvalue(api, exclusion):
    '''
    test to raise exception when frequency param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='nope')

@pytest.mark.vcr()
def test_exclusions_edit_interval_typerror(api, exclusion):
    '''
    test to raise exception when type of interval param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], interval='nope')

@pytest.mark.vcr()
def test_exclusions_edit_weekdays_typerror(api, exclusion):
    '''
    test to raise exception when type of weekdays param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency='Weekly', weekdays='nope')

@pytest.mark.vcr()
def test_exclusions_edit_weekdays_unexpectedvalue(api, exclusion):
    '''
    test to raise exception when weekdays param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='Weekly', weekdays=['MO', 'WE', 'nope'])

@pytest.mark.vcr()
def test_exclusions_edit_dayofmonth_typerror(api, exclusion):
    '''
    test to raise exception when type of day_of_month param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency='monthly', day_of_month='nope')

@pytest.mark.vcr()
def test_exclusions_edit_dayofmonth_unexpectedvalue(api, exclusion):
    '''
    test to raise exception when day_of_month param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='monthly', day_of_month=0)

@pytest.mark.vcr()
def test_exclusions_edit_standard_user_permission_error(stdapi, exclusion):
    '''
    test to raise exception when standard user try to edit exclusion.
    '''
    with pytest.raises(PermissionError):
        stdapi.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_exclusions_edit_network_select_notfounderror(api, exclusion):
    '''
    test to raise exception when user provided network_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.exclusions.edit(exclusion['id'], network_id='00000000-0000-0000-0000-100000000001')

@pytest.mark.vcr()
def test_exclusions_edit_network_select_unexpectedvalueerror(api, exclusion):
    '''
    test to raise exception when network_id param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], network_id='nope')

@pytest.mark.vcr()
def test_exclusions_edit_network_select_typeerror(api, exclusion):
    '''
    test to raise exception when type of network_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], network_id=1)

@pytest.mark.vcr()
def test_exclusions_edit_success(api, exclusion):
    '''
    test to edit exclusion name
    '''
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))
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

@pytest.mark.vcr()
def test_exclusions_edit_network_success(api, exclusion, network):
    '''
    test to edit exclusion network
    '''
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()), network_id=network['uuid'])
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

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_daily(api, exclusion):
    '''
    test to edit exclusion frequency from onetime to daily
    '''
    resp = api.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='daily', interval=2)
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

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_weekly_valdefault(api, exclusion):
    '''
    test to edit exclusion frequency from onetime to weekly
    and assign default value to weekdays param
    '''
    resp = api.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='weekly', interval=2)
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

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_weekly_valassigned(api, exclusion):
    '''
    test to edit exclusion frequency from onetime to weekly
    and assign user defined value to weekdays param
    '''
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
        frequency='weekly', interval=2, weekdays=['TH', 'FR'])
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

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_weekly_valavailable(api):
    '''
    test to edit weekly exclusion and assign existing weekdays values to weekdays param
    '''
    exclusion = api.exclusions.create(
        str(uuid.uuid4()), ['127.0.0.1'], start_time = datetime.utcnow(),
        end_time = datetime.utcnow() + timedelta(hours=1),
        frequency='weekly', weekdays=['TH', 'FR'])
    resp = api.exclusions.edit(exclusion['id'], frequency='weekly', interval=2)
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_enable_false_to_weekly_valdefault(api):
    '''
    test to enable exclusion and assign frequency as weekly and weekdays as default
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'], enabled=True, start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1), frequency='weekly', interval=2)
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_enable_false_to_weekly_valassigned(api):
    '''
    test to enable exclusion and assign frequency as weekly and weekdays as defined
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(
        exclusion['id'], enabled=True, start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='weekly', interval=2, weekdays=['TH', 'FR'])
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_monthly_valddefault(api, exclusion):
    '''
    test to edit exclusion frequency from onetime to monthly
    and assign default value to day_of_month param
    '''
    resp = api.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='monthly', interval=2)
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

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_monthly_valassigned(api, exclusion):
    '''
    test to edit exclusion frequency from onetime to monthly
    and assign user defined value to day_of_month param
    '''
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
        frequency='monthly', interval=2, day_of_month=8)
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

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_monthly_valavailable(api):
    '''
    test to edit exclusion and assign existing day_of_month value to day_of_month param
    '''
    exclusion = api.exclusions.create\
        (str(uuid.uuid4()), ['127.0.0.1'], start_time = datetime.utcnow(),
        end_time = datetime.utcnow() + timedelta(hours=1), frequency='monthly', day_of_month=8)
    resp = api.exclusions.edit(exclusion['id'], frequency='monthly', interval=2)
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_enable_false_to_monthly_valdefault(api):
    '''
    test to enable exclusion and assign frequency as monthly and day_of_month as default
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'], enabled=True, start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1), frequency='monthly', interval=2)
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_enable_false_to_monthly_valassigned(api):
    '''
    test to enable exclusion and assign frequency as monthly and day_of_month as defined
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(
        exclusion['id'], enabled=True, start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='monthly', interval=2, day_of_month=8)
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_freq_onetime_to_yearly(api, exclusion):
    '''
    test to edit exclusion frequency from onetime to yearly
    '''
    resp = api.exclusions.edit(
        exclusion['id'], name=str(uuid.uuid4()), frequency='yearly', interval=2)
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

@pytest.mark.vcr()
def test_exclusions_edit_enable_true_exclusion(api):
    '''
    test to enable exclusion
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'], enabled=True, start_time = datetime.utcnow(),
        end_time = datetime.utcnow() + timedelta(hours=1))
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_interval_exclusion_valdefault(api):
    '''
    test to enable exclusion and assign default interval value
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'], enabled=True,
        start_time = datetime.utcnow(), end_time = datetime.utcnow() + timedelta(hours=1))
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_interval_exclusion_valassigned(api):
    '''
    test to enable exclusion and assign defined interval value
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'], enabled=True, interval=3,
        start_time = datetime.utcnow(), end_time = datetime.utcnow() + timedelta(hours=1))
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_interval_exclusion_valavailable(api):
    '''
    test to edit exclusion and assign existing interval value
    '''
    exclusion = api.exclusions.create(
        str(uuid.uuid4()), ['127.0.0.1'], enabled=True, frequency='Weekly',
        interval=2, start_time=datetime.utcnow(), end_time=datetime.utcnow() + timedelta(hours=1))
    resp = api.exclusions.edit(exclusion['id'])
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
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_edit_enabled_false_exclusion(api):
    '''
    test to edit enabled false exclusion
    '''
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'], members=['127.0.0.2'])
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_list(api):
    '''
    test to list exclusions
    '''
    items = api.exclusions.list()
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

@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'io_exclusion.csv'))
def test_exclusion_import_exclusion(api, datafiles):
    '''
    test to import exclusion from file
    '''
    with open(os.path.join(str(datafiles), 'io_exclusion.csv'), 'rb') as fobj:
        api.exclusions.exclusions_import(fobj)
