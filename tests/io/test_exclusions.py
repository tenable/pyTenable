from datetime import datetime, timedelta
from tenable.errors import *
from ..checker import check, single
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
        api.exclusions.create(1, ['127.0.0.1'])

@pytest.mark.vcr()
def test_exclusions_create_members_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), '127.0.0.1')

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
        api.exclusions.edit(exclusion['id'], weekdays='nope')

@pytest.mark.vcr()
def test_exclusions_edit_weekdays_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], weekdays=['MO', 'WE', 'nope'])

@pytest.mark.vcr()
def test_exclusions_edit_dayofmonth_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], day_of_month='nope')

@pytest.mark.vcr()
def test_exclusions_edit_dayofmonth_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], day_of_month=0)

@pytest.mark.vcr()
def test_exclusions_edit_standard_user_permission_error(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

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
        check(exclusion['schedule'], 'endtime', 'datetime')
        check(exclusion['schedule'], 'rrules', dict)
        check(exclusion['schedule']['rrules'], 'freq', str)
        check(exclusion['schedule']['rrules'], 'interval', int)
        check(exclusion['schedule'], 'starttime', 'datetime')
        check(exclusion['schedule'], 'timezone', str)