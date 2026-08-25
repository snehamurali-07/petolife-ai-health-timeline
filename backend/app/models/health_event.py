import uuid

from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class HealthEvent(Base):
    __tablename__ = "health_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    pet_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pets.id"),
        nullable=False
    )

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=True
    )

    event_date = Column(Date, nullable=True)

    event_type = Column(String, nullable=False)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    status = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )