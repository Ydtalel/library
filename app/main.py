from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "DB OK!"}
