from tenable.errors import *
from .fixtures import *
import uuid

def test_attachment_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.attachment('nope', 1)

def test_attachment_attachement_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.attachment(1, 'nope')

@pytest.mark.xfail(raises=InvalidInputError)
def test_attachement_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.attachment(1, 1, 'none')

#def test_configure_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.configure('nope')
#
#def test_configure_notfounderror(api):
#    with pytest.raises(NotFoundError):
#        api.scans.configure(1, name=str(uuid.uuid4()))

@pytest.mark.skip(reason="Scan Create/Modify not yet written")
def test_configure(api, scan):
    name = str(uuid.uuid())
    mod = api.scans.configure(scan['id'], name=name)
    assert mod['id'] == scan['id']
    assert mod['name'] == name

def test_copy_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.copy('nope')

def test_copy_folder_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.copy(1, folder_id='nope')

def test_copy_name_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.copy(1, name=1)

def test_copy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.copy(1)

@pytest.mark.skip(reason="Scan Create/Modify not yet written")
def test_copy(api, scan):
    clone = api.scans.copy(scan['id'])

###
### Create tests go here
###

def test_delete_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.delete('nope')

def test_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.delete(0)

@pytest.mark.skip(reason="Scan Create/Modify not yet written")
def test_delete(api, scan):
    api.scans.delete(scan['id'])

def test_delete_history_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.delete_history('nope', 1)

def test_delete_history_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.delete_history(1, 'nope')

def test_delete_history_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.delete_history(1, 1)

def test_details_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.details('nope')

def test_details_history_it_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.details(1, 'nope')

@pytest.mark.skip(reason="Need scan data to test")
def test_details(api):
    pass

###
### Add Export tests here...
###

def test_host_details_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.host_details('nope', 1)

def test_host_details_host_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.host_details(1, 'nope')

def test_host_details_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.host_details(1, 1, 'nope')

def test_host_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.host_details(1, 1)

@pytest.mark.skip(reason="Need scan data to test")
def test_host_details(api, scan):
    pass

def test_import_scan_folder_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.import_scan(None, folder_id='nope')

def test_import_scan_password_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.import_scan(None, password=1)

@pytest.mark.skip(reason="Need scan data to test")
def test_import_scan(api):
    pass

def test_list_folder_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.list(folder_id='nope')

def test_list_last_modified_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.list(last_modified='nope')

def test_list(api):
    scans = api.scans.list()
    assert isinstance(scans, dict)
    assert 'folders' in scans
    assert 'scans' in scans

def test_pause_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.pause('nope')

def test_plugin_output_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output('nope', 1, 1)

def test_plugin_output_host_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 'nope', 1)

def test_plugin_output_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 1, 'nope')

def test_plugin_output_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 1, 1, history_id='nope')

@pytest.mark.skip(reason="Need scan data to test")
def test_plugin_output(api):
    pass

def test_read_status_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.set_read_status('nope', False)

def test_read_status_rad_status_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.set_read_status(1, 'nope')

@pytest.mark.skip(reason="Need scan data to test")
def test_read_status(api):
    pass

def test_resume_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.resume('nope')

@pytest.mark.skip(reason="Need scan data to test")
def test_resume(api):
    pass

def test_schedule_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.schedule('nope', False)

def test_schedule_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.schedule(1, 'nope')

@pytest.mark.skip(reason="Need scan data to test")
def test_schedule(api):
    pass

def test_stop_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.stop('nope')

@pytest.mark.skip(reason="Need scan data to test")
def test_stop(api):
    pass

def test_timezones(api):
    assert isinstance(api.scans.timezones(), list)