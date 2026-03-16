"""
Tests for the TenableOne Attack Path Export API.

This module tests all public methods of the attack path ExportAPI class.
"""

import json
import pytest
import responses
from io import BytesIO

from tenable.tenableone.attack_path.export.schema import (
    AttackPathColumnKey,
    AttackPathExportType,
    AttackTechniqueColumnKey,
    ExportFilter,
    ExportFilterCondition,
    ExportRequestId,
    ExportRequestStatus,
    ExportStatus,
    ExportSortParams,
    FileFormat,
    SortDirection,
    VectorsExportParams,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def export_request_id_response() -> dict:
    """Fixture for export request ID response."""
    return {"export_id": "export-ap-12345"}


@pytest.fixture
def export_status_response_finished() -> dict:
    """Fixture for a finished export status response."""
    return {
        "export_id": "export-ap-12345",
        "status": "FINISHED",
        "submitted_at": "2025-06-01T00:00:00Z",
        "last_refreshed_at": "2025-06-01T00:05:00Z",
    }


@pytest.fixture
def export_status_response_processing() -> dict:
    """Fixture for a processing export status response."""
    return {
        "export_id": "export-ap-12345",
        "status": "PROCESSING",
        "submitted_at": "2025-06-01T00:00:00Z",
        "last_refreshed_at": "2025-06-01T00:01:00Z",
    }


@pytest.fixture
def export_data() -> bytes:
    """Fixture for export download data."""
    return b"path_name,priority\nPath A,9\nPath B,7\n"


# ---------------------------------------------------------------------------
# attack_paths() tests
# ---------------------------------------------------------------------------

@responses.activate
def test_attack_paths_minimal(tenable_one_api, export_request_id_response):
    """Test attack_paths with only required parameters."""
    expected_body = {
        "export_type": "VECTORS",
        "file_format": "CSV",
        "params": {},
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-path",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_paths(
        export_type=AttackPathExportType.VECTORS,
        file_format=FileFormat.CSV,
    )

    assert isinstance(result, ExportRequestId)
    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_paths_with_columns(tenable_one_api, export_request_id_response):
    """Test attack_paths with specific columns."""
    expected_body = {
        "export_type": "VECTORS",
        "file_format": "JSON",
        "params": {},
        "columns": ["path_name", "priority", "source_nes"],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-path",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_paths(
        export_type=AttackPathExportType.VECTORS,
        file_format=FileFormat.JSON,
        columns=[
            AttackPathColumnKey.PATH_NAME,
            AttackPathColumnKey.PRIORITY,
            AttackPathColumnKey.SOURCE_NES,
        ],
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_paths_with_file_name(tenable_one_api, export_request_id_response):
    """Test attack_paths with a custom file name."""
    expected_body = {
        "export_type": "VECTORS",
        "file_format": "CSV",
        "params": {},
        "file_name": "my_attack_paths_export",
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-path",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_paths(
        export_type=AttackPathExportType.VECTORS,
        file_format=FileFormat.CSV,
        file_name="my_attack_paths_export",
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_paths_with_params(tenable_one_api, export_request_id_response):
    """Test attack_paths with full params object (sort, filters, vector_ids, pagination)."""
    params = VectorsExportParams(
        sort=ExportSortParams(property="priority", direction=SortDirection.DESC),
        filters=ExportFilter(
            operator="and",
            value=[
                ExportFilterCondition(
                    key="priority",
                    operator="gte",
                    value="8",
                ),
            ],
        ),
        vector_ids=["vec-001", "vec-002"],
        page_number=1,
        max_entries_per_page=500,
    )

    expected_body = {
        "export_type": "VECTORS",
        "file_format": "CSV",
        "params": {
            "sort": {"property": "priority", "direction": "desc"},
            "filters": {
                "operator": "and",
                "value": [
                    {"key": "priority", "operator": "gte", "value": "8"},
                ],
            },
            "vector_ids": ["vec-001", "vec-002"],
            "page_number": 1,
            "max_entries_per_page": 500,
        },
        "columns": ["path_name", "priority"],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-path",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_paths(
        export_type=AttackPathExportType.VECTORS,
        file_format=FileFormat.CSV,
        params=params,
        columns=[AttackPathColumnKey.PATH_NAME, AttackPathColumnKey.PRIORITY],
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_paths_all_columns(tenable_one_api, export_request_id_response):
    """Test attack_paths requesting every available column."""
    all_columns = list(AttackPathColumnKey)

    expected_body = {
        "export_type": "VECTORS",
        "file_format": "JSON",
        "params": {},
        "columns": [c.value for c in all_columns],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-path",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_paths(
        export_type=AttackPathExportType.VECTORS,
        file_format=FileFormat.JSON,
        columns=all_columns,
    )

    assert result.export_id == "export-ap-12345"


# ---------------------------------------------------------------------------
# attack_techniques() tests
# ---------------------------------------------------------------------------

@responses.activate
def test_attack_techniques_minimal(tenable_one_api, export_request_id_response):
    """Test attack_techniques with only required parameters."""
    expected_body = {
        "file_format": "JSON",
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.JSON,
    )

    assert isinstance(result, ExportRequestId)
    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_with_columns(tenable_one_api, export_request_id_response):
    """Test attack_techniques with specific columns."""
    expected_body = {
        "file_format": "CSV",
        "columns": ["mitre_id", "technique_name", "priority"],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.CSV,
        columns=[
            AttackTechniqueColumnKey.MITRE_ID,
            AttackTechniqueColumnKey.TECHNIQUE_NAME,
            AttackTechniqueColumnKey.PRIORITY,
        ],
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_with_filter_and_sort(
    tenable_one_api, export_request_id_response
):
    """Test attack_techniques with filter and sort parameters."""
    expected_body = {
        "file_format": "JSON",
        "filter": {
            "operator": "and",
            "value": [
                {"key": "priority", "operator": "gte", "value": "7"},
                {"key": "status", "operator": "==", "value": "active"},
            ],
        },
        "sort": {"property": "priority", "direction": "desc"},
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.JSON,
        filter=ExportFilter(
            operator="and",
            value=[
                ExportFilterCondition(key="priority", operator="gte", value="7"),
                ExportFilterCondition(key="status", operator="==", value="active"),
            ],
        ),
        sort=ExportSortParams(property="priority", direction=SortDirection.DESC),
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_with_pagination(
    tenable_one_api, export_request_id_response
):
    """Test attack_techniques with pagination parameters."""
    expected_body = {
        "file_format": "CSV",
        "page_number": 2,
        "max_findings_per_page": 100,
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.CSV,
        page_number=2,
        max_findings_per_page=100,
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_with_ids(tenable_one_api, export_request_id_response):
    """Test attack_techniques filtered by attack_technique_ids."""
    expected_body = {
        "file_format": "JSON",
        "attack_technique_ids": ["T1021", "T1078", "T1059"],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.JSON,
        attack_technique_ids=["T1021", "T1078", "T1059"],
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_with_file_name(
    tenable_one_api, export_request_id_response
):
    """Test attack_techniques with a custom file name."""
    expected_body = {
        "file_format": "CSV",
        "file_name": "techniques_report",
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.CSV,
        file_name="techniques_report",
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_all_params(tenable_one_api, export_request_id_response):
    """Test attack_techniques with every parameter populated."""
    expected_body = {
        "file_format": "JSON",
        "filter": {
            "operator": "and",
            "value": [
                {"key": "state", "operator": "==", "value": "active"},
            ],
        },
        "sort": {"property": "technique_name", "direction": "asc"},
        "columns": ["mitre_id", "technique_name", "tactics"],
        "file_name": "full_export",
        "page_number": 1,
        "max_findings_per_page": 250,
        "attack_technique_ids": ["T1021"],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.JSON,
        filter=ExportFilter(
            operator="and",
            value=[
                ExportFilterCondition(key="state", operator="==", value="active"),
            ],
        ),
        sort=ExportSortParams(property="technique_name", direction=SortDirection.ASC),
        columns=[
            AttackTechniqueColumnKey.MITRE_ID,
            AttackTechniqueColumnKey.TECHNIQUE_NAME,
            AttackTechniqueColumnKey.TACTICS,
        ],
        file_name="full_export",
        page_number=1,
        max_findings_per_page=250,
        attack_technique_ids=["T1021"],
    )

    assert result.export_id == "export-ap-12345"


@responses.activate
def test_attack_techniques_all_columns(tenable_one_api, export_request_id_response):
    """Test attack_techniques requesting every available column."""
    all_columns = list(AttackTechniqueColumnKey)

    expected_body = {
        "file_format": "CSV",
        "columns": [c.value for c in all_columns],
    }

    responses.add(
        responses.POST,
        "https://cloud.tenable.com/api/v1/t1/apa/export/attack-technique",
        json=export_request_id_response,
        match=[responses.matchers.json_params_matcher(expected_body)],
    )

    result = tenable_one_api.attack_path.export.attack_techniques(
        file_format=FileFormat.CSV,
        columns=all_columns,
    )

    assert result.export_id == "export-ap-12345"


# ---------------------------------------------------------------------------
# status() tests
# ---------------------------------------------------------------------------

@responses.activate
def test_status_finished(tenable_one_api, export_status_response_finished):
    """Test getting export status for a finished export."""
    export_id = "export-ap-12345"

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/status",
        json=export_status_response_finished,
    )

    result = tenable_one_api.attack_path.export.status(export_id)

    assert isinstance(result, ExportRequestStatus)
    assert result.export_id == "export-ap-12345"
    assert result.status == ExportStatus.FINISHED
    assert result.submitted_at is not None
    assert result.last_refreshed_at is not None


@responses.activate
def test_status_processing(tenable_one_api, export_status_response_processing):
    """Test getting export status for a processing export."""
    export_id = "export-ap-12345"

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/status",
        json=export_status_response_processing,
    )

    result = tenable_one_api.attack_path.export.status(export_id)

    assert result.status == ExportStatus.PROCESSING


@responses.activate
def test_status_queued(tenable_one_api):
    """Test getting export status for a queued export."""
    export_id = "export-ap-99999"
    response_data = {
        "export_id": "export-ap-99999",
        "status": "QUEUED",
        "submitted_at": "2025-06-01T00:00:00Z",
        "last_refreshed_at": None,
    }

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/status",
        json=response_data,
    )

    result = tenable_one_api.attack_path.export.status(export_id)

    assert result.export_id == "export-ap-99999"
    assert result.status == ExportStatus.QUEUED
    assert result.last_refreshed_at is None


@responses.activate
def test_status_error(tenable_one_api):
    """Test getting export status for a failed export."""
    export_id = "export-ap-err"
    response_data = {
        "export_id": "export-ap-err",
        "status": "ERROR",
        "submitted_at": "2025-06-01T00:00:00Z",
        "last_refreshed_at": "2025-06-01T00:02:00Z",
    }

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/status",
        json=response_data,
    )

    result = tenable_one_api.attack_path.export.status(export_id)

    assert result.status == ExportStatus.ERROR


@responses.activate
def test_status_cancelled(tenable_one_api):
    """Test getting export status for a cancelled export."""
    export_id = "export-ap-cancel"
    response_data = {
        "export_id": "export-ap-cancel",
        "status": "CANCELLED",
        "submitted_at": "2025-06-01T00:00:00Z",
        "last_refreshed_at": "2025-06-01T00:03:00Z",
    }

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/status",
        json=response_data,
    )

    result = tenable_one_api.attack_path.export.status(export_id)

    assert result.status == ExportStatus.CANCELLED


# ---------------------------------------------------------------------------
# download() tests
# ---------------------------------------------------------------------------

@responses.activate
def test_download_without_file_object(tenable_one_api, export_data):
    """Test downloading export data returned as bytes."""
    export_id = "export-ap-12345"

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/download",
        body=export_data,
        content_type="application/octet-stream",
    )

    result = tenable_one_api.attack_path.export.download(export_id)

    assert isinstance(result, bytes)
    assert result == export_data
    assert len(result) > 0


@responses.activate
def test_download_with_file_object(tenable_one_api, export_data):
    """Test downloading export data streamed into a file object."""
    export_id = "export-ap-12345"
    fobj = BytesIO()

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/download",
        body=export_data,
        content_type="application/octet-stream",
    )

    result = tenable_one_api.attack_path.export.download(export_id, fobj)

    assert result is fobj
    assert isinstance(result, BytesIO)
    assert result.getvalue() == export_data


@responses.activate
def test_download_empty_response(tenable_one_api):
    """Test downloading when the response body is empty."""
    export_id = "export-ap-empty"

    responses.add(
        responses.GET,
        f"https://cloud.tenable.com/api/v1/t1/apa/export/{export_id}/download",
        body=b"",
        content_type="application/octet-stream",
    )

    result = tenable_one_api.attack_path.export.download(export_id)

    assert isinstance(result, bytes)
    assert result == b""


# ---------------------------------------------------------------------------
# Schema / model unit tests
# ---------------------------------------------------------------------------

def test_file_format_enum_values():
    """Test FileFormat enum has expected values."""
    assert FileFormat.CSV == "CSV"
    assert FileFormat.JSON == "JSON"


def test_export_status_enum_values():
    """Test ExportStatus enum has all expected values."""
    assert ExportStatus.QUEUED == "QUEUED"
    assert ExportStatus.PROCESSING == "PROCESSING"
    assert ExportStatus.FINISHED == "FINISHED"
    assert ExportStatus.ERROR == "ERROR"
    assert ExportStatus.CANCELLED == "CANCELLED"


def test_attack_path_export_type_enum_values():
    """Test AttackPathExportType enum has expected values."""
    assert AttackPathExportType.VECTORS == "VECTORS"


def test_sort_direction_enum_values():
    """Test SortDirection enum values."""
    assert SortDirection.ASC == "asc"
    assert SortDirection.DESC == "desc"


def test_attack_path_column_key_enum_values():
    """Test AttackPathColumnKey enum has all expected values."""
    expected = {
        "path_name", "priority", "source_nes", "target_acr",
        "sequence_chain", "enabler_list", "asset_ids",
    }
    assert {c.value for c in AttackPathColumnKey} == expected


def test_attack_technique_column_key_enum_values():
    """Test AttackTechniqueColumnKey enum has all expected values."""
    expected = {
        "mitre_id", "technique_name", "priority", "status", "state",
        "through", "source_names", "source_classes", "source_ids",
        "target_names", "target_classes", "target_ids", "tactics",
        "data_sources", "top_attack_path_count", "critical_assets_count",
    }
    assert {c.value for c in AttackTechniqueColumnKey} == expected


def test_export_request_id_model():
    """Test ExportRequestId model creation."""
    obj = ExportRequestId(export_id="abc-123")
    assert obj.export_id == "abc-123"


def test_export_request_status_model():
    """Test ExportRequestStatus model creation with all fields."""
    obj = ExportRequestStatus(
        export_id="abc-123",
        status=ExportStatus.FINISHED,
        submitted_at="2025-01-01T00:00:00Z",
        last_refreshed_at="2025-01-01T01:00:00Z",
    )
    assert obj.export_id == "abc-123"
    assert obj.status == ExportStatus.FINISHED
    assert obj.submitted_at is not None
    assert obj.last_refreshed_at is not None


def test_export_request_status_model_optional_fields():
    """Test ExportRequestStatus with only required fields."""
    obj = ExportRequestStatus(
        export_id="abc-123",
        status=ExportStatus.QUEUED,
    )
    assert obj.submitted_at is None
    assert obj.last_refreshed_at is None


def test_export_filter_condition_model():
    """Test ExportFilterCondition model creation."""
    f = ExportFilterCondition(key="priority", operator="gte", value="8")
    assert f.key == "priority"
    assert f.operator == "gte"
    assert f.value == "8"


def test_export_filter_model():
    """Test ExportFilter model with nested conditions."""
    ef = ExportFilter(
        operator="and",
        value=[
            ExportFilterCondition(key="priority", operator="gte", value="5"),
            ExportFilterCondition(key="status", operator="==", value="active"),
        ],
    )
    assert ef.operator == "and"
    assert len(ef.value) == 2


def test_export_filter_nested():
    """Test ExportFilter with nested ExportFilter."""
    inner = ExportFilter(
        operator="or",
        value=[
            ExportFilterCondition(key="a", operator="==", value="x"),
            ExportFilterCondition(key="b", operator="==", value="y"),
        ],
    )
    outer = ExportFilter(
        operator="and",
        value=[
            ExportFilterCondition(key="c", operator="!=", value="10"),
            inner,
        ],
    )
    assert outer.operator == "and"
    assert len(outer.value) == 2


def test_export_sort_params_model():
    """Test ExportSortParams model creation."""
    sp = ExportSortParams(property="priority", direction=SortDirection.DESC)
    assert sp.property == "priority"
    assert sp.direction == SortDirection.DESC
    assert sp.type is None


def test_export_sort_params_with_type():
    """Test ExportSortParams model with optional type field."""
    sp = ExportSortParams(property="name", direction=SortDirection.ASC, type="string")
    assert sp.type == "string"


def test_vectors_export_params_model():
    """Test VectorsExportParams model with all fields."""
    params = VectorsExportParams(
        sort=ExportSortParams(property="priority", direction=SortDirection.DESC),
        filters=ExportFilter(
            operator="and",
            value=[ExportFilterCondition(key="p", operator="==", value="v")],
        ),
        vector_ids=["v1", "v2"],
        page_number=3,
        max_entries_per_page=100,
    )
    assert params.sort.property == "priority"
    assert params.vector_ids == ["v1", "v2"]
    assert params.page_number == 3
    assert params.max_entries_per_page == 100


