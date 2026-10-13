"""
test plugins
"""

from datetime import date

import pytest
import responses
from responses import matchers

from tenable.io.plugins import PluginIterator

from ..checker import check


@responses.activate
def test_families(tvm):
    """test to get the plugin families"""
    responses.add(
        responses.GET,
        'https://nourl/plugins/families',
        json={
            'families': [
                {'count': 11342, 'name': 'AIX Local Security Checks', 'id': 1},
                {'count': 1164, 'name': 'Amazon Linux Local Security Checks', 'id': 35},
            ]
        },
    )
    families = tvm.plugins.families()
    assert isinstance(families, list)
    for family in families:
        check(family, 'count', int)
        check(family, 'id', int)
        check(family, 'name', str)


@responses.activate
def test_family_details(tvm):
    """test to get the family details"""
    responses.add(
        responses.GET,
        'https://nourl/plugins/families/27',
        json={
            'plugins': [
                {'id': 83346, 'name': '.bash_history Files Disclosed via Web Server'},
                {'id': 33821, 'name': '.svn/entries Disclosed via Web Server'},
            ],
            'name': 'CGI abuses',
            'id': 27,
        },
    )
    data = tvm.plugins.family_details(27)
    assert isinstance(data, dict)
    check(data, 'name', str)
    check(data, 'id', int)
    check(data, 'plugins', list)
    for plugin in data['plugins']:
        check(plugin, 'id', int)
        check(plugin, 'name', str)
    assert data['id'] == 27


@responses.activate
def test_plugin_details(tvm):
    """test to get the plugin details"""
    responses.add(
        responses.GET,
        'https://nourl/plugins/plugin/19506',
        json={
            'attributes': [
                {'attribute_value': 'scan_info.nasl', 'attribute_name': 'fname'},
                {
                    'attribute_value': 'Nessus Scan Information',
                    'attribute_name': 'plugin_name',
                },
            ],
            'family_name': 'Settings',
            'name': 'Nessus Scan Information',
            'id': 19506,
        },
    )
    detail = tvm.plugins.plugin_details(19506)
    assert isinstance(detail, dict)
    check(detail, 'attributes', list)
    for attribute in detail['attributes']:
        check(attribute, 'attribute_name', str)
        check(attribute, 'attribute_value', str)
    check(detail, 'family_name', str)
    check(detail, 'id', int)
    check(detail, 'name', str)
    assert detail['id'] == 19506


def test_plugins_list_page_typeerror(tvm):
    """test to raise the exception when parameter is not passed of expected type"""
    with pytest.raises(TypeError):
        tvm.plugins.list(page='one')


def test_plugins_list_size_typeerror(tvm):
    """test to raise the exception when parameter is not passed of expected type"""
    with pytest.raises(TypeError):
        tvm.plugins.list(size='one')


def test_plugins_list_last_updated_date_typeerror(tvm):
    """test to raise the exception when parameter is not passed of expected type"""
    with pytest.raises(TypeError):
        tvm.plugins.list(last_updated=1)


def test_plugins_list_num_pages_typeerror(tvm):
    """test to raise the exception when parameter is not passed of expected type"""
    with pytest.raises(TypeError):
        tvm.plugins.list(num_pages='one')


@responses.activate
def test_plugins_list_success(tvm):
    """test to get the plugins list"""
    responses.add(
        responses.GET,
        'https://nourl/plugins/plugin',
        json={
            'data': {
                'plugin_details': [
                    {
                        'id': 32,
                        'name': 'Siemens S7-300 Series PLC CPU Firmware <= 3.2.11 DoS',
                        'attributes': {
                            'intel_type': 'SENSOR',
                            'synopsis': 'A Siemens S7-300 programmable logic controller (PLC) has been detected which is vulnerable to a Denial of Service (DoS) attack vector.',
                            'description': 'Siemens S7-300 PLC central processing units (CPUs) contain an unspecified flaw that may allow a remote attacker to use a specially crafted packet to cause the device to enter defect mode until a cold restart is performed.',
                            'solution': 'Upgrade the firmware to version 3.2.12 or later.',
                            'plugin_publication_date': '2019-05-21T00:00:00Z',
                            'vuln_publication_date': '2016-06-08T00:00:00Z',
                            'patch_publication_date': '2016-06-08T00:00:00Z',
                            'has_patch': True,
                            'exploit_available': False,
                            'risk_factor': 'HIGH',
                            'plugin_modification_date': '2019-09-30T00:00:00Z',
                            'always_run': False,
                            'compliance': False,
                            'cvss_temporal_score': 5.8,
                            'cvss3_temporal_score': 6.5,
                            'cvss3_base_score': 7.5,
                        },
                    }
                ]
            },
            'size': 10,
            'total_count': 144113,
        },
        match=[
            matchers.query_param_matcher(
                {'last_updated': '2019-01-01', 'size': '10', 'page': '1'}
            )
        ],
    )
    responses.add(
        responses.GET,
        'https://nourl/plugins/plugin',
        json={
            'data': {
                'plugin_details': [
                    {
                        'id': 69,
                        'name': 'Rockwell Automation/Allen-Bradley 1768-EWEB Ethernet/IP Enhanced Web Server Module',
                        'attributes': {
                            'intel_type': 'SENSOR',
                            'synopsis': 'A Rockwell Automation/Allen-Bradley 1768-EWEB Ethernet/IP Enhanced Web Server Module has been detected.',
                            'description': 'Rockwell Automation/Allen-Bradley 1768-EWEB module, known as Enhanced Web Server module, provides access to control syst',
                            'solution': 'N/A',
                            'see_also': [],
                            'plugin_publication_date': '2019-05-13T00:00:00Z',
                            'has_patch': False,
                            'exploit_available': False,
                            'risk_factor': 'NONE',
                            'plugin_modification_date': '2019-09-30T00:00:00Z',
                            'always_run': False,
                            'compliance': False,
                            'cve': [],
                            'bid': [],
                            'xref': [],
                            'xrefs': [],
                            'vpr': {},
                        },
                    }
                ]
            },
            'size': 10,
            'params': {'page': 2, 'size': 10, 'last_updated': '2019-01-01'},
            'total_count': 144113,
        },
        match=[
            matchers.query_param_matcher(
                {'last_updated': '2019-01-01', 'size': '10', 'page': '2'}
            )
        ],
    )
    plugins = tvm.plugins.list(last_updated=date(2019, 1, 1), num_pages=2, size=10)
    for plugin in plugins:
        check(plugin, 'attributes', dict)
        check(plugin['attributes'], 'description', str)
        check(plugin['attributes'], 'plugin_publication_date', str)
        check(plugin['attributes'], 'plugin_modification_date', str)
        check(plugin['attributes'], 'synopsis', str)
        check(plugin['attributes'], 'risk_factor', str)
        check(plugin, 'id', int)
        check(plugin, 'name', str)


@responses.activate
def test_plugin_iterator_populate_family_cache(tvm):
    """test for _populate_family_cache in PluginIterator"""
    responses.add(
        responses.GET,
        'https://nourl/plugins/families',
        json={
            'families': [
                {'count': 11391, 'name': 'AIX Local Security Checks', 'id': 27},
                {'count': 1955, 'name': 'Amazon Linux Local Security Checks', 'id': 28},
                {'count': 121, 'name': 'Backdoors', 'id': 9},
                {'count': 26, 'name': 'Brute force attacks', 'id': 43},
            ]
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/plugins/families/27',
        json={
            'plugins': [
                {'id': 22372, 'name': 'AIX 5.1 : IY19744'},
                {'id': 22373, 'name': 'AIX 5.1 : IY20486'},
            ],
            'name': 'AIX Local Security Checks',
            'id': 27,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/plugins/families/28',
        json={
            'plugins': [
                {'id': 110453, 'name': 'Amazon Linux 2 : 389-ds-base (ALAS-2018-1036)'},
                {'id': 118401, 'name': 'Amazon Linux 2 : 389-ds-base (ALAS-2018-1094)'},
            ],
            'name': 'Amazon Linux Local Security Checks',
            'id': 28,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/plugins/families/9',
        json={
            'plugins': [
                {'id': 11187, 'name': '4553 Parasite Mothership Backdoor Detection'},
                {'id': 12128, 'name': 'Agobot.FO Backdoor Detection'},
            ],
            'name': 'Backdoors',
            'id': 9,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/plugins/families/43',
        json={
            'plugins': [
                {'id': 15868, 'name': 'Hydra (NASL wrappers options)'},
                {'id': 44915, 'name': 'Hydra Error Summary'},
            ],
            'name': 'Brute force attacks',
            'id': 43,
        },
    )
    getattr(PluginIterator(tvm), '_populate_family_cache')()


@responses.activate
def test_plugins_populate_family_cache_with_maptable(tvm):
    """test next method in PluginIterator"""
    responses.add(
        responses.GET,
        'https://nourl/plugins/plugin',
        json={
            'data': {
                'plugin_details': [
                    {
                        'id': 32,
                        'name': 'Siemens S7-300 Series PLC CPU Firmware <= 3.2.11 DoS',
                    }
                ]
            },
            'size': 4,
            'total_count': 154899,
        },
        match=[
            matchers.query_param_matcher(
                {'last_updated': '2019-01-01', 'size': '4', 'page': '1'}
            )
        ],
    )
    plugins = tvm.plugins.list(last_updated=date(2019, 1, 1), num_pages=1, size=4)
    plugins._maptable = {'plugins': {12122: 13, 12050: 13}, 'families': {13: 'Netware'}}
    for plugin in plugins:
        check(plugin, 'name', str)
