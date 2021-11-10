'''
Testing the exports endpoints
'''
import re
from uuid import UUID
import pytest
import responses
from tenable.io.exports.schema import AssetExportSchema
from tenable.io.exports.iterator import ExportsIterator

RE_BASE = (r'https://cloud.tenable.com/(vulns|assets|compliance)/export/'
           r'([0-9a-fA-F\-]+)'
           )


@responses.activate
def test_status(api):
    responses.add(responses.GET,
                  re.compile(f'{RE_BASE}/status'),
                  json={'uuid': '01234567-89ab-cdef-0123-4567890abcde',
                        'status': 'FINISHED',
                        }
                  )
    status = api.exports.status('vulns',
                                '01234567-89ab-cdef-0123-4567890abcde'
                                )
    assert isinstance(status, dict)
    assert status.uuid == '01234567-89ab-cdef-0123-4567890abcde'
    assert status.status == 'FINISHED'


@responses.activate
def test_cancel(api):
    responses.add(responses.POST,
                  re.compile(f'{RE_BASE}/cancel'),
                  json={'status': 'CANCELLED'}
                  )
    assert 'CANCELLED' == api.exports.cancel(
        'vulns',
        '01234567-89ab-cdef-0123-4567890abcde'
    )


@responses.activate
def test_download_chunk(api):
    url = re.compile(f'{RE_BASE}/chunks/[0-9]+')
    responses.add(responses.GET, url)  # An empty chunk that should be retried.
    responses.add(responses.GET, url, json=[{'name': 'example_item1'},
                                            {'name': 'example_item2'}
                                            ]
                  )
    resp = api.exports.download_chunk('vulns',
                                      '01234567-89ab-cdef-0123-4567890abcde',
                                      1
                                      )
    assert isinstance(resp, list)



@responses.activate
def test_jobs(api):
    responses.add(responses.GET,
                  re.compile((r'https://cloud.tenable.com/'
                              r'(vulns|assets|compliance)/export/status'
                              )),
                  json={'exports': [{'name': 'job1'},
                                    {'name': 'job2'}
                                    ]
                  })
    jobs = api.exports.jobs('vulns')
    assert isinstance(jobs, list)


@pytest.fixture
def export_request():
    with responses.RequestsMock() as rsps:
        url = re.compile(
             r'https://cloud.tenable.com/(vulns|assets|compliance)/export'
        )
        rsps.add(responses.POST, url, json={
            'export_uuid': '01234567-89ab-cdef-0123-4567890abcde'
        })
        yield rsps


def test_base_export(export_request, api):
    asset_export = api.exports._export('assets',
                                       AssetExportSchema()
                                       )
    assert isinstance(asset_export, ExportsIterator)
    asset_export = api.exports._export('assets',
                                       AssetExportSchema(),
                                       use_iterator=False
                                       )
    assert asset_export == UUID('01234567-89ab-cdef-0123-4567890abcde')


def test_asset_export(export_request, api):
    export = api.exports.assets()
    assert isinstance(export, ExportsIterator)


def test_vuln_export(export_request, api):
    export = api.exports.vulns()
    assert isinstance(export, ExportsIterator)


def test_compliance_export(export_request, api):
    export = api.exports.compliance()
    assert isinstance(export, ExportsIterator)
