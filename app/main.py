from fastapi import FastAPI
from app import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings  # Correctly load the Settings with env support

print("✅ Database Connected Successfully")

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to my API!"}
