'''
test file for testing various scenarios in tickets
'''
import pytest

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check


@pytest.fixture
def ticket(request, security_center, vcr):
    '''
    test fixture for ticket
    '''
    assignee = security_center.current.user(fields=['id', 'name'])
    assert isinstance(assignee, dict)
    check(assignee, 'id', str)
    with vcr.use_cassette('test_ticket_create_success'):
        ticket = security_center.tickets.create('pytest', {'id': assignee['id'] })
    
    def teardown():
        try:
            with vcr.use_cassette('test_ticket_close_success'):
                security_center.tickets.edit(int(ticket['id']), status='Closed')
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return ticket


def test_tickets_constructor_assignee_typeerror(security_center):
    '''
    test tickets constructor for 'assignee' unexpected value error
    '''
    with pytest.raises(TypeError):
        security_center.tickets._constructor(assignee='not a dict')


def test_tickets_constructor_name_typeerror(security_center):
    '''
    test tickets constructor for 'name' unexpected value error
    '''
    with pytest.raises(TypeError):
        security_center.tickets._constructor(name=1)


def test_tickets_constructor_description_typeerror(security_center):
    '''
    test tickets constructor for 'description' unexpected value error
    '''
    with pytest.raises(TypeError):
        security_center.tickets._constructor(description=1)


def test_tickets_constructor_notes_typeerror(security_center):
    '''
    test tickets constructor for 'notes' unexpected value error
    '''
    with pytest.raises(TypeError):
        security_center.tickets._constructor(notes=1)


def test_tickets_constructor_classification_typeerror(security_center):
    '''
    test tickets constructor for 'classification' unexpected value error
    '''
    with pytest.raises(TypeError):
        security_center.tickets._constructor(classification=1)


def test_tickets_constructor_classification_unexpectedvalueerror(security_center):
    '''
    test tickets constructor for 'classification' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.tickets._constructor(classification='not a category')


def test_tickets_constructor_status_typeerror(security_center):
    '''
    test tickets constructor for 'status' unexpected value error
    '''
    with pytest.raises(TypeError):
        security_center.tickets._constructor(status=1)


def test_tickets_constructor_status_unexpectedvalueerror(security_center):
    '''
    test tickets constructor for 'status' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.tickets._constructor(status='not a status')


def test_tickets_constructor_assignee(security_center):
    '''
    Tests assignee is mapped correctly in the constructor.
    '''
    ticket_params = {'assignee': {}}

    ticket = security_center.tickets._constructor(**ticket_params)

    assert 'assignee' in ticket


def test_tickets_constructor_success(security_center):
    '''
    test ticket constructor for success
    '''
    resp = security_center.tickets._constructor(
        name = 'Example',
        assignee = { 'id': 0 },
        classification='Information',
        description='Test123',
        notes='Example notes'
    )
    assert resp == {
        'name': 'Example',
        'assignee': {
            'id': 0
        },
        'classification': 'Information',
        'description': 'Test123',
        'notes': 'Example notes'
    }


@pytest.mark.vcr()
def test_tickets_create_success(ticket):
    '''
    test ticket create for success
    '''
    assert isinstance(ticket, dict)
    check(ticket, 'id', str)


@pytest.mark.vcr()
def test_tickets_list_success(security_center):
    '''
    test ticket list for success
    '''
    tickets = security_center.tickets.list(fields=['id', 'name', 'description'])
    assert 'usable' in tickets, '\'usable\' not in tickets list'
    usable = tickets['usable']
    assert isinstance(usable, list), '\'usable\' not a list'

    assert 'manageable' in tickets, '\'manageable\' not in tickets list'
    manageable = tickets['manageable']
    assert isinstance(manageable, list), '\'manageable\' not a list'

    for ticket in usable:    
        check(ticket, 'id', str)
        check(ticket, 'name', str)
        check(ticket, 'description', str)
    for ticket in manageable:
        check(ticket, 'id', str)
        check(ticket, 'name', str)
        check(ticket, 'description', str)


@pytest.mark.vcr()
def test_tickets_details_id_typeerror(security_center):
    '''
    test tickets details for id type error
    '''
    with pytest.raises(TypeError):
        security_center.tickets.details('one')


@pytest.mark.vcr()
def test_tickets_details_fields_typeerror(security_center):
    '''
    test tickets details for 'fields item' type error
    '''
    with pytest.raises(TypeError):
        security_center.tickets.details(1, fields=[1])


@pytest.mark.vcr()
def test_tickets_edit_success(security_center, ticket):
    '''
    test ticket edits for success
    '''
    ticket = security_center.tickets.details(ticket['id'])
    assert isinstance(ticket, dict)
    check(ticket, 'id', str)
    security_center.tickets.edit(
        int(ticket['id']),
        description='edited description',
        notes='edited additional notes',
        classification='False Positive',
        status='Resolved'
    )

@pytest.mark.vcr()
def test_tickets_details_success(security_center, ticket):
    '''
    test ticket details for success
    '''
    ticket = security_center.tickets.details(ticket['id'])
    assert isinstance(ticket, dict)
    check(ticket, 'id', str)
    check(ticket, 'name', str)
    check(ticket, 'description', str)
    check(ticket, 'assignee', dict)
    check(ticket, 'creator', dict)
    check(ticket, 'owner', dict)
    check(ticket, 'ownerGroup', dict)
    check(ticket, 'assigneeGroup', dict)
    check(ticket, 'queries', list)
    check(ticket, 'classification', str)
    check(ticket, 'status', str)
    check(ticket, 'notes', str)
    check(ticket, 'assignedTime', str)
    check(ticket, 'resolvedTime', str)
    check(ticket, 'closedTime', str)
    check(ticket, 'createdTime', str)
    check(ticket, 'modifiedTime', str)
    check(ticket, 'canUse', str)
    check(ticket, 'canManage', str)
    check(ticket, 'canRespond', str)