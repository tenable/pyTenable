"""
test file for testing various scenarios in current
"""

import responses
from responses import matchers

from tests.checker import check


@responses.activate
def test_current_associate_cert(tsc):
    """
    test current associate certificate
    """
    responses.post(
        'https://nourl/rest/currentUser/associateCert',
        json={
            'type': 'regular',
            'response': {
                'success': 'certificate is associated successfully to the current user'
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189100,
        },
    )
    resp = tsc.current.associate_cert()
    assert isinstance(resp, dict)
    check(resp, 'success', str)
    assert (
        resp['success'] == 'certificate is associated successfully to the current user'
    )


@responses.activate
def test_current_org(tsc):
    """
    test current organization
    """
    responses.get(
        'https://nourl/rest/currentOrganization',
        json={
            'type': 'regular',
            'response': {'id': '1', 'name': 'current_org'},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189100,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name'})],
    )
    org = tsc.current.org(fields=['id', 'name'])
    assert isinstance(org, dict)
    check(org, 'id', str)
    check(org, 'name', str)


@responses.activate
def test_current_user(tsc):
    """
    test current user
    """
    responses.get(
        'https://nourl/rest/currentUser',
        json={
            'type': 'regular',
            'response': {'id': '1', 'name': 'current_user'},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189100,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name'})],
    )
    user = tsc.current.user(fields=['id', 'name'])
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'name', str)
