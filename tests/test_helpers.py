from app.helpers import make_query


class TestMakeQuery:
    def test_make_query_correct(self, correct_query):
        assert make_query('string') == correct_query

    def test_make_query_incorrect(self, incorrect_query):
        assert make_query('string') != incorrect_query
