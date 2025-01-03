from fastapi import FastAPI
from app.routers import auth, admin, movies
from app.database import Base, engine
from app.config import load_clients
import json
from app.logging_config import setup_logging
import logging
from pdbwhereami import whereami

setup_logging()

# Define the FastAPI app instance at the module level
app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
whereami()
app.include_router(admin.router)
whereami()
app.include_router(movies.router)
whereami()

# Load client configurations
CONFIG_FILE = "app/config/clients.json"
clients = load_clients(CONFIG_FILE)

# Optional: Define a startup event to log clients or other initialization tasks
@app.on_event("startup")
async def startup_event():
    print(f"Loaded clients: {clients}")

logging.debug("Debugging initialized")