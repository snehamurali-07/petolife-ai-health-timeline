import uuid

from sqlalchemy import Column, String, Date, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    current_weight = Column(Numeric, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )