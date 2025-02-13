"""
Testing the WAS exports endpoints
"""

import re
from uuid import UUID

import pytest
import responses
from restfly.errors import RequestConflictError

from tenable.io.exports.iterator import ExportsIterator

RE_BASE = r'https://nourl/was/v1/export/vulns/' r'([0-9a-fA-F\-]+)'


@responses.activate
def test_status(tvm):
    responses.add(
        responses.GET,
        re.compile(f'{RE_BASE}/status'),
        json={
            'uuid': '01234567-89ab-cdef-0123-4567890abcde',
            'status': 'FINISHED',
        },
    )
    status = tvm.exports.status('was', '01234567-89ab-cdef-0123-4567890abcde')
    assert isinstance(status, dict)
    assert status.uuid == '01234567-89ab-cdef-0123-4567890abcde'
    assert status.status == 'FINISHED'


@responses.activate
def test_cancel(tvm):
    responses.add(
        responses.POST, re.compile(f'{RE_BASE}/cancel'), json={'status': 'CANCELLED'}
    )
    assert 'CANCELLED' == tvm.exports.cancel(
        'was', '01234567-89ab-cdef-0123-4567890abcde'
    )


@responses.activate
def test_download_chunk(tvm):
    url = re.compile(f'{RE_BASE}/chunks/[0-9]+')
    responses.add(responses.GET, url)
    responses.add(
        responses.GET, url, json=[{'name': 'example_item1'}, {'name': 'example_item2'}]
    )
    resp = tvm.exports.download_chunk('was', '01234567-89ab-cdef-0123-4567890abcde', 1)
    assert isinstance(resp, list)


@responses.activate
def test_jobs(tvm):
    responses.add(
        responses.GET,
        re.compile(r'https://nourl/was/v1/export/vulns/status'),
        json={'exports': [{'name': 'job1'}, {'name': 'job2'}]},
    )
    jobs = tvm.exports.jobs('was')
    assert isinstance(jobs, list)


@pytest.fixture
def export_request():
    with responses.RequestsMock() as rsps:
        url = re.compile(r'https://nourl/was/v1/export/vulns')
        rsps.add(
            responses.POST,
            url,
            json={'export_uuid': '01234567-89ab-cdef-0123-4567890abcde'},
        )
        yield rsps


def test_was_findings_export(export_request, tvm):
    export = tvm.exports.was()
    assert isinstance(export, ExportsIterator)


def test_was_findings_export_returns_uuid(export_request, tvm):
    export_uuid = tvm.exports.was(use_iterator=False)
    assert export_uuid == UUID('01234567-89ab-cdef-0123-4567890abcde')


@responses.activate
def test_export_adoption_false(tvm):
    job_id = '01234567-89ab-cdef-0123-4567890abcde'
    responses.post(
        'https://nourl/was/v1/export/vulns',
        status=409,
        json={
            'active_job_id': job_id,
            'failure_reason': 'Some message goes here from platform',
        },
    )
    assert UUID(job_id) == tvm.exports.was(use_iterator=False)
    with pytest.raises(RequestConflictError):
        tvm.exports.was(adopt_existing=False)


@responses.activate
def test_export_adoption_true(tvm):
    job_id = '01234567-89ab-cdef-0123-4567890abcde'
    responses.post(
        'https://nourl/was/v1/export/vulns',
        status=409,
        json={
            'active_job_id': job_id,
            'failure_reason': 'Some message goes here from platform',
        },
    )
    assert UUID(job_id) == tvm.exports.was(use_iterator=False)
    assert UUID(job_id) == tvm.exports.was(adopt_existing=True, use_iterator=False)
