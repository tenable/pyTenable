from tenable.errors import *
from ..checker import check
import datetime, sys, pytest, os

@pytest.fixture
def alert(request, vcr, sc):
    with vcr.use_cassette('alert'):
        alert = sc.alerts.create(
            ('severity', '=', '3,4'),
            name='Example Alert',
            trigger=('sumip', '>=', '100'),
            action=[{
                'type': 'notification',
                'message': 'Example Message',
                'users': [{'id': 1}]
            }])
    def teardown():
        try:
            sc.alerts.delete(int(alert['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return alert

def test_alerts_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(name=1)

def test_alerts_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(description=1)

def test_alerts_constructor_query_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(query=1)

def test_alerts_constructor_always_exec_on_trigger_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(always_exec_on_trigger='nope')

def test_alerts_constructor_trigger_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(trigger=1)

def test_alerts_constructor_trigger_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(trigger=(1, '=', 'something'))

def test_alerts_constructor_trigger_operator_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(trigger=('name', 1, 'something'))

def test_alerts_constructor_trigger_operator_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.alerts._constructor(trigger=('name', 'eq', 'something'))

def test_alerts_constructor_trigger_value_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts._constructor(trigger=('name', '=', 1))

def test_alerts_constructor(sc):
    r = sc.alerts._constructor(
        ('severity', '=', '3,4'),
        name='Example Alert',
        trigger=('sumip', '>=', '100'),
        action=[{
            'type': 'notification', 
            'message': 'Example Message', 
            'users': [{'id': 1}]}])
    assert r == {
        'name': 'Example Alert',
        'action': [{
            'message': 'Example Message',
            'type': 'notification',
            'users': [{'id': 1}]
        }],
        'query': {
            'type': 'vuln',
            'filters': [{
                'filterName': 'severity',
                'operator': '=',
                'value': '3,4'
        }]},
        'triggerName': 'sumip',
        'triggerOperator': '>=',
        'triggerValue': '100'
    }

def test_alerts_list_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts.list(fields=1)

@pytest.mark.vcr()
def test_alerts_list_success(sc, alert):
    alerts = sc.alerts.list()
    assert isinstance(alerts, dict)
    for a in alerts['manageable']:
        check(a, 'description', str)
        check(a, 'id', str)
        check(a, 'name', str)
        check(a, 'status', str)

def test_alerts_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts.details('nope')

def test_alerts_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts.details(1, fields=1)

@pytest.mark.vcr()
def test_alerts_details_success(sc, alert):
    a = sc.alerts.details(int(alert['id']))
    assert isinstance(a, dict)
    check(a, 'action', list)
    for i in a['action']:
        assert isinstance(i, dict)
        check(i, 'type', str)
        check(i, 'definition', dict)
        if i['type'] == 'notification':
            check(i['definition'], 'message', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
        if i['type'] == 'email':
            check(i['definition'], 'subject', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'addresses', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
            check(i['definition'], 'includeResults', str)
        if i['type'] == 'report':
            check(i['definition'], 'report', dict)
            check(i['definition']['report'], 'id', str)
        if i['type'] == 'scan':
            check(i['definition'], 'scan', dict)
            check(i['definition']['scan'], 'id', int)
        if i['type'] == 'syslog':
            check(i['definition'], 'host', str)
            check(i['definition'], 'port', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'severity', str)
        if i['type'] == 'ticket':
            check(i['definition'], 'assignee', dict)
            check(i['definition']['assignee'], 'id', str)
            check(i['definition'], 'name', str)
            check(i['definition'], 'description', str)
            check(i['definition'], 'notes', str)
        check(i, 'id', str)
        check(i, 'objectID', str, allow_none=True)
        check(i, 'users', list)
        for u in i['users']:
            check(u, 'firstname', str)
            check(u, 'id', str)
            check(u, 'lastname', str)
            check(u, 'username', str) 
    check(a, 'canManage', str)
    check(a, 'canUse', str)
    check(a, 'description', str)
    check(a, 'didTriggerLastEvaluation', str)
    check(a, 'executeOnEveryTrigger', str)
    check(a, 'id', str)
    check(a, 'lastEvaluated', str)
    check(a, 'lastTriggered', str)
    check(a, 'modifiedTime', str)
    check(a, 'name', str)
    check(a, 'owner', dict)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'id', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'description', str)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a, 'query', dict)
    check(a['query'], 'description', str)
    check(a['query'], 'id', str)
    check(a['query'], 'name', str)
    check(a, 'schedule', dict)
    check(a['schedule'], 'type', str)
    check(a, 'status', str)
    check(a, 'triggerName', str)
    check(a, 'triggerOperator', str)
    check(a, 'triggerValue', str)

@pytest.mark.vcr()
def test_alerts_create_success(sc, alert):
    a = alert
    assert isinstance(a, dict)
    check(a, 'action', list)
    for i in a['action']:
        assert isinstance(i, dict)
        check(i, 'type', str)
        check(i, 'definition', dict)
        if i['type'] == 'notification':
            check(i['definition'], 'message', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
        if i['type'] == 'email':
            check(i['definition'], 'subject', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'addresses', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
            check(i['definition'], 'includeResults', str)
        if i['type'] == 'report':
            check(i['definition'], 'report', dict)
            check(i['definition']['report'], 'id', str)
        if i['type'] == 'scan':
            check(i['definition'], 'scan', dict)
            check(i['definition']['scan'], 'id', int)
        if i['type'] == 'syslog':
            check(i['definition'], 'host', str)
            check(i['definition'], 'port', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'severity', str)
        if i['type'] == 'ticket':
            check(i['definition'], 'assignee', dict)
            check(i['definition']['assignee'], 'id', str)
            check(i['definition'], 'name', str)
            check(i['definition'], 'description', str)
            check(i['definition'], 'notes', str)
        check(i, 'id', str)
        check(i, 'objectID', str, allow_none=True)
        check(i, 'users', list)
        for u in i['users']:
            check(u, 'firstname', str)
            check(u, 'id', str)
            check(u, 'lastname', str)
            check(u, 'username', str) 
    check(a, 'canManage', str)
    check(a, 'canUse', str)
    check(a, 'description', str)
    check(a, 'didTriggerLastEvaluation', str)
    check(a, 'executeOnEveryTrigger', str)
    check(a, 'id', str)
    check(a, 'lastEvaluated', str)
    check(a, 'lastTriggered', str)
    check(a, 'modifiedTime', str)
    check(a, 'name', str)
    check(a, 'owner', dict)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'id', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'description', str)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a, 'query', dict)
    check(a['query'], 'description', str)
    check(a['query'], 'id', str)
    check(a['query'], 'name', str)
    check(a, 'schedule', dict)
    check(a['schedule'], 'type', str)
    check(a, 'status', str)
    check(a, 'triggerName', str)
    check(a, 'triggerOperator', str)
    check(a, 'triggerValue', str)

def test_alerts_edit_id_typerror(sc):
    with pytest.raises(TypeError):
        sc.alerts.edit('one')

@pytest.mark.vcr()
def test_alerts_edit_success(sc, alert):
    a = sc.alerts.edit(int(alert['id']), name='new name for example')
    assert isinstance(a, dict)
    check(a, 'action', list)
    for i in a['action']:
        assert isinstance(i, dict)
        check(i, 'type', str)
        check(i, 'definition', dict)
        if i['type'] == 'notification':
            check(i['definition'], 'message', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
        if i['type'] == 'email':
            check(i['definition'], 'subject', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'addresses', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
            check(i['definition'], 'includeResults', str)
        if i['type'] == 'report':
            check(i['definition'], 'report', dict)
            check(i['definition']['report'], 'id', str)
        if i['type'] == 'scan':
            check(i['definition'], 'scan', dict)
            check(i['definition']['scan'], 'id', int)
        if i['type'] == 'syslog':
            check(i['definition'], 'host', str)
            check(i['definition'], 'port', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'severity', str)
        if i['type'] == 'ticket':
            check(i['definition'], 'assignee', dict)
            check(i['definition']['assignee'], 'id', str)
            check(i['definition'], 'name', str)
            check(i['definition'], 'description', str)
            check(i['definition'], 'notes', str)
        check(i, 'id', str)
        check(i, 'objectID', str, allow_none=True)
        check(i, 'users', list)
        for u in i['users']:
            check(u, 'firstname', str)
            check(u, 'id', str)
            check(u, 'lastname', str)
            check(u, 'username', str) 
    check(a, 'canManage', str)
    check(a, 'canUse', str)
    check(a, 'description', str)
    check(a, 'didTriggerLastEvaluation', str)
    check(a, 'executeOnEveryTrigger', str)
    check(a, 'id', str)
    check(a, 'lastEvaluated', str)
    check(a, 'lastTriggered', str)
    check(a, 'modifiedTime', str)
    check(a, 'name', str)
    check(a, 'owner', dict)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'id', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'description', str)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a, 'query', dict)
    check(a['query'], 'description', str)
    check(a['query'], 'id', str)
    check(a['query'], 'name', str)
    check(a, 'schedule', dict)
    check(a['schedule'], 'type', str)
    check(a, 'status', str)
    check(a, 'triggerName', str)
    check(a, 'triggerOperator', str)
    check(a, 'triggerValue', str)

def test_alerts_delete_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts.delete('one')

@pytest.mark.vcr()
def test_alerts_delete_success(sc, alert):
    sc.alerts.delete(int(alert['id']))

def test_alerts_execute_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.alerts.execute('one')

@pytest.mark.vcr()
def test_alerts_execute_successs(sc, alert):
    a = sc.alerts.execute(int(alert['id']))
    assert isinstance(a, dict)
    check(a, 'action', list)
    for i in a['action']:
        assert isinstance(i, dict)
        check(i, 'type', str)
        check(i, 'definition', dict)
        if i['type'] == 'notification':
            check(i['definition'], 'message', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
        if i['type'] == 'email':
            check(i['definition'], 'subject', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'addresses', str)
            check(i['definition'], 'users', list)
            for u in i['definition']['users']:
                check(u, 'firstname', str)
                check(u, 'id', str)
                check(u, 'lastname', str)
                check(u, 'username', str)
            check(i['definition'], 'includeResults', str)
        if i['type'] == 'report':
            check(i['definition'], 'report', dict)
            check(i['definition']['report'], 'id', str)
        if i['type'] == 'scan':
            check(i['definition'], 'scan', dict)
            check(i['definition']['scan'], 'id', int)
        if i['type'] == 'syslog':
            check(i['definition'], 'host', str)
            check(i['definition'], 'port', str)
            check(i['definition'], 'message', str)
            check(i['definition'], 'severity', str)
        if i['type'] == 'ticket':
            check(i['definition'], 'assignee', dict)
            check(i['definition']['assignee'], 'id', str)
            check(i['definition'], 'name', str)
            check(i['definition'], 'description', str)
            check(i['definition'], 'notes', str)
        check(i, 'id', str)
        check(i, 'objectID', str, allow_none=True)
        check(i, 'users', list)
        for u in i['users']:
            check(u, 'firstname', str)
            check(u, 'id', str)
            check(u, 'lastname', str)
            check(u, 'username', str) 
    check(a, 'canManage', str)
    check(a, 'canUse', str)
    check(a, 'description', str)
    check(a, 'didTriggerLastEvaluation', str)
    check(a, 'executeOnEveryTrigger', str)
    check(a, 'id', str)
    check(a, 'lastEvaluated', str)
    check(a, 'lastTriggered', str)
    check(a, 'modifiedTime', str)
    check(a, 'name', str)
    check(a, 'owner', dict)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'id', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'description', str)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a, 'query', dict)
    check(a['query'], 'description', str)
    check(a['query'], 'id', str)
    check(a['query'], 'name', str)
    check(a, 'schedule', dict)
    check(a['schedule'], 'type', str)
    check(a, 'status', str)
    check(a, 'triggerName', str)
    check(a, 'triggerOperator', str)
    check(a, 'triggerValue', str)