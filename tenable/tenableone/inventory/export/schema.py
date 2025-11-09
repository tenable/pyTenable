"""
Export Schema
=============

This module contains the shared schema definitions for the Export APIs.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from tenable.tenableone.inventory.schema import PropertyFilter, Query

class ExportType(str, Enum):
    """Export type enumeration."""

    FINDINGS = 'findings'
    ASSETS = 'assets'


class ExportStatus(str, Enum):
    """Export status enumeration."""

    QUEUED = 'QUEUED'
    PROCESSING = 'PROCESSING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'
    CANCELLED = 'CANCELLED'


class DatasetFileFormat(str, Enum):
    """Dataset file format enumeration."""

    CSV = 'CSV'
    JSON = 'JSON'


class DatasetExportRequest(BaseModel):
    """Dataset export request model."""

    filters: Optional[List[PropertyFilter]] = Field(
        None, description='List of filters to apply'
    )
    query: Optional[Query] = Field(
        None, description='Query to apply'
    )


class ExportRequestId(BaseModel):
    """Export request ID model."""

    export_id: str = Field(..., description='The export request ID')


class ExportRequestStatus(BaseModel):
    """Export request status model."""

    export_id: str = Field(..., description='The export request ID')
    submitted_at: Optional[datetime] = Field(
        None, description='When the export was submitted'
    )
    last_refreshed_at: Optional[datetime] = Field(
        None, description='When the export was last refreshed'
    )
    status: ExportStatus = Field(..., description='The current status of the export')
    chunks_available: List[int] = Field(
        default_factory=list,
        description='A list of chunk numbers that are ready for download',
    )


class ExportJob(BaseModel):
    """Export job model for listing export jobs."""

    export_id: str = Field(..., description='The unique identifier (UUID) of the export request')
    submitted_at: Optional[datetime] = Field(
        None, description='A timestamp in ISO 8601 format indicating the date and time the export request was submitted'
    )
    last_refreshed_at: Optional[datetime] = Field(
        None, description='A timestamp in ISO 8601 format indicating the date and time the export request was last checked for completion'
    )
    status: ExportStatus = Field(..., description='The status of the export request')
    export_type: ExportType = Field(..., description='The type of export request')


class ExportJobsResponse(BaseModel):
    """Response model for listing export jobs."""

    exports: List[ExportJob] = Field(..., description='List of export jobs')
