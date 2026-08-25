import uuid

from sqlalchemy import Column, String, Text, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    pet_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    event_date = Column(Date, nullable=False)

    event_type = Column(String, nullable=False)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    status = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )