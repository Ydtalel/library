from fastapi import FastAPI, Depends
from app.routers import auth, books, authors, readers

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(readers.router, prefix="/readers", tags=["Readers"])


@app.get("/")
async def root():
    return {"message": "DB OK!"}
