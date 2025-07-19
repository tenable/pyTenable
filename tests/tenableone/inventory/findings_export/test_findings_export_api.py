import json
from datetime import datetime

import pytest
import responses

from tenable.tenableone.inventory.findings_export.schema import (
    ExportRequestId,
    ExportRequestStatus,
    ExportStatus,
    PropertyFilter,
    PropertyOperator,
    PublicDatasetExportRequest,
)
from tenable.tenableone.inventory.schema import SortDirection


@pytest.fixture
def export_request_id_response() -> dict:
    return {"export_id": "export-12345"}


@pytest.fixture
def export_status_response() -> dict:
    return {
        "export_id": "export-12345",
        "submitted_at": "2024-01-15T10:30:00Z",
        "last_refreshed_at": "2024-01-15T10:35:00Z",
        "status": "FINISHED",
        "chunks_available": [0, 1, 2]
    }


@pytest.fixture
def export_data() -> bytes:
    return b"finding_id,severity,status,created_at\n123,HIGH,OPEN,2024-01-15\n456,MEDIUM,CLOSED,2024-01-14"


@responses.activate
def test_export_basic(tenable_one_api, export_request_id_response):
    """Test basic export without any parameters."""
    # Arrange
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.findings_export.export()
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_export_with_properties(tenable_one_api, export_request_id_response):
    """Test export with properties parameter."""
    # Arrange
    properties = "severity,status,created_at"
    expected_params = {"properties": properties}
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[responses.matchers.query_param_matcher(expected_params)]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.findings_export.export(properties=properties)
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_export_with_filters(tenable_one_api, export_request_id_response):
    """Test export with filters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="severity",
            operator=PropertyOperator.EQUAL,
            value=["HIGH"]
        )
    ]
    expected_body = {
        "filters": [
            {
                "property": "severity",
                "operator": "=",
                "value": ["HIGH"]
            }
        ]
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[responses.matchers.body_matcher(params=json.dumps(expected_body))]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.findings_export.export(filters=filters)
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_export_with_all_parameters(tenable_one_api, export_request_id_response):
    """Test export with all parameters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="severity",
            operator=PropertyOperator.EQUAL,
            value=["HIGH"]
        )
    ]
    properties = "severity,status,created_at"
    use_readable_name = True
    max_chunk_file_size = 10485760  # 10MB
    sort_by = "severity"
    sort_direction = SortDirection.DESC
    
    expected_params = {
        "properties": properties,
        "use_readable_name": True,
        "max_chunk_file_size": 10485760,
        "sort": "severity:desc"
    }
    expected_body = {
        "filters": [
            {
                "property": "severity",
                "operator": "=",
                "value": ["HIGH"]
            }
        ]
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/findings',
        json=export_request_id_response,
        match=[
            responses.matchers.body_matcher(params=json.dumps(expected_body)),
            responses.matchers.query_param_matcher(expected_params)
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.findings_export.export(
        filters=filters,
        properties=properties,
        use_readable_name=use_readable_name,
        max_chunk_file_size=max_chunk_file_size,
        sort_by=sort_by,
        sort_direction=sort_direction
    )
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_status(tenable_one_api, export_status_response):
    """Test getting export status."""
    # Arrange
    export_id = "export-12345"
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/status',
        json=export_status_response
    )
    
    # Act
    result: ExportRequestStatus = tenable_one_api.inventory.findings_export.status(export_id)
    
    # Assert
    assert result.export_id == "export-12345"
    assert result.status == ExportStatus.FINISHED
    assert result.chunks_available == [0, 1, 2]
    assert result.submitted_at is not None
    assert result.last_refreshed_at is not None


@responses.activate
def test_download(tenable_one_api, export_data):
    """Test downloading export data."""
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
    result: bytes = tenable_one_api.inventory.findings_export.download(export_id, chunk_id)
    
    # Assert
    assert result == export_data
    assert isinstance(result, bytes)


@responses.activate
def test_download_with_stream(tenable_one_api, export_data):
    """Test downloading export data with streaming."""
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
    result: bytes = tenable_one_api.inventory.findings_export.download(export_id, chunk_id)
    
    # Assert
    assert result == export_data
    assert len(result) > 0


def test_property_filter_model():
    """Test PropertyFilter model creation and validation."""
    # Arrange & Act
    filter_obj = PropertyFilter(
        property="severity",
        operator=PropertyOperator.EQUAL,
        value=["HIGH"]
    )
    
    # Assert
    assert filter_obj.property == "severity"
    assert filter_obj.operator == PropertyOperator.EQUAL
    assert filter_obj.value == ["HIGH"]


def test_export_request_id_model():
    """Test ExportRequestId model creation and validation."""
    # Arrange & Act
    export_id = ExportRequestId(export_id="export-12345")
    
    # Assert
    assert export_id.export_id == "export-12345"


def test_export_request_status_model():
    """Test ExportRequestStatus model creation and validation."""
    # Arrange & Act
    status = ExportRequestStatus(
        export_id="export-12345",
        status=ExportStatus.FINISHED,
        chunks_available=[0, 1, 2]
    )
    
    # Assert
    assert status.export_id == "export-12345"
    assert status.status == ExportStatus.FINISHED
    assert status.chunks_available == [0, 1, 2]


def test_public_dataset_export_request_model():
    """Test PublicDatasetExportRequest model creation and validation."""
    # Arrange
    filters = [
        PropertyFilter(
            property="severity",
            operator=PropertyOperator.EQUAL,
            value=["HIGH"]
        )
    ]
    
    # Act
    request = PublicDatasetExportRequest(filters=filters)
    
    # Assert
    assert request.filters is not None
    assert len(request.filters) == 1
    assert request.filters[0].property == "severity"


@responses.activate
def test_export_status_queued(tenable_one_api):
    """Test export status when queued."""
    # Arrange
    export_id = "export-12345"
    status_response = {
        "export_id": "export-12345",
        "status": "QUEUED",
        "chunks_available": []
    }
    
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/status',
        json=status_response
    )
    
    # Act
    result: ExportRequestStatus = tenable_one_api.inventory.findings_export.status(export_id)
    
    # Assert
    assert result.status == ExportStatus.QUEUED
    assert result.chunks_available == []


@responses.activate
def test_export_status_processing(tenable_one_api):
    """Test export status when processing."""
    # Arrange
    export_id = "export-12345"
    status_response = {
        "export_id": "export-12345",
        "status": "PROCESSING",
        "chunks_available": []
    }
    
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/status',
        json=status_response
    )
    
    # Act
    result: ExportRequestStatus = tenable_one_api.inventory.findings_export.status(export_id)
    
    # Assert
    assert result.status == ExportStatus.PROCESSING
    assert result.chunks_available == []


@responses.activate
def test_export_status_error(tenable_one_api):
    """Test export status when error."""
    # Arrange
    export_id = "export-12345"
    status_response = {
        "export_id": "export-12345",
        "status": "ERROR",
        "chunks_available": []
    }
    
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/inventory/export/{export_id}/status',
        json=status_response
    )
    
    # Act
    result: ExportRequestStatus = tenable_one_api.inventory.findings_export.status(export_id)
    
    # Assert
    assert result.status == ExportStatus.ERROR
    assert result.chunks_available == [] 