def make_query(pattern_text: str):
    """
    Creates query dictionary for ElasticSearch search() method
    """
    return {'query': {
        'match': {
            'text': {
                'query': pattern_text,
                'minimum_should_match': 1
            }
        }
    }
    }
