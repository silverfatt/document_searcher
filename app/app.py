from database import prepare_db, engine, Document, DB_URL
from datetime import datetime
from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException, status
from helpers import make_query
from schemas import DocumentScheme
from sqlalchemy.orm import sessionmaker

app = FastAPI()
es = Elasticsearch(hosts=['http://localhost:9200'])
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
    new_doc_to_es = {
        'text': new_document.text
    }
    s.commit()
    resp = es.index(index="doc-index", id=new_document.doc_id, document=new_doc_to_es)
    print(resp)
    return {'id': new_document.doc_id, 'rubrics': new_document.rubrics, 'text': new_document.text,
            'created_date': new_document.created_date}


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
    resp = es.delete(index="doc-index", id=doc_id)
    print(resp)
    return {'deleted': doc_id}


@app.get("/search")
async def search_document(pattern_text: str):
    """
    Find first 20 documents with pattern_text's entries
    """
    resp = es.search(index="doc-index", body=make_query(pattern_text), size=20)
    return resp
