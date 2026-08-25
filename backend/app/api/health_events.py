from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.health_event import HealthEvent


router = APIRouter(
    prefix="/pets",
    tags=["Health Timeline"]
)


@router.get("/{pet_id}/timeline")
def get_pet_timeline(
    pet_id: UUID,
    db: Session = Depends(get_db)
):

    events = (
        db.query(HealthEvent)
        .filter(HealthEvent.pet_id == pet_id)
        .order_by(
            HealthEvent.event_date.desc()
        )
        .all()
    )

    return events