from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.timeline_event import TimelineEvent


router = APIRouter(
    prefix="/pets",
    tags=["Timeline"]
)


@router.get("/{pet_id}/timeline")
def get_timeline(
    pet_id: UUID,
    db: Session = Depends(get_db)
):
    events = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.pet_id == pet_id)
        .order_by(TimelineEvent.event_date.desc())
        .all()
    )

    return [
        {
            "id": str(event.id),
            "pet_id": str(event.pet_id),
            "date": event.event_date.isoformat(),
            "type": event.event_type,
            "title": event.title,
            "description": event.description,
            "status": event.status
        }
        for event in events
    ]