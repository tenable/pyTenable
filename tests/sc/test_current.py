import pytest
from tests.checker import check


@pytest.mark.vcr()
def test_current_associate_cert(sc):
    resp = sc.current.associate_cert()
    assert isinstance(resp, dict)
    check(resp, 'success', str)
    assert resp['success'] == 'certificate is associated successfully to the current user'


@pytest.mark.vcr()
def test_current_org(sc):
    org = sc.current.org(fields=['id', 'name'])
    assert isinstance(org, dict)
    check(org, 'id', str)
    check(org, 'name', str)


@pytest.mark.vcr()
def test_current_user(sc):
    user = sc.current.user(fields=['id', 'name'])
    assert isinstance(user, dict)
    check(user, 'id', str)
    check(user, 'name', str)


