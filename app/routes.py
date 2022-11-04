from datetime import datetime

from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker

from app.database import engine, Document
from app.helpers import make_query
from app.schemas import DocumentScheme

router = APIRouter()
es = Elasticsearch(hosts=['http://localhost:9200'])

session = sessionmaker(bind=engine)
s = session()


@router.get("/")
async def ping():
    return {"message": "hello"}


@router.post("/add")
async def add_document(document: DocumentScheme):
    """
    Add a new document do database
    """
    new_document = Document(rubrics=document.rubrics, text=document.text, created_date=datetime.now())
    s.add(new_document)
    s.commit()
    new_doc_to_es = {
        'text': new_document.text
    }
    try:
        resp = es.index(index="doc-index", id=new_document.doc_id, document=new_doc_to_es)
    except Exception:
        s.delete(new_document)
        s.commit()
        raise HTTPException(status_code=404, detail="Disconnected from ES")
    return {'id': new_document.doc_id, 'rubrics': new_document.rubrics, 'text': new_document.text,
            'created_date': new_document.created_date}


@router.delete("/delete")
async def delete_document(doc_id: int):
    """
    Delete a document from database
    """
    document_to_delete = s.query(Document).filter(Document.doc_id == doc_id).first()
    if not document_to_delete:
        return {'not exists': doc_id}
    s.delete(document_to_delete)
    s.commit()
    resp = es.delete(index="doc-index", id=doc_id)
    return {'deleted': doc_id}


@router.get("/search")
async def search_document(pattern_text: str):
    """
    Find first 20 documents with pattern_text's entries
    """
    resp = es.search(index="doc-index", body=make_query(pattern_text), size=20)
    return resp
