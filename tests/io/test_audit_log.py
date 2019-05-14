from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_auditlog_event_field_name_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events((1, 'gt', '2018-01-01'))

@pytest.mark.vcr()
def test_auditlog_event_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events(('date', 1, '2018-01-01'))

@pytest.mark.vcr()
def test_auditlog_event_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events(('date', 'gt', 1))

@pytest.mark.vcr()
def test_auditlog_event_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events(limit='nope')

@pytest.mark.vcr()
def test_auditlog_events_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.audit_log.events()

@pytest.mark.vcr()
def test_auditlog_events(api):
    events = api.audit_log.events(('date', 'gt', '2018-01-01'), limit=100)
    assert isinstance(events, list)
    e = events[-1]
    check(e, 'action', str)
    check(e, 'actor', dict)
    check(e['actor'], 'id', 'uuid')
    check(e['actor'], 'name', str, allow_none=True)
    check(e, 'crud', str)
    check(e, 'description', str, allow_none=True)
    check(e, 'fields', list)
    for d in e['fields']:
        check(d, 'key', str)
        check(d, 'value', str)
    check(e, 'id', str)
    check(e, 'is_anonymous', bool, allow_none=True)
    check(e, 'is_failure', bool, allow_none=True)
    check(e, 'received', 'datetime')
    check(e, 'target', dict)
    check(e['target'], 'id', 'uuid')
    check(e['target'], 'name', str)
    check(e['target'], 'type', str)