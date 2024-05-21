import pytest
import re
import random
import responses
from tenable.nessus.iterators.plugins import PluginIterator


@responses.activate
def test_plugins_families(nessus):
    fam_mock = {'id': 1, 'name': 'Example Family', 'count': 192}
    responses.add(responses.GET,
                  'https://localhost:8834/plugins/families',
                  json={
                    'families': [fam_mock for _ in range(100)]   
                  })
    resp = nessus.plugins.families()
    assert isinstance(resp, list)
    for item in resp:
        assert item == fam_mock


@responses.activate
def test_plugins_family_details(nessus):
    fam_mock = {
        'name': 'Example Family',
        'id': 1,
        'plugins': [{'id': 1, 'name': 'Example Plugin'} for _ in range(100)]
    }
    responses.add(responses.GET,
                  'https://localhost:8834/plugins/families/1',
                  json=fam_mock
                  )
    resp = nessus.plugins.family_details(1)
    assert isinstance(resp, dict)
    assert resp == fam_mock


@responses.activate
def test_plugins_plugin_details(nessus):
    plugin_mock = {
        'name': 'Example Plugin',
        'id': 1,
        'family_name': 'Example Family',
        'attributes': [{'attribute_name': 'name',
                        'attribute_value': 'value'} for _ in range(100)
                        ]
    }
    responses.add(responses.GET,
                  'https://localhost:8834/plugins/plugin/1',
                  json=plugin_mock
                  )
    resp = nessus.plugins.plugin_details(1)
    assert isinstance(resp, dict)
    assert resp == plugin_mock


@responses.activate
def test_plugins_plugin_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/plugins/families',
                  json={'families': []}
                  )
    resp = nessus.plugins.list()
    assert isinstance(resp, PluginIterator)