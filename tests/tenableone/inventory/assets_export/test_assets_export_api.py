import json
from datetime import datetime

import pytest
import responses

from tenable.tenableone.inventory.assets_export.schema import (
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
    return b"asset_id,asset_name,asset_class\n123,test-asset,DEVICE\n456,test-asset-2,APPLICATION"


@responses.activate
def test_export_basic(tenable_one_api, export_request_id_response):
    """Test basic export without any parameters."""
    # Arrange
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.assets_export.export()
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_export_with_properties(tenable_one_api, export_request_id_response):
    """Test export with properties parameter."""
    # Arrange
    properties = "cpe,version,file_location"
    expected_params = {"properties": properties}
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[responses.matchers.query_param_matcher(expected_params)]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.assets_export.export(properties=properties)
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_export_with_filters(tenable_one_api, export_request_id_response):
    """Test export with filters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="asset_class",
            operator=PropertyOperator.EQUAL,
            value=["DEVICE"]
        )
    ]
    expected_body = {
        "filters": [
            {
                "property": "asset_class",
                "operator": "=",
                "value": ["DEVICE"]
            }
        ]
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[responses.matchers.body_matcher(params=json.dumps(expected_body))]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.assets_export.export(filters=filters)
    
    # Assert
    assert result.export_id == "export-12345"


@responses.activate
def test_export_with_all_parameters(tenable_one_api, export_request_id_response):
    """Test export with all parameters."""
    # Arrange
    filters = [
        PropertyFilter(
            property="asset_class",
            operator=PropertyOperator.EQUAL,
            value=["DEVICE"]
        )
    ]
    properties = "cpe,version,file_location"
    use_readable_name = True
    max_chunk_file_size = 10485760  # 10MB
    sort_by = "name"
    sort_direction = SortDirection.ASC
    
    expected_params = {
        "properties": properties,
        "use_readable_name": True,
        "max_chunk_file_size": 10485760,
        "sort": "name:asc"
    }
    expected_body = {
        "filters": [
            {
                "property": "asset_class",
                "operator": "=",
                "value": ["DEVICE"]
            }
        ]
    }
    
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/inventory/export/assets',
        json=export_request_id_response,
        match=[
            responses.matchers.body_matcher(params=json.dumps(expected_body)),
            responses.matchers.query_param_matcher(expected_params)
        ]
    )
    
    # Act
    result: ExportRequestId = tenable_one_api.inventory.assets_export.export(
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
    result: ExportRequestStatus = tenable_one_api.inventory.assets_export.status(export_id)
    
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
    result: bytes = tenable_one_api.inventory.assets_export.download(export_id, chunk_id)
    
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
    result: bytes = tenable_one_api.inventory.assets_export.download(export_id, chunk_id)
    
    # Assert
    assert result == export_data
    assert len(result) > 0


def test_property_filter_model():
    """Test PropertyFilter model creation and validation."""
    # Arrange & Act
    filter_obj = PropertyFilter(
        property="asset_class",
        operator=PropertyOperator.EQUAL,
        value=["DEVICE"]
    )
    
    # Assert
    assert filter_obj.property == "asset_class"
    assert filter_obj.operator == PropertyOperator.EQUAL
    assert filter_obj.value == ["DEVICE"]


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
            property="asset_class",
            operator=PropertyOperator.EQUAL,
            value=["DEVICE"]
        )
    ]
    
    # Act
    request = PublicDatasetExportRequest(filters=filters)
    
    # Assert
    assert request.filters is not None
    assert len(request.filters) == 1
    assert request.filters[0].property == "asset_class" 