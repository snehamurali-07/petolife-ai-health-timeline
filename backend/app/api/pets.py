from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetResponse


router = APIRouter(
    prefix="/pets",
    tags=["Pets"]
)


@router.post("/", response_model=PetResponse)
def create_pet(
    pet_data: PetCreate,
    db: Session = Depends(get_db)
):
    pet = Pet(
        name=pet_data.name,
        species=pet_data.species,
        breed=pet_data.breed,
        date_of_birth=pet_data.date_of_birth,
        gender=pet_data.gender,
        current_weight=pet_data.current_weight
    )

    db.add(pet)
    db.commit()
    db.refresh(pet)

    return pet


@router.get("/", response_model=list[PetResponse])
def get_pets(
    db: Session = Depends(get_db)
):
    pets = db.query(Pet).all()
    return pets


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(
    pet_id: UUID,
    db: Session = Depends(get_db)
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return pet