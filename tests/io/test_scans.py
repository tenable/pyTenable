'''
test scans
'''
import uuid
import time
import os
from io import BytesIO
from sys import stdout
import pytest
from tenable.reports.nessusv2 import NessusReportv2
from tenable.errors import UnexpectedValueError, NotFoundError, InvalidInputError
from tests.checker import check, single
from tests.io.conftest import SCAN_ID_WITH_RESULTS

@pytest.fixture(name='scheduled_scan')
def fixture_scheduled_scan(request, api):
    '''
    Fixture to create scheduled scan
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True)
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )

    def teardown():
        '''
        cleanup function to delete scan
        '''
        try:
            api.scans.delete(scan['id'])
        except NotFoundError:
            pass

    request.addfinalizer(teardown)
    return scan


@pytest.mark.vcr()
def test_scan_create_scan_document_template_typeerror(api):
    '''
    test to raise exception when type of template param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        getattr(api.scans, '_create_scan_document')({'template': 123})


@pytest.mark.vcr()
def test_scan_create_scan_document_template_unexpected_value_error(api):
    '''
    test to raise exception when template param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.scans, '_create_scan_document')({'template': 'nothing_here'})


@pytest.mark.vcr()
def test_scan_create_scan_socument_template_pass(api):
    '''
    test to create scan document basic template
    '''
    templates = api.policies.templates()
    resp = getattr(api.scans, '_create_scan_document')({'template': 'basic'})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['basic']


@pytest.mark.vcr()
def test_scan_create_scan_document_policies_id_pass(api):
    '''
    test to create scan document policy param using id
    '''
    policies = api.policies.list()
    policy = policies[0]
    resp = getattr(api.scans, '_create_scan_document')({'policy': policy['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']


@pytest.mark.vcr()
def test_scan_create_scan_document_policies_name_pass(api):
    '''
    test to create scan document with policy param using name
    '''
    policies = api.policies.list()
    policy = policies[0]
    resp = getattr(api.scans, '_create_scan_document')({'policy': policy['name']})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']


# def test_scan_create_scan_document_targets

@pytest.mark.vcr()
def test_scan_create_scan_document_scanner_unexpectedvalueerror(api):
    '''
    test to raise exception when scanner param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.scans, '_create_scan_document')({'scanner': 'nothing to see here'})


@pytest.mark.vcr()
def test_scan_create_scan_document_scanner_uuid_pass(api):
    '''
    test to create scan document with scanner uuid param
    '''
    scanners = api.scanners.allowed_scanners()
    scanner = scanners[1]
    resp = getattr(api.scans, '_create_scan_document')({'scanner': scanner['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', 'scanner-uuid')
    assert resp['settings']['scanner_id'] == scanner['id']


@pytest.mark.vcr()
def test_scan_create_scan_document_scanner_name_pass(api):
    '''
    test to create scan document with scanner name param
    '''
    scanners = api.scanners.allowed_scanners()
    scanner = scanners[1]
    resp = getattr(api.scans, '_create_scan_document')({'scanner': scanner['name']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', str)
    assert resp['settings']['scanner_id'] == scanner['id']

# @pytest.mark.vcr()
# def test_scan_attachment_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.attachment('nope', 1)

@pytest.mark.vcr()
def test_scan_attachment_attachement_id_typeerror(api):
    '''
    test to raise exception when type of attachment_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.attachment(1, 'nope')


@pytest.mark.vcr()
@pytest.mark.xfail(raises=InvalidInputError)
def test_scan_attachement_notfounderror(api):
    '''
    test to raise exception when attachment not found.
    '''
    with pytest.raises(NotFoundError):
        api.scans.attachment(1, 1, 'none')


@pytest.mark.vcr()
def test_scan_create_scan_schedule_freq_typeerror(api):
    '''
    test to raise exception when type of frequency param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.create_scan_schedule(enabled=True, frequency=1)


@pytest.mark.vcr()
def test_scan_create_scan_schedule_freq_unexpectedvalueerror(api):
    '''
    test to raise exception when frequency param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.create_scan_schedule(enabled=True, frequency='nope')


@pytest.mark.vcr()
def test_scan_create_scan_schedule_interval_typeerror(api):
    '''
    test to raise exception when type of interval param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.create_scan_schedule(enabled=True, interval='nope')


@pytest.mark.vcr()
def test_scan_create_scan_schedule_day_of_month_typeerror(api):
    '''
    test to raise exception when type of day_of_month param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.create_scan_schedule(enabled=True, frequency='monthly', day_of_month='nope')


@pytest.mark.vcr()
def test_scan_create_scan_schedule_day_of_month_unexpectedvalueerror(api):
    '''
    test to raise exception when day_of_month param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.create_scan_schedule(enabled=True, frequency='monthly', day_of_month=300)


@pytest.mark.vcr()
def test_scan_create_scan_schedule_weekdays_typeerror(api):
    '''
    test to raise exception when type of weekdays param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.create_scan_schedule(enabled=True, frequency='weekly', weekdays='nope')


@pytest.mark.vcr()
def test_scan_create_scan_schedule_weekdays_unexpectedvalueerror(api):
    '''
    test to raise exception when weekdays param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.create_scan_schedule(
            enabled=True, frequency='weekly', weekdays=['MO', 'WE', 'nope'])

@pytest.mark.vcr()
def test_scan_create_scan_schedule_starttime_typeerror(api):
    '''
    test to raise exception when type of starttime param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.create_scan_schedule(enabled=True, starttime='fail')


@pytest.mark.vcr()
def test_scan_create_scan_schedule_timezone_typeerror(api):
    '''
    test to raise exception when type of timezone param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.create_scan_schedule(enabled=True, timezone=1)


@pytest.mark.vcr()
def test_scan_create_scan_schedule_timezone_unexpectedvalueerror(api):
    '''
    test to raise exception when timezone param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.create_scan_schedule(enabled=True, timezone='the zone of time')


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_freq_typeerror(api, scan):
    '''
    test to raise exception when type of frequency param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.configure_scan_schedule(scan['id'], enabled=True, frequency=1)


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_freq_unexpectedvalueerror(api, scan):
    '''
    test to raise exception when frequency param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.configure_scan_schedule(scan['id'], enabled=True, frequency='nope')


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_interval_typeerror(api, scan):
    '''
    test to raise exception when type of interval param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.configure_scan_schedule(scan['id'], enabled=True, interval='nope')


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_day_of_month_typeerror(api, scan):
    '''
    test to raise exception when type of day_of_month param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='monthly', day_of_month='nope')


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_day_of_month_unexpectedvalueerror(api, scan):
    '''
    test to raise exception when day_of_month param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='monthly', day_of_month=300)


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_weekdays_typeerror(api, scan):
    '''
    test to raise exception when type of weekdays param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='weekly', weekdays='nope')


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_weekdays_unexpectedvalueerror(api, scan):
    '''
    test to raise exception when weekdays param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='weekly', weekdays=['MO', 'WE', 'nope'])


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_starttime_typeerror(api, scan):
    '''
    test to raise exception when type of starttime param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.configure_scan_schedule(scan['id'], enabled=True, starttime='fail')


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_timezone_typeerror(api, scan):
    '''
    test to raise exception when type of timezone param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.configure_scan_schedule(scan['id'], enabled=True, timezone=1)


@pytest.mark.vcr()
def test_scan_configure_scan_schedule_timezone_unexpectedvalueerror(api, scan):
    '''
    test to raise exception when timezone param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.configure_scan_schedule(scan['id'], enabled=True, timezone='the zone of time')


# @pytest.mark.vcr()
# def test_scan_configure_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.configure('abc123')

# @pytest.mark.vcr()
# def test_scan_configure_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.configure('nope')

@pytest.mark.vcr()
def test_scan_configure_notfounderror(api):
    '''
    test to raise exception when scan_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scans.configure(1, name=str(uuid.uuid4()))


@pytest.mark.vcr()
def test_scan_configure(api, scan):
    '''
    test to configure scan
    '''
    mod = api.scans.configure(scan['id'], name='MODIFIED')
    assert mod['id'] == scan['id']
    assert mod['name'] == 'MODIFIED'


@pytest.mark.vcr()
def test_scan_configure_schedule_onetime_to_daily(api, scheduled_scan):
    '''
    test to edit scan schedule frequency from onetime to daily
    '''
    schedule = api.scans.configure_scan_schedule(scheduled_scan['id'], frequency='daily')
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=DAILY;INTERVAL=1'


@pytest.mark.vcr()
def test_scan_configure_schedule_onetime_to_weekly_valdefault(api, scheduled_scan):
    '''
    test to edit scheduled scan frequency from onetime to weekly
    and assign default value to weekdays param
    '''
    schedule = api.scans.configure_scan_schedule(scheduled_scan['id'], frequency='weekly')
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,MO,TU,WE,TH,FR,SA'


@pytest.mark.vcr()
def test_scan_configure_schedule_onetime_to_weekly_valassigned(api, scheduled_scan):
    '''
    test to edit scheduled scan frequency from onetime to weekly
    and assign user defined value to weekdays param
    '''
    schedule = api.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='weekly', weekdays=['MO', 'TU'])
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU'


@pytest.mark.vcr()
def test_scan_configure_schedule_freq_weekly_valavailable(api):
    '''
    test to edit weekly scheduled scan and assign existing weekdays values to weekdays param
    '''
    create_schedule = api.scans.create_scan_schedule(
        enabled=True, frequency='weekly', weekdays=['MO', 'TU'])
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=create_schedule)
    update_schedule = api.scans.configure_scan_schedule(id=scan['id'], interval=2)
    mod = api.scans.configure(scan['id'],
                              schedule_scan=update_schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TU'
    api.scans.delete(mod['id'])


@pytest.mark.vcr()
def test_scan_configure_schedule_onetime_to_monthly_valdefault(api, scheduled_scan):
    '''
    test to edit scheduled scan frequency from onetime to monthly
    and assign default value to day_of_month param
    '''
    schedule = api.scans.configure_scan_schedule(scheduled_scan['id'], frequency='monthly')
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'].split(';')[0] == 'FREQ=MONTHLY'
    api.scans.delete(mod['id'])


@pytest.mark.vcr()
def test_scan_configure_schedule_onetime_to_monthly_valassigned(api, scheduled_scan):
    '''
    test to edit scheduled scan frequency from onetime to monthly
    and assign user defined value to day_of_month param
    '''
    schedule = api.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='monthly', day_of_month=8)
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8'


@pytest.mark.vcr()
def test_scan_configure_schedule_freq_monthly_valavailable(api):
    '''
    test to edit scheduled scan and assign existing day_of_month value to day_of_month param
    '''
    create_schedule = api.scans.create_scan_schedule(
        enabled=True, frequency='monthly', day_of_month=8)
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=create_schedule)
    update_schedule = api.scans.configure_scan_schedule(scan['id'], interval=2)
    mod = api.scans.configure(scan['id'],
                              schedule_scan=update_schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=8'
    api.scans.delete(mod['id'])


@pytest.mark.vcr()
def test_scan_configure_schedule_freq_yearly(api, scheduled_scan):
    '''
    test to edit scheduled schan frequency from onetime to yearly
    '''
    update_schedule = api.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='yearly', interval=2)
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=update_schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=YEARLY;INTERVAL=2'


@pytest.mark.vcr()
def test_scan_configure_enable_scan_schedule(api, scan):
    '''
    test to enable scan schedule
    '''
    schedule = api.scans.configure_scan_schedule(scan['id'], enabled=True)
    mod = api.scans.configure(scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=ONETIME;INTERVAL=1'


@pytest.mark.vcr()
def test_scan_configure_disable_scan_schedule(api, scheduled_scan):
    '''
    test to disable scan schedule
    '''
    schedule = api.scans.configure_scan_schedule(scheduled_scan['id'], enabled=False)
    mod = api.scans.configure(scheduled_scan['id'],
                              schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is False


# @pytest.mark.vcr()
# def test_scan_copy_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.copy('nope')

@pytest.mark.vcr()
def test_scan_copy_folder_id_typeerror(api):
    '''
    test to raise exception when type of folder_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.copy(1, folder_id='nope')


@pytest.mark.vcr()
def test_scan_copy_name_typeerror(api):
    '''
    test to raise exception when type of name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.copy(1, name=1)


@pytest.mark.vcr()
def test_scan_copy_notfounderror(api):
    '''
    test to raise exception when scan_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scans.copy(1)


@pytest.mark.vcr()
def test_scan_copy(api, scan):
    '''
    test to copy scan
    '''
    clone = api.scans.copy(scan['id'])
    assert isinstance(clone, dict)
    check(clone, 'control', bool)
    check(clone, 'creation_date', int)
    check(clone, 'enabled', bool)
    check(clone, 'id', int)
    check(clone, 'last_modification_date', int)
    check(clone, 'owner', str)
    check(clone, 'name', str)
    check(clone, 'read', bool)
    check(clone, 'rrules', str, allow_none=True)
    # This is in the documentation, however isn't always returned oddly.
    # check(clone, 'schedule_uuid', 'scanner-uuid')
    check(clone, 'shared', bool)
    check(clone, 'starttime', str, allow_none=True)
    check(clone, 'status', str)
    check(clone, 'timezone', str, allow_none=True)
    check(clone, 'user_permissions', int)
    check(clone, 'uuid', 'scanner-uuid')


@pytest.mark.vcr()
def test_scan_create_no_template_pass(scan):
    '''
    test to create scan when no template is provided by user
    '''
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_default_schedule(api):
    '''
    test to create scan with default schedule
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True)
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=ONETIME;INTERVAL=1'
    api.scans.delete(scan['id'])


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_freq_daily(api):
    '''
    test to create scheduled scan with frequency as daily
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True, frequency='daily')
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=DAILY;INTERVAL=1'
    api.scans.delete(scan['id'])


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_freq_weekly_valdefault(api):
    '''
    test to create scheduled scan with frequency as weekly
    and default weekdays value
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True, frequency='weekly')
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,MO,TU,WE,TH,FR,SA'
    api.scans.delete(scan['id'])


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_freq_weekly_valassigned(api):
    '''
    test to create scheduled scan with frequency as weekly
    with user defined weekdays values
    '''
    schedule_scan = api.scans.create_scan_schedule(
        enabled=True, frequency='weekly', weekdays=['MO', 'TU'])
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU'
    api.scans.delete(scan['id'])


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_freq_monthly_valdefault(api):
    '''
    test to create scheduled scan with frequency as monthly
    and day_of_month as default value
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True, frequency='monthly')
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'].split(';')[0] == 'FREQ=MONTHLY'
    api.scans.delete(scan['id'])


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_freq_monthly_valassigned(api):
    '''
    test to create scheduled scan with frequency as monthly
    with user defined day_of_month value
    '''
    schedule_scan = api.scans.create_scan_schedule(
        enabled=True, frequency='monthly', day_of_month=8)
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8'
    api.scans.delete(scan['id'])


@pytest.mark.vcr()
def test_scan_create_scheduled_scan_freq_yearly(api):
    '''
    test to create scheduled scan with frequency as yearly
    '''
    schedule_scan = api.scans.create_scan_schedule(enabled=True, frequency='yearly', interval=2)
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=YEARLY;INTERVAL=2'
    api.scans.delete(scan['id'])

#@pytest.mark.vcr()
#def test_scan_delete_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.delete('nope')

@pytest.mark.vcr()
def test_scan_delete_notfounderror(api):
    '''
    test to raise exception when scan_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scans.delete(0)


@pytest.mark.vcr()
def test_scan_delete(api, scan):
    '''
    test to delete scan
    '''
    api.scans.delete(scan['id'])

# @pytest.mark.vcr()
# def test_scan_delete_history_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.delete_history('nope', 1)

# @pytest.mark.vcr()
# def test_scan_delete_history_history_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.delete_history(1, 'nope')

@pytest.mark.vcr()
def test_scan_delete_history_notfounderror(api):
    '''
    test to raise exception when scan_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scans.delete_history(1, 1)

# @pytest.mark.vcr()
# def test_scan_details_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.details('nope')

@pytest.mark.vcr()
def test_scan_details_history_it_typeerror(api):
    '''
    test to raise exception when type of scan_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.details(1, 'nope')


@pytest.mark.vcr()
def test_scan_results(api):
    '''
    test to get scan results
    '''
    scan_list = [id['id'] for id in list(
        filter(lambda value: value['status'] == 'completed', api.scans.list()))]
    if scan_list:
        scan_results = api.scans.results(scan_list[0])
        assert isinstance(scan_results, dict)
        result = scan_results
        check(result, 'info', dict)
        info = result['info']
        check(info, 'acls', list, allow_none=True)
        if result['info']['acls']:
            for acls in result['info']['acls']:
                check(acls, 'owner', int, allow_none=True)
                check(acls, 'type', str, allow_none=True)
                check(acls, 'permissions', int, allow_none=True)
                check(acls, 'id', int, allow_none=True)
                check(acls, 'name', str, allow_none=True)
                check(acls, 'display_name', str, allow_none=True)
        check(info, 'schedule_uuid', str, allow_none=True)
        check(info, 'edit_allowed', bool)
        check(info, 'status', str)
        check(info, 'alt_targets_used', bool, allow_none=True)
        check(info, 'scanner_start', int, allow_none=True)
        check(info, 'policy', str, allow_none=True)
        check(info, 'pci-can-upload', bool, allow_none=True)
        check(info, 'scan_start', int, allow_none=True)
        check(info, 'hasaudittrail', bool)
        check(info, 'user_permissions', int)
        check(info, 'folder_id', int, allow_none=True)
        check(info, 'no_target', bool)
        check(info, 'owner', str)
        check(info, 'targets', str, allow_none=True)
        check(info, 'control', bool)
        check(info, 'object_id', int, allow_none=True)
        check(info, 'scanner_name', str, allow_none=True)
        check(info, 'uuid', str)
        check(info, 'haskb', bool)
        check(info, 'scanner_end', int, allow_none=True)
        check(info, 'scan_end', int)
        # check(info, 'hostcount', int)
        check(info, 'scan_type', str, allow_none=True)
        check(info, 'name', str)

        check(result, 'comphosts', list)
        if 'comphosts' in result and len(result['comphosts']) > 0:
            for comphosts in result['comphosts']:
                check(comphosts, 'totalchecksconsidered', int)
                check(comphosts, 'numchecksconsidered', int)
                check(comphosts, 'scanprogresstotal', int)
                check(comphosts, 'scanprogresscurrent', int)
                check(comphosts, 'host_index', int)
                check(comphosts, 'score', int)
                check(comphosts, 'severitycount', dict)
                check(comphosts, 'progress', str)
                check(comphosts, 'critical', int)
                check(comphosts, 'high', int)
                check(comphosts, 'medium', int)
                check(comphosts, 'low', int)
                check(comphosts, 'info', int)
                check(comphosts, 'host_id', int)
                check(comphosts, 'hostname', str)

        check(result, 'hosts', list)
        if 'hosts' in result and len(result['hosts']) > 0:
            for hosts in result['hosts']:
                check(hosts, 'totalchecksconsidered', int)
                check(hosts, 'numchecksconsidered', int)
                check(hosts, 'scanprogresstotal', int)
                check(hosts, 'scanprogresscurrent', int)
                check(hosts, 'host_index', int)
                check(hosts, 'score', int)
                check(hosts, 'severitycount', dict)
                check(hosts, 'progress', str)
                check(hosts, 'critical', int)
                check(hosts, 'high', int)
                check(hosts, 'medium', int)
                check(hosts, 'low', int)
                check(hosts, 'info', int)
                check(hosts, 'host_id', int)
                check(hosts, 'hostname', str)

        check(result, 'notes', list)
        if len(result['notes']) > 0:
            for notes in result['notes']:
                check(notes, 'title', str)
                check(notes, 'message', str)
                check(notes, 'severity', int)

        check(result, 'remediations', dict)
        check(result['remediations'], 'num_hosts', int)
        check(result['remediations'], 'num_cves', int)
        check(result['remediations'], 'num_impacted_hosts', int)
        check(result['remediations'], 'num_remediated_cves', int)
        check(result['remediations'], 'remediations', list)

        if len(result['remediations']['remediations']) > 0:
            for remediation in result['remediations']['remediations']:
                check(remediation, 'value', str)
                check(remediation, 'remediation', str)
                check(remediation, 'hosts', int)
                check(remediation, 'vulns', int)

        check(result, 'vulnerabilities', list)
        if 'vulnerabilities' in result and len(result['vulnerabilities']) > 0:
            for vulnerability in result['vulnerabilities']:
                check(vulnerability, 'count', int)
                check(vulnerability, 'plugin_name', str)
                check(vulnerability, 'vuln_index', int)
                check(vulnerability, 'severity', int)
                check(vulnerability, 'plugin_id', int)
                # Mentioned in the docs, however doesn't appear to show in testing
                # check(vulnerability, 'severity_index', int)
                check(vulnerability, 'plugin_family', str)

        check(result, 'history', list)
        for history in result['history']:
            check(history, 'alt_targets_used', bool)
            check(history, 'scheduler', int)
            check(history, 'status', str)
            check(history, 'type', str, allow_none=True)
            check(history, 'uuid', str)
            check(history, 'last_modification_date', int)
            check(history, 'creation_date', int)
            check(history, 'owner_id', int)
            check(history, 'history_id', int)
            check(history, 'is_archived', bool)

        check(result, 'compliance', list)
        if 'compliance' in result and len(result['compliance']) > 0:
            for compliance in result['compliance']:
                check(compliance, 'count', int)
                check(compliance, 'plugin_name', str)
                check(compliance, 'vuln_index', int)
                check(compliance, 'severity', int)
                check(compliance, 'plugin_id', int)
                # Mentioned in the docs, however doesn't appear to show in testing
                # check(compliance, 'severity_index', int)
                check(compliance, 'plugin_family', str)


# @pytest.mark.vcr()
# def test_scan_export_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.export('nope')

@pytest.mark.vcr()
def test_scan_export_history_id_typeerror(api):
    '''
    test to raise exception when type of history_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.export(1, history_id='nope')


@pytest.mark.vcr()
def test_scan_export_format_typeerror(api):
    '''
    test to raise exception when type of format param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.export(1, format=1)


@pytest.mark.vcr()
def test_scan_export_format_unexpectedvalueerror(api):
    '''
    test to raise exception when format param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.export(1, format='something else')


@pytest.mark.vcr()
def test_scan_export_password_typeerror(api):
    '''
    test to raise exception when type of password param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.export(1, password=1)


@pytest.mark.vcr()
def test_scan_export_chapters_typeerror(api):
    '''
    test to raise exception when type of chapter param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.export(1, chapters=1)


@pytest.mark.vcr()
def test_scan_export_chapters_unexpectedvalueerror(api):
    '''
    test to raise exception when chapter param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.export(1, chapters=['nothing to see here'])


@pytest.mark.vcr()
def test_scan_export_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.export(1, filter_type=1)


@pytest.mark.vcr()
def test_scan_export_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.export(1, filter_type='nothing')


@pytest.mark.vcr()
def test_scan_export_was_typeerror(api):
    '''
    test to raise exception when scan_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.export(SCAN_ID_WITH_RESULTS, scan_type='bad-value')

@pytest.mark.vcr()
def test_scan_export_bytesio(api):
    '''
    test to export scan using optional `stream_hook` kwarg, provided by user (Issue #305)
    '''
    def stream_hook(response, _fobj, chunk_size=1024):
        """This is an example callable, the caller provides this"""
        progress_bytes = 0
        total_size = int(response.headers.get('content-length', 0))
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                progress_bytes += len(chunk)
                stdout.write('Progress: %d / %d\n' % (progress_bytes, total_size))
                _fobj.write(chunk)
        stdout.write('Complete, %d/%d bytes received in stream_hook\n' % (progress_bytes, total_size))

    fobj = api.scans.export(SCAN_ID_WITH_RESULTS, stream_hook=stream_hook)
    assert isinstance(fobj, BytesIO)

    counter = 0
    for _ in NessusReportv2(fobj):
        counter += 1
        if counter > 10:
            break

@pytest.mark.vcr()
def test_scan_export_bytesio(api):
    '''
    test to export scan
    '''
    scan_list = [id['id'] for id in list(
        filter(lambda value: value['status'] == 'completed', api.scans.list()))]
    if scan_list:
        fobj = api.scans.export(scan_list[0])
        assert isinstance(fobj, BytesIO)

        counter = 0
        for _ in NessusReportv2(fobj):
            counter += 1
            if counter > 10:
                break


@pytest.mark.vcr()
def test_scan_export_file_object(api):
    '''
    test to export scan file object
    '''
    scan_list = [id['id'] for id in list(
        filter(lambda value: value['status'] == 'completed', api.scans.list()))]
    if scan_list:
        filename = '{}.nessus'.format(uuid.uuid4())
        with open(filename, 'wb') as fobj:
            api.scans.export(scan_list[0], fobj=fobj)

        with open(filename, 'rb') as fobj:
            counter = 0
            for _ in NessusReportv2(fobj):
                counter += 1
                if counter > 10:
                    break
        os.remove(filename)

# @pytest.mark.vcr()
# def test_scan_host_details_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.host_details('nope', 1)

@pytest.mark.vcr()
def test_scan_host_details_host_id_typeerror(api):
    '''
    test to raise exception when type of host_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.host_details(1, 'nope')


@pytest.mark.vcr()
def test_scan_host_details_history_id_typeerror(api):
    '''
    test to raise exception when type of history_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.host_details(1, 1, 'nope')


@pytest.mark.vcr()
def test_scan_host_details_notfounderror(api):
    '''
    test to raise exception when scan_id not found.
    '''
    with pytest.raises(NotFoundError):
        api.scans.host_details(1, 1)


@pytest.mark.vcr()
def test_scan_host_details(api, scan_results):
    '''
    test to retrieve the host details from a specific scan
    '''
    try:
        host = api.scans.host_details(
            scan_results['id'], scan_results['results']['hosts'][0]['asset_id'])
        assert isinstance(host, dict)
        check(host, 'info', dict)
        check(host['info'], 'host-fqdn', str, allow_none=True)
        check(host['info'], 'host_end', str)
        check(host['info'], 'host_start', str)
        check(host['info'], 'operating-system', list, allow_none=True)
        check(host['info'], 'host-ip', str)
        check(host['info'], 'mac-address', str, allow_none=True)

        check(host, 'vulnerabilities', list)
        for vulnerability in host['vulnerabilities']:
            check(vulnerability, 'count', int)
            check(vulnerability, 'severity', int)
            check(vulnerability, 'plugin_family', str)
            check(vulnerability, 'hostname', str)
            check(vulnerability, 'plugin_name', str)
            check(vulnerability, 'severity_index', int)
            check(vulnerability, 'vuln_index', int)
            check(vulnerability, 'host_id', int)
            check(vulnerability, 'plugin_id', int)

        check(host, 'compliance', list)
        for compliance in host['compliance']:
            check(compliance, 'count', int)
            check(compliance, 'plugin_name', str)
            check(compliance, 'vuln_index', int)
            check(compliance, 'severity', int)
            check(compliance, 'plugin_id', int)
            check(compliance, 'severity_index', int)
            check(compliance, 'plugin_family', str)
    except KeyError as key:
        print('Key error: ', key)


@pytest.mark.vcr()
def test_scan_import_scan_folder_id_typeerror(api):
    '''
    test to raise exception when type of folder_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.import_scan(None, folder_id='nope')


@pytest.mark.vcr()
def test_scan_import_scan_password_typeerror(api):
    '''
    test to raise exception when type of password param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.import_scan(None, password=1)


@pytest.mark.vcr()
def test_scan_import_scan(api):
    '''
    test to import scan
    '''
    scan_list = [id['id'] for id in list(
        filter(lambda value: value['status'] == 'completed', api.scans.list()))]
    if scan_list:
        fobj = api.scans.export(scan_list[0])
        api.scans.import_scan(fobj)

# @pytest.mark.vcr()
# def test_scan_launch_scanid_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.launch('nope')

@pytest.mark.vcr()
def test_scan_launch_targets_typerror(api):
    '''
    test to raise exception when type of targets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.launch(1, targets='nope')


@pytest.mark.skip(reason="Switching between scan states can be tricky")
def test_scan_launch(api, scan):
    '''
    test to launch scan
    '''
    api.scans.launch(scan['id'])
    time.sleep(5)
    api.scans.stop(scan['id'], block=True)


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
def test_scan_launch_alt_targets(api, scan):
    '''
    test to launch scan
    '''
    api.scans.launch(scan['id'], targets=['127.0.0.2'])
    time.sleep(5)
    api.scans.stop(scan['id'], block=True)


@pytest.mark.vcr()
def test_scan_list_folder_id_typeerror(api):
    '''
    test to raise exception when type of folder_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.list(folder_id='nope')


@pytest.mark.vcr()
def test_scan_list_last_modified_typeerror(api):
    '''
    test to raise exception when type of last_modified param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.list(last_modified='nope')


@pytest.mark.vcr()
def test_scan_list(api):
    '''
    test to get list of scans
    '''
    scans = api.scans.list()
    assert isinstance(scans, list)
    scan = scans[0]
    check(scan, 'control', bool)
    check(scan, 'creation_date', int)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'legacy', bool)
    check(scan, 'owner', str)
    check(scan, 'name', str)
    check(scan, 'permissions', int)
    check(scan, 'read', bool)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'schedule_uuid', 'scanner-uuid')
    check(scan, 'shared', bool)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'status', str)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', 'scanner-uuid')

# @pytest.mark.vcr()
# def test_scan_pause_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.pause('nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
def test_scan_pause_scan(api, scan):
    '''
    test to pause scan
    '''
    _ = api.scans.launch(scan['id'])
    api.scans.pause(scan['id'], block=True)

# @pytest.mark.vcr()
# def test_scan_plugin_output_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.plugin_output('nope', 1, 1)

@pytest.mark.vcr()
def test_scan_plugin_output_host_id_typeerror(api):
    '''
    test to raise exception when type of host_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 'nope', 1)


@pytest.mark.vcr()
def test_scan_plugin_output_plugin_id_typeerror(api):
    '''
    test to raise exception when type of plugin_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 1, 'nope')


@pytest.mark.vcr()
def test_scan_plugin_output_history_id_typeerror(api):
    '''
    test to raise exception when type of history_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 1, 1, history_id='nope')


@pytest.mark.vcr()
def test_scan_plugin_output(api, scan_results):
    '''
    test to get scan plugin output
    '''
    try:
        host = api.scans.host_details(
            scan_results['id'], scan_results['results']['hosts'][0]['asset_id'])
        output = api.scans.plugin_output(
            scan_results['id'],
            host['vulnerabilities'][0]['host_id'],
            host['vulnerabilities'][0]['plugin_id'])
        output_info_pdesc = output['info']['plugindescription']
        output_info_pdesc_patt = output_info_pdesc['pluginattributes']
        output_info_pdesc_patt_pinfo = output_info_pdesc['pluginattributes']['plugin_information']
        assert isinstance(output, dict)
        check(output, 'info', dict)
        check(output['info'], 'plugindescription', dict)
        check(output_info_pdesc, 'pluginattributes', dict)
        check(output_info_pdesc, 'pluginfamily', str)
        check(output_info_pdesc, 'pluginid', str)
        check(output_info_pdesc, 'pluginname', str)
        check(output_info_pdesc, 'severity', int)
        check(output_info_pdesc_patt, 'description', str)
        check(output_info_pdesc_patt, 'has_patch', bool)
        check(output_info_pdesc_patt, 'plugin_information', dict)
        check(output_info_pdesc_patt_pinfo, 'plugin_family', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_id', int)
        check(output_info_pdesc_patt_pinfo, 'plugin_modification_date', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_publication_date', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_type', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_version', str)
        check(output_info_pdesc_patt, 'risk_information', dict)
        check(output_info_pdesc_patt['risk_information'], 'risk_factor', str)
        check(output_info_pdesc_patt, 'solution', str, allow_none=True)
        check(output_info_pdesc_patt, 'synopsis', str, allow_none=True)

        check(output, 'outputs', list)
        for data in output['outputs']:
            check(data, 'has_attachment', int)
            check(data, 'hosts', list, allow_none=True)
            check(data, 'plugin_output', str, allow_none=True)
            check(data, 'ports', dict)
            for port in data['ports']:
                check(data['ports'], port, list)
                for port_detail in data['ports'][port]:
                    check(port_detail, 'hostname', str)
            check(data, 'severity', int)
    except KeyError as error:
        print('Invalid key', error)


# @pytest.mark.vcr()
# def test_scan_read_status_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.set_read_status('nope', False)

@pytest.mark.vcr()
def test_scan_read_status_read_status_typeerror(api):
    '''
    test to raise exception when type of read_status param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.set_read_status(1, 'nope')


@pytest.mark.vcr()
def test_scan_read_status(api, scan):
    '''
    test to get scan read status
    '''
    scans = api.scans.list()
    scan = scans[0]
    api.scans.set_read_status(scans[0]['id'], not scans[0]['read'])
    for resp in api.scans.list():
        if resp['id'] == scan['id']:
            assert scan['read'] != resp['read']

# @pytest.mark.vcr()
# def test_scan_resume_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.resume('nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
@pytest.mark.vcr()
def test_scan_resume(api, scan):
    '''
    test to resume scan
    '''
    api.scans.launch(scan['id'])
    time.sleep(5)
    api.scans.pause(scan['id'], block=True)
    time.sleep(5)
    api.scans.resume(scan['id'])
    time.sleep(5)
    api.scans.stop(scan['id'], block=True)

# @pytest.mark.vcr()
# def test_scan_schedule_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.schedule('nope', False)

@pytest.mark.vcr()
def test_scan_schedule_enabled_typeerror(api):
    '''
    test to raise exception when type of enabled param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.schedule(1, 'nope')


@pytest.mark.skip(reason="Need to configure the scan w/ a schedule.")
@pytest.mark.vcr()
def test_scan_schedule(api, scan):
    '''
    test to disable scan schedule
    '''
    api.scans.schedule(scan['id'], False)

# @pytest.mark.vcr()
# def test_scan_stop_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.stop('nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
@pytest.mark.vcr()
def test_scan_stop(api, scan):
    '''
    test to stop scan
    '''
    api.scans.launch(scan['id'])
    time.sleep(5)
    api.scans.stop(scan['id'])

# @pytest.mark.vcr()
# def test_scan_status_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.status('no')

@pytest.mark.vcr()
def test_scan_status(api, scan):
    '''
    test to check scan status
    '''
    status = api.scans.status(scan['id'])
    single(status, str)


@pytest.mark.vcr()
def test_scan_timezones(api):
    '''
    test to get list of allowed timezone strings
    '''
    assert isinstance(api.scans.timezones(), list)


@pytest.mark.vcr()
def test_scan_check_auto_targets_success(api):
    '''
    test to evaluates a list of targets and/or tags against
    the scan route configuration of scanner groups
    '''
    resp = api.scans.check_auto_targets(10, 5, targets=['127.0.0.1'])
    assert isinstance(resp, dict)
    check(resp, 'matched_resource_uuids', list)
    check(resp, 'missed_targets', list)
    check(resp, 'total_matched_resource_uuids', int)
    check(resp, 'total_missed_targets', int)


@pytest.mark.vcr()
def test_scan_check_auto_targets_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets('nope', 5, targets=['127.0.0.1'])


@pytest.mark.vcr()
def test_scan_check_auto_targets_matched_resource_limit_typeerror(api):
    '''
    test to raise exception when type of matched_resource_limit param
    does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 'nope', targets=['127.0.0.1'])


@pytest.mark.vcr()
def test_scan_check_auto_targets_network_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when network_uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.check_auto_targets(10, 5, network_uuid='nope', targets=['127.0.0.1'])


@pytest.mark.vcr()
def test_scan_check_auto_targets_network_uuid_typeerror(api):
    '''
    test to raise exception when type of network_uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, network_uuid=1, targets=['127.0.0.1'])


@pytest.mark.vcr()
def test_scan_check_auto_targets_tags_unexpectedvalueerror(api):
    '''
    test to raise exception when type of any value in tags param
    does not match the expected type.
    '''
    with pytest.raises(UnexpectedValueError):
        api.scans.check_auto_targets(10, 5, tags=['nope'], targets=['127.0.0.1'])


@pytest.mark.vcr()
def test_scan_check_auto_targets_tags_typeerror(api):
    '''
    test to raise exception when type of tags param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, tags=1, targets=['127.0.0.1'])


@pytest.mark.vcr()
def test_scan_check_auto_targets_targets_typeerror(api):
    '''
    test to raise exception when type of targets param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.scans.check_auto_targets(10, 5, targets=1)


# @pytest.mark.vcrx()
# def test_scan_results_success(api, scan_results, scan):
#     # print('scan: {}'.format(scan.history['id']))
#     # print('*'*25)
#     # print('scan_results: {}'.format(scan_results))
#     api.scans.details()

@pytest.mark.vcr()
def test_scan_create_scan_schedule_success(api):
    '''test to create a scan schedule'''
    api.scans.create_scan_schedule(enabled=False)


@pytest.mark.vcr()
def test_scan_create_scan_success(api):
    '''
    test to create a scan
    '''
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        targets=['127.0.0.1'])
    assert isinstance(scan, dict)
    check(scan, 'tag_type', None, allow_none=True)
    check(scan, 'container_id', 'uuid')
    check(scan, 'owner_uuid', 'uuid')
    check(scan, 'uuid', str)
    check(scan, 'name', str)
    check(scan, 'description', None, allow_none=True)
    check(scan, 'policy_id', int)
    check(scan, 'scanner_id', None, allow_none=True)
    check(scan, 'scanner_uuid', str)
    check(scan, 'emails', None, allow_none=True)
    check(scan, 'sms', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'include_aggregate', bool)
    check(scan, 'scan_time_window', None, allow_none=True)
    check(scan, 'custom_targets', str)
    check(scan, 'target_network_uuid', None, allow_none=True)
    check(scan, 'rrules', None, allow_none=True)
    check(scan, 'default_permissions', int)
    check(scan, 'timezone', None, allow_none=True)
    check(scan, 'notification_filters', None, allow_none=True)
    check(scan, 'auto_routed', int)
    check(scan, 'remediation', int)
    check(scan, 'user_permissions', int)
    check(scan, 'starttime', None, allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'creation_date', int)
    check(scan, 'type', str)
    check(scan, 'id', int)


@pytest.mark.vcr()
def test_scan_create_scan_document_policy_setting_valueerror(api):
    '''
    test to raise when policy setting is invalid
    '''
    with pytest.raises(UnexpectedValueError):
        getattr(api.scans, '_create_scan_document')({'policy': 'some_policy'})


@pytest.mark.vcr()
def test_scan_create_scan_document_credentials_pass(api):
    '''
    test to create a scan document along with credentials
    '''
    credentials = api.credentials.list()
    for credential in credentials:
        getattr(api.scans, '_create_scan_document')(
            {'credentials': credential})
