"""
test agent_config
"""

import pytest
import responses
from responses.matchers import json_params_matcher

from tenable.errors import ForbiddenError, UnexpectedValueError
from tests.checker import check


@pytest.mark.vcr()
def test_agentconfig_edit_software_update_typeerror(api):
    """
    test to raise exception when type of software_update param does not match the expected type.
    """
    with pytest.raises(TypeError):
        api.agent_config.edit(software_update='nope')


@pytest.mark.vcr()
def test_agentconfig_edit_auto_unlink_typerror(api):
    """
    test to raise exception when type of auto_unlink param does not match the expected type.
    """
    with pytest.raises(TypeError):
        api.agent_config.edit(auto_unlink='nope')


@pytest.mark.vcr()
def test_agentconfig_edit_auto_unlink_out_of_bounds(api):
    """
    test to raise exception when auto_unlink param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        api.agent_config.edit(auto_unlink=500)


@pytest.mark.vcr()
def test_agentconfig_edit_standard_user_should_fail(stdapi):
    """
    test to raise exception when standard_user tries to edit agent_config.
    """
    with pytest.raises(ForbiddenError):
        stdapi.agent_config.edit(auto_unlink=30)


@pytest.mark.vcr()
def test_agentconfig_edit_set_autounlink(api):
    """
    test to edit autounlink param.
    """
    resp = api.agent_config.edit(auto_unlink=31)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['auto_unlink']['expiration'] == 31


@pytest.mark.vcr()
def test_agentconfig_edit_disable_autounlink(api):
    """
    test to disable autounlink param.
    """
    resp = api.agent_config.edit(auto_unlink=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['auto_unlink']['enabled'] is False


@pytest.mark.vcr()
def test_agentconfig_edit_disable_softwareupdate(api):
    """
    test to disable software_update param.
    """
    resp = api.agent_config.edit(software_update=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['software_update'] is False


@pytest.mark.vcr()
def test_agentconfig_show_details(api):
    """
    test to show agent_config details
    """
    resp = api.agent_config.details()
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)


@pytest.mark.vcr()
def test_agentconfig_show_standard_user_should_fail(stdapi):
    """
    test to raise exception when standard user try to view details of agent_config
    """
    with pytest.raises(ForbiddenError):
        stdapi.agent_config.details()


@pytest.mark.vcr()
def test_agentconfig_show_details_fields(api):
    """
    test to show agent_config details
    """
    resp = api.agent_config.details(scanner_id=0)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)


@pytest.mark.vcr()
def test_agentconfig_edit_success_fields(api):
    """
    test to edit the agent_config and verify their types
    """
    resp = api.agent_config.edit(scanner_id=False)
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
