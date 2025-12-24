# app/main.py

from app.routers.auth import router as auth_router

from fastapi import FastAPI

app = FastAPI(title="Kitap Çeşmesi")

@app.get("/")
def root():
    return {"message": "Kitap Çeşmesi API is running"}

app.include_router(auth_router,prefix="/auth", tags=["Auth"])
