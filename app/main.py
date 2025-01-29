from fastapi import FastAPI
from app.routers import artists

# Initialize FastAPI app
app = FastAPI(title="Aritmetica Network API", version="1.0.0")

# Include routers
app.include_router(artists.router)