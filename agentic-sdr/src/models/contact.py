from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import enum
from src.models.base import Base


class PersonaType(str, enum.Enum):
    tdm = "TDM"
    odm = "ODM"
    financial_sponsor = "Financial_Sponsor"
    it = "IT"
    safety = "Safety"
    exec_sponsor = "Exec_Sponsor"


class OutreachStatus(str, enum.Enum):
    pending = "pending"
    enrolled = "enrolled"
    replied = "replied"
    bounced = "bounced"
    opted_out = "opted_out"


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)
    title: Mapped[str | None] = mapped_column(String)
    persona_type: Mapped[str | None] = mapped_column(String)
    linkedin_url: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    outreach_status: Mapped[str] = mapped_column(String, default=OutreachStatus.pending)
    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
