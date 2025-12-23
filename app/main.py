# app/main.py
from fastapi import FastAPI

app = FastAPI(title="Kitap Çeşmesi")

@app.get("/")
def root():
    return {"message": "Kitap Çeşmesi API is running"}
