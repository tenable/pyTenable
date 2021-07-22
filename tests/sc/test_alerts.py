'''
test file to test various scenarios in sc alerts
'''
import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check


@pytest.fixture
def alert(request, vcr, security_center):
    '''
    test fixture for alert
    '''
    with vcr.use_cassette('alert'):
        alert = security_center.alerts.create(
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
            security_center.alerts.delete(int(alert['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return alert


def test_alerts_constructor_name_typeerror(security_center):
    '''
    test alerts constructor for name type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(name=1)


def test_alerts_constructor_description_typeerror(security_center):
    '''
    test alerts constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(description=1)


def test_alerts_constructor_query_typeerror(security_center):
    '''
    test alerts constructor for query type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(query=1)


def test_alerts_constructor_always_exec_on_trigger_typeerror(security_center):
    '''
    test alerts constructor for 'always exec on trigger' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(always_exec_on_trigger='nope')


def test_alerts_constructor_trigger_typeerror(security_center):
    '''
    test alerts constructor for trigger type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(trigger=1)


def test_alerts_constructor_trigger_name_typeerror(security_center):
    '''
    test alerts constructor for 'trigger name' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(trigger=(1, '=', 'something'))


def test_alerts_constructor_trigger_operator_typeerror(security_center):
    '''
    test alerts constructor for 'trigger operator' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(trigger=('name', 1, 'something'))


def test_alerts_constructor_trigger_operator_unexpectedvalueerror(security_center):
    '''
    test alerts constructor for 'trigger operator' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.alerts._constructor(trigger=('name', 'eq', 'something'))


def test_alerts_constructor_trigger_value_typeerror(security_center):
    '''
    test alerts constructor for 'trigger value' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts._constructor(trigger=('name', '=', 1))


def test_alerts_constructor_success(security_center):
    '''
    test alerts constructor for success
    '''
    alert = security_center.alerts._constructor(query_id=1,
                                                always_exec_on_trigger=True,
                                                schedule={'type': 'ical'})
    assert isinstance(alert, dict)


def test_alerts_constructor(security_center):
    '''
    test alerts constructor
    '''
    alert = security_center.alerts._constructor(
        ('severity', '=', '3,4'),
        name='Example Alert',
        trigger=('sumip', '>=', '100'),
        action=[{
            'type': 'notification',
            'message': 'Example Message',
            'users': [{'id': 1}]}])
    assert alert == {
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


def test_alerts_list_fields_typeerror(security_center):
    '''
    test alerts for list fields type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts.list(fields=1)


@pytest.mark.vcr()
def test_alerts_list_success(security_center, alert):
    '''
    test alerts for list success
    '''
    alerts = security_center.alerts.list()
    assert isinstance(alerts, dict)
    for alert in alerts['manageable']:
        check(alert, 'description', str)
        check(alert, 'id', str)
        check(alert, 'name', str)
        check(alert, 'status', str)


def test_alerts_details_id_typeerror(security_center):
    '''
    test alerts for 'details id' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts.details('nope')


def test_alerts_fields_typeerror(security_center):
    '''
    test alerts for fields type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts.details(1, fields=1)


@pytest.mark.vcr()
def test_alerts_details_success(security_center, alert):
    '''
    test alerts for details success
    '''
    alert = security_center.alerts.details(int(alert['id']))
    assert isinstance(alert, dict)
    check(alert, 'action', list)
    for action in alert['action']:
        assert isinstance(action, dict)
        check(action, 'type', str)
        check(action, 'definition', dict)
        if action['type'] == 'notification':
            check(action['definition'], 'message', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
        if action['type'] == 'email':
            check(action['definition'], 'subject', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'addresses', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
            check(action['definition'], 'includeResults', str)
        if action['type'] == 'report':
            check(action['definition'], 'report', dict)
            check(action['definition']['report'], 'id', str)
        if action['type'] == 'scan':
            check(action['definition'], 'scan', dict)
            check(action['definition']['scan'], 'id', int)
        if action['type'] == 'syslog':
            check(action['definition'], 'host', str)
            check(action['definition'], 'port', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'severity', str)
        if action['type'] == 'ticket':
            check(action['definition'], 'assignee', dict)
            check(action['definition']['assignee'], 'id', str)
            check(action['definition'], 'name', str)
            check(action['definition'], 'description', str)
            check(action['definition'], 'notes', str)
        check(action, 'id', str)
        check(action, 'objectID', str, allow_none=True)
        check(action, 'users', list)
        for user in action['users']:
            check(user, 'firstname', str)
            check(user, 'id', str)
            check(user, 'lastname', str)
            check(user, 'username', str)
    check(alert, 'canManage', str)
    check(alert, 'canUse', str)
    check(alert, 'description', str)
    check(alert, 'didTriggerLastEvaluation', str)
    check(alert, 'executeOnEveryTrigger', str)
    check(alert, 'id', str)
    check(alert, 'lastEvaluated', str)
    check(alert, 'lastTriggered', str)
    check(alert, 'modifiedTime', str)
    check(alert, 'name', str)
    check(alert, 'owner', dict)
    check(alert['owner'], 'firstname', str)
    check(alert['owner'], 'id', str)
    check(alert['owner'], 'lastname', str)
    check(alert['owner'], 'username', str)
    check(alert, 'ownerGroup', dict)
    check(alert['ownerGroup'], 'description', str)
    check(alert['ownerGroup'], 'id', str)
    check(alert['ownerGroup'], 'name', str)
    check(alert, 'query', dict)
    check(alert['query'], 'description', str)
    check(alert['query'], 'id', str)
    check(alert['query'], 'name', str)
    check(alert, 'schedule', dict)
    check(alert['schedule'], 'type', str)
    check(alert, 'status', str)
    check(alert, 'triggerName', str)
    check(alert, 'triggerOperator', str)
    check(alert, 'triggerValue', str)


@pytest.mark.vcr()
def test_alerts_create_success(alert):
    '''
    test alerts for create success
    '''
    assert isinstance(alert, dict)
    check(alert, 'action', list)
    for action in alert['action']:
        assert isinstance(action, dict)
        check(action, 'type', str)
        check(action, 'definition', dict)
        if action['type'] == 'notification':
            check(action['definition'], 'message', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
        if action['type'] == 'email':
            check(action['definition'], 'subject', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'addresses', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
            check(action['definition'], 'includeResults', str)
        if action['type'] == 'report':
            check(action['definition'], 'report', dict)
            check(action['definition']['report'], 'id', str)
        if action['type'] == 'scan':
            check(action['definition'], 'scan', dict)
            check(action['definition']['scan'], 'id', int)
        if action['type'] == 'syslog':
            check(action['definition'], 'host', str)
            check(action['definition'], 'port', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'severity', str)
        if action['type'] == 'ticket':
            check(action['definition'], 'assignee', dict)
            check(action['definition']['assignee'], 'id', str)
            check(action['definition'], 'name', str)
            check(action['definition'], 'description', str)
            check(action['definition'], 'notes', str)
        check(action, 'id', str)
        check(action, 'objectID', str, allow_none=True)
        check(action, 'users', list)
        for user in action['users']:
            check(user, 'firstname', str)
            check(user, 'id', str)
            check(user, 'lastname', str)
            check(user, 'username', str)
    check(alert, 'canManage', str)
    check(alert, 'canUse', str)
    check(alert, 'description', str)
    check(alert, 'didTriggerLastEvaluation', str)
    check(alert, 'executeOnEveryTrigger', str)
    check(alert, 'id', str)
    check(alert, 'lastEvaluated', str)
    check(alert, 'lastTriggered', str)
    check(alert, 'modifiedTime', str)
    check(alert, 'name', str)
    check(alert, 'owner', dict)
    check(alert['owner'], 'firstname', str)
    check(alert['owner'], 'id', str)
    check(alert['owner'], 'lastname', str)
    check(alert['owner'], 'username', str)
    check(alert, 'ownerGroup', dict)
    check(alert['ownerGroup'], 'description', str)
    check(alert['ownerGroup'], 'id', str)
    check(alert['ownerGroup'], 'name', str)
    check(alert, 'query', dict)
    check(alert['query'], 'description', str)
    check(alert['query'], 'id', str)
    check(alert['query'], 'name', str)
    check(alert, 'schedule', dict)
    check(alert['schedule'], 'type', str)
    check(alert, 'status', str)
    check(alert, 'triggerName', str)
    check(alert, 'triggerOperator', str)
    check(alert, 'triggerValue', str)


def test_alerts_edit_id_typerror(security_center):
    '''
    test alerts for 'edit id' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts.edit('one')


@pytest.mark.vcr()
def test_alerts_edit_success(security_center, alert):
    '''
    test alerts for edit success
    '''
    alert = security_center.alerts.edit(int(alert['id']), name='new name for example')
    assert isinstance(alert, dict)
    check(alert, 'action', list)
    for action in alert['action']:
        assert isinstance(action, dict)
        check(action, 'type', str)
        check(action, 'definition', dict)
        if action['type'] == 'notification':
            check(action['definition'], 'message', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
        if action['type'] == 'email':
            check(action['definition'], 'subject', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'addresses', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
            check(action['definition'], 'includeResults', str)
        if action['type'] == 'report':
            check(action['definition'], 'report', dict)
            check(action['definition']['report'], 'id', str)
        if action['type'] == 'scan':
            check(action['definition'], 'scan', dict)
            check(action['definition']['scan'], 'id', int)
        if action['type'] == 'syslog':
            check(action['definition'], 'host', str)
            check(action['definition'], 'port', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'severity', str)
        if action['type'] == 'ticket':
            check(action['definition'], 'assignee', dict)
            check(action['definition']['assignee'], 'id', str)
            check(action['definition'], 'name', str)
            check(action['definition'], 'description', str)
            check(action['definition'], 'notes', str)
        check(action, 'id', str)
        check(action, 'objectID', str, allow_none=True)
        check(action, 'users', list)
        for user in action['users']:
            check(user, 'firstname', str)
            check(user, 'id', str)
            check(user, 'lastname', str)
            check(user, 'username', str)
    check(alert, 'canManage', str)
    check(alert, 'canUse', str)
    check(alert, 'description', str)
    check(alert, 'didTriggerLastEvaluation', str)
    check(alert, 'executeOnEveryTrigger', str)
    check(alert, 'id', str)
    check(alert, 'lastEvaluated', str)
    check(alert, 'lastTriggered', str)
    check(alert, 'modifiedTime', str)
    check(alert, 'name', str)
    check(alert, 'owner', dict)
    check(alert['owner'], 'firstname', str)
    check(alert['owner'], 'id', str)
    check(alert['owner'], 'lastname', str)
    check(alert['owner'], 'username', str)
    check(alert, 'ownerGroup', dict)
    check(alert['ownerGroup'], 'description', str)
    check(alert['ownerGroup'], 'id', str)
    check(alert['ownerGroup'], 'name', str)
    check(alert, 'query', dict)
    check(alert['query'], 'description', str)
    check(alert['query'], 'id', str)
    check(alert['query'], 'name', str)
    check(alert, 'schedule', dict)
    check(alert['schedule'], 'type', str)
    check(alert, 'status', str)
    check(alert, 'triggerName', str)
    check(alert, 'triggerOperator', str)
    check(alert, 'triggerValue', str)


def test_alerts_delete_id_typeerror(security_center):
    '''
    test alerts for 'delete id' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts.delete('one')


@pytest.mark.vcr()
def test_alerts_delete_success(security_center, alert):
    '''
    test alerts for delete success
    '''
    security_center.alerts.delete(int(alert['id']))


def test_alerts_execute_id_typeerror(security_center):
    '''
    test alerts for 'execute id' type error
    '''
    with pytest.raises(TypeError):
        security_center.alerts.execute('one')


@pytest.mark.vcr()
def test_alerts_execute_success(security_center, alert):
    '''
    test alerts for execute success
    '''
    alert = security_center.alerts.execute(int(alert['id']))
    assert isinstance(alert, dict)
    check(alert, 'action', list)
    for action in alert['action']:
        assert isinstance(action, dict)
        check(action, 'type', str)
        check(action, 'definition', dict)
        if action['type'] == 'notification':
            check(action['definition'], 'message', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
        if action['type'] == 'email':
            check(action['definition'], 'subject', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'addresses', str)
            check(action['definition'], 'users', list)
            for user in action['definition']['users']:
                check(user, 'firstname', str)
                check(user, 'id', str)
                check(user, 'lastname', str)
                check(user, 'username', str)
            check(action['definition'], 'includeResults', str)
        if action['type'] == 'report':
            check(action['definition'], 'report', dict)
            check(action['definition']['report'], 'id', str)
        if action['type'] == 'scan':
            check(action['definition'], 'scan', dict)
            check(action['definition']['scan'], 'id', int)
        if action['type'] == 'syslog':
            check(action['definition'], 'host', str)
            check(action['definition'], 'port', str)
            check(action['definition'], 'message', str)
            check(action['definition'], 'severity', str)
        if action['type'] == 'ticket':
            check(action['definition'], 'assignee', dict)
            check(action['definition']['assignee'], 'id', str)
            check(action['definition'], 'name', str)
            check(action['definition'], 'description', str)
            check(action['definition'], 'notes', str)
        check(action, 'id', str)
        check(action, 'objectID', str, allow_none=True)
        check(action, 'users', list)
        for user in action['users']:
            check(user, 'firstname', str)
            check(user, 'id', str)
            check(user, 'lastname', str)
            check(user, 'username', str)
    check(alert, 'canManage', str)
    check(alert, 'canUse', str)
    check(alert, 'description', str)
    check(alert, 'didTriggerLastEvaluation', str)
    check(alert, 'executeOnEveryTrigger', str)
    check(alert, 'id', str)
    check(alert, 'lastEvaluated', str)
    check(alert, 'lastTriggered', str)
    check(alert, 'modifiedTime', str)
    check(alert, 'name', str)
    check(alert, 'owner', dict)
    check(alert['owner'], 'firstname', str)
    check(alert['owner'], 'id', str)
    check(alert['owner'], 'lastname', str)
    check(alert['owner'], 'username', str)
    check(alert, 'ownerGroup', dict)
    check(alert['ownerGroup'], 'description', str)
    check(alert['ownerGroup'], 'id', str)
    check(alert['ownerGroup'], 'name', str)
    check(alert, 'query', dict)
    check(alert['query'], 'description', str)
    check(alert['query'], 'id', str)
    check(alert['query'], 'name', str)
    check(alert, 'schedule', dict)
    check(alert['schedule'], 'type', str)
    check(alert, 'status', str)
    check(alert, 'triggerName', str)
    check(alert, 'triggerOperator', str)
    check(alert, 'triggerValue', str)
