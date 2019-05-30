from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_reports_report_digest_typeerror(api):
    with pytest.raises(TypeError):
        api.reports.report(1)

@pytest.mark.vcr()
def test_reports_report(api):
    images = api.images.list()
    i = images.next()
    r = api.reports.report(i['digest'])
    assert isinstance(r, dict)
    check(r, 'image_name', str)
    check(r, 'docker_image_id', str)
    check(r, 'created_at', 'datetime')
    check(r, 'updated_at', 'datetime')
    check(r, 'platform', str)
    check(r, 'findings', list)
    for v in r['findings']:
        check(v, 'nvdFinding', dict)
        check(v['nvdFinding'], 'cve', str)
        check(v['nvdFinding'], 'published_date', str)
        check(v['nvdFinding'], 'modified_date', str)
        check(v['nvdFinding'], 'description', str)
        check(v['nvdFinding'], 'cvss_score', str)
        check(v['nvdFinding'], 'access_vector', str)
        check(v['nvdFinding'], 'access_complexity', str)
        check(v['nvdFinding'], 'auth', str)
        check(v['nvdFinding'], 'availability_impact', str)
        check(v['nvdFinding'], 'confidentiality_impact', str)
        check(v['nvdFinding'], 'integrity_impact', str)
        check(v['nvdFinding'], 'cwe', str)
        check(v['nvdFinding'], 'cpe', list)
        for i in v['nvdFinding']['cpe']:
            single(i, str)
        check(v['nvdFinding'], 'remediation', str)
        check(v['nvdFinding'], 'references', list)
        for i in v['nvdFinding']['references']:
            single(i, str)
        check(v, 'packages', list)
        for p in v['packages']:
            check(p, 'name', str)
            check(p, 'version', str)
    check(r, 'malware', list)
    for m in r['malware']:
        check(m, 'infectedFile', str)
        check(m, 'fileTypeDescriptor', str)
        check(m, 'md5', str)
        check(m, 'sha256', str)
    check(r, 'potentially_unwanted_programs', list)
    for p in r['potentially_unwanted_programs']:
        check(p, 'file', str)
        check(p, 'md5', str)
        check(p, 'sha256', str)
    check(r, 'sha256', str)
    check(r, 'os', str)
    check(r, 'os_version', str)
    check(r, 'os_architecture', str)
    check(r, 'installed_packages', list)
    for i in r['installed_packages']:
        check(i, 'name', str)
        check(i, 'version', str)
    check(r, 'risk_score', int)
    check(r, 'digest', str)