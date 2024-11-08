import os
import pytest
from tenable.errors import AuthenticationWarning
from tenable.ot import TenableOT


def test_session_auth():
    os.environ.pop('TOT_API_KEY', None)
    with pytest.warns(AuthenticationWarning):
        t = TenableOT(url='http://nourl')
