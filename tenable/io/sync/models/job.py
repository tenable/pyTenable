from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


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
    failure_message: Optional[str] = None
    summary: Optional[JobSummary] = None
    created_at: datetime
    state_changed_at: datetime


class LogLine(BaseModel):
    id: str
    chunk_id: str
    log_level: str
    message: str
    path: str
