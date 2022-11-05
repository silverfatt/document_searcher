# from app.routes import add_document, delete_document, search_document
import time

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_add_document(simple_document, simple_document_scheme):
    response = client.post('/add', json=simple_document_scheme)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['text'] == simple_document.text
    client.delete(f'/delete?doc_id={response.json()["id"]}')


def test_delete_document(simple_document_scheme):
    response_after_add = client.post('/add', json=simple_document_scheme)
    response_after_delete = client.delete(f'/delete?doc_id={response_after_add.json()["id"]}')
    assert response_after_delete.json() == {'deleted': response_after_add.json()['id']}


def test_delete_document_not_exists(simple_document_scheme):
    response_after_delete = client.delete(f'/delete?doc_id=-1')
    assert response_after_delete.json() == {'detail': 'Document does not exist'}


def test_search_document(simple_document_scheme_for_search):
    response_after_add = client.post('/add', json=simple_document_scheme_for_search)
    time.sleep(2)
    response_after_search = client.get(f'/search?pattern_text={simple_document_scheme_for_search["text"]}')
    assert response_after_search.json() == {'result': [
        {'doc_id': response_after_add.json()['id'], 'rubrics': response_after_add.json()['rubrics'],
         'text': response_after_add.json()['text'],
         'created_date': response_after_add.json()['created_date']}]}
    client.delete(f'/delete?doc_id={response_after_add.json()["id"]}')
