import os
import uuid
from datetime import date
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.models.timeline_event import TimelineEvent
from app.services.ai_services import analyze_health_document


router = APIRouter(
    prefix="/pets/{pet_id}/documents",
    tags=["Documents"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_document(
    pet_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # ---------------------------------------------------------
    # 1. Validate file
    # ---------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    # ---------------------------------------------------------
    # 2. Save uploaded file
    # ---------------------------------------------------------

    file_extension = Path(file.filename).suffix

    stored_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / stored_filename

    try:
        contents = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    # ---------------------------------------------------------
    # 3. Create Document database record
    # ---------------------------------------------------------

    document = Document(
        id=uuid.uuid4(),
        pet_id=pet_id,
        file_name=file.filename,
        file_path=str(file_path),
        document_type=file.content_type,
        processing_status="uploaded"
    )

    db.add(document)

    try:
        db.commit()
        db.refresh(document)

    except Exception as e:
        db.rollback()

        # Delete uploaded file if DB operation fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save document record: {str(e)}"
        )

    # ---------------------------------------------------------
    # 4. Analyze document using Gemini
    # ---------------------------------------------------------

    try:

        ai_result = analyze_health_document(
            str(file_path),
            file.content_type
        )

        print("\n========== GEMINI RESPONSE ==========")
        print(ai_result)
        print("=====================================\n")

    except Exception as e:

        print("AI processing failed:", str(e))

        document.processing_status = "failed"

        db.commit()

        return {
            "message": "Document uploaded but AI processing failed",
            "document_id": str(document.id),
            "pet_id": str(pet_id),
            "file_name": file.filename,
            "ai_result": {}
        }

    # ---------------------------------------------------------
    # 5. Save AI-generated timeline events
    # ---------------------------------------------------------

    events = ai_result.get("events", [])

    saved_events = []

    for event in events:

        try:

            event_date = date.fromisoformat(
                event["date"]
            )

            timeline_event = TimelineEvent(
                id=uuid.uuid4(),

                pet_id=pet_id,

                event_date=event_date,

                event_type=event.get(
                    "type",
                    "other"
                ),

                title=event.get(
                    "title",
                    "Health Event"
                ),

                description=event.get(
                    "description"
                ),

                status=event.get(
                    "status"
                )
            )

            db.add(timeline_event)

            saved_events.append(timeline_event)

        except Exception as e:

            print(
                "Failed to save timeline event:",
                event,
                str(e)
            )

    # ---------------------------------------------------------
    # 6. Update document processing status
    # ---------------------------------------------------------

    document.processing_status = "processed"

    try:

        db.commit()

        print("\n========== TIMELINE DEBUG ==========")

        saved = (
            db.query(TimelineEvent)
            .filter(TimelineEvent.pet_id == pet_id)
            .all()
        )

        print("Pet ID:", pet_id)
        print("Events found in DB:", len(saved))

        for e in saved:
            print(
                e.id,
                e.pet_id,
                e.event_date,
                e.event_type,
                e.title
            )

        print("====================================\n")
        db.refresh(document)

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save AI results: {str(e)}"
        )

    # ---------------------------------------------------------
    # 7. Return response
    # ---------------------------------------------------------

    return {
        "message": "Document processed successfully",

        "document_id": str(document.id),

        "pet_id": str(pet_id),

        "file_name": file.filename,

        "events_saved": len(saved_events),

        "ai_result": ai_result
    }