from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class JobSummaryDetails(BaseModel):
    created: int
    deleted: int
    ignored: int
    updated: int


class JobSummary(BaseModel):
    assets: JobSummaryDetails
    findings: JobSummaryDetails


class Job(BaseModel):
    id: UUID
    state: str
    sync_id: str
    failure_message: str | None = None
    summary: JobSummary | None = None
    created_at: datetime
    state_changed_at: datetime


class LogLine(BaseModel):
    id: str
    chunk_id: Annotated[int, Field(validation_alias='chunk_sequence_number')]
    log_level: str
    message: str
    path: str
    object_id: str
    type: Annotated[str, Field(validation_alias='audit_type')]
