from fastapi import FastAPI
from app.routers import auth, books, authors, readers, rents

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(readers.router, prefix="/readers", tags=["Readers"])
app.include_router(rents.router, prefix="/rents", tags=["Rents"])
