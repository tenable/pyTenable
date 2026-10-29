from enum import Enum

from pydantic import BaseModel, model_validator
from typing import Any, Dict, List, Optional

from tenable.tenableone.attack_path.vectors.schema import SearchPagination


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
    accepted = "accepted"


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


class TopAttackTechnique(BaseModel):
    mitre_id: Optional[str] = None
    name: Optional[str] = None
    technique_name: Optional[str] = None
    priority: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    tactics: Optional[List[Any]] = None
    mitigations: Optional[List[Any]] = None
    malwares: Optional[List[Any]] = None
    tools: Optional[List[Any]] = None
    created: Optional[str] = None
    last_updated_at: Optional[str] = None
    serial_id: Optional[int] = None
    vector_count: Optional[int] = None
    total_vector_count: Optional[int] = None
    critical_assets_count: Optional[int] = None
    total_critical_assets_count: Optional[int] = None
    assets_ids: Optional[List[Any]] = None
    detection_ids: Optional[List[Any]] = None
    weaknesses_ids: Optional[List[Any]] = None
    groups: Optional[List[Any]] = None
    source_information: Optional[List[Any]] = None
    related_nodes: Optional[Dict[str, Any]] = None


class TopAttackTechniquesSearchResponse(BaseModel):
    data: List[TopAttackTechnique]
    pagination: Optional[SearchPagination] = None
    total: Optional[int] = None

    @model_validator(mode='after')
    def _total_from_pagination(self):
        if self.total is None and self.pagination is not None:
            self.total = self.pagination.total
        return self
