from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from src.models.base import Base


class Industry(str, enum.Enum):
    manufacturing = "Manufacturing"
    food_bev = "Food_Bev"
    healthcare_pharma = "Healthcare_Pharma"
    retail = "Retail"
    logistics = "Logistics"


class AccountStatus(str, enum.Enum):
    researching = "researching"
    qualified = "qualified"
    disqualified = "disqualified"
    in_outreach = "in_outreach"
    meeting_booked = "meeting_booked"
    dormant = "dormant"


class ExclusionReason(str, enum.Enum):
    customer = "customer"
    target = "target"
    strategic = "strategic"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    domain: Mapped[str | None] = mapped_column(String)
    industry: Mapped[str | None] = mapped_column(String)
    annual_revenue: Mapped[float | None] = mapped_column(Float)
    facility_count: Mapped[int | None] = mapped_column(Integer)
    hq_country: Mapped[str | None] = mapped_column(String)
    wms_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    automation_footprint: Mapped[bool] = mapped_column(Boolean, default=False)
    icp_score: Mapped[float] = mapped_column(Float, default=0.0)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String, default=AccountStatus.researching)
    exclusion_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    disqualification_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_activity_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
