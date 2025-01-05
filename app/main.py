from fastapi import FastAPI, Request
from app.routers import auth, movies
from app.database import Base, engine
from app.config import load_clients
import json
from app.logging_config import setup_logging
import logging
from pdbwhereami import whereami

setup_logging()

# Define the FastAPI app instance at the module level
app = FastAPI()

# Load client configurations
CONFIG_FILE = "app/config/clients.json"
clients = load_clients(CONFIG_FILE)

# Optional: Define a startup event to log clients or other initialization tasks
@app.on_event("startup")
async def startup_event():
    print(f"Loaded clients: {clients}")

# Include routers
app.include_router(auth.router)
app.include_router(movies.router)

logging.debug("Debugging initialized")