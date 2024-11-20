import pytest


@pytest.fixture
def was_export_uuid(api, vcr):
    with vcr.use_cassette('was_vuln_export'):
        export_uuid = api.was_exports.export(since=0,
                                        include_unlicensed=True,
                                        severity=['medium', 'high', 'critical']
                                        )
    return export_uuid
