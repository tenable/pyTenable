from .fixtures import *
from tenable.errors import *

def test_agent_filters(api):
    filters = api.filters.agents_filters()
    assert isinstance(filters, list)