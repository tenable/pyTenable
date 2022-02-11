import pytest
import responses


AGENT_GROUP = {
    'id': 1,
    'name': 'Example Agent Group',
    'owner_id': 1,
    'owner': 'Administrator',
    'shared': 16,
    'user_permissions': 16,
    'creation_date': 1234567890,
    'last_modification_date': 1234567890
}


@responses.activate
def test_agent_groups_add_agent(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/agent-groups/1/agents/1'
                  )
    nessus.agent_groups.add_agent(group_id=1, agent_id=1)


@responses.activate
def test_agent_groups_add_agents(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/agent-groups/1/agents'
                  )
    nessus.agent_groups.add_agents(group_id=1, agents=[1, 2, 3, 4])


@responses.activate
def test_agent_groups_configure(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/agent-groups/1'
                  )
    nessus.agent_groups.configure(group_id=1, name='Example')


@responses.activate
def test_agent_groups_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/agent-groups',
                  json=AGENT_GROUP
                  )
    resp = nessus.agent_groups.create(name='Example')
    assert resp == AGENT_GROUP


@responses.activate
def test_agent_groups_delete_group(nessus):
    responses.add(responses.DELETE, 'https://localhost:8834/agent-groups/1')
    nessus.agent_groups.delete_group(1)


@responses.activate
def test_agent_groups_delete_groups(nessus):
    responses.add(responses.DELETE, 'https://localhost:8834/agent-groups')
    nessus.agent_groups.delete_groups([1, 2, 3])


@responses.activate
def test_agent_groups_delete_agent(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/agent-groups/1/agents/1'
                  )
    nessus.agent_groups.delete_agent(1, 1)


@responses.activate
def test_agent_groups_delete_agents(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/agent-groups/1/agents'
                  )
    nessus.agent_groups.delete_agents(1, [1, 2, 3])


@responses.activate
def test_agent_groups_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/agent-groups/1',
                  json=AGENT_GROUP
                  )
    resp = nessus.agent_groups.details(1)
    assert resp == AGENT_GROUP


@responses.activate
def test_agent_groups_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/agent-groups',
                  json={'groups': [AGENT_GROUP for _ in range(20)]}
                  )
    resp = nessus.agent_groups.list()
    assert isinstance(resp, list)
    for item in resp:
        assert AGENT_GROUP == item