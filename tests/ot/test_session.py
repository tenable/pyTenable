import pytest
from tenable.errors import AuthenticationWarning
from tenable.ot import TenableOT


def test_session_auth():
    with pytest.warns(AuthenticationWarning):
        t = TenableOT()
