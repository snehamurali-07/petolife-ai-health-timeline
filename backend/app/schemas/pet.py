from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PetCreate(BaseModel):
    name: str
    species: str
    breed: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    current_weight: float | None = None


class PetResponse(PetCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)