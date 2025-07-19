"""
Export Schema
============

This module contains the shared schema definitions for the Export APIs.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ExportStatus(str, Enum):
    """Export status enumeration."""
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class PropertyOperator(str, Enum):
    """Property operator enumeration."""
    EQUAL = "="
    NOT_EQUAL = "!="
    LESS_EQUAL = "<="
    BETWEEN = "between"
    MATCH = "match"
    GREATER_EQUAL = ">="
    LESS = "<"
    GREATER = ">"
    CONTAINS = "contains"
    NOT_CONTAINS = "not contains"
    EXISTS = "exists"
    NOT_EXISTS = "not exists"
    OLDER_THAN = "older than"
    NEWER_THAN = "newer than"
    WITHIN_LAST = "within last"


class PropertyFilter(BaseModel):
    """Property filter model."""
    property: str = Field(..., description="The property on which the filtering operation is performed")
    operator: PropertyOperator = Field(..., description="The operator to use for filtering")
    value: List[str] = Field(..., description="The value used for comparison in the filtering operation")


class DatasetExportRequest(BaseModel):
    """Dataset export request model."""
    filters: Optional[List[PropertyFilter]] = Field(None, description="List of filters to apply")


class ExportRequestId(BaseModel):
    """Export request ID model."""
    export_id: str = Field(..., description="The export request ID")


class ExportRequestStatus(BaseModel):
    """Export request status model."""
    export_id: str = Field(..., description="The export request ID")
    submitted_at: Optional[datetime] = Field(None, description="When the export was submitted")
    last_refreshed_at: Optional[datetime] = Field(None, description="When the export was last refreshed")
    status: ExportStatus = Field(..., description="The current status of the export")
    chunks_available: List[int] = Field(
        default_factory=list,
        description="A list of chunk numbers that are ready for download"
    ) 