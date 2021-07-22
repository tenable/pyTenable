'''
test file for testing various scenarios in current
'''
import pytest

from tests.checker import check


@pytest.mark.vcr()
def test_current_associate_cert(security_center):
    '''
    test current associate certificate
    '''
    resp = security_center.current.associate_cert()
    assert isinstance(resp, dict)
    check(resp, 'success', str)
    assert resp['success'] == 'certificate is associated successfully to the current user'


@pytest.mark.vcr()
def test_current_org(security_center):
    '''
    test current organization
    '''
    org = security_center.current.org(fields=['id', 'name'])
    assert isinstance(org, dict)
    check(org, 'id', str)
    check(org, 'name', str)


@pytest.mark.vcr()
def test_current_user(security_center):
    '''
    test current user
    '''
    user = security_center.current.user(fields=['id', 'name'])
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'name', str)
