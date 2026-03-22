from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
import enum
from src.models.base import Base


class SignalType(str, enum.Enum):
    job_posting = "job_posting"
    new_dc = "new_dc"
    wms_migration = "wms_migration"
    audit_failure = "audit_failure"
    exec_mandate = "exec_mandate"
    automation_adoption = "automation_adoption"


class SignalSource(str, enum.Enum):
    clay = "Clay"
    exa = "Exa"
    linkedin = "LinkedIn"
    news = "news"


SIGNAL_POINTS = {
    SignalType.job_posting: 25,
    SignalType.new_dc: 25,
    SignalType.wms_migration: 20,
    SignalType.audit_failure: 20,
    SignalType.automation_adoption: 10,
    SignalType.exec_mandate: 20,
}


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    signal_type: Mapped[str] = mapped_column(String, nullable=False)
    signal_source: Mapped[str] = mapped_column(String, nullable=False)
    signal_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    raw_content: Mapped[str | None] = mapped_column(Text)
    points_contributed: Mapped[float] = mapped_column(Float, default=0.0)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
