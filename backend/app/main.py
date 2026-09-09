from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Email AI",
    description="AI-powered email assistant",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Email AI API is running"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }