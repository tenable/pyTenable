from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_server_properties(api):
    assert isinstance(api.server.properties(), dict)

@pytest.mark.vcr()
def test_server_status(api):
    assert isinstance(api.server.status(), dict)