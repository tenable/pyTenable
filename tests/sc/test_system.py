import zipfile
import pytest
import responses
from ..checker import check
from tenable.errors import UnexpectedValueError


@responses.activate
def test_system_details(tsc):
    responses.get(
        'https://nourl/rest/system',
        json={
            'type': 'regular',
            'response': {
                'reportTypes': [
                    {
                        'name': 'PDF',
                        'type': 'pdf',
                        'enabled': 'true',
                        'attributeSets': [],
                    }
                ],
                'version': '5.8.0',
                'buildID': '201810303290',
                'banner': '',
                'releaseID': '201810303290',
                'uuid': '6d32dff0-2e6e-5fef-982f-80b05a31fcad',
                'logo': 'assets/mariana/images/sc4icon.png',
                'serverAuth': 'any',
                'serverClassification': 'None',
                'sessionTimeout': '3600',
                'licenseStatus': 'Valid',
                'ACAS': 'false',
                'freshInstall': 'no',
                'headerText': '',
                'loginNotifications': 'false',
                'PasswordComplexity': 'false',
                'telemetryEnabled': 'false',
                'timezones': [{'name': 'Africa/Abidjan', 'gmtOffset': 0}],
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1553200042,
        },
    )
    s = tsc.system.details()
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


def test_system_diagnostics_task_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.system.diagnostics(task=1)


def test_system_diagnostics_type_unexpectedvalueerror(tsc):
    with pytest.raises(UnexpectedValueError):
        tsc.system.diagnostics(task='something else')


def test_system_diagnostics_options_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.system.diagnostics(options=1)


def test_system_diagnostics_options_item_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.system.diagnostics(options=[1])


def test_system_diagnostics_options_item_unexpectedvalueerror(tsc):
    with pytest.raises(UnexpectedValueError):
        tsc.system.diagnostics(options=['something else'])


@responses.activate
def test_system_diagnostics_success(tsc):
    responses.get(
        'https://nourl/rest/system/diagnostics',
        json={
            'type': 'regular',
            'response': {
                'statusJava': 'true',
                'statusRPM': 'true',
                'statusDisk': 'true',
                'statusThresholdDisk': '5%',
                'statusLastChecked': '1553141401',
                'diagnosticsGenerated': 1553200129,
                'diagnosticsGenerateState': '-1',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553200169,
        },
    )
    responses.post(
        'https://nourl/rest/system/diagnostics/generate',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553200169,
        },
    )
    responses.get(
        'https://nourl/rest/system/diagnostics',
        json={
            'type': 'regular',
            'response': {
                'statusJava': 'true',
                'statusRPM': 'true',
                'statusDisk': 'true',
                'statusThresholdDisk': '5%',
                'statusLastChecked': '1553141401',
                'diagnosticsGenerated': 1553200173,
                'diagnosticsGenerateState': '-1',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553200175,
        },
    )
    responses.post(
        'https://nourl/rest/system/diagnostics/download',
        body=b'PK\x05\x06' + b'\x00' * 18,  # an empty zip archive
        content_type='application/zip',
        headers={'content-disposition': 'attachment; filename=debug.zip'},
    )
    fobj = tsc.system.diagnostics()
    assert zipfile.is_zipfile(fobj)


@responses.activate
def test_system_current_locale_success(tsc):
    responses.get(
        'https://nourl/rest/system/locale',
        json={
            'type': 'regular',
            'response': {'code': '', 'name': '', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553201668,
        },
    )
    l = tsc.system.current_locale()
    assert isinstance(l, dict)
    check(l, 'code', str)
    check(l, 'description', str)
    check(l, 'name', str)


@responses.activate
def test_system_list_locales_success(tsc):
    responses.get(
        'https://nourl/rest/system/locales',
        json={
            'type': 'regular',
            'response': {
                'ja': {'code': 'ja', 'name': 'Japanese'},
                'zh_CN': {'code': 'zh_CN', 'name': 'Chinese (Simplified)'},
                'zh_TW': {'code': 'zh_TW', 'name': 'Chinese (Traditional)'},
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553201639,
        },
    )
    l = tsc.system.list_locales()
    assert isinstance(l, dict)
    for key in l.keys():
        check(l[key], 'code', str)
        check(l[key], 'name', str)


def test_system_set_locale_locale_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.system.set_locale(1)


@pytest.mark.skip(
    reason='This appears to be 1-way, need a sacrificial system to test with'
)
def test_system_set_locale_success(tsc):
    locales = tsc.system.list_locales()
    assert tsc.system.set_locale('ja') == 'ja'


@responses.activate
def test_system_status_success(tsc):
    responses.get(
        'https://nourl/rest/system/diagnostics',
        json={
            'type': 'regular',
            'response': {
                'statusJava': 'true',
                'statusRPM': 'true',
                'statusDisk': 'true',
                'statusThresholdDisk': '5%',
                'statusLastChecked': '1553141401',
                'diagnosticsGenerated': 1553200173,
                'diagnosticsGenerateState': '-1',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553201615,
        },
    )
    s = tsc.system.status()
    assert isinstance(s, dict)
    check(s, 'diagnosticsGenerateState', str)
    check(s, 'diagnosticsGenerated', int)
    check(s, 'statusDisk', str)
    check(s, 'statusJava', str)
    check(s, 'statusLastChecked', str)
    check(s, 'statusRPM', str)
    check(s, 'statusThresholdDisk', str)
