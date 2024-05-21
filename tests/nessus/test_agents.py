import pytest
import responses
from tenable.nessus.iterators.pagination import PaginationIterator


AGENT = {
    'core_version': '10.1.0',
    'distro': 'win-x86-64',
    'groups': [1],
    'last_connect': 1644594740,
    'last_scanned': 1644594740,
    'linked_on': 1608044316,
    'name': 'Example',
    'mac_address': '00:de:ad:be:ef:00',
    'platform': 'WINDOWS',
    'status': 'on',
    'unlinked_on': None,
    'uuid': '48b8d13d-67ce-4784-8e5b-5f70d5545996'
}


@responses.activate
def test_agents_delete(nessus):
    responses.add(responses.DELETE, 'https://localhost:8834/agents/1')
    nessus.agents.delete(1)


@responses.activate
def test_agents_delete_many(nessus):
    responses.add(responses.DELETE, 'https://localhost:8834/agents')
    nessus.agents.delete_many([1, 2, 3])


@responses.activate
def test_agents_unlink(nessus):
    responses.add(responses.DELETE, 'https://localhost:8834/agents/1/unlink')
    nessus.agents.unlink(1)


@responses.activate
def test_agents_unlink_many(nessus):
    responses.add(responses.DELETE, 'https://localhost:8834/agents/unlink')
    nessus.agents.unlink_many([1, 2, 3])


@responses.activate
def test_agents_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/agents/1',
                  json={'agents': [AGENT]})
    resp = nessus.agents.details(1)
    assert resp == AGENT


@responses.activate
def test_agents_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/agents',
                  json={'agents': [AGENT for _ in range(20)]}
                  )

    # Test JSON Response
    resp = nessus.agents.list(return_json=True)
    assert isinstance(resp, list)
    for item in resp:
        assert item == AGENT

    # Test Iterator Response
    resp = nessus.agents.list()
    assert isinstance(resp, PaginationIterator)
    for item in resp:
        assert item == AGENT
