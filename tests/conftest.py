from datetime import datetime

import pytest

from app.database import Document


@pytest.fixture()
def correct_query():
    query = {'query': {
        'match': {
            'text': {
                'query': 'string',
                'minimum_should_match': 1
            }
        }
    }
    }
    return query


@pytest.fixture()
def incorrect_query():
    query = {'query': {
        'match': {
            'text': {
                'query': 1,
                'minimum_should_match': 'string'
            }
        }
    }
    }
    return query


@pytest.fixture()
def simple_document():
    doc = Document(doc_id=1, text='1!!%%&&test%%&&!!1', rubrics=['comedy'], created_date=datetime(2020, 1, 1))
    return doc


@pytest.fixture()
def simple_document_for_search():
    doc = Document(doc_id=1, text='1!!%%&&search test%%&&!!1', rubrics=['comedy'], created_date=datetime(2020, 1, 1))
    return doc


@pytest.fixture()
def simple_document_scheme():
    doc = {
        "rubrics": [
            "string"
        ],
        "text": "1!!%%&&test%%&&!!1"
    }
    return doc


@pytest.fixture()
def simple_document_scheme_for_search():
    doc = {
        "rubrics": [
            "string"
        ],
        "text": "???search???"
    }
    return doc
