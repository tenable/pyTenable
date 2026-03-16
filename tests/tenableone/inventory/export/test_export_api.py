"""
Tests for the unified TenableOne Inventory Export API.

This module tests all public methods of the unified ExportAPI class.
"""

import json
import pytest
import responses
from tenable.tenableone.inventory.export.schema import (
    DatasetExportRequest,
    DatasetFileFormat,
    ExportRequestId,
    ExportRequestStatus,
    ExportStatus,
    ExportJobsResponse,
    ExportJob,
    ExportType,
)
from tenable.tenableone.inventory.schema import SortDirection, PropertyFilter, Operator, Query, QueryMode


@pytest.fixture
def export_request_id_response() -> dict:
    """Fixture for export request ID response."""
    return {"export_id": "export-12345"}


@pytest.fixture
def export_status_response() -> dict:
    """Fixture for export status response."""
    return {
        "export_id": "export-12345",
        "status": "FINISHED",
        "chunks_available": [0, 1, 2],
        "submitted_at": "2023-01-01T00:00:00Z",
        "last_refreshed_at": "2023-01-01T01:00:00Z"
    }


@pytest.fixture
def export_data() -> bytes:
    """Fixture for export data."""
    return b"test,data,export\n1,2,3\n4,5,6"


@pytest.fixture
def export_jobs_response() -> dict:
    """Fixture for export jobs list response."""
    return {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            },
            {
                "export_id": "export-67890",
                "status": "PROCESSING",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            },
            {
                "export_id": "export-11111",
                "status": "ERROR",
                "export_type": "assets",
                "submitted_at": "2025-01-01T02:00:00Z",
                "last_refreshed_at": "2025-01-01T02:01:00Z"
            }
        ]
    }


@responses.activate
def test_assets_export(tenable_one_api, export_request_id_response):
    """Test assets export with all parameters populated."""
    # Arrange
    filters = [
        PropertyFilter(
            property="asset_class",
            operator=Operator.EQUAL,
            value=["DEVICE"]
        ),
        PropertyFilter(
            property="ip_address",
            operator=Operator.CONTAINS,
            value=["192.168.1.1", "192.168.1.2"]
        )
    ]
    properties = ["cpe", "version", "file_location", "asset_name", "ip_address"]
    use_readable_name = True
    max_chunk_file_size = 10485760  # 10MB
    sort_by = "name"
    sort_direction = SortDirection.ASC
    file_format = DatasetFileFormat.CSV
    
    expected_params = {
        "properties": "cpe,version,file_location,asset_name,ip_address",
        "use_readable_name": True,
        "max_chunk_file_size": 10485760,
        "sort": "name:asc",
        "file_format": "CSV"
    }
    expected_body = {
        "filters": [
            {
                "property": "asset_class",
                "operator": "=",
                "value": ["DEVICE"]
            },
            {
                "property": "ip_address",
                "operator": "contains",
                "value": ["192.168.1.1", "192.168.1.2"]
            }
        ]
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.assets(
        filters=filters,
        properties=properties,
        use_readable_name=use_readable_name,
        max_chunk_file_size=max_chunk_file_size,
        sort_by=sort_by,
        sort_direction=sort_direction,
        file_format=file_format
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_findings_export(tenable_one_api, export_request_id_response):
    """Test findings export with all parameters populated."""
    # Arrange
    filters = [
        PropertyFilter(
            property="severity",
            operator=Operator.EQUAL,
            value=["HIGH"]
        ),
        PropertyFilter(
            property="status",
            operator=Operator.CONTAINS,
            value=["OPEN", "REOPENED"]
        )
    ]
    properties = ["severity", "status", "created_at", "vulnerability_name", "asset_name"]
    use_readable_name = True
    max_chunk_file_size = 20971520  # 20MB
    sort_by = "severity"
    sort_direction = SortDirection.DESC
    file_format = DatasetFileFormat.JSON
    
    expected_params = {
        "properties": "severity,status,created_at,vulnerability_name,asset_name",
        "use_readable_name": True,
        "max_chunk_file_size": 20971520,
        "sort": "severity:desc",
        "file_format": "JSON"
    }
    expected_body = {
        "filters": [
            {
                "property": "severity",
                "operator": "=",
                "value": ["HIGH"]
            },
            {
                "property": "status",
                "operator": "contains",
                "value": ["OPEN", "REOPENED"]
            }
        ]
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.findings(
        filters=filters,
        properties=properties,
        use_readable_name=use_readable_name,
        max_chunk_file_size=max_chunk_file_size,
        sort_by=sort_by,
        sort_direction=sort_direction,
        file_format=file_format
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_assets_export_with_compress(tenable_one_api, export_request_id_response):
    """Test assets export with compress parameter set to True."""
    # Arrange
    properties = ["cpe", "version", "file_location"]
    compress = True
    
    expected_params = {
        "properties": "cpe,version,file_location",
        "compress": True
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.assets(
        properties=properties,
        compress=compress
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_findings_export_with_compress(tenable_one_api, export_request_id_response):
    """Test findings export with compress parameter set to True."""
    # Arrange
    properties = ["severity", "status", "created_at"]
    compress = True
    
    expected_params = {
        "properties": "severity,status,created_at",
        "compress": True
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.findings(
        properties=properties,
        compress=compress
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_assets_export_with_compress_false(tenable_one_api, export_request_id_response):
    """Test assets export with compress parameter set to False."""
    # Arrange
    properties = ["cpe", "version", "file_location"]
    compress = False
    
    expected_params = {
        "properties": "cpe,version,file_location",
        "compress": False
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.assets(
        properties=properties,
        compress=compress
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_findings_export_with_compress_false(tenable_one_api, export_request_id_response):
    """Test findings export with compress parameter set to False."""
    # Arrange
    properties = ["severity", "status", "created_at"]
    compress = False
    
    expected_params = {
        "properties": "severity,status,created_at",
        "compress": False
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.findings(
        properties=properties,
        compress=compress
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_assets_export_with_simple_query(tenable_one_api, export_request_id_response):
    """Test assets export with simple query parameter."""
    # Arrange
    properties = ["cpe", "version", "file_location"]
    query = Query(text="test query", mode=QueryMode.SIMPLE)
    
    expected_params = {
        "properties": "cpe,version,file_location"
    }
    expected_body = {
        "query": {
            "text": "test query",
            "mode": "simple"
        }
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.assets(
        properties=properties,
        query=query
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_assets_export_with_advanced_query(tenable_one_api, export_request_id_response):
    """Test assets export with query parameter using advanced mode."""
    # Arrange
    properties = ["cpe", "version", "file_location"]
    query = Query(text="advanced search", mode=QueryMode.ADVANCED)
    
    expected_params = {
        "properties": "cpe,version,file_location"
    }
    expected_body = {
        "query": {
            "text": "advanced search",
            "mode": "advanced"
        }
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.assets(
        properties=properties,
        query=query
    )

    # Assert
    assert result.export_id == "export-12345"

@responses.activate
def test_assets_export_with_filters_and_query(tenable_one_api, export_request_id_response):
    """Test assets export with both filters and query parameters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="asset_class",
            operator=Operator.EQUAL,
            value=["DEVICE"]
        )
    ]
    query = Query(text="test query", mode=QueryMode.ADVANCED)
    properties = ["cpe", "version", "file_location"]
    
    expected_params = {
        "properties": "cpe,version,file_location"
    }
    expected_body = {
        "filters": [
            {
                "property": "asset_class",
                "operator": "=",
                "value": ["DEVICE"]
            }
        ],
        "query": {
            "text": "test query",
            "mode": "advanced"
        }
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.assets(
        filters=filters,
        query=query,
        properties=properties
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_findings_export_with_simple_query(tenable_one_api, export_request_id_response):
    """Test findings export with simple query parameter."""
    # Arrange
    properties = ["severity", "status", "created_at"]
    query = Query(text="vulnerability search", mode=QueryMode.SIMPLE)
    
    expected_params = {
        "properties": "severity,status,created_at"
    }
    expected_body = {
        "query": {
            "text": "vulnerability search",
            "mode": "simple"
        }
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.findings(
        properties=properties,
        query=query
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_findings_export_with_advanced_query(tenable_one_api, export_request_id_response):
    """Test findings export with query parameter using advanced mode."""
    # Arrange
    properties = ["severity", "status", "created_at"]
    query = Query(text="critical vulnerabilities", mode=QueryMode.ADVANCED)
    
    expected_params = {
        "properties": "severity,status,created_at"
    }
    expected_body = {
        "query": {
            "text": "critical vulnerabilities",
            "mode": "advanced"
        }
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.findings(
        properties=properties,
        query=query
    )

    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_findings_export_with_filters_and_query(tenable_one_api, export_request_id_response):
    """Test findings export with both filters and query parameters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="severity",
            operator=Operator.EQUAL,
            value=["HIGH"]
        )
    ]
    query = Query(text="test query", mode=QueryMode.SIMPLE)
    properties = ["severity", "status", "created_at"]
    
    expected_params = {
        "properties": "severity,status,created_at"
    }
    expected_body = {
        "filters": [
            {
                "property": "severity",
                "operator": "=",
                "value": ["HIGH"]
            }
        ],
        "query": {
            "text": "test query",
            "mode": "simple"
        }
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.query_param_matcher(expected_params),
            responses.matchers.body_matcher(params=json.dumps(expected_body))
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.export.findings(
        filters=filters,
        query=query,
        properties=properties
    )

    # Assert
    assert result.export_id == "export-12345"




@responses.activate
def test_status(tenable_one_api, export_status_response):
    """Test getting export status with finished export."""
    # Arrange
    export_id = "export-12345"
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/status',
        json=export_status_response
    )
    
    # Act
    result: ExportRequestStatus = tenable_one_api.inventory.export.status(export_id)
    
    # Assert
    assert result.export_id == "export-12345"
    assert result.status == ExportStatus.FINISHED
    assert result.chunks_available == [0, 1, 2]
    assert result.submitted_at is not None
    assert result.last_refreshed_at is not None


@responses.activate
def test_assets_status(tenable_one_api):
    """Test listing asset export jobs."""
    # Arrange
    assets_response = {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            },
            {
                "export_id": "export-11111",
                "status": "PROCESSING",
                "export_type": "assets",
                "submitted_at": "2025-01-01T02:00:00Z",
                "last_refreshed_at": "2025-01-01T02:01:00Z"
            }
        ]
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response
    )

    # Act
    result = tenable_one_api.inventory.export.assets_status()

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 2
    assert result.exports[0].export_id == "export-12345"
    assert result.exports[0].status == ExportStatus.FINISHED
    assert result.exports[0].export_type == ExportType.ASSETS
    assert result.exports[1].export_id == "export-11111"
    assert result.exports[1].status == ExportStatus.PROCESSING
    assert result.exports[1].export_type == ExportType.ASSETS


@responses.activate
def test_findings_status(tenable_one_api):
    """Test listing finding export jobs."""
    # Arrange
    findings_response = {
        "exports": [
            {
                "export_id": "export-67890",
                "status": "FINISHED",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            },
            {
                "export_id": "export-22222",
                "status": "ERROR",
                "export_type": "findings",
                "submitted_at": "2025-01-01T03:00:00Z",
                "last_refreshed_at": "2025-01-01T03:01:00Z"
            }
        ]
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response
    )

    # Act
    result = tenable_one_api.inventory.export.findings_status()

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 2
    assert result.exports[0].export_id == "export-67890"
    assert result.exports[0].status == ExportStatus.FINISHED
    assert result.exports[0].export_type == ExportType.FINDINGS
    assert result.exports[1].export_id == "export-22222"
    assert result.exports[1].status == ExportStatus.ERROR
    assert result.exports[1].export_type == ExportType.FINDINGS


@responses.activate
def test_assets_status_with_filter(tenable_one_api):
    """Test listing asset export jobs with status filter."""
    # Arrange
    assets_response = {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            }
        ]
    }

    expected_params = {
        'status': 'FINISHED'
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.assets_status(status='FINISHED')

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 1
    assert result.exports[0].status == ExportStatus.FINISHED


@responses.activate
def test_findings_status_with_filter(tenable_one_api):
    """Test listing finding export jobs with status filter."""
    # Arrange
    findings_response = {
        "exports": [
            {
                "export_id": "export-67890",
                "status": "PROCESSING",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            }
        ]
    }

    expected_params = {
        'status': 'PROCESSING'
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.findings_status(status='PROCESSING')

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 1
    assert result.exports[0].status == ExportStatus.PROCESSING


@responses.activate
def test_assets_status_with_limit(tenable_one_api):
    """Test listing asset export jobs with limit parameter."""
    # Arrange
    assets_response = {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            }
        ]
    }

    expected_params = {
        'limit': 100
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.assets_status(limit=100)

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 1


@responses.activate
def test_findings_status_with_limit(tenable_one_api):
    """Test listing finding export jobs with limit parameter."""
    # Arrange
    findings_response = {
        "exports": [
            {
                "export_id": "export-67890",
                "status": "FINISHED",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            }
        ]
    }

    expected_params = {
        'limit': 50
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.findings_status(limit=50)

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 1


@responses.activate
def test_assets_status_with_multiple_statuses(tenable_one_api):
    """Test listing asset export jobs with comma-separated statuses."""
    # Arrange
    assets_response = {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            },
            {
                "export_id": "export-11111",
                "status": "PROCESSING",
                "export_type": "assets",
                "submitted_at": "2025-01-01T02:00:00Z",
                "last_refreshed_at": "2025-01-01T02:01:00Z"
            }
        ]
    }

    expected_params = {
        'status': 'FINISHED,PROCESSING'
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.assets_status(status='FINISHED,PROCESSING')

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 2


@responses.activate
def test_findings_status_with_multiple_statuses(tenable_one_api):
    """Test listing finding export jobs with comma-separated statuses."""
    # Arrange
    findings_response = {
        "exports": [
            {
                "export_id": "export-67890",
                "status": "FINISHED",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            },
            {
                "export_id": "export-22222",
                "status": "ERROR",
                "export_type": "findings",
                "submitted_at": "2025-01-01T03:00:00Z",
                "last_refreshed_at": "2025-01-01T03:01:00Z"
            }
        ]
    }

    expected_params = {
        'status': 'FINISHED,ERROR'
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.findings_status(status='FINISHED,ERROR')

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 2


@responses.activate
def test_assets_status_with_all_parameters(tenable_one_api):
    """Test listing asset export jobs with all parameters (status and limit)."""
    # Arrange
    assets_response = {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            }
        ]
    }

    expected_params = {
        'status': 'FINISHED',
        'limit': 50
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.assets_status(
        status='FINISHED',
        limit=50
    )

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 1


@responses.activate
def test_findings_status_with_all_parameters(tenable_one_api):
    """Test listing finding export jobs with all parameters (status and limit)."""
    # Arrange
    findings_response = {
        "exports": [
            {
                "export_id": "export-67890",
                "status": "PROCESSING",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            }
        ]
    }

    expected_params = {
        'status': 'PROCESSING',
        'limit': 25
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response,
        match=[
            responses.matchers.query_param_matcher(expected_params)
        ]
    )

    # Act
    result = tenable_one_api.inventory.export.findings_status(
        status='PROCESSING',
        limit=25
    )

    # Assert
    assert isinstance(result, ExportJobsResponse)
    assert len(result.exports) == 1


@responses.activate
def test_assets_status_limit_boundary_values(tenable_one_api):
    """Test listing asset export jobs with limit boundary values (1 and 1000)."""
    # Arrange
    assets_response = {
        "exports": [
            {
                "export_id": "export-12345",
                "status": "FINISHED",
                "export_type": "assets",
                "submitted_at": "2025-01-01T00:00:00Z",
                "last_refreshed_at": "2025-01-01T00:01:00Z"
            }
        ]
    }

    # Test minimum limit (1)
    expected_params_min = {
        'limit': 1
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response,
        match=[
            responses.matchers.query_param_matcher(expected_params_min)
        ]
    )

    result_min = tenable_one_api.inventory.export.assets_status(limit=1)
    assert isinstance(result_min, ExportJobsResponse)

    # Test maximum limit (1000)
    expected_params_max = {
        'limit': 1000
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets/status',
        json=assets_response,
        match=[
            responses.matchers.query_param_matcher(expected_params_max)
        ]
    )

    result_max = tenable_one_api.inventory.export.assets_status(limit=1000)
    assert isinstance(result_max, ExportJobsResponse)


@responses.activate
def test_findings_status_limit_boundary_values(tenable_one_api):
    """Test listing finding export jobs with limit boundary values (1 and 1000)."""
    # Arrange
    findings_response = {
        "exports": [
            {
                "export_id": "export-67890",
                "status": "FINISHED",
                "export_type": "findings",
                "submitted_at": "2025-01-01T01:00:00Z",
                "last_refreshed_at": "2025-01-01T01:01:00Z"
            }
        ]
    }

    # Test minimum limit (1)
    expected_params_min = {
        'limit': 1
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response,
        match=[
            responses.matchers.query_param_matcher(expected_params_min)
        ]
    )

    result_min = tenable_one_api.inventory.export.findings_status(limit=1)
    assert isinstance(result_min, ExportJobsResponse)

    # Test maximum limit (1000)
    expected_params_max = {
        'limit': 1000
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings/status',
        json=findings_response,
        match=[
            responses.matchers.query_param_matcher(expected_params_max)
        ]
    )

    result_max = tenable_one_api.inventory.export.findings_status(limit=1000)
    assert isinstance(result_max, ExportJobsResponse)


@responses.activate
def test_download_with_file_object(tenable_one_api, export_data):
    """Test downloading export data with file object."""
    # Arrange
    from io import BytesIO
    export_id = "export-12345"
    chunk_id = "0"
    fobj = BytesIO()
    
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/download/{chunk_id}',
        body=export_data,
        content_type='application/octet-stream'
    )
    
    # Act
    result = tenable_one_api.inventory.export.download(export_id, chunk_id, fobj)
    
    # Assert
    assert result == fobj
    assert result.getvalue() == export_data
    assert isinstance(result, BytesIO)


@responses.activate
def test_download_without_file_object(tenable_one_api, export_data):
    """Test downloading export data without file object (returns bytes)."""
    # Arrange
    export_id = "export-12345"
    chunk_id = "0"
    
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/download/{chunk_id}',
        body=export_data,
        content_type='application/octet-stream'
    )
    
    # Act
    result = tenable_one_api.inventory.export.download(export_id, chunk_id)
    
    # Assert
    assert result == export_data
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_property_filter_model_with_all_fields():
    """Test PropertyFilter model creation with all fields."""
    # Arrange & Act
    filter_obj = PropertyFilter(
        property="asset_class",
        operator=Operator.EQUAL,
        value=["DEVICE", "SERVER"]
    )
    
    # Assert
    assert filter_obj.property == "asset_class"
    assert filter_obj.operator == Operator.EQUAL
    assert filter_obj.value == ["DEVICE", "SERVER"]


def test_export_request_id_model_with_export_id():
    """Test ExportRequestId model creation."""
    # Arrange & Act
    export_id = ExportRequestId(export_id="export-12345")
    
    # Assert
    assert export_id.export_id == "export-12345"


def test_export_request_status_model_with_all_fields():
    """Test ExportRequestStatus model creation with all fields."""
    # Arrange & Act
    status = ExportRequestStatus(
        export_id="export-12345",
        status=ExportStatus.FINISHED,
        chunks_available=[0, 1, 2, 3],
        submitted_at="2023-01-01T00:00:00Z",
        last_refreshed_at="2023-01-01T01:00:00Z"
    )
    
    # Assert
    assert status.export_id == "export-12345"
    assert status.status == ExportStatus.FINISHED
    assert status.chunks_available == [0, 1, 2, 3]
    assert status.submitted_at is not None
    assert status.last_refreshed_at is not None


def test_dataset_export_request_model_with_filters():
    """Test DatasetExportRequest model creation with filters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="asset_class",
            operator=Operator.EQUAL,
            value=["DEVICE"]
        ),
        PropertyFilter(
            property="ip_address",
            operator=Operator.CONTAINS,
            value=["192.168.1.1", "192.168.1.2"]
        )
    ]
    
    # Act
    request = DatasetExportRequest(filters=filters)
    
    # Assert
    assert request.filters is not None
    assert len(request.filters) == 2
    assert request.filters[0].property == "asset_class"
    assert request.filters[1].property == "ip_address"
