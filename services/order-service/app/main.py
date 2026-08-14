from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.service_name)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.service_name,
        "environment": settings.environment,
    }

@app.get("/")
def root():
    return {"message": f"{settings.service_name} is running"}