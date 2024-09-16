#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 

@Time    : 2024/8/2 下午5:18
@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : comment.py.py
@IDE     : PyCharm
"""


class Tab:
    def __init__(self, port, tab_id, title="", ws_url=None):
        self.port = port
        self.tab_id = tab_id
        self.title = title
        self.ws_url = ws_url

    def __repr__(self):
        return f"<Tab Port: {self.port}, Tab ID: {self.tab_id}, Title: {self.title}>"
