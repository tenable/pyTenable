from datetime import datetime, timedelta
from fixtures import *
from tenable.errors import *
import uuid

@pytest.fixture
def exclusion(request, api):
    excl = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))
    def teardown():
        try:
            api.agent_exclusions.delete(excl['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return excl

def test_create_no_times(api):
    with pytest.raises(AttributeError):
        api.agent_exclusions.create(str(uuid.uuid4()))

def test_create_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            scanner_id='nope',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(1.02,
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_starttime_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            start_time='fail', 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_endtime_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            start_time=datetime.utcnow(), 
            end_time='nope')

def test_create_timezone_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            timezone=1,
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_timezone_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            timezone='not a real timezone',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_description_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            description=True,
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_frequency_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            frequency=True,
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_frequency_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            frequency='nope',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_interval_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            interval='nope',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_weekdays_typerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            weekdays='nope',
            frequency='weekly',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_weekdays_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            weekdays=['MO', 'TU', 'nope'],
            frequency='weekly',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_dayofmonth_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            day_of_month='nope',
            frequency='monthly',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_dayofmonth_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.create(str(uuid.uuid4()),
            day_of_month=0,
            frequency='monthly',
            start_time=datetime.utcnow(), 
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_create_onetime_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1))
    assert isinstance(resp, dict)
    api.agent_exclusions.delete(resp['id'])

def test_create_daily_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='daily')
    assert isinstance(resp, dict)
    api.agent_exclusions.delete(resp['id'])

def test_create_weekly_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='weekly',
        weekdays=['mo', 'we', 'fr'])
    assert isinstance(resp, dict)
    api.agent_exclusions.delete(resp['id'])

def test_create_monthly_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='monthly',
        day_of_month=15)
    assert isinstance(resp, dict)
    api.agent_exclusions.delete(resp['id'])

def test_create_yearly_exclusion(api):
    resp = api.agent_exclusions.create(str(uuid.uuid4()),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        frequency='yearly')
    assert isinstance(resp, dict)
    api.agent_exclusions.delete(resp['id'])

def test_create_standard_users_cant_create(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_exclusions.create(str(uuid.uuid4()),
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=1))

def test_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.agent_exclusions.delete(123)

def test_delete_exclusion(api, exclusion):
    api.agent_exclusions.delete(exclusion['id'])

def test_delete_standard_user_fail(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.agent_exclusions.delete(exclusion['id'])

def test_edit_no_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit()

def test_edit_exclusion_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit('nope')

def test_edit_scanner_id_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], scanner_id='nope')

def test_edit_name_typeerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], name=1.02)

def test_edit_starttime_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], start_time='nope')

def test_edit_timezone_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], timezone=1)

def test_edit_timezone_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(exclusion['id'], timezone='nope')

def test_edit_description_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], description=1)

def test_edit_frequency_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], frequency=1)

def test_edit_frequency_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(exclusion['id'], frequency='nope')

def test_edit_interval_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], interval='nope')

def test_edit_weekdays_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], weekdays='nope')

def test_edit_weekdays_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(exclusion['id'], weekdays=['MO', 'WE', 'nope'])

def test_edit_dayofmonth_typerror(api, exclusion):
    with pytest.raises(TypeError):
        api.agent_exclusions.edit(exclusion['id'], day_of_month='nope')

def test_edit_dayofmonth_unexpectedvalue(api, exclusion):
    with pytest.raises(UnexpectedValueError):
        api.agent_exclusions.edit(exclusion['id'], day_of_month=0)

def test_edit_standard_user_permission_error(stdapi, exclusion):
    with pytest.raises(PermissionError):
        stdapi.agent_exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

def test_edit_success(api, exclusion):
    api.agent_exclusions.edit(exclusion['id'], name=str(uuid.uuid4()))

def test_list_blackouts(api, exclusion):
    items = api.agent_exclusions.list()
    assert isinstance(items, list)
    assert exclusion in items