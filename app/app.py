from datetime import datetime

from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import sessionmaker

from database import prepare_db, engine, Document, DB_URL
from schemas import DocumentScheme

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
    try:
        resp = es.index(index="doc-index", id=new_document.doc_id, document=new_doc_to_es)
        s.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="ElasticSearch server is not available. Did not add anything")
    print(resp)
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
    try:
        resp = es.delete(index="doc-index", id=doc_id)
        s.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="ElasticSearch server is not available. Did not delete anything")
    print(resp)
    return {'deleted': doc_id}
