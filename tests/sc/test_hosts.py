"""
test file to test various scenarios
in sc hosts
"""

import pytest

from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception
from ..checker import check


@pytest.mark.vcr()
def test_hosts_list_success_for_fields(security_center):
    """
    testing hosts list success for fields
    """
    hosts = security_center.hosts.list(
        fields=['id', 'uuid', 'tenableUUID', 'name', 'ipAddress'],
    )
    assert isinstance(hosts, list)
    for host in hosts:
        check(host, 'id', str)
        check(host, 'uuid', str)
        check(host, 'tenableUUID', str)
        check(host, 'name', str)
        check(host, 'ipAddress', str)

@pytest.mark.vcr()
def test_hosts_list_success(security_center):
    """
    testing hosts list success
    """
    resp = security_center.hosts.list()
    assert isinstance(resp, list)
    a_resp = resp[0]
    check(a_resp, 'id', str)
    check(a_resp, 'uuid', str)
    check(a_resp, 'tenableUUID', str)
    check(a_resp, 'name', str)
    check(a_resp, 'ipAddress', str)
    check(a_resp, 'os', str)
    check(a_resp, 'firstSeen', str)
    check(a_resp, 'lastSeen', str)
