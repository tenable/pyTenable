from enum import Enum

from pydantic import BaseModel, RootModel, model_validator
from typing import Dict, List, Optional, Any, Union


class PathStatusEnum(Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    in_review = "in_review"
    done = "done"
    chain_prevented = "chain_prevented"
    accepted = "accepted"


class SourceInformationSchema(BaseModel):
    provider_detection_id: Optional[str] = None
    detection_code: Optional[str] = None
    reason_code_name: Optional[str] = None
    asset_id: Optional[str] = None
    id: Optional[str] = None
    provider_code: Optional[str] = None
    type: Optional[str] = None
    reason_id: Optional[str] = None
    plugin_name: Optional[str] = None


class TechniqueSchema(BaseModel):
    source_information: Optional[str] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    asset_id: Optional[str] = None
    id: Optional[int] = None
    labels: Optional[List[str]] = None
    procedure_uuid: Optional[str] = None


class NodeSchema(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    asset_id: Optional[str] = None
    id: Optional[int] = None
    labels: Optional[List[str]] = None


class VectorSchema(BaseModel):
    is_new: Optional[bool] = None
    vector_id: Optional[str] = None
    path: Optional[Any] = None
    techniques: Optional[List[TechniqueSchema]] = None
    nodes: Optional[List[NodeSchema]] = None
    findings_names: Optional[List[str]] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    first_aes: Optional[Any] = None
    last_acr: Optional[int] = None


class VectorsPageSchema(BaseModel):
    data: Optional[List[VectorSchema]] = None
    page_number: Optional[int] = None
    count: Optional[int] = None
    total: Optional[int] = None


# New schemas for top attack paths search endpoint
class PublicVectorFilterCondition(BaseModel):
    property: str
    operator: str
    value: Union[str, int, bool, List[Any]]


class PublicVectorFilterOperator(BaseModel):
    operator: str = "AND"
    value: List['PublicVectorFilterType']


class PublicVectorFilterType(RootModel[Union[PublicVectorFilterCondition, PublicVectorFilterOperator]]):
    pass


class VectorRow(BaseModel):
    is_new: Optional[bool] = None
    vector_id: Optional[str] = None
    path: Optional[Any] = None
    techniques: Optional[List[Any]] = None
    nodes: Optional[List[Any]] = None
    findings_names: Optional[List[str]] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    first_aes: Optional[float] = None
    last_acr: Optional[int] = None
    path_status: Optional[PathStatusEnum] = None
    priority: Optional[float] = None
    graph_node: Optional[Dict[str, Any]] = None
    mitigations: Optional[List[Any]] = None


class SearchSortInfo(BaseModel):
    name: Optional[str] = None
    order: Optional[str] = None


class SearchPagination(BaseModel):
    total: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    sort: Optional[SearchSortInfo] = None


class DiscoverPageTableResponse(BaseModel):
    data: List[VectorRow]
    pagination: Optional[SearchPagination] = None
    total: Optional[int] = None

    @model_validator(mode='after')
    def _total_from_pagination(self):
        # The API reports the total inside ``pagination``; keep ``total`` populated
        # for callers that read it directly.
        if self.total is None and self.pagination is not None:
            self.total = self.pagination.total
        return self
