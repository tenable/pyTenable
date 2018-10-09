from .fixtures import *
from tenable.errors import *

def test_families(api):
    api.plugins.families()

def test_family_details_family_id_typeerror(api):
    with pytest.raises(TypeError):
        api.plugins.family_details('nope')

def test_family_details(api):
    resp = api.plugins.family_details(27)
    assert resp['id'] == 27

def test_plugin_details_plugin_id_typerror(api):
    with pytest.raises(TypeError):
        api.plugins.plugin_details('nope')

def test_plugin_details(api):
    resp = api.plugins.plugin_details(19506)
    assert resp['id'] == 19506
