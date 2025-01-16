from fastapi import FastAPI, Depends
from app.routers import auth, books, authors

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors.router, prefix="/authors", tags=["Authors"])


@app.get("/")
async def root():
    return {"message": "DB OK!"}
