"""
test file for testing various scenarios in tickets
"""
import re
import responses

from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check

RE_BASE = (
    r'https://nourl/rest'
)


def test_contructor(tsc):
    '''
    test tickets contstructor
    '''
    tickets = tsc.tickets._constructor(assignee={'id': 0}, name='test', description='test123', notes='additional notes', classification='Information', status='Resolved')
    assert isinstance(tickets, dict)
    assert tickets['assignee'] == {'id': 0}
    assert tickets['name'] == 'test'
    assert tickets['description'] == 'test123'
    assert tickets['notes'] == 'additional notes'
    assert tickets['classification'] == 'Information'
    assert tickets['status'] == 'Resolved'


@responses.activate
def test_tickets_list(tsc):
    '''
    test listing tickets
    '''
    responses.add(
        responses.GET,
        re.compile(f'{RE_BASE}/ticket'),
        json={
            "type" : "regular",
            "response" : {
                "usable" : [
                    {
                        "id" : "1",
                        "name" : "TestTicket",
                        "description" : ""            }
                ],
                "manageable" : [
                    {
                        "id" : "1",
                        "name" : "TestTicket",
                        "description" : ""            }
                ]
            },
            "error_code" : 0,
            "error_msg" : "",
            "warnings" : {},
            "timestamp" : 1423499298
        }
    )
    tickets = tsc.tickets.list(fields={'id': 1})
    assert isinstance(tickets, dict)
    assert isinstance(tickets['usable'], list)
    assert len(tickets['usable']) > 0
    assert isinstance(tickets['usable'][0], dict)
    assert tickets['usable'][0]['id'] == '1'


@responses.activate
def test_tickets_create(tsc):
    '''
    test creating a ticket
    '''
    responses.add(
        responses.POST,
        re.compile(f'{RE_BASE}/ticket'),
        json={
            "type" : "regular",
            "response" : {
                "id" : "1",
                "name" : "test",
                "description" : "Test",
                "classification" : "Unauthorized System",
                "status" : "assigned",
                "notes" : "Created for testing of alerts",
                "assignedTime" : "1424810461",
                "resolvedTime" : "-1",
                "closedTime" : "-1",
                "createdTime" : "1424810461",
                "modifiedTime" : "1424810461",
                "queries" : [],
                "canUse" : "true",
                "canManage" : "true",
                "canRespond" : "true",
                "creator" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "Security Manager",
                    "lastname" : "",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "owner" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "Security Manager",
                    "lastname" : "",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "assignee" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "Security Manager",
                    "lastname" : "",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "ownerGroup" : {
                    "id" : "0",
                    "name" : "Full Access",
                    "description" : "Full Access group"     },
                "assigneeGroup" : {
                    "id" : "0",
                    "name" : "Full Access",
                    "description" : "Full Access group"     }
            },
            "error_code" : 0,
            "error_msg" : "",
            "warnings" : [],
            "timestamp" : 1426879889
        }
    )
    tickets = tsc.tickets.create(
        name="test",
        assignee={
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "Security Manager",
                    "lastname" : "",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     }
        )
    assert isinstance(tickets, dict)


@responses.activate
def test_tickets_details(tsc):
    '''
    test getting a specific test
    '''
    responses.add(
        responses.GET,
        re.compile(f'{RE_BASE}/ticket/1'),
        json={
            "type" : "regular",
            "response" : {
                "id" : "1",
                "name" : "TestTicket",
                "description" : "",
                "classification" : "Information",
                "status" : "assigned",
                "notes" : "",
                "assignedTime" : "1423501383",
                "resolvedTime" : "-1",
                "closedTime" : "-1",
                "createdTime" : "1423501383",
                "modifiedTime" : "1423501383",
                "canUse" : "true",
                "canManage" : "true",
                "canRespond" : "true",
                "creator" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "hi",
                    "lastname" : "User",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "owner" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "hi",
                    "lastname" : "User",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "assignee" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "hi",
                    "lastname" : "User",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "ownerGroup" : {
                    "id" : "0",
                    "name" : "Full Access",
                    "description" : "Full Access group"     },
                "assigneeGroup" : {
                    "id" : "0",
                    "name" : "Full Access",
                    "description" : "Full Access group"     }
            },
            "error_code" : 0,
            "error_msg" : "",
            "warnings" : {},
            "timestamp" : 1423501383
        }
    )
    ticket = tsc.tickets.details(id=1, fields={'classification': 'Information'})
    assert isinstance(ticket, dict)
    assert ticket['classification'] == 'Information'


@responses.activate
def test_tickets_edit(tsc):
    '''
    testing editing a ticket
    '''
    responses.add(
        responses.PATCH,
        re.compile(f'{RE_BASE}/ticket/1'),
        json={
            "type" : "regular",
            "response" : {
                "id" : "1",
                "name" : "TestTicket",
                "description" : "",
                "classification" : "False Positive",
                "status" : "assigned",
                "notes" : "",
                "assignedTime" : "1423501383",
                "resolvedTime" : "-1",
                "closedTime" : "-1",
                "createdTime" : "1423501383",
                "modifiedTime" : "1423501383",
                "canUse" : "true",
                "canManage" : "true",
                "canRespond" : "true",
                "creator" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "hi",
                    "lastname" : "User",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "owner" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "hi",
                    "lastname" : "User",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "assignee" : {
                    "id" : "1",
                    "username" : "head",
                    "firstname" : "hi",
                    "lastname" : "User",
                    "uuid" : "96F2AD1B-1B83-462E-908A-84E6054F6B64"     },
                "ownerGroup" : {
                    "id" : "0",
                    "name" : "Full Access",
                    "description" : "Full Access group"     },
                "assigneeGroup" : {
                    "id" : "0",
                    "name" : "Full Access",
                    "description" : "Full Access group"     }
            },
            "error_code" : 0,
            "error_msg" : "",
            "warnings" : {},
            "timestamp" : 1423501383
        }
    )
    ticket = tsc.tickets.edit(id=1, classification="False Positive")
    assert isinstance(ticket, dict)
    assert ticket['classification'] == 'False Positive'
