from .fixtures import *
from datetime import datetime, timedelta
from tenable.errors import *

@pytest.fixture
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

def test_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(1, ['127.0.0.1'])

def test_create_members_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), '127.0.0.1')

def test_create_start_time_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), ['127.0.0.1'],
            start_time='now',
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_end_time_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time='later')

def test_create_timezone_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            timezone=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_timezone_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            timezone='the zone of time',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_description_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            description=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_frequency_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            frequency=1,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_frequency_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            frequency='nope',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_interval_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            interval='nope',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_weekdays_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            weekdays='nope',
            frequency='weekly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_weekdays_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            weekdays=['MO', 'WE', 'nope'],
            frequency='weekly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_day_of_month_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            day_of_month='nope',
            frequency='monthly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_day_of_month_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            day_of_month=82,
            frequency='monthly',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'], enabled='yes')

def test_create_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_onetime_exclusion(api):
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))
    assert isinstance(resp, dict)
    api.exclusions.delete(resp['id'])

def test_create_daily_exclusion(api):
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='daily')
    assert isinstance(resp, dict)
    api.exclusions.delete(resp['id'])

def test_create_weekly_exclusion(api):
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='weekly',
        weekdays=['mo', 'we', 'fr'])
    assert isinstance(resp, dict)
    api.exclusions.delete(resp['id'])

def test_create_monthly_exclusion(api):
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='monthly',
        day_of_month=15)
    assert isinstance(resp, dict)
    api.exclusions.delete(resp['id'])

def test_create_yearly_exclusion(api):
    resp = api.exclusions.create(str(uuid.uuid4()), ['127.0.0.1'],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='yearly')
    assert isinstance(resp, dict)
    api.exclusions.delete(resp['id'])

def test_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.exclusions.delete(999999)

def test_delete_exclusion(api, exclusion):
    api.exclusions.delete(exclusion['id'])

def test_delete_standard_user_fail(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.exclusions.delete(exclusion['id'])

def test_edit_no_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.edit()

def test_edit_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.exclusions.edit('nope')

def test_edit_members_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], members='192.168.0.1')

def test_edit_name_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], name=1.02)

def test_edit_starttime_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], start_time='nope')

def test_edit_timezone_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], timezone=1)

def test_edit_timezone_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], timezone='nope')

def test_edit_description_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], description=1)

def test_edit_frequency_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], frequency=1)

def test_edit_frequency_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], frequency='nope')

def test_edit_interval_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], interval='nope')

def test_edit_weekdays_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], weekdays='nope')

def test_edit_weekdays_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], weekdays=['MO', 'WE', 'nope'])

def test_edit_dayofmonth_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.exclusions.edit(exclusion['id'], day_of_month='nope')

def test_edit_dayofmonth_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.exclusions.edit(exclusion['id'], day_of_month=0)

def test_edit_standard_user_permission_error(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

def test_edit_success(api, exclusion):
    api.exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

def test_list(api, exclusion):
    items = api.exclusions.list()
    assert isinstance(items, list)
    assert exclusion in items