from pydantic import BaseModel
from typing import List, Optional, Any


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
