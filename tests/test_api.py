from seletrans.api import *


DEBUG = True
WORD = "book"
SENTENSE = "book is our friend"


def test_baidu():
    with Baidu(DEBUG) as ts:
        res = ts.query(WORD)
        print(res.result)
        assert res.result == "书"
        res = ts.query(SENTENSE)
        print(res.result)
        assert res.result == "书是我们的朋友"


def test_deepl():
    with DeepL(DEBUG) as ts:
        res = ts.query(WORD)
        print(res.result)
        assert "书" in res.result
        print(res.dict_result)
        assert "书" in res.dict_result
        res = ts.query(SENTENSE)
        print(res.result)
        assert "书是我们的朋友" in res.result
        print(res.dict_result)
        assert res.dict_result == ""
