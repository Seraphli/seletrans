from seletrans.api import *


DEBUG = True


def test_baidu_en_word():
    with Baidu(DEBUG) as ts:
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


def test_baidu_en_sentence():
    with Baidu(DEBUG) as ts:
        res = ts.query("Books are our friends")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["书是我们的朋友"]
        assert res.dict_result == []


def test_baidu_zh_word():
    with Baidu(DEBUG) as ts:
        res = ts.query("书", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["book"]
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
                "text": "book",
            },
            {
                "type": "n.",
                "means": [
                    "剧本",
                    "电影剧本",
                    "广播(或讲话等)稿",
                    "笔迹",
                    "(一种语言的)字母系统，字母表",
                    "笔试答卷",
                    "脚本（程序）（计算机的一系列指令）",
                ],
                "text": "script",
            },
            {
                "type": "n.",
                "means": ["信", "函", "字母", "(缝制在运动服上的)校运动队字母标志"],
                "text": "letter",
            },
            {
                "type": "v.",
                "means": [
                    "写",
                    "编写",
                    "写信",
                    "写作",
                    "写字",
                    "作曲",
                    "写道",
                    "开（支票等）",
                    "将（数据）写入（存储器）",
                    "好使",
                ],
                "text": "write",
            },
        ]


def test_baidu_zh_sentence():
    with Baidu(DEBUG) as ts:
        res = ts.query("书籍是我们的朋友", target="en")
        print(res.result)
        print(res.dict_result)
        res.play_sound()
        assert res.result == ["Books are our friends"]
        assert res.dict_result == []
