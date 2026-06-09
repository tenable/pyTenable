import pytest

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.access_control.models import AllowedIPAddresses


def test_allowed_ip_address_model():
    m = AllowedIPAddresses.model_validate(
        {
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        }
    )
    assert m.ipv4 == ["192.168.0.1", "127.0.0.1"]
    assert m.ipv6 == []
    assert m.model_dump(mode="json") == {
        "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
        "allowed_ipv6_addresses": "",
    }
