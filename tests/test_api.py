from seletrans.api import *


DEBUG = True


def test_baidu():
    with Baidu(DEBUG) as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "书"
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "书籍是我们的朋友"
        res = ts.query("书", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "book"
        res = ts.query("书籍是我们的朋友", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "Books are our friends"


def test_deepl():
    with DeepL(DEBUG) as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert "书" in res.result
        # assert "书" in res.dict_result
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert "书籍是我们的朋友" in res.result
        # assert res.dict_result == ""
        res = ts.query("书", source="zh", target="en-US")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "book"
        res = ts.query("书籍是我们的朋友", source="zh", target="en-US")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "Books are our friends"


def test_google():
    with Google(DEBUG) as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert "书" in res.result
        # assert "书" in res.dict_result
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert "书是我们的朋友" in res.result
        # assert res.dict_result == ""
        res = ts.query("书", source="zh-CN", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "book"
        res = ts.query("书籍是我们的朋友", source="zh-CN", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "Books are our friends"


def test_bing():
    with Bing(DEBUG) as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert "书" in res.result
        # assert "书" in res.dict_result
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert "书是我们的朋友" in res.result
        # assert res.dict_result == ""
        res = ts.query("书", source="zh-Hans", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "book"
        res = ts.query("书籍是我们的朋友", source="zh-Hans", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        # assert res.result == "Books are our friends"


def test_seletrans():
    with Seletrans("bing")() as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
