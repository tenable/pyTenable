from datetime import datetime, timedelta
from tenable.errors import *
from ..checker import check, single
from tests.io.test_networks import network
import uuid, pytest

@pytest.fixture
@pytest.mark.vcr()
def exclusion(request, api):
    excl = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))
    def teardown():
        try:
            api.exclusions.delete(excl['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return excl

@pytest.mark.vcr()
def test_exclusions_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(1, ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_members_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), '127.0.0.1',
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_start_time_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), ['127.0.0.1'],
            start_time='now',
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_end_time_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time='later')

@pytest.mark.vcr()
def test_exclusions_create_timezone_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            timezone=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_timezone_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            timezone='the zone of time',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_description_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            description=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_frequency_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            frequency=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_frequency_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            frequency='nope',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_interval_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            interval='nope',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_weekdays_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            weekdays='nope',
            frequency='weekly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_weekdays_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            weekdays=['MO', 'WE', 'nope'],
            frequency='weekly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_day_of_month_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            day_of_month='nope',
            frequency='monthly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_day_of_month_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            day_of_month=82,
            frequency='monthly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled='yup')

@pytest.mark.vcr()
def test_exclusions_create_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1),
            network_id='nope')

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1),
            network_id=1)

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1),
            network_id='00000000-0000-0000-0000-100000000001')

@pytest.mark.vcr()
def test_exclusions_create_onetime_exclusion(api):
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
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    assert isinstance(resp, dict)
    check(resp, 'description', str, allow_none=True)
    check(resp, 'id', int)
    check(resp, 'last_modification_date', int)
    check(resp, 'members', str)
    check(resp, 'name', str)
    check(resp, 'schedule', dict)
    check(resp['schedule'], 'enabled', bool)
    assert resp['schedule']['enabled'] == False
    api.exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_exclusions_create_with_selected_network_exclusion(api, network):
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
    with pytest.raises(NotFoundError):
        api.exclusions.delete(999999)

@pytest.mark.vcr()
def test_exclusions_delete_exclusion(api, exclusion):
    api.exclusions.delete(exclusion['id'])

@pytest.mark.vcr()
def test_exclusions_delete_standard_user_fail(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.exclusions.delete(exclusion['id'])

@pytest.mark.vcr()
def test_exclusions_edit_no_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.edit()

@pytest.mark.vcr()
def test_exclusions_edit_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.edit('nope')

@pytest.mark.vcr()
def test_exclusions_edit_members_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], members='192.168.0.1')

@pytest.mark.vcr()
def test_exclusions_edit_name_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], name=1.02)

@pytest.mark.vcr()
def test_exclusions_edit_starttime_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], start_time='nope')

@pytest.mark.vcr()
def test_exclusions_edit_timezone_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], timezone=1)

@pytest.mark.vcr()
def test_exclusions_edit_timezone_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], timezone='nope')

@pytest.mark.vcr()
def test_exclusions_edit_description_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], description=1)

@pytest.mark.vcr()
def test_exclusions_edit_frequency_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency=1)

@pytest.mark.vcr()
def test_exclusions_edit_frequency_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='nope')

@pytest.mark.vcr()
def test_exclusions_edit_interval_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], interval='nope')

@pytest.mark.vcr()
def test_exclusions_edit_weekdays_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency='Weekly', weekdays='nope')

@pytest.mark.vcr()
def test_exclusions_edit_weekdays_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='Weekly', weekdays=['MO', 'WE', 'nope'])

@pytest.mark.vcr()
def test_exclusions_edit_dayofmonth_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency='monthly', day_of_month='nope')

@pytest.mark.vcr()
def test_exclusions_edit_dayofmonth_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='monthly', day_of_month=0)

@pytest.mark.vcr()
def test_exclusions_edit_standard_user_permission_error(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_exclusions_edit_network_select_notfounderror(api, exclusion):
    with pytest.raises(NotFoundError):
        api.exclusions.edit(exclusion['id'], network_id='00000000-0000-0000-0000-100000000001')

@pytest.mark.vcr()
def test_exclusions_edit_network_select_unexpectedvalueerror(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], network_id='nope')

@pytest.mark.vcr()
def test_exclusions_edit_network_select_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], network_id=1)

@pytest.mark.vcr()
def test_exclusions_edit_success(api, exclusion):
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
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
                               frequency='daily',
                               interval=2)

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
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
                               frequency='weekly',
                               interval=2)
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
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
                               frequency='weekly',
                               interval=2,
                               weekdays=['TH', 'FR'])
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
                                      start_time = datetime.utcnow(),
                                      end_time = datetime.utcnow() + timedelta(hours=1),
                                      frequency='weekly', weekdays=['TH', 'FR'])
    resp = api.exclusions.edit(exclusion['id'],
                               frequency='weekly',
                               interval=2)
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'],
                               enabled=True,
                               start_time=datetime.utcnow(),
                               end_time=datetime.utcnow() + timedelta(hours=1),
                               frequency='weekly',
                               interval=2)
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'],
                               enabled=True,
                               start_time=datetime.utcnow(),
                               end_time=datetime.utcnow() + timedelta(hours=1),
                               frequency='weekly',
                               interval=2,
                               weekdays=['TH', 'FR'])
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
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
                               frequency='monthly',
                               interval=2)
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
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
                               frequency='monthly',
                               interval=2,
                               day_of_month=8)
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
                                      start_time = datetime.utcnow(),
                                      end_time = datetime.utcnow() + timedelta(hours=1),
                                      frequency='monthly', day_of_month=8)
    resp = api.exclusions.edit(exclusion['id'],
                               frequency='monthly',
                               interval=2)
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'],
                               enabled=True,
                               start_time=datetime.utcnow(),
                               end_time=datetime.utcnow() + timedelta(hours=1),
                               frequency='monthly',
                               interval=2)
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'],
                               enabled=True,
                               start_time=datetime.utcnow(),
                               end_time=datetime.utcnow() + timedelta(hours=1),
                               frequency='monthly',
                               interval=2,
                               day_of_month=8)
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
    resp = api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()),
                               frequency='yearly',
                               interval=2)
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
    exclusion = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled=False)
    resp = api.exclusions.edit(exclusion['id'],
                               enabled=True,
                               start_time = datetime.utcnow(),
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
def test_exclusions_edit_enabled_false_exclusion(api):
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
        if exclusion['schedule']['enabled'] == True:
            check(exclusion['schedule'], 'endtime', 'datetime')
            check(exclusion['schedule'], 'rrules', dict)
            check(exclusion['schedule']['rrules'], 'freq', str)
            check(exclusion['schedule']['rrules'], 'interval', int)
            check(exclusion['schedule'], 'starttime', 'datetime')
            check(exclusion['schedule'], 'timezone', str)