from seletrans.api import *


DEBUG = True


def test_baidu():
    with Baidu(DEBUG) as ts:
        res = ts.query("book", target="zh")
        print(res.result)
        print(res.dict_result)
        # assert res.result == "书"
        res = ts.query("Books are our friends", target="zh")
        print(res.result)
        print(res.dict_result)
        # assert res.result == "书籍是我们的朋友"
        res = ts.query("书", target="en")
        print(res.result)
        print(res.dict_result)
        # assert res.result == "book"
        res = ts.query("书籍是我们的朋友", target="en")
        print(res.result)
        print(res.dict_result)
        # assert res.result == "Books are our friends"


def test_deepl():
    with DeepL(DEBUG) as ts:
        res = ts.query("book", target="zh")
        print(res.result)
        print(res.dict_result)
        # assert "书" in res.result
        # assert "书" in res.dict_result
        res = ts.query("Books are our friends", target="zh")
        print(res.result)
        print(res.dict_result)
        # assert "书是我们的朋友" in res.result
        # assert res.dict_result == ""
        res = ts.query("书", source="zh", target="en-US")
        print(res.result)
        print(res.dict_result)
        # assert res.result == "book"
        res = ts.query("书是我们的朋友", source="zh", target="en-US")
        print(res.result)
        print(res.dict_result)
        # assert res.result == "Books are our friends"
