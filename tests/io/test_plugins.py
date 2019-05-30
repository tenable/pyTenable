from tenable.errors import *
from ..checker import check, single
from datetime import date
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

@pytest.mark.vcr()
def test_plugins_list_page_typeerror(api):
    with pytest.raises(TypeError):
        api.plugins.list(page='one')

@pytest.mark.vcr()
def test_plugins_list_size_typeerror(api):
    with pytest.raises(TypeError):
        api.plugins.list(size='one')

@pytest.mark.vcr()
def test_plugins_list_last_updated_date_typeerror(api):
    with pytest.raises(TypeError):
        api.plugins.list(last_updated=1)

@pytest.mark.vcr()
def test_plugins_list_num_pages_typeerror(api):
    with pytest.raises(TypeError):
        api.plugins.list(num_pages='one')

@pytest.mark.vcr()
def test_plugins_list_success(api):
    plugins = api.plugins.list(
        last_updated=date(2019, 1, 1),
        num_pages=2,
        size=10)
    for p in plugins:
        check(p, 'attributes', dict)
        check(p['attributes'], 'description', str)
        check(p['attributes'], 'plugin_publication_date', str)
        check(p['attributes'], 'plugin_modification_date', str)
        check(p['attributes'], 'plugin_version', str)
        check(p['attributes'], 'synopsis', str)
        check(p['attributes'], 'risk_factor', str)
        check(p, 'id', int)
        check(p, 'name', str)