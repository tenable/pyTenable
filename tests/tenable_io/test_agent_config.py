from tenable.errors import *
from fixtures import *

def test_edit_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_config.edit(scanner_id='nope')

def test_edit_software_update_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_config.edit(software_update='nope')

def test_edit_auto_unlink_typerror(api):
    with pytest.raises(TypeError):
        api.agent_config.edit(auto_unlink='nope')

def test_edit_auto_unlink_out_of_bounds(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_config.edit(auto_unlink=500)

def test_edit_standard_user_should_fail(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_config.edit(auto_unlink=30)

def test_edit_set_autounlink(api):
    assert isinstance(api.agent_config.edit(auto_unlink=30), dict)

def test_edit_disable_autounlink(api):
    assert isinstance(api.agent_config.edit(auto_unlink=False), dict)

def test_show_error_conditions(api):
    with pytest.raises(TypeError):
        api.agent_config.details(scanner_id='nope')

def test_show_details(api):
    assert isinstance(api.agent_config.details(), dict)

def test_show_standard_user_should_fail(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_config.details()