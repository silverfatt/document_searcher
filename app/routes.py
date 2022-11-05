from elasticsearch import Elasticsearch
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker

from app.database import db_engine
from app.operations import add_doc, delete_doc, search_doc
from app.schemas import DocumentScheme

router = APIRouter()
es = Elasticsearch(hosts=['http://localhost:9200'])
session = sessionmaker(bind=db_engine)
s = session()


@router.get("/")
async def ping():
    return {"message": "hello"}


@router.post("/add")
async def add_document(document: DocumentScheme):
    """
    Add a new document do database
    """
    new_document = add_doc(s, es, document)
    return {'id': new_document.doc_id, 'rubrics': new_document.rubrics, 'text': new_document.text,
            'created_date': new_document.created_date}


@router.delete("/delete")
async def delete_document(doc_id: int):
    """
    Delete a document from database
    """
    delete_doc(s, es, doc_id)
    return {'deleted': doc_id}


@router.get("/search")
async def search_document(pattern_text: str):
    """
    Find first 20 documents with pattern_text's entries
    """
    objects = search_doc(s, es, pattern_text)
    return {'result': objects}
