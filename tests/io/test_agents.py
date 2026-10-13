"""
test agents
"""

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError

from ..checker import check

FILTERS_SCANS_AGENTS = {
    'filters': [
        {
            'name': 'distro',
            'readable_name': 'Distro',
            'operators': ['match', 'nmatch'],
            'control': {
                'readable_regex': 'Distro Name (e.g. es7-x86-64)',
                'type': 'entry',
                'regex': '.*',
            },
        }
    ]
}


@responses.activate
def test_agents_list_offset_typeerror(tvm):
    """
    test to raise the exception when type of offset is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(offset='nope')


@responses.activate
def test_agents_list_limit_typeerror(tvm):
    """
    test to raise the exception when type of limit is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(limit='nope')


@responses.activate
def test_agents_list_sort_field_typeerror(tvm):
    """
    test to raise the exception when type of sort field is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(sort=((1, 'asc'),))


@responses.activate
def test_agents_list_sort_direction_typeerror(tvm):
    """
    test to raise the exception when type of sort direction is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(sort=(('uuid', 1),))


@responses.activate
def test_agents_list_sort_direction_unexpectedvalue(tvm):
    """
    test to raise the exception when value of sort direction is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(UnexpectedValueError):
        tvm.agents.list(sort=(('uuid', 'nope'),))


@responses.activate
def test_agents_list_filter_name_typeerror(tvm):
    """
    test to raise the exception when type of filter name is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list((1, 'match', 'win'))


@responses.activate
def test_agents_list_filter_operator_typeerror(tvm):
    """
    test to raise the exception when type of filter operator is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(('distro', 1, 'win'))


@responses.activate
def test_agents_list_filter_value_typeerror(tvm):
    """
    test to raise the exception when type of filter value is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(('distro', 'match', 1))


@responses.activate
def test_agents_list_filter_type_typeerror(tvm):
    """
    test to raise the exception when type of filter type is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(filter_type=1)


@responses.activate
def test_agents_list_wildcard_typeerror(tvm):
    """
    test to raise the exception when type of wildcard is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(wildcard=1)


@responses.activate
def test_agents_list_wildcard_fields_typeerror(tvm):
    """
    test to raise the exception when type of wildcard fields is not as defined
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    with pytest.raises(TypeError):
        tvm.agents.list(wildcard_fields='nope')


@responses.activate
def test_agents_list(tvm, agent):
    """
    test to get the agents list
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents',
        json={
            'agents': [agent] * 50,
            'pagination': {'total': 51, 'limit': 50, 'offset': 0},
        },
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents',
        json={
            'agents': [agent],
            'pagination': {'total': 51, 'limit': 50, 'offset': 50},
        },
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '50'})],
    )
    count = 0
    agents = tvm.agents.list()
    for agent in agents:
        count += 1
        check(agent, 'distro', str)
        check(agent, 'id', int)
        check(agent, 'ip', str)
        check(agent, 'linked_on', int)
        check(agent, 'name', str)
        check(agent, 'platform', str)
        check(agent, 'status', str)
        check(agent, 'uuid', 'uuid')
    assert count == agents.total == 51


def test_agents_details_scanner_id_typeerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    with pytest.raises(TypeError):
        tvm.agents.details(scanner_id='nope')


@responses.activate
def test_agents_details_agent_details(tvm, agent):
    """
    test to get the agent details
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/2022688',
        json={
            'id': 2022688,
            'uuid': 'f3800546-1813-499d-8352-57d28d58dc97',
            'name': '00fc9870f38d',
            'platform': 'LINUX',
            'distro': 'es7-x86-64',
            'ip': '172.17.0.2',
            'linked_on': 1522359489,
            'status': 'off',
        },
    )
    resp = tvm.agents.details(agent['id'])
    check(resp, 'distro', str)
    check(resp, 'id', int)
    check(resp, 'ip', str)
    check(resp, 'linked_on', int)
    check(resp, 'name', str)
    check(resp, 'platform', str)
    check(resp, 'status', str)
    check(resp, 'uuid', 'uuid')
    assert resp['id'] == agent['id']


# Add tests for singular & bulk agent deletion.
# att tests for task_status.
@responses.activate
def test_agents_list_fields(tvm):
    """
    test to get the agent list
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/agents', json=FILTERS_SCANS_AGENTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents',
        json={
            'agents': [],
            'pagination': {
                'total': 0,
                'limit': 45,
                'offset': 5,
                'sort': [{'name': 'name', 'order': 'asc'}],
            },
        },
        match=[
            matchers.query_param_matcher(
                {'ft': 'or', 'w': 'match', 'wf': 'name', 'limit': '45', 'offset': '5'}
            )
        ],
    )
    count = 0
    agents = tvm.agents.list(
        filter_type='or', limit=45, offset=5, wildcard='match', wildcard_fields=['name']
    )
    for agent in agents:
        count += 1
        check(agent, 'distro', str)
        check(agent, 'id', int)
        check(agent, 'ip', str)
        check(agent, 'linked_on', int)
        check(agent, 'name', str)
        check(agent, 'platform', str)
        check(agent, 'status', str)
        check(agent, 'uuid', 'uuid')
    assert count == agents.total


def test_agents_unlink_multiple_agent_id_typeerror(tvm):
    """
    test to raise the exception when types of multiple agent_ids are not as defined
    """
    with pytest.raises(TypeError) as type_error:
        tvm.agents.unlink('nope', 'test', scanner_id=11)
    assert len(type_error.value.args) == 1, (
        'Test-case should raise only one validation error.'
    )

    assert type_error.value.args[0] == 'agent_ids is of type str.  Expected int', (
        'Invalid type validation error for agent_ids parameter is not raised by test-case.'
    )


def test_agents_task_status_scanner_id_typeerror(tvm):
    """
    test to raise the exception when type of scanner_id is not as defined
    """
    with pytest.raises(TypeError) as type_error:
        tvm.agents.task_status(scanner_id='nope')
    assert len(type_error.value.args) == 1, (
        'Test-case should raise only one validation error.'
    )

    assert (
        "task_status() missing 1 required positional argument: 'task_uuid'"
        in type_error.value.args[0]
    ), (
        'Missing value of required scanner_id parameter error is not raised by test-case.'
    )
