from datetime import datetime
from typing import Dict, Union

import elastic_transport
import elasticsearch
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database import Document
from app.helpers import make_query
from app.schemas import DocumentScheme


def add_doc(s: Session, es: elasticsearch.Elasticsearch, document: DocumentScheme) -> Document:
    """
    Creates new document in database and elasticsearch index
    """
    new_document = Document(rubrics=document.rubrics, text=document.text, created_date=datetime.now())
    s.add(new_document)
    s.commit()
    new_doc_to_es = {
        'text': new_document.text
    }
    try:
        es.index(index="doc-index", id=new_document.doc_id, document=new_doc_to_es)
    except (elastic_transport.ConnectionError, elastic_transport.ConnectionTimeout):
        s.delete(new_document)
        s.commit()
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to connect to search engine")
    return new_document


def delete_doc(s: Session, es: elasticsearch.Elasticsearch, doc_id: int) -> None:
    """
    Deletes document from database and elasticsearch index
    """
    document_to_delete = s.query(Document).filter(Document.doc_id == doc_id).first()
    if not document_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document does not exist")
    try:
        es.delete(index="doc-index", id=doc_id)
        s.delete(document_to_delete)
        s.commit()
    except (elastic_transport.ConnectionError, elastic_transport.ConnectionTimeout):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to connect to search engine")


def search_doc(s: Session, es: elasticsearch.Elasticsearch, pattern_text: str) -> Dict[str, Union[str, int]]:
    """
    Searches for pattern_text's entries in index and returns all rows from database for found items
    """
    try:
        resp = es.search(index="doc-index", body=make_query(pattern_text), size=20)
        ids = [int(x['_id']) for x in resp['hits']['hits']]
        objects = s.query(Document).filter(Document.doc_id.in_(ids)).order_by(Document.created_date.desc()).all()
    except (elastic_transport.ConnectionError, elastic_transport.ConnectionTimeout):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to connect to search engine")
    except elasticsearch.NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Index does not exist. Create some documents firstly")
    return objects
