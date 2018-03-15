from .fixtures import *
from tenable.errors import *

def test_event_field_name_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events((1, 'gt', '2018-01-01'))

def test_event_filter_operator_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events(('date', 1, '2018-01-01'))

def test_event_filter_value_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events(('date', 'gt', 1))

def test_event_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.audit_log.events(limit='nope')

def test_events_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.audit_log.events()

def test_events(api):
    events = api.audit_log.events(('date', 'gt', '2018-01-01'), limit=100)