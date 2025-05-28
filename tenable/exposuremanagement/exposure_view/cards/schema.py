import enum
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, NonNegativeInt


class CESTrendDataPoint(BaseModel):
    date: datetime
    cesScore: Optional[int]

class CardType(enum.Enum):
    GLOBAL = "GLOBAL"
    CATEGORY = "CATEGORY"
    EXPOSURE = "EXPOSURE"
    CUSTOM = "CUSTOM"

class CESGrade(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"
    CESNone = "None"

class ExposureClass(enum.Enum):
    ALL = "ALL"
    IDENTITY = "IDENTITY"
    VM = "VM"
    CLOUD = "CLOUD"
    OT = "OT"

class CESScore(BaseModel):
    score: int
    grade: CESGrade


class Card(BaseModel):
    card_id: int
    card_name: str
    card_type: str = CardType.CUSTOM.value
    is_global: bool = False
    ces_score: CESScore = None
    sla_percentage: Optional[float] = None
    ces_trend: List[CESTrendDataPoint] = []
    tag_count: int = 0
    exposures: List[ExposureClass] = []
    last_data_update_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    sources: Optional[List[str]] = None

class Pagination(BaseModel):
    page_number: Optional[NonNegativeInt] = 1
    page_size: Optional[NonNegativeInt] = 25


class Cards(BaseModel):
    cards: List[Card] = []
    pagination: Pagination = None

class CardsResponse(BaseModel):
    data: Cards

class CardFilter(BaseModel):
    is_global_Card: Optional[bool] = None
    card_id: Optional[int] = None
    asset_id: Optional[int] = None
    text_query: Optional[str] = None
