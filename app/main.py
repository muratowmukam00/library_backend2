# app/main.py

from app.routers.auth import router as auth_router
from app.routers.author import router as author_router
from app.routers.book import router as book_router
from app.routers.category import router as category_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Kitap Çeşmesi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Kitap Çeşmesi API is running"}

app.include_router(auth_router,prefix="/auth", tags=["Auth"])
app.include_router(author_router,prefix="/admin/authors", tags=["Author"])
app.include_router(category_router,prefix="/admin/category", tags=["Category"])
app.include_router(book_router,prefix="/admin/books", tags=["Book"])

