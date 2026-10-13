"""
test file to test various scenarios in sc alerts
"""

import pytest
import responses

from tenable.errors import UnexpectedValueError
from ..checker import check


@pytest.fixture
def alert():
    """
    test fixture for alert
    """
    return {
        'id': '8',
        'name': 'Example Alert',
        'description': '',
        'triggerName': 'sumip',
        'triggerOperator': '>=',
        'triggerValue': '100',
        'modifiedTime': '1550599951',
        'createdTime': '1550599951',
        'lastTriggered': '0',
        'lastEvaluated': '0',
        'executeOnEveryTrigger': 'false',
        'didTriggerLastEvaluation': 'false',
        'status': '0',
        'canUse': 'true',
        'canManage': 'true',
    }


def test_alerts_constructor_name_typeerror(tsc):
    """
    test alerts constructor for name type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(name=1)


def test_alerts_constructor_description_typeerror(tsc):
    """
    test alerts constructor for description type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(description=1)


def test_alerts_constructor_query_typeerror(tsc):
    """
    test alerts constructor for query type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(query=1)


def test_alerts_constructor_always_exec_on_trigger_typeerror(tsc):
    """
    test alerts constructor for 'always exec on trigger' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(always_exec_on_trigger='nope')


def test_alerts_constructor_trigger_typeerror(tsc):
    """
    test alerts constructor for trigger type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(trigger=1)


def test_alerts_constructor_trigger_name_typeerror(tsc):
    """
    test alerts constructor for 'trigger name' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(trigger=(1, '=', 'something'))


def test_alerts_constructor_trigger_operator_typeerror(tsc):
    """
    test alerts constructor for 'trigger operator' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(trigger=('name', 1, 'something'))


def test_alerts_constructor_trigger_operator_unexpectedvalueerror(tsc):
    """
    test alerts constructor for 'trigger operator' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.alerts._constructor(trigger=('name', 'eq', 'something'))


def test_alerts_constructor_trigger_value_typeerror(tsc):
    """
    test alerts constructor for 'trigger value' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts._constructor(trigger=('name', '=', 1))


def test_alerts_constructor_success(tsc):
    """
    test alerts constructor for success
    """
    alert = tsc.alerts._constructor(
        query_id=1, always_exec_on_trigger=True, schedule={'type': 'ical'}
    )
    assert isinstance(alert, dict)


def test_alerts_constructor(tsc):
    """
    test alerts constructor
    """
    alert = tsc.alerts._constructor(
        ('severity', '=', '3,4'),
        name='Example Alert',
        trigger=('sumip', '>=', '100'),
        action=[
            {'type': 'notification', 'message': 'Example Message', 'users': [{'id': 1}]}
        ],
    )
    assert alert == {
        'name': 'Example Alert',
        'action': [
            {'message': 'Example Message', 'type': 'notification', 'users': [{'id': 1}]}
        ],
        'query': {
            'type': 'vuln',
            'filters': [{'filterName': 'severity', 'operator': '=', 'value': '3,4'}],
        },
        'triggerName': 'sumip',
        'triggerOperator': '>=',
        'triggerValue': '100',
    }


def test_alerts_list_fields_typeerror(tsc):
    """
    test alerts for list fields type error
    """
    with pytest.raises(TypeError):
        tsc.alerts.list(fields=1)


@responses.activate
def test_alerts_list_success(tsc, alert):
    """
    test alerts for list success
    """
    responses.get(
        'https://nourl/rest/alert',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {'id': '1', 'name': 'Test Alert', 'description': '', 'status': '0'},
                    {
                        'id': '3',
                        'name': 'Example Alert',
                        'description': '',
                        'status': '0',
                    },
                ],
                'manageable': [
                    {'id': '1', 'name': 'Test Alert', 'description': '', 'status': '0'},
                    {
                        'id': '3',
                        'name': 'Example Alert',
                        'description': '',
                        'status': '0',
                    },
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550599938,
        },
    )
    alerts = tsc.alerts.list()
    assert isinstance(alerts, dict)
    for alert in alerts['manageable']:
        check(alert, 'description', str)
        check(alert, 'id', str)
        check(alert, 'name', str)
        check(alert, 'status', str)


def test_alerts_details_id_typeerror(tsc):
    """
    test alerts for 'details id' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts.details('nope')


def test_alerts_fields_typeerror(tsc):
    """
    test alerts for fields type error
    """
    with pytest.raises(TypeError):
        tsc.alerts.details(1, fields=1)


@responses.activate
def test_alerts_details_success(tsc, alert):
    """
    test alerts for details success
    """
    responses.get(
        'https://nourl/rest/alert/8',
        json={
            'type': 'regular',
            'response': {
                'id': '4',
                'name': 'Example Alert',
                'description': '',
                'triggerName': 'sumip',
                'triggerOperator': '>=',
                'triggerValue': '100',
                'modifiedTime': '1550599941',
                'createdTime': '1550599941',
                'lastTriggered': '0',
                'lastEvaluated': '0',
                'executeOnEveryTrigger': 'false',
                'didTriggerLastEvaluation': 'false',
                'status': '0',
                'action': [
                    {
                        'id': '4',
                        'type': 'notification',
                        'definition': {
                            'message': 'Example Message',
                            'users': [
                                {
                                    'id': '1',
                                    'username': 'steve',
                                    'firstname': 'Steve',
                                    'lastname': 'McGrath',
                                }
                            ],
                        },
                        'status': '0',
                        'users': [
                            {
                                'id': '1',
                                'username': 'steve',
                                'firstname': 'Steve',
                                'lastname': 'McGrath',
                            }
                        ],
                        'objectID': None,
                    }
                ],
                'schedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                'query': {
                    'id': '570',
                    'name': "Query for alert 'Example Alert' at 1550599941",
                    'description': '',
                },
                'canUse': 'true',
                'canManage': 'true',
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550599943,
        },
    )
    alert = tsc.alerts.details(int(alert['id']))
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


@responses.activate
def test_alerts_create_success(tsc):
    """
    test alerts for create success
    """
    responses.post(
        'https://nourl/rest/alert',
        json={
            'type': 'regular',
            'response': {
                'id': '8',
                'name': 'Example Alert',
                'description': '',
                'triggerName': 'sumip',
                'triggerOperator': '>=',
                'triggerValue': '100',
                'modifiedTime': '1550599951',
                'createdTime': '1550599951',
                'lastTriggered': '0',
                'lastEvaluated': '0',
                'executeOnEveryTrigger': 'false',
                'didTriggerLastEvaluation': 'false',
                'status': '0',
                'action': [
                    {
                        'id': '9',
                        'type': 'notification',
                        'definition': {
                            'message': 'Example Message',
                            'users': [
                                {
                                    'id': '1',
                                    'username': 'steve',
                                    'firstname': 'Steve',
                                    'lastname': 'McGrath',
                                }
                            ],
                        },
                        'status': '0',
                        'users': [
                            {
                                'id': '1',
                                'username': 'steve',
                                'firstname': 'Steve',
                                'lastname': 'McGrath',
                            }
                        ],
                        'objectID': None,
                    }
                ],
                'schedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                'query': {
                    'id': '574',
                    'name': "Query for alert 'Example Alert' at 1550599951",
                    'description': '',
                },
                'canUse': 'true',
                'canManage': 'true',
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550599951,
        },
    )
    alert = tsc.alerts.create(
        ('severity', '=', '3,4'),
        name='Example Alert',
        trigger=('sumip', '>=', '100'),
        action=[
            {'type': 'notification', 'message': 'Example Message', 'users': [{'id': 1}]}
        ],
    )
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


def test_alerts_edit_id_typerror(tsc):
    """
    test alerts for 'edit id' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts.edit('one')


@responses.activate
def test_alerts_edit_success(tsc, alert):
    """
    test alerts for edit success
    """
    responses.patch(
        'https://nourl/rest/alert/8',
        json={
            'type': 'regular',
            'response': {
                'id': '6',
                'name': 'new name for example',
                'description': '',
                'triggerName': 'sumip',
                'triggerOperator': '>=',
                'triggerValue': '100',
                'modifiedTime': '1550599948',
                'createdTime': '1550599946',
                'lastTriggered': '0',
                'lastEvaluated': '0',
                'executeOnEveryTrigger': 'false',
                'didTriggerLastEvaluation': 'false',
                'status': '0',
                'action': [
                    {
                        'id': '7',
                        'type': 'notification',
                        'definition': {
                            'message': 'Example Message',
                            'users': [
                                {
                                    'id': '1',
                                    'username': 'steve',
                                    'firstname': 'Steve',
                                    'lastname': 'McGrath',
                                }
                            ],
                        },
                        'status': '0',
                        'users': [
                            {
                                'id': '1',
                                'username': 'steve',
                                'firstname': 'Steve',
                                'lastname': 'McGrath',
                            }
                        ],
                        'objectID': None,
                    }
                ],
                'schedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                'query': {
                    'id': '572',
                    'name': "Query for alert 'Example Alert' at 1550599946",
                    'description': '',
                },
                'canUse': 'true',
                'canManage': 'true',
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550599948,
        },
    )
    alert = tsc.alerts.edit(int(alert['id']), name='new name for example')
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


def test_alerts_delete_id_typeerror(tsc):
    """
    test alerts for 'delete id' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts.delete('one')


@responses.activate
def test_alerts_delete_success(tsc, alert):
    """
    test alerts for delete success
    """
    responses.delete(
        'https://nourl/rest/alert/8',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550599950,
        },
    )
    tsc.alerts.delete(int(alert['id']))


def test_alerts_execute_id_typeerror(tsc):
    """
    test alerts for 'execute id' type error
    """
    with pytest.raises(TypeError):
        tsc.alerts.execute('one')


@responses.activate
def test_alerts_execute_success(tsc, alert):
    """
    test alerts for execute success
    """
    responses.post(
        'https://nourl/rest/alert/8/execute',
        json={
            'type': 'regular',
            'response': {
                'id': '8',
                'name': 'Example Alert',
                'description': '',
                'triggerName': 'sumip',
                'triggerOperator': '>=',
                'triggerValue': '100',
                'modifiedTime': '1550599951',
                'createdTime': '1550599951',
                'lastTriggered': '0',
                'lastEvaluated': '0',
                'executeOnEveryTrigger': 'false',
                'didTriggerLastEvaluation': 'false',
                'status': '0',
                'action': [
                    {
                        'id': '9',
                        'type': 'notification',
                        'definition': {
                            'message': 'Example Message',
                            'users': [
                                {
                                    'id': '1',
                                    'username': 'steve',
                                    'firstname': 'Steve',
                                    'lastname': 'McGrath',
                                }
                            ],
                        },
                        'status': '0',
                        'users': [
                            {
                                'id': '1',
                                'username': 'steve',
                                'firstname': 'Steve',
                                'lastname': 'McGrath',
                            }
                        ],
                        'objectID': None,
                    }
                ],
                'schedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                'query': {
                    'id': '574',
                    'name': "Query for alert 'Example Alert' at 1550599951",
                    'description': '',
                },
                'canUse': 'true',
                'canManage': 'true',
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550599952,
        },
    )
    alert = tsc.alerts.execute(int(alert['id']))
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
