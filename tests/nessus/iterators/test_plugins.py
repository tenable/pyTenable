import re
import responses
from tenable.nessus.iterators.plugins import PluginIterator


@responses.activate
def test_plugin_iterator(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/plugins/families',
                  json={'families': [{'id': i, 'count': 1} for i in range(2)]}
                  )
    fam_details = re.compile(r'https://localhost:8834/plugins/families/\d+')
    responses.add(responses.GET,
                  fam_details,
                  json={
                      'name': 'Example',
                      'id': 1,
                      'plugins': [{'id': i} for i in range(100)]
                  })
    plugin_details = re.compile(r'https://localhost:8834/plugins/plugin/\d+')
    plugin_mock = {
        'id': 1,
        'name': 'Example',
        'family_name': 'Family Example',
        'attributes': [{'attribute_name': 'name', 
                        'attribute_value': 'value'
                        }]
    }
    responses.add(responses.GET, plugin_details, json=plugin_mock)
    iter = PluginIterator(nessus)
    for plugin in iter:
        assert plugin == plugin_mock
    

@responses.activate
def test_plugin_iterator_instances_do_not_share_plugins(nessus):
    responses.get('https://localhost:8834/plugins/families',
                  json={'families': [{'id': 1, 'count': 3}]}
                  )
    responses.get('https://localhost:8834/plugins/families/1',
                  json={'id': 1, 'plugins': [{'id': i} for i in range(3)]}
                  )
    first = PluginIterator(nessus)
    second = PluginIterator(nessus)
    assert first.plugins == [0, 1, 2]
    assert second.plugins == [0, 1, 2]
    assert first.total == second.total == 3
