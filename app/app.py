from fastapi import FastAPI

from database import prepare_db
from schemas import DocumentScheme

app = FastAPI()
prepare_db()

@app.get("/")
async def root():
    return {"message": "hello"}

@app.post("/add")
async def add_document(document: DocumentScheme):
    pass