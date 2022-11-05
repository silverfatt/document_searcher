import time

import pytest
from elasticsearch import Elasticsearch
from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker

from app.database import Base, db_engine
from app.operations import add_doc, delete_doc, search_doc

Base.metadata.create_all(db_engine)
session = sessionmaker(bind=db_engine)
s = session()
es = Elasticsearch(['http://localhost:9200'])


def test_add_doc(simple_document):
    added_doc = add_doc(s, es, simple_document)
    assert added_doc.text == simple_document.text
    assert added_doc.rubrics == simple_document.rubrics
    delete_doc(s, es, added_doc.doc_id)


def test_delete_doc():
    with pytest.raises(HTTPException):
        delete_doc(s, es, -1)


def test_search_doc(simple_document_for_search):
    added_doc = add_doc(s, es, simple_document_for_search)
    time.sleep(2)
    assert search_doc(s, es, added_doc.text)[0].doc_id == [added_doc][0].doc_id
    delete_doc(s, es, added_doc.doc_id)
