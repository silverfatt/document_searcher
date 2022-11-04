from datetime import datetime

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from database import prepare_db, engine, Document, DB_URL
from schemas import DocumentScheme

app = FastAPI()
try:
    prepare_db()
except Exception:
    print("Wrong database info. Check DB_USER, DB_PASSWORD, DB_NAME and DB_HOST variables.")
    print(f"Current URL:{DB_URL}")
    exit(1)

session = sessionmaker(bind=engine)
s = session()


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/add")
async def add_document(document: DocumentScheme):
    """
    Add new document do database
    """
    new_document = Document(rubrics=document.rubrics, text=document.text, created_date=datetime.now())
    s.add(new_document)
    s.commit()
    return {'rubrics': new_document.rubrics, 'text': new_document.text, 'created_date': new_document.created_date}


@app.delete("/delete")
async def delete_document(doc_id: int):
    """
    Delete document from database
    """
    document_to_delete = s.query(Document).filter(Document.doc_id == doc_id).first()
    if not document_to_delete:
        return {'not exists': doc_id}
    s.delete(document_to_delete)
    s.commit()
    return {'deleted': doc_id}
