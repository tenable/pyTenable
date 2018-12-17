from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_families(api):
    families = api.plugins.families()
    assert isinstance(families, list)
    for f in families:
        check(f, 'count', int)
        check(f, 'id', int)
        check(f, 'name', str)

@pytest.mark.vcr()
def test_family_details_family_id_typeerror(api):
    with pytest.raises(TypeError):
        api.plugins.family_details('nope')

@pytest.mark.vcr()
def test_family_details(api):
    f = api.plugins.family_details(27)
    assert isinstance(f, dict)
    check(f, 'name', str)
    check(f, 'id', int)
    check(f, 'plugins', list)
    for p in f['plugins']:
        check(p, 'id', int)
        check(p, 'name', str)
    assert f['id'] == 27

@pytest.mark.vcr()
def test_plugin_details_plugin_id_typerror(api):
    with pytest.raises(TypeError):
        api.plugins.plugin_details('nope')

@pytest.mark.vcr()
def test_plugin_details(api):
    p = api.plugins.plugin_details(19506)
    assert isinstance(p, dict)
    check(p, 'attributes', list)
    for a in p['attributes']:
        check(a, 'attribute_name', str)
        check(a, 'attribute_value', str)
    check(p, 'family_name', str)
    check(p, 'id', int)
    check(p, 'name', str)
    assert p['id'] == 19506
