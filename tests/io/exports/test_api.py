'''
Testing the exports endpoints
'''
import time
from uuid import UUID

import pytest

from tenable.io import TenableIO
from tenable.io.exports.iterator import ExportsIterator
from tenable.io.exports.schema import AssetExportSchema


@pytest.mark.vcr()
def test_status(api):
    export = api.exports.compliance()
    retry_count = 5
    status = api.exports.status(export_type='compliance', export_uuid=UUID(export.uuid))
    while status.status != 'FINISHED' and retry_count >= 0:
        time.sleep(10)
        status = api.exports.status(export_type='compliance', export_uuid=UUID(export.uuid))
        retry_count = retry_count - 1

    assert status.status == 'FINISHED'
    assert isinstance(status, dict)


@pytest.mark.vcr()
def test_cancel(api):
    export = api.exports.vulns()
    api.exports.cancel(export_type='vulns', export_uuid=UUID(export.uuid))
    retry_count = 5
    status = api.exports.status(export_type='vulns', export_uuid=UUID(export.uuid))
    while status.status != 'CANCELLED' and retry_count >= 0:
        time.sleep(10)
        status = api.exports.status(export_type='vulns', export_uuid=UUID(export.uuid))
        retry_count = retry_count - 1
    assert status.status == 'CANCELLED'


@pytest.mark.vcr()
def test_download_chunk(api):
    export = api.exports.vulns(num_assets=50)
    retry_count = 10
    status = api.exports.status(export_type='vulns', export_uuid=UUID(export.uuid))
    while status.status != 'FINISHED' and retry_count >= 0:
        time.sleep(10)
        status = api.exports.status(export_type='vulns', export_uuid=UUID(export.uuid))
        retry_count = retry_count - 1
    assert status.status == 'FINISHED'
    resp = api.exports.download_chunk('vulns', export.uuid, 1)

    assert isinstance(resp, list)


@pytest.mark.vcr()
def test_jobs(api):
    jobs = api.exports.jobs('vulns')
    assert isinstance(jobs, list)


@pytest.mark.vcr()
def test_base_export(api):
    asset_export = api.exports._export('assets',
                                       AssetExportSchema()
                                       )
    assert isinstance(asset_export, ExportsIterator)
    asset_export = api.exports._export('assets',
                                       AssetExportSchema(),
                                       use_iterator=False
                                       )
    assert isinstance(asset_export, UUID)


@pytest.mark.vcr()
def test_asset_export(api):
    export = api.exports.assets()
    assert isinstance(export, ExportsIterator)


@pytest.mark.vcr()
def test_vuln_export(api):
    export = api.exports.vulns()
    assert isinstance(export, ExportsIterator)


@pytest.mark.vcr()
def test_compliance_export(api):
    export = api.exports.compliance()
    assert isinstance(export, ExportsIterator)


@pytest.mark.vcr()
def test_initiate_export(api: TenableIO):
    def is_valid_uuid(export_uuid):
        try:
            return UUID(str(export_uuid))
        except ValueError:
            return None

    export_uuid = api.exports.initiate_export("assets", chunk_size=1000)
    assert is_valid_uuid(export_uuid)

    export_uuid = api.exports.initiate_export("vulns")
    assert is_valid_uuid(export_uuid)

    export_uuid = api.exports.initiate_export("compliance")
    assert is_valid_uuid(export_uuid)


@pytest.mark.vcr()
def test_vulns_export_with_scan_uuid(api: TenableIO, scan_results):
    scan_uuid_to_test = scan_results['results']['history'][0]['uuid']
    vulns = api.exports.vulns(since=0, scan_uuid=scan_uuid_to_test)

    vulns = [v["scan"]["uuid"] for v in vulns]

    assert len(vulns) > 0

    # All the results' scan.uuid field should match scan UUID in the request.
    assert all(vul == scan_uuid_to_test for vul in vulns)


@pytest.mark.vcr()
def test_scan_uuid(api: TenableIO, scan_results):
    scan_uuid = {"last_scan_id": scan_results['results']['history'][0]['uuid']}
    data = api.exports.assets(**scan_uuid)
    my_list = [d for d in data]
    assert len(my_list) > 0
