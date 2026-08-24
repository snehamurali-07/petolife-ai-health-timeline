from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.pets import router as pets_router
from app.api import documents

from app.db.database import Base, engine
from app.models import Pet, Document

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PetOlife AI Health Timeline API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pets_router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {
        "message": "PetOlife AI Health Timeline API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }