from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_agentconfig_edit_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_config.edit(scanner_id='nope')

@pytest.mark.vcr()
def test_agentconfig_edit_software_update_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_config.edit(software_update='nope')

@pytest.mark.vcr()
def test_agentconfig_edit_auto_unlink_typerror(api):
    with pytest.raises(TypeError):
        api.agent_config.edit(auto_unlink='nope')

@pytest.mark.vcr()
def test_agentconfig_edit_auto_unlink_out_of_bounds(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_config.edit(auto_unlink=500)

@pytest.mark.vcr()
def test_agentconfig_edit_standard_user_should_fail(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_config.edit(auto_unlink=30)

@pytest.mark.vcr()
def test_agentconfig_edit_set_autounlink(api):
    resp = api.agent_config.edit(auto_unlink=30)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)

@pytest.mark.vcr()
def test_agentconfig_edit_disable_autounlink(api):
    resp = api.agent_config.edit(auto_unlink=False)
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)

@pytest.mark.vcr()
def test_agentconfig_show_error_conditions(api):
    with pytest.raises(TypeError):
        api.agent_config.details(scanner_id='nope')

@pytest.mark.vcr()
def test_agentconfig_show_details(api):
    resp = api.agent_config.details()
    assert isinstance(resp, dict)
    check(resp, 'auto_unlink', dict)
    check(resp['auto_unlink'], 'enabled', bool)
    check(resp['auto_unlink'], 'expiration', int)
    check(resp, 'software_update', bool)

@pytest.mark.vcr()
def test_agentconfig_show_standard_user_should_fail(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_config.details()