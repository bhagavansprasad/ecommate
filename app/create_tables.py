from app.database import Base, engine
from app.models import User  # Ensure you import all models here

# Recreate all tables
print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
