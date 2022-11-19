from seletrans.api import *


def test_seletrans_bing():
    with Seletrans("bing")() as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书"]
        assert res.dict_result == [
            {"type": "NOUN", "means": ["书", "本 书", "图书", "簿", "书籍", "书本", "本", "读书"]},
            {"type": "VERB", "means": ["预订", "预定", "订"]},
        ]

        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书籍是我们的朋友"]
        assert res.dict_result == []


def test_seletrans_baidu():
    with Seletrans("baidu")() as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书"]
        assert res.dict_result == [
            {
                "type": "n.",
                "means": [
                    "书，书籍",
                    "著作，印刷（或电子）出版物",
                    "本子，簿子",
                    "成册（成套）的东西",
                    "账簿，账目，会计簿",
                    "（长篇作品的）篇，卷，部",
                    "（顾客或雇员）名册",
                    "赌注记录",
                ],
            },
            {"type": "v.", "means": ["预订，预约", "（警方）把...记录在案", "记名警告（犯规运动员）"]},
        ]

        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书是我们的朋友"]
        assert res.dict_result == []


def test_seletrans_google():
    with Seletrans("google")() as ts:
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

        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书是我们的朋友", "书籍是我们的朋友"]
        assert res.dict_result == []


def test_seletrans_deepl():
    with Seletrans("deepl")() as ts:
        res = ts.query("book")
        print(res.result)
        print(res.dict_result)
        res.play_sound()

        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
