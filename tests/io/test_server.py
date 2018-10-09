from tenable.errors import *
from .fixtures import *

def test_server_properties(api):
    assert isinstance(api.server.properties(), dict)

def test_server_status(api):
    assert isinstance(api.server.status(), dict)