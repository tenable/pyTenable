'''
test plugins
'''
from datetime import date
import pytest
from tenable.io.plugins import PluginIterator
from ..checker import check


@pytest.mark.vcr()
def test_families(api):
    '''test to get the plugin families'''
    families = api.plugins.families()
    assert isinstance(families, list)
    for family in families:
        check(family, 'count', int)
        check(family, 'id', int)
        check(family, 'name', str)


@pytest.mark.vcr()
def test_family_details_family_id_typeerror(api):
    '''test to raise the exception when parameter is not passed of expected type'''
    with pytest.raises(TypeError):
        api.plugins.family_details('nope')


@pytest.mark.vcr()
def test_family_details(api):
    '''test to get the family details'''
    data = api.plugins.family_details(27)
    assert isinstance(data, dict)
    check(data, 'name', str)
    check(data, 'id', int)
    check(data, 'plugins', list)
    for plugin in data['plugins']:
        check(plugin, 'id', int)
        check(plugin, 'name', str)
    assert data['id'] == 27


@pytest.mark.vcr()
def test_plugin_details_plugin_id_typerror(api):
    '''test to raise the exception when parameter is not passed of expected type'''
    with pytest.raises(TypeError):
        api.plugins.plugin_details('nope')


@pytest.mark.vcr()
def test_plugin_details(api):
    '''test to get the plugin details'''
    detail = api.plugins.plugin_details(19506)
    assert isinstance(detail, dict)
    check(detail, 'attributes', list)
    for attribute in detail['attributes']:
        check(attribute, 'attribute_name', str)
        check(attribute, 'attribute_value', str)
    check(detail, 'family_name', str)
    check(detail, 'id', int)
    check(detail, 'name', str)
    assert detail['id'] == 19506


@pytest.mark.vcr()
def test_plugins_list_page_typeerror(api):
    '''test to raise the exception when parameter is not passed of expected type'''
    with pytest.raises(TypeError):
        api.plugins.list(page='one')


@pytest.mark.vcr()
def test_plugins_list_size_typeerror(api):
    '''test to raise the exception when parameter is not passed of expected type'''
    with pytest.raises(TypeError):
        api.plugins.list(size='one')


@pytest.mark.vcr()
def test_plugins_list_last_updated_date_typeerror(api):
    '''test to raise the exception when parameter is not passed of expected type'''
    with pytest.raises(TypeError):
        api.plugins.list(last_updated=1)


@pytest.mark.vcr()
def test_plugins_list_num_pages_typeerror(api):
    '''test to raise the exception when parameter is not passed of expected type'''
    with pytest.raises(TypeError):
        api.plugins.list(num_pages='one')


@pytest.mark.vcr()
def test_plugins_list_success(api):
    '''test to get the plugins list'''
    plugins = api.plugins.list(
        last_updated=date(2019, 1, 1),
        num_pages=2,
        size=10)
    for plugin in plugins:
        check(plugin, 'attributes', dict)
        check(plugin['attributes'], 'description', str)
        check(plugin['attributes'], 'plugin_publication_date', str)
        check(plugin['attributes'], 'plugin_modification_date', str)
        check(plugin['attributes'], 'synopsis', str)
        check(plugin['attributes'], 'risk_factor', str)
        check(plugin, 'id', int)
        check(plugin, 'name', str)


@pytest.mark.vcr()
def test_plugin_iterator_populate_family_cache(api):
    '''test for _populate_family_cache in PluginIterator'''
    getattr(PluginIterator(api), '_populate_family_cache')()


@pytest.mark.vcr()
def test_plugins_populate_family_cache_with_maptable(api):
    '''test next method in PluginIterator'''
    plugins = api.plugins.list(
        last_updated=date(2019, 1, 1),
        num_pages=1,
        size=4)
    plugins._maptable = {'plugins': {12122: 13, 12050: 13}, 'families': {13: 'Netware'}}
    for plugin in plugins:
        check(plugin, 'name', str)
