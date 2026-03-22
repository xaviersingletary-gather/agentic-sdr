from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
import enum
from src.models.base import Base


class Channel(str, enum.Enum):
    linkedin = "LinkedIn"
    email = "email"
    phone_flag = "phone_flag"


class OutreachStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    opened = "opened"
    replied = "replied"
    bounced = "bounced"


SEQUENCE_DAYS = [0, 3, 7, 14, 30]


class Outreach(Base):
    __tablename__ = "outreach"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey("contacts.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    template_id: Mapped[str | None] = mapped_column(String)
    message_content: Mapped[str | None] = mapped_column(Text)
    sequence_day: Mapped[int] = mapped_column(Integer, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default=OutreachStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
