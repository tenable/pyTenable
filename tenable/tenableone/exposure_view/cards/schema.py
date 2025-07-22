import enum
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, NonNegativeInt, ConfigDict, Field


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

class DataCategory(enum.Enum):
    GLOBAL = "GLOBAL"
    WEB_APPLICATIONS = "WEB_APPLICATIONS"
    COMPUTING_RESOURCES = "COMPUTING_RESOURCES"
    IDENTITIES = "IDENTITIES"
    CLOUD_RESOURCES = "CLOUD_RESOURCES"
    OPERATIONAL_TECH = "OPERATIONAL_TECH"

class SlaSeverityLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    OVERALL = "OVERALL"


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
    offset: Optional[int] = 0
    limit: Optional[NonNegativeInt] = 25


class Cards(BaseModel):
    data: List[Card] = []
    pagination: Pagination = None

class CardFilter(BaseModel):
    is_global_Card: Optional[bool] = None
    card_id: Optional[int] = None
    asset_id: Optional[int] = None
    text_query: Optional[str] = None

class SlaBreakdownFilter(enum.Enum):
    ANY = "ANY"
    REMEDIATED = "REMEDIATED"
    NON_REMEDIATED = "NON_REMEDIATED"

class Timeframe(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    start_date: datetime
    end_date: datetime

class GetCardRequest(BaseModel):
    trend_timeframe: Timeframe = None
    sla_efficiency_timeframe: Timeframe = None
    sla_breakdown_filter: SlaBreakdownFilter = SlaBreakdownFilter.ANY
    include_trend_events: bool = False

class GetCardByIdFilter(BaseModel):
    id: str
    get_card_request: GetCardRequest = None

class IndustryBenchmark(BaseModel):
    industry_id: int
    ces_score: CESScore = None

class ScoreBenchmark(BaseModel):
    industry_benchmark: IndustryBenchmark
    population_benchmark: CESScore = None

class AssetRiskBreakdown(BaseModel):
    critical: float = None
    high: float = None
    medium_low: float = None

class CesTrendMetricDataPoint(BaseModel):
    date: datetime
    ces_score: CESScore = None

class ScoreTrendEventDetailDescription(BaseModel):
    rank: int
    change_title: str
    change_label: str
    value_before: str
    value_after: str

class ScoreTrendEventDetail(BaseModel):
    affected_points: int
    risk_categories: List[DataCategory]
    exposure_classes: List[ExposureClass]
    description: ScoreTrendEventDetailDescription

class ScoreTrendEvent(BaseModel):
    timestamp: datetime
    description: str
    event_detail: List[ScoreTrendEventDetail]
    executive_summary: str = None

class ScoreTrendMetric(BaseModel):
    ces_trend: List[CesTrendMetricDataPoint]
    target_score: int = None
    events: List[ScoreTrendEvent] = None

class SeveritySummaryStat(BaseModel):
    sla_severity_level: SlaSeverityLevel
    sla_inside_count: int
    sla_total_count: int
    sla_efficiency: float
    sla_efficiency_target: float



class RiskBreakdownCategory(BaseModel):
    number_of_risks: int
    percentage_of_total: float

class SlaOverallRiskBreakdown(BaseModel):
    risk_inside_sla: RiskBreakdownCategory
    risks_outside_sla: RiskBreakdownCategory

class SlaBreakdownRiskDistributionInDays(BaseModel):
    inside_sla: int = None
    outside_sla: int = None

class BusinessContextExposureClassDistribution(BaseModel):
    exposure_class: ExposureClass
    contribution_percentage: float

class SlaBreakdownTag(BaseModel):
    id: str
    name: str


class SlaBreakdown(BaseModel):
    risk_distribution: SlaOverallRiskBreakdown = None
    risk_distribution_in_days: SlaBreakdownRiskDistributionInDays = None
    exposure_category_breakdown: List[BusinessContextExposureClassDistribution] = None
    top_affecting_tags: List[SlaBreakdownTag] = None


class ExposureClassesDetails(BaseModel):
    score_benchmark: ScoreBenchmark = None
    asset_risk_breakdown: AssetRiskBreakdown = None
    score_trend_metric: ScoreTrendMetric = None
    sla_efficiency: List[SeveritySummaryStat] = None
    sla_breakdown: SlaBreakdown = None


class CardDetails(Card):
    exposure_classes_details: dict[ExposureClass, ExposureClassesDetails] = None


class GetCardByIdResponse(BaseModel):
    card_details: CardDetails





