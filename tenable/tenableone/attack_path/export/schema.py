"""
Attack Path Export Schema
=========================

This module contains the schema definitions for the Attack Path Export APIs.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class FileFormat(str, Enum):
    """File format enumeration."""

    CSV = 'CSV'
    JSON = 'JSON'


class ExportStatus(str, Enum):
    """Export status enumeration."""

    QUEUED = 'QUEUED'
    PROCESSING = 'PROCESSING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'
    CANCELLED = 'CANCELLED'


class AttackPathExportType(str, Enum):
    """Attack path export type enumeration."""

    VECTORS = 'VECTORS'


class AttackPathColumnKey(str, Enum):
    """Column keys available for attack path exports."""

    PATH_NAME = 'path_name'
    PRIORITY = 'priority'
    SOURCE_NES = 'source_nes'
    TARGET_ACR = 'target_acr'
    SEQUENCE_CHAIN = 'sequence_chain'
    ENABLER_LIST = 'enabler_list'
    ASSET_IDS = 'asset_ids'


class AttackTechniqueColumnKey(str, Enum):
    """Column keys available for attack technique exports."""

    MITRE_ID = 'mitre_id'
    TECHNIQUE_NAME = 'technique_name'
    PRIORITY = 'priority'
    STATUS = 'status'
    STATE = 'state'
    THROUGH = 'through'
    SOURCE_NAMES = 'source_names'
    SOURCE_CLASSES = 'source_classes'
    SOURCE_IDS = 'source_ids'
    TARGET_NAMES = 'target_names'
    TARGET_CLASSES = 'target_classes'
    TARGET_IDS = 'target_ids'
    TACTICS = 'tactics'
    DATA_SOURCES = 'data_sources'
    TOP_ATTACK_PATH_COUNT = 'top_attack_path_count'
    CRITICAL_ASSETS_COUNT = 'critical_assets_count'


class SortDirection(str, Enum):
    """Sort direction enumeration."""

    ASC = 'asc'
    DESC = 'desc'


class SortType(str, Enum):
    """Sort type enumeration."""

    STRING = 'string'
    NUMBER = 'number'


class LogicalOperator(str, Enum):
    """Logical operator enumeration for combining multiple filters."""

    AND = 'and'
    OR = 'or'


class ExportSortParams(BaseModel):
    """Sort parameters for export requests."""

    property: str = Field(..., description='The property to sort by')
    direction: SortDirection = Field(..., description='The sort direction')
    type: Optional[SortType] = Field(
        None,
        description='The data type of the sort property.',
    )


class ExportFilterCondition(BaseModel):
    """A single filter condition."""

    operator: str = Field(
        ...,
        description='Comparison operator (e.g., ==, !=, includes, excludes)',
    )
    key: str = Field(..., description='Property key for filter condition')
    value: str = Field(..., description='Value for filter condition')


class ExportFilter(BaseModel):
    """A filter group with AND/OR operator and nested conditions."""

    operator: Optional[LogicalOperator] = Field(
        None,
        description='The logical operator to combine filters',
    )
    value: Optional[List[Union['ExportFilter', ExportFilterCondition]]] = Field(
        None, description='The list of filters or nested filter groups'
    )


class VectorsExportParams(BaseModel):
    """Parameters for exporting pre-computed vectors."""

    sort: Optional[ExportSortParams] = Field(
        None, description='Sort parameters'
    )
    filters: Optional[Union[ExportFilter, ExportFilterCondition]] = Field(
        None, description='Filters to apply'
    )
    vector_ids: Optional[List[str]] = Field(
        None, description='List of vector IDs to filter by'
    )
    page_number: Optional[int] = Field(
        None, description='The page number to export'
    )
    max_entries_per_page: Optional[int] = Field(
        None, description='Maximum number of entries per page'
    )


class AttackPathExportRequest(BaseModel):
    """Request model for attack path exports."""

    export_type: AttackPathExportType = Field(
        ..., description='The type of export'
    )
    file_format: FileFormat = Field(..., description='The output file format')
    params: VectorsExportParams = Field(
        ..., description='Export parameters'
    )
    columns: Optional[List[AttackPathColumnKey]] = Field(
        None, description='Columns to include in the export'
    )
    file_name: Optional[str] = Field(
        None, description='The name of the export file'
    )


class AttackTechniqueExportRequest(BaseModel):
    """Request model for attack technique exports."""

    file_format: FileFormat = Field(..., description='The output file format')
    filter: Optional[Union[ExportFilter, ExportFilterCondition]] = Field(
        None, description='Filters to apply'
    )
    sort: Optional[ExportSortParams] = Field(
        None, description='Sort parameters'
    )
    columns: Optional[List[AttackTechniqueColumnKey]] = Field(
        None, description='Columns to include in the export'
    )
    file_name: Optional[str] = Field(
        None, description='The name of the export file'
    )
    page_number: Optional[int] = Field(
        None, description='The page number to export'
    )
    max_findings_per_page: Optional[int] = Field(
        None, description='Maximum number of findings per page'
    )
    attack_technique_ids: Optional[List[str]] = Field(
        None, description='List of attack technique IDs to filter by'
    )


class ExportRequestId(BaseModel):
    """Export request ID model."""

    export_id: str = Field(..., description='The export request ID')


class ExportRequestStatus(BaseModel):
    """Export request status model."""

    export_id: str = Field(..., description='The export request ID')
    status: ExportStatus = Field(
        ..., description='The current status of the export'
    )
    submitted_at: Optional[datetime] = Field(
        None, description='When the export was submitted'
    )
    last_refreshed_at: Optional[datetime] = Field(
        None, description='When the export was last refreshed'
    )
