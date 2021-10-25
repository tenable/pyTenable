'''
test audit-log
'''
import pytest
from tenable.errors import ForbiddenError
from tests.checker import check

@pytest.mark.vcr()
def test_auditlog_event_field_name_typeerror(api):
    '''
    test to raise exception when type of filter_name param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.audit_log.events((1, 'gt', '2018-01-01'))

@pytest.mark.vcr()
def test_auditlog_event_filter_operator_typeerror(api):
    '''
    test to raise exception when type of filter_operator param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.audit_log.events(('date', 1, '2018-01-01'))

@pytest.mark.vcr()
def test_auditlog_event_filter_value_typeerror(api):
    '''
    test to raise exception when type of filter_value param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.audit_log.events(('date', 'gt', 1))

@pytest.mark.vcr()
def test_auditlog_event_limit_typeerror(api):
    '''
    test to raise exception when type of limit param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.audit_log.events(limit='nope')

@pytest.mark.vcr()
def test_auditlog_events_standard_user_permissionerror(stdapi):
    '''
    test to raise exception when standard_user tries to get audit log.
    '''
    with pytest.raises(ForbiddenError):
        stdapi.audit_log.events()

@pytest.mark.vcr()
def test_auditlog_events(api):
    '''
    test to get audit log
    '''
    events = api.audit_log.events(('date', 'gt', '2018-01-01'), limit=100)
    assert isinstance(events, list)
    event = events[-1]
    check(event, 'action', str)
    check(event, 'actor', dict)
    check(event['actor'], 'id', 'uuid')
    check(event['actor'], 'name', str, allow_none=True)
    check(event, 'crud', str)
    check(event, 'description', str, allow_none=True)
    check(event, 'fields', list)
    for field in event['fields']:
        check(field, 'key', str)
        check(field, 'value', str)
    check(event, 'id', str)
    check(event, 'is_anonymous', bool, allow_none=True)
    check(event, 'is_failure', bool, allow_none=True)
    check(event, 'received', 'datetime')
    check(event, 'target', dict)
    check(event['target'], 'id', str)
    check(event['target'], 'name', str, allow_none=True)
    check(event['target'], 'type', str)
