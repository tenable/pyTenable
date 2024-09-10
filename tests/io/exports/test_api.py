'''
Testing the exports endpoints
'''
import re
from uuid import UUID
import pytest
import responses
from restfly.errors import RequestConflictError
from tenable.io import TenableIO
from tenable.io.exports.schema import AssetExportSchema
from tenable.io.exports.iterator import ExportsIterator

RE_BASE = (r'https://nourl/(vulns|assets|compliance)/export/'
           r'([0-9a-fA-F\-]+)'
           )


@responses.activate
def test_status(tvm):
    responses.add(responses.GET,
                  re.compile(f'{RE_BASE}/status'),
                  json={'uuid': '01234567-89ab-cdef-0123-4567890abcde',
                        'status': 'FINISHED',
                        }
                  )
    status = tvm.exports.status('vulns',
                                '01234567-89ab-cdef-0123-4567890abcde'
                                )
    assert isinstance(status, dict)
    assert status.uuid == '01234567-89ab-cdef-0123-4567890abcde'
    assert status.status == 'FINISHED'


@responses.activate
def test_cancel(tvm):
    responses.add(responses.POST,
                  re.compile(f'{RE_BASE}/cancel'),
                  json={'status': 'CANCELLED'}
                  )
    assert 'CANCELLED' == tvm.exports.cancel('vulns',
                                             '01234567-89ab-cdef-0123-4567890abcde'
                                             )


@responses.activate
def test_download_chunk(tvm):
    url = re.compile(f'{RE_BASE}/chunks/[0-9]+')
    responses.add(responses.GET, url)  # An empty chunk that should be retried.
    responses.add(responses.GET, url, json=[{'name': 'example_item1'},
                                            {'name': 'example_item2'}
                                            ]
                  )
    resp = tvm.exports.download_chunk('vulns',
                                      '01234567-89ab-cdef-0123-4567890abcde',
                                      1
                                      )
    assert isinstance(resp, list)



@responses.activate
def test_jobs(tvm):
    responses.add(responses.GET,
                  re.compile((r'https://nourl/'
                              r'(vulns|assets|compliance)/export/status'
                              )),
                  json={'exports': [{'name': 'job1'},
                                    {'name': 'job2'}
                                    ]
                  })
    jobs = tvm.exports.jobs('vulns')
    assert isinstance(jobs, list)


@pytest.fixture
def export_request():
    with responses.RequestsMock() as rsps:
        url = re.compile(
             r'https://nourl/(vulns|assets|compliance)/export'
        )
        rsps.add(responses.POST, url, json={
            'export_uuid': '01234567-89ab-cdef-0123-4567890abcde'
        })
        yield rsps


def test_base_export(export_request, tvm):
    asset_export = tvm.exports._export('assets',
                                       AssetExportSchema()
                                       )
    assert isinstance(asset_export, ExportsIterator)
    asset_export = tvm.exports._export('assets',
                                       AssetExportSchema(),
                                       use_iterator=False
                                       )
    assert asset_export == UUID('01234567-89ab-cdef-0123-4567890abcde')


def test_asset_export(export_request, tvm):
    export = tvm.exports.assets()
    assert isinstance(export, ExportsIterator)


def test_vuln_export(export_request, tvm):
    export = tvm.exports.vulns()
    assert isinstance(export, ExportsIterator)


def test_compliance_export(export_request, tvm):
    export = tvm.exports.compliance()
    assert isinstance(export, ExportsIterator)


def test_initiate_export(export_request, tvm):
    job_id = UUID('01234567-89ab-cdef-0123-4567890abcde')
    assert job_id == tvm.exports.initiate_export("assets", chunk_size=1000)
    assert job_id == tvm.exports.initiate_export("vulns")
    assert job_id == tvm.exports.initiate_export("compliance")


@responses.activate
def test_export_adoption(tvm):
    job_id = '01234567-89ab-cdef-0123-4567890abcde'
    responses.post('https://nourl/vulns/export',
                   status=409,
                   json={
                       'active_job_id': job_id,
                       'failure_reason': 'Some message goes here from platform'
                   }
                   )
    assert UUID(job_id) == tvm.exports.initiate_export('vulns')
    with pytest.raises(RequestConflictError):
        tvm.exports.initiate_export('vulns', adopt_existing=False)

@pytest.mark.vcr()
def test_list_compliance_export_jobs_returns_a_list(api):
    jobs = api.exports.list_compliance_export_jobs()
    assert isinstance(jobs, list)
