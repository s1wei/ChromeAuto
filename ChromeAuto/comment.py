#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 
"""


class Tab:
    def __init__(self, port, tab_id, title="", ws_url=None):
        self.port = port
        self.tab_id = tab_id
        self.title = title
        self.ws_url = ws_url

    def __repr__(self):
        return f"<Tab Port: {self.port}, Tab ID: {self.tab_id}, Title: {self.title}>"
