import logging
from uuid import UUID

import pytest
import responses
from pydantic import ValidationError
from requests import status_codes
from responses.matchers import json_params_matcher, query_param_matcher
from responses.registries import OrderedRegistry
from restfly.errors import InvalidContentError

from tenable.io.sync.job_manager import JobManager, SyncJobTerminated

# TODO: The testing here needs to be expanded upon to cover more of the edge-cases that
#       can arise.  FOr now, this should work.


@pytest.fixture
def job(tvm):
    return JobManager(
        api=tvm,
        sync_id="example_id",
        job_uuid=UUID("12345678-1234-1234-1234-123456789012"),
    )


@pytest.fixture
def ex_asset():
    return {"id": "12345", "device": {}}


@responses.activate(registry=OrderedRegistry)
def test_job_chunk_cache(job, ex_asset):
    for c in range(1, 11):
        responses.post(
            f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}/chunks/{c}",
            json={"success": True},
        )
    responses.post(
        f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}/_submit",
        json={"success": True},
    )

    job.cache_max = 10

    with job:
        for _ in range(95):
            job.add(ex_asset, "device-asset")

    assert job.counters["device-asset"]["accepted"] == 95


@responses.activate
def test_job_add_failure_terminate(job):
    responses.delete(
        f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}"
    )

    with pytest.raises(ValidationError):
        with job:
            job.add({}, "device-asset")


@responses.activate
def test_job_add_failure_invalid_content(job, ex_asset):
    responses.post(
        f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}/chunks/1",
        status=422,
        json={"error": "something"},
    )
    responses.delete(
        f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}"
    )

    with pytest.raises(SyncJobTerminated) as err:
        job.cache_max = 10
        with job:
            for _ in range(20):
                job.add(ex_asset, "device-asset")
        assert '{"error": "something"}' in err.msg


@responses.activate
def test_job_add_failure_apierror(job, ex_asset, caplog):
    responses.post(
        f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}/chunks/1",
        status=400,
        json={"error": "something"},
    )
    responses.delete(
        f"https://nourl/api/v3/data/synchronizations/example_id/jobs/{job.uuid}"
    )

    with pytest.raises(SyncJobTerminated), caplog.at_level(logging.WARNING):
        job.cache_max = 10
        job.max_retries = 1
        job._retry_delay = 0
        with job:
            for _ in range(20):
                job.add(ex_asset, "device-asset")

    assert "Upstream API Error Occurred" in caplog.text
