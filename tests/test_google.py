from seletrans.api import *


DEBUG = True


def test_google_en_word():
    with Google(DEBUG) as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ['书', '预约', '书籍']
        assert res.dict_result == [
            {
                "type": "noun",
                "means": [
                    "书",
                    "簿",
                    "著作",
                    "册",
                    "书本",
                    "本子",
                    "卷",
                    "籍",
                    "册子",
                    "编",
                    "簿子",
                    "著",
                ],
            },
            {"type": "verb", "means": ["定"]},
        ]


def test_google_en_sentence():
    with Google(DEBUG) as ts:
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书是我们的朋友", "书籍是我们的朋友"]
        assert res.dict_result == []


def test_google_zh_word():
    with Google(DEBUG) as ts:
        res = ts.query("书", source="zh-CN", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["Book", "Write", "the book", "books"]
        assert res.dict_result == [
            {
                "type": "noun",
                "means": ["book", "letter", "script", "style of calligraphy"],
            },
            {"type": "verb", "means": ["write"]},
        ]


def test_google_zh_sentence():
    with Google(DEBUG) as ts:
        res = ts.query("书籍是我们的朋友", source="zh-CN", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["Books are our friends", "Books Are Our Friends"]
        assert res.dict_result == []
