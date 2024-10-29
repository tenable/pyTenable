import box
import pytest
import responses
from responses.matchers import json_params_matcher, query_param_matcher

from tenable.io.sync.api import SynchronizationJobCreationError
from tenable.io.sync.iterator import JobListIterator, JobLogIterator
from tenable.io.sync.job_manager import JobManager
from tenable.io.sync.models.job import Job, LogLine


@pytest.fixture
def example_job():
    return {
        "id": "12345678-1234-1234-1234-123456789012",
        "sync_id": "example_id",
        "state": "ACTIVE",
        "failure_message": None,
        "summary": None,
        "created_at": "2025-01-29T17:22:00.669839+00:00",
        "state_changed_at": "2025-01-29T17:22:00.669839+00:00",
    }


@responses.activate
def test_sync_api_list(tvm, example_job):
    responses.get(
        "https://nourl/api/v3/data/synchronizations/jobs",
        match=[
            query_param_matcher(
                {
                    "limit": 25,
                }
            )
        ],
        json={"jobs": [example_job for _ in range(20)]},
    )
    jobs = tvm.sync.list()
    assert isinstance(jobs, JobListIterator)
    for job in jobs:
        assert isinstance(job, Job)
        assert str(job.id) == "12345678-1234-1234-1234-123456789012"

    jobs = tvm.sync.list(return_json=True)
    assert isinstance(jobs, box.BoxList)
    for job in jobs:
        assert job.to_dict() == example_job


@responses.activate
def test_sync_api_get(tvm, example_job):
    responses.get(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs/12345678-1234-1234-1234-123456789012",
        json=example_job,
    )
    job = tvm.sync.get("example_id", "12345678-1234-1234-1234-123456789012")
    assert isinstance(job, Job)
    assert str(job.id) == "12345678-1234-1234-1234-123456789012"


@responses.activate
def test_sync_api_create(tvm):
    responses.post(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs",
        match=[
            json_params_matcher(
                {"active_state_timeout_seconds": 1800, "expire_after_seconds": 604800}
            )
        ],
        json={"id": "12345678-1234-1234-1234-123456789012", "success": True},
    )
    job = tvm.sync.create("example_id")
    assert isinstance(job, JobManager)
    assert str(job.uuid) == "12345678-1234-1234-1234-123456789012"
    raw = tvm.sync.create("example_id", return_json=True)
    assert raw.to_dict() == {
        "id": "12345678-1234-1234-1234-123456789012",
        "success": True,
    }


@responses.activate
def test_sync_api_create_fail(tvm):
    responses.post(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs",
        match=[
            json_params_matcher(
                {"active_state_timeout_seconds": 1800, "expire_after_seconds": 604800}
            )
        ],
        json={"id": "12345678-1234-1234-1234-123456789012", "success": False},
    )
    with pytest.raises(SynchronizationJobCreationError):
        tvm.sync.create("example_id")


@responses.activate
def test_sync_api_upload_chunk(tvm):
    test_object = {
        "object_type": "cve-finding",
        "asset_id": "12345",
        "id": "123456",
        "cve": {"cves": ["CVE-2018-0001"]},
    }
    responses.post(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs/12345678-1234-1234-1234-123456789012/chunks/1",
        match=[json_params_matcher({"objects": [test_object for _ in range(100)]})],
        json={"success": True},
    )
    assert (
        tvm.sync.upload_chunk(
            "example_id",
            "12345678-1234-1234-1234-123456789012",
            1,
            [test_object for _ in range(100)],
        )
        is True
    )


@responses.activate
def test_sync_api_delete(tvm):
    responses.delete(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs/12345678-1234-1234-1234-123456789012",
    )
    tvm.sync.delete("example_id", "12345678-1234-1234-1234-123456789012")


@responses.activate
def test_sync_api_submit(tvm):
    responses.post(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs/12345678-1234-1234-1234-123456789012/_submit",
        match=[json_params_matcher({"number_of_chunks": 20})],
        json={"success": True},
    )
    assert (
        tvm.sync.submit("example_id", "12345678-1234-1234-1234-123456789012", 20)
        is True
    )


@responses.activate
def test_sync_api_audit_logs(tvm):
    responses.get(
        "https://nourl/api/v3/data/synchronizations/example_id/jobs/12345678-1234-1234-1234-123456789012/audits",
        json={
            "audits": [
                {
                    "audit_type": "ORPHANED_FINDING",
                    "chunk_sequence_number": 0,
                    "id": "12345678-1234-1234-1234-123456789012",
                    "log_level": "INFO",
                    "message": "something special",
                    "object_id": "abcd",
                    "path": "something",
                }
                for _ in range(20)
            ]
        },
    )

    logs = tvm.sync.audit_logs(
        "example_id", "12345678-1234-1234-1234-123456789012", return_json=True
    )
    assert isinstance(logs, list)
    for line in logs:
        assert isinstance(line, LogLine)

    logs = tvm.sync.audit_logs("example_id", "12345678-1234-1234-1234-123456789012")
    assert isinstance(logs, JobLogIterator)
    for line in logs:
        assert isinstance(line, LogLine)
        assert str(line.id) == "12345678-1234-1234-1234-123456789012"
        assert line.message == "something special"
        assert line.chunk_id == 0
        assert line.log_level == "INFO"
        assert line.object_id == "abcd"
        assert line.path == "something"
        assert line.type == "ORPHANED_FINDING"
