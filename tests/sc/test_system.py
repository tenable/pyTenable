from tenable.errors import *
from ..checker import check, single
import pytest, zipfile

@pytest.mark.vcr()
def test_system_details(unauth):
    s = unauth.system.details()
    assert isinstance(s, dict)
    check(s, 'ACAS', str)
    check(s, 'PasswordComplexity', str)
    check(s, 'banner', str)
    check(s, 'buildID', str)
    check(s, 'freshInstall', str)
    check(s, 'headerText', str)
    check(s, 'licenseStatus', str)
    check(s, 'loginNotifications', str)
    check(s, 'logo', str)
    check(s, 'releaseID', str)
    check(s, 'reportTypes', list)
    for i in s['reportTypes']:
        check(i, 'attributeSets', list)
        check(i, 'enabled', str)
        check(i, 'name', str)
        check(i, 'type', str)
    check(s, 'serverAuth', str)
    check(s, 'serverClassification', str)
    check(s, 'sessionTimeout', str)
    check(s, 'telemetryEnabled', str)
    check(s, 'timezones', list)
    for i in s['timezones']:
        check(i, 'gmtOffset', (int, float))
        check(i, 'name', str)
    check(s, 'uuid', str)
    check(s, 'version', str)

@pytest.mark.vcr()
def test_system_diagnostics_task_typeerror(admin):
    with pytest.raises(TypeError):
        admin.system.diagnostics(task=1)

@pytest.mark.vcr()
def test_system_diagnostics_type_unexpectedvalueerror(admin):
    with pytest.raises(UnexpectedValueError):
        admin.system.diagnostics(task='something else')

@pytest.mark.vcr()
def test_system_diagnostics_options_typeerror(admin):
    with pytest.raises(TypeError):
        admin.system.diagnostics(options=1)

@pytest.mark.vcr()
def test_system_diagnostics_options_item_typeerror(admin):
    with pytest.raises(TypeError):
        admin.system.diagnostics(options=[1])

@pytest.mark.vcr()
def test_system_diagnostics_options_item_unexpectedvalueerror(admin):
    with pytest.raises(UnexpectedValueError):
        admin.system.diagnostics(options=['something else'])

@pytest.mark.vcr()
def test_system_diagnostics_success(admin):
    fobj = admin.system.diagnostics()
    assert zipfile.is_zipfile(fobj)

@pytest.mark.vcr()
def test_system_current_locale_success(admin):
    l = admin.system.current_locale()
    assert isinstance(l, dict)
    check(l, 'code', str)
    check(l, 'description', str)
    check(l, 'name', str)

@pytest.mark.vcr()
def test_system_list_locales_success(admin):
    l = admin.system.list_locales()
    assert isinstance(l, dict)
    for key in l.keys():
        check(l[key], 'code', str)
        check(l[key], 'name', str)

@pytest.mark.vcr()
def test_system_set_locale_locale_typeerror(admin):
    with pytest.raises(TypeError):
        admin.system.set_locale(1)

@pytest.mark.vcr()
@pytest.mark.skip(reason='This appears to be 1-way, need a sacrificial system to test with')
def test_system_set_locale_success(admin):
    locales = admin.system.list_locales()
    assert admin.system.set_locale('ja') == 'ja'

@pytest.mark.vcr()
def test_system_status_success(admin):
    s = admin.system.status()
    assert isinstance(s, dict)
    check(s, 'diagnosticsGenerateState', str)
    check(s, 'diagnosticsGenerated', int)
    check(s, 'statusDisk', str)
    check(s, 'statusJava', str)
    check(s, 'statusLastChecked', str)
    check(s, 'statusRPM', str)
    check(s, 'statusThresholdDisk', str)