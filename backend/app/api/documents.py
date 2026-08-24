import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.pet import Pet
from app.models.document import Document

from app.services.ocr_service import extract_text_from_image

router = APIRouter(
    prefix="/pets",
    tags=["Documents"]
)


UPLOAD_DIR = "uploads"


os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{pet_id}/documents/")
async def upload_document(
    pet_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Check that pet exists
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    # 2. Validate file type
    allowed_types = {
        "application/pdf",
        "image/jpeg",
        "image/png"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG and PNG files are supported"
        )

    # 3. Generate unique filename
    extension = os.path.splitext(file.filename)[1]

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # 4. Save file
    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Extract text from image
    extracted_text = ""

    if file.content_type in {
        "image/jpeg",
        "image/png"
    }:
        extracted_text = extract_text_from_image(file_path)
    # 5. Save document information in database
    document = Document(
        pet_id=pet_id,
        file_name=file.filename,
        file_path=file_path,
        document_type=file.content_type,
        processing_status="uploaded"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
    "message": "Document uploaded successfully",
    "document_id": str(document.id),
    "pet_id": str(pet_id),
    "file_name": document.file_name,
    "status": document.processing_status,
    "extracted_text": extracted_text
}