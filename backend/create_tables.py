from app.db.database import engine, Base

# Import models so SQLAlchemy registers them
from app.models.pet import Pet
from app.models.document import Document
from app.models.health_event import HealthEvent


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done!")