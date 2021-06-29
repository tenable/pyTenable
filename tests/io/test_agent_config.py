'''
test agent_config
'''
import pytest
from tenable.errors import UnexpectedValueError, PermissionError
from tests.checker import check


@pytest.mark.vcr()
def test_agentconfig_edit_scanner_id_typeerror(api):
    '''
    test to raise exception when type of scanner_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.agent_config.edit(scanner_id='nope')


@pytest.mark.vcr()
def test_agentconfig_edit_software_update_typeerror(api):
    '''
    test to raise exception when type of software_update param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.agent_config.edit(software_update='nope')


@pytest.mark.vcr()
def test_agentconfig_edit_auto_unlink_typerror(api):
    '''
    test to raise exception when type of auto_unlink param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.agent_config.edit(auto_unlink='nope')


@pytest.mark.vcr()
def test_agentconfig_edit_auto_unlink_out_of_bounds(api):
    '''
    test to raise exception when auto_unlink param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.agent_config.edit(auto_unlink=500)


@pytest.mark.vcr()
def test_agentconfig_edit_standard_user_should_fail(stdapi):
    '''
    test to raise exception when standard_user tries to edit agent_config.
    '''
    with pytest.raises(PermissionError):
        stdapi.agent_config.edit(auto_unlink=30)


@pytest.mark.vcr()
def test_agentconfig_edit_set_autounlink(api):
    '''
    test to edit autounlink param.
    '''
    resp = api.agent_config.edit(auto_unlink=31)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['auto_unlink']['expiration'] == 31


@pytest.mark.vcr()
def test_agentconfig_edit_disable_autounlink(api):
    '''
    test to disable autounlink param.
    '''
    resp = api.agent_config.edit(auto_unlink=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['auto_unlink']['enabled'] is False


@pytest.mark.vcr()
def test_agentconfig_edit_disable_softwareupdate(api):
    '''
    test to disable software_update param.
    '''
    resp = api.agent_config.edit(software_update=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)
    assert resp['software_update'] is False


@pytest.mark.vcr()
def test_agentconfig_show_error_conditions(api):
    '''
    test to show error conditions
    '''
    with pytest.raises(TypeError):
        api.agent_config.details(scanner_id='nope')


@pytest.mark.vcr()
def test_agentconfig_show_details(api):
    '''
    test to show agent_config details
    '''
    resp = api.agent_config.details()
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)


@pytest.mark.vcr()
def test_agentconfig_show_standard_user_should_fail(stdapi):
    '''
    test to raise exception when standard user try to view details of agent_config
    '''
    with pytest.raises(PermissionError):
        stdapi.agent_config.details()


# --------------------------------------------------------------------------------------------------
@pytest.mark.vcr()
def test_agentconfig_show_details_fields(api):
    '''
    test to show agent_config details
    '''
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
