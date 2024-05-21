import pytest

from tenable.ot import TenableOT


def test_session_auth():
    t = TenableOT(api_key="SECRET_KEY")
    with pytest.warns(
        UserWarning, match="Session Auth isn't supported with the Tenable OT Security APIs"
    ):
        t._session_auth()
