from enum import Enum

from pydantic import BaseModel, Field
from typing import List, Optional


class PriorityEnum(Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class StateEnum(Enum):
    open = "open"
    archive = "archive"


class StatusEnum(Enum):
    in_progress = "in_progress"
    done = "done"
    to_do = "to_do"
    in_review = "in_review"


class NodeInfoSchema(BaseModel):
    name: Optional[str] = None
    fullname: Optional[str] = None
    id: Optional[str] = None
    labels: List[str] = []
    isCrownJewel: bool
    vulnerability_id: Optional[str] = None
    asset_id: Optional[str] = None


class FindingRelatedNodesSchema(BaseModel):
    sources: List[NodeInfoSchema] = []
    targets: List[NodeInfoSchema] = []
    cause: Optional[NodeInfoSchema] = None


class SourceInformationSchema(BaseModel):
    id: Optional[str] = None
    asset_id: Optional[str] = None
    type: Optional[str] = None
    provider_detection_id: Optional[str] = None
    provider_code: Optional[str] = None
    reason_id: Optional[str] = None
    reason_code_name: Optional[str] = None
    detection_code: Optional[str] = None


class FindingSchema(BaseModel):
    mitre_id: Optional[str] = None
    mitigations: List[str] = []
    malwares: List[str] = []
    tools: List[str] = []
    groups: List[str] = []
    name: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    procedureName: Optional[str] = None
    relatedNodes: Optional[FindingRelatedNodesSchema] = None
    tactics: List[str] = []
    critical_assets_count: Optional[int] = None
    total_critical_assets_count: Optional[int] = None
    totalVectorCount: Optional[int] = None
    vectorCount: Optional[int] = None
    state: Optional[StateEnum] = None
    status: Optional[StatusEnum] = None
    created: Optional[int] = None
    is_active: Optional[bool] = None
    has_history: Optional[bool] = None
    last_updated_at: Optional[str] = None
    source_information: List[SourceInformationSchema] = []
    weaknesses_ids: List[str] = []
    assets_ids: List[str] = []
    detection_ids: List[str] = []
    serial_id: Optional[int] = None


class FindingsPageSchema(BaseModel):
    data: List[FindingSchema] = []
    next: Optional[str] = None
    page_number: Optional[int] = None
    count: Optional[int] = None
    total: Optional[int] = None
