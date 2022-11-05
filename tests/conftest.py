import pytest

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
