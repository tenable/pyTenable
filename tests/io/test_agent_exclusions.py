from datetime import datetime as dtime, timedelta
from tenable.errors import *
from ..checker import check, single
import uuid, pytest

@pytest.fixture
@pytest.mark.vcr()
def agentexclusion(request, api):
    excl = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=dtime.utcnow(),
        end_time=dtime.utcnow() + timedelta(hours=1))
    def teardown():
        try:
            api.agent_exclusions.delete(excl['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return excl

@pytest.mark.vcr()
def test_agentexclusions_create_no_times(api):
    with pytest.raises(AttributeError):
        api.agent_exclusions.create(str(uuid.uuid4()))

@pytest.mark.vcr()
def test_agentexclusions_create_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            scanner_id='nope',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(1.02,
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_starttime_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            start_time='fail', 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_endtime_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            start_time=dtime.utcnow(), 
            end_time='nope')

@pytest.mark.vcr()
def test_agentexclusions_create_timezone_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            timezone=1,
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_timezone_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            timezone='not a real timezone',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_description_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            description=True,
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_frequency_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            frequency=True,
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_frequency_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            frequency='nope',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_interval_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            interval='nope',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_weekdays_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            weekdays='nope',
            frequency='weekly',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_weekdays_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            weekdays=['MO', 'TU', 'nope'],
            frequency='weekly',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_dayofmonth_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            day_of_month='nope',
            frequency='monthly',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_dayofmonth_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            day_of_month=0,
            frequency='monthly',
            start_time=dtime.utcnow(), 
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_create_onetime_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=dtime.utcnow(),
        end_time=dtime.utcnow() + timedelta(hours=1))
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
    check(resp['schedule']['rrules'], 'interval', int)
    api.agent_exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_agentexclusions_create_daily_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=dtime.utcnow(),
        end_time=dtime.utcnow() + timedelta(hours=1),
        frequency='daily')
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
    check(resp['schedule']['rrules'], 'interval', int)
    api.agent_exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_agentexclusions_create_weekly_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=dtime.utcnow(),
        end_time=dtime.utcnow() + timedelta(hours=1),
        frequency='weekly',
        weekdays=['mo', 'we', 'fr'])
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
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule']['rrules'], 'byweekday', str)
    api.agent_exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_agentexclusions_create_monthly_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=dtime.utcnow(),
        end_time=dtime.utcnow() + timedelta(hours=1),
        frequency='monthly',
        day_of_month=15)
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
    check(resp['schedule']['rrules'], 'interval', int)
    check(resp['schedule']['rrules'], 'bymonthday', int)
    api.agent_exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_agentexclusions_create_yearly_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=dtime.utcnow(),
        end_time=dtime.utcnow() + timedelta(hours=1),
        frequency='yearly')
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
    check(resp['schedule']['rrules'], 'interval', int)
    api.agent_exclusions.delete(resp['id'])

@pytest.mark.vcr()
def test_agentexclusions_create_standard_users_cant_create(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_exclusions.create(str(uuid.uuid4()),
            start_time=dtime.utcnow(),
            end_time=dtime.utcnow() + timedelta(hours=1))

@pytest.mark.vcr()
def test_agentexclusions_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.agent_exclusions.delete(123)

@pytest.mark.vcr()
def test_agentexclusions_delete_exclusion(api, agentexclusion):
    api.agent_exclusions.delete(agentexclusion['id'])

@pytest.mark.vcr()
def test_agentexclusions_delete_standard_user_fail(stdapi, agentexclusion):
    with pytest.raises(PermissionError):
        stdapi.agent_exclusions.delete(agentexclusion['id'])

@pytest.mark.vcr()
def test_agentexclusions_edit_no_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit()

@pytest.mark.vcr()
def test_agentexclusions_edit_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit('nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_scanner_id_typeerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], scanner_id='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_name_typeerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], name=1.02)

@pytest.mark.vcr()
def test_agentexclusions_edit_starttime_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], start_time='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_timezone_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], timezone=1)

@pytest.mark.vcr()
def test_agentexclusions_edit_timezone_unexpectedvalue(api, agentexclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(agentexclusion['id'], timezone='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_description_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], description=1)

@pytest.mark.vcr()
def test_agentexclusions_edit_frequency_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], frequency=1)

@pytest.mark.vcr()
def test_agentexclusions_edit_frequency_unexpectedvalue(api, agentexclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(agentexclusion['id'], frequency='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_interval_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], interval='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_weekdays_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], weekdays='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_weekdays_unexpectedvalue(api, agentexclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(agentexclusion['id'], weekdays=['MO', 'WE', 'nope'])

@pytest.mark.vcr()
def test_agentexclusions_edit_dayofmonth_typerror(api, agentexclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(agentexclusion['id'], day_of_month='nope')

@pytest.mark.vcr()
def test_agentexclusions_edit_dayofmonth_unexpectedvalue(api, agentexclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(agentexclusion['id'], day_of_month=0)

@pytest.mark.vcr()
def test_agentexclusions_edit_standard_user_permission_error(stdapi, agentexclusion):
    with pytest.raises(PermissionError):
        stdapi.agent_exclusions.edit(agentexclusion['id'], name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_agentexclusions_edit_success(api, agentexclusion):
    api.agent_exclusions.edit(agentexclusion['id'], name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_agentexclusions_list_blackouts(api, agentexclusion):
    items = api.agent_exclusions.list()
    assert isinstance(items, list)
    a = items[0]
    