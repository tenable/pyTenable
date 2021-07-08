'''
test reports
'''
import pytest
from ..checker import check, single


@pytest.mark.vcr()
def test_reports_report_digest_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.reports.report(1)


@pytest.mark.vcr()
def test_reports_report(api):
    '''test to get the image report by the image digest'''
    images = api.images.list()
    image = images.next()
    resp = api.reports.report(image['digest'])
    assert isinstance(resp, dict)
    check(resp, 'image_name', str)
    check(resp, 'docker_image_id', str)
    check(resp, 'created_at', 'datetime')
    check(resp, 'updated_at', 'datetime')
    check(resp, 'platform', str)
    check(resp, 'findings', list)
    for data in resp['findings']:
        check(data, 'nvdFinding', dict)
        check(data['nvdFinding'], 'cve', str)
        check(data['nvdFinding'], 'published_date', str)
        check(data['nvdFinding'], 'modified_date', str)
        check(data['nvdFinding'], 'description', str)
        check(data['nvdFinding'], 'cvss_score', str)
        check(data['nvdFinding'], 'access_vector', str)
        check(data['nvdFinding'], 'access_complexity', str)
        check(data['nvdFinding'], 'auth', str)
        check(data['nvdFinding'], 'availability_impact', str)
        check(data['nvdFinding'], 'confidentiality_impact', str)
        check(data['nvdFinding'], 'integrity_impact', str)
        check(data['nvdFinding'], 'cwe', str)
        check(data['nvdFinding'], 'cpe', list)
        for info in data['nvdFinding']['cpe']:
            single(info, str)
        check(data['nvdFinding'], 'remediation', str)
        check(data['nvdFinding'], 'references', list)
        for info in data['nvdFinding']['references']:
            single(info, str)
        check(data, 'packages', list)
        for info in data['packages']:
            check(info, 'name', str)
            check(info, 'version', str)
    check(resp, 'malware', list)
    for info in resp['malware']:
        check(info, 'infectedFile', str)
        check(info, 'fileTypeDescriptor', str)
        check(info, 'md5', str)
        check(info, 'sha256', str)
    check(resp, 'potentially_unwanted_programs', list)
    for info in resp['potentially_unwanted_programs']:
        check(info, 'file', str)
        check(info, 'md5', str)
        check(info, 'sha256', str)
    check(resp, 'sha256', str)
    check(resp, 'os', str)
    check(resp, 'os_version', str)
    check(resp, 'os_architecture', str)
    check(resp, 'installed_packages', list)
    for info in resp['installed_packages']:
        check(info, 'name', str)
        check(info, 'version', str)
    check(resp, 'risk_score', int)
    check(resp, 'digest', str)
