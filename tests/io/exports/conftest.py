import pytest


@pytest.fixture
def vuln_uuid(api, vcr):
    with vcr.use_cassette('vuln_export'):
        export_uuid = api.exports.vulns(since=0,
                                        include_unlicensed=True,
                                        severity=['medium', 'high', 'critical']
                                        )
    return export_uuid


@pytest.fixture
def asset_uuid(api, vcr):
    with vcr.use_cassette('asset_export'):
        export_uuid = api.exports.assets(updated_at=0, is_licensed=False)
    return export_uuid


@pytest.fixture
def comp_uuid(api, vcr):
    with vcr.use_cassette('compliance_export'):
        export_uuid = api.exports.compliance(first_seen=0)
    return export_uuid
