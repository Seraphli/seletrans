from seletrans.api import *


DEBUG = True


def test_deepl_en_word():
    with DeepL(DEBUG) as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书"]
        assert res.dict_result == [
            {"type": "NOUN", "means": ["书", "本 书", "图书", "簿", "书籍", "书本", "本", "读书"]},
            {"type": "VERB", "means": ["预订", "预定", "订"]},
        ]


def test_deepl_en_sentence():
    with DeepL(DEBUG) as ts:
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书籍是我们的朋友"]
        assert res.dict_result == []


def test_deepl_zh_word():
    with DeepL(DEBUG) as ts:
        res = ts.query("书", source="zh", target="en-US")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["book"]
        assert res.dict_result == [{"type": "NOUN", "means": ["book"]}]


def test_deepl_zh_sentence():
    with DeepL(DEBUG) as ts:
        res = ts.query("书籍是我们的朋友", source="zh", target="en-US")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["Books are our friends"]
        assert res.dict_result == []
