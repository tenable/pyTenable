"""
test agent_config
"""

import pytest
import responses
from responses.matchers import json_params_matcher

from tenable.errors import ForbiddenError, UnexpectedValueError
from tests.checker import check


def test_agentconfig_edit_software_update_typeerror(tvm):
    """
    test to raise exception when type of software_update param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.agent_config.edit(software_update='nope')


def test_agentconfig_edit_auto_unlink_typerror(tvm):
    """
    test to raise exception when type of auto_unlink param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.agent_config.edit(auto_unlink='nope')


def test_agentconfig_edit_auto_unlink_out_of_bounds(tvm):
    """
    test to raise exception when auto_unlink param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.agent_config.edit(auto_unlink=500)


@responses.activate
def test_agentconfig_edit_standard_user_should_fail(tvm):
    """
    test to raise exception when standard_user tries to edit agent_config.
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/config',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_config.edit(auto_unlink=30)


@responses.activate
def test_agentconfig_edit_set_autounlink(tvm):
    """
    test to edit autounlink param.
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/config',
        json={
            'auto_unlink': {'enabled': True, 'expiration': 31},
            'software_update': True,
        },
    )
    resp = tvm.agent_config.edit(auto_unlink=31)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['auto_unlink']['expiration'] == 31


@responses.activate
def test_agentconfig_edit_disable_autounlink(tvm):
    """
    test to disable autounlink param.
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/config',
        json={
            'auto_unlink': {'enabled': False, 'expiration': 31},
            'software_update': True,
        },
    )
    resp = tvm.agent_config.edit(auto_unlink=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['auto_unlink']['enabled'] is False


@responses.activate
def test_agentconfig_edit_disable_softwareupdate(tvm):
    """
    test to disable software_update param.
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/config',
        json={
            'auto_unlink': {'enabled': False, 'expiration': 31},
            'software_update': False,
        },
    )
    resp = tvm.agent_config.edit(software_update=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['software_update'] is False


@responses.activate
def test_agentconfig_show_details(tvm):
    """
    test to show agent_config details
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/config',
        json={
            'auto_unlink': {'enabled': False, 'expiration': 30},
            'software_update': True,
        },
    )
    resp = tvm.agent_config.details()
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)


@responses.activate
def test_agentconfig_show_standard_user_should_fail(tvm):
    """
    test to raise exception when standard user try to view details of agent_config
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/config',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.agent_config.details()


@responses.activate
def test_agentconfig_show_details_fields(tvm):
    """
    test to show agent_config details
    """
    responses.add(
        responses.GET,
        'https://nourl/scanners/1/agents/config',
        json={
            'auto_unlink': {'enabled': False, 'expiration': 30},
            'software_update': True,
        },
    )
    resp = tvm.agent_config.details(scanner_id=0)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)


@responses.activate
def test_agentconfig_edit_success_fields(tvm):
    """
    test to edit the agent_config and verify their types
    """
    responses.add(
        responses.PUT,
        'https://nourl/scanners/1/agents/config',
        json={
            'auto_unlink': {'enabled': False, 'expiration': 30},
            'software_update': True,
        },
    )
    resp = tvm.agent_config.edit(scanner_id=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict, allow_none=True)
    check(resp, 'software_update', bool, allow_none=True)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)


AGENT_CONFIG = {
    'auto_unlink': {'enabled': False, 'expiration': 30},
    'concurrent_update': {'enabled': True, 'max_concurrent_update': 500},
    'software_update': True,
    'hybrid_scanning_enabled': True,
}


@responses.activate
@pytest.mark.parametrize(
    'kwargs, body',
    [
        ({}, {'auto_unlink': {}}),
        (
            {'concurrent_update': True, 'max_concurrent_update': 500},
            {
                'auto_unlink': {},
                'concurrent_update': {'enabled': True, 'max_concurrent_update': 500},
            },
        ),
        (
            {'concurrent_update': False},
            {'auto_unlink': {}, 'concurrent_update': {'enabled': False}},
        ),
        (
            {'max_concurrent_update': 0},
            {'auto_unlink': {}, 'concurrent_update': {'max_concurrent_update': 0}},
        ),
        (
            {'max_concurrent_update': 2500},
            {'auto_unlink': {}, 'concurrent_update': {'max_concurrent_update': 2500}},
        ),
        (
            {'hybrid_scanning_enabled': True},
            {'auto_unlink': {}, 'hybrid_scanning_enabled': True},
        ),
        (
            {'hybrid_scanning_enabled': False},
            {'auto_unlink': {}, 'hybrid_scanning_enabled': False},
        ),
        (
            {
                'software_update': True,
                'auto_unlink': 30,
                'concurrent_update': True,
                'max_concurrent_update': 1234,
                'hybrid_scanning_enabled': False,
            },
            {
                'auto_unlink': {'enabled': True, 'expiration': 30},
                'software_update': True,
                'concurrent_update': {'enabled': True, 'max_concurrent_update': 1234},
                'hybrid_scanning_enabled': False,
            },
        ),
    ],
)
def test_agentconfig_edit_concurrent_and_hybrid(tvm, kwargs, body):
    responses.put(
        'https://nourl/scanners/1/agents/config',
        json=AGENT_CONFIG,
        match=[json_params_matcher(body, strict_match=True)],
    )
    assert tvm.agent_config.edit(**kwargs) == AGENT_CONFIG


@responses.activate
@pytest.mark.parametrize(
    'kwargs, error',
    [
        ({'max_concurrent_update': 2501}, UnexpectedValueError),
        ({'max_concurrent_update': -1}, UnexpectedValueError),
        ({'max_concurrent_update': '100'}, TypeError),
        ({'max_concurrent_update': True}, TypeError),
        ({'concurrent_update': 'maybe'}, TypeError),
        ({'concurrent_update': 1}, TypeError),
        ({'hybrid_scanning_enabled': 'maybe'}, TypeError),
        ({'hybrid_scanning_enabled': 1}, TypeError),
    ],
)
def test_agentconfig_edit_concurrent_and_hybrid_invalid(tvm, kwargs, error):
    with pytest.raises(error):
        tvm.agent_config.edit(**kwargs)
    assert len(responses.calls) == 0


def test_agentconfig_edit_new_options_keyword_only(tvm):
    with pytest.raises(TypeError):
        tvm.agent_config.edit(1, None, None, True)
