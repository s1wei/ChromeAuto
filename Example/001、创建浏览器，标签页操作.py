#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 

@Time    : 2024/9/20 下午5:50
@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : 001、创建浏览器，标签页操作.py
@IDE     : PyCharm
"""

import os
import ChromeAuto

# 示例调用
try:
    remote_port = 9333
    chrome_example = ChromeAuto.ChromeInit(
        remote_port=remote_port,
        # windows使用这个路径：
        # chrome_path=os.path.join("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        cache_dir=os.path.join(f"ChromeData/{remote_port}"),
        clear_cache=False,
        cache_template=os.path.join(f"ChromeData/{remote_port}"),
        command_line={
            "proxy": "",  # 代理地址
            "user_agent": "",  # UserAgent标识
            "maximize": False,  # 启动时最大化
            "ignore_certificate_errors": False,  # 忽视证书错误
            "check_default_browser": False,  # 检查默认浏览器
            "skip_first_run": True,  # 跳过首次运行
            "no_referer": True,  # 不发送HttpReferer头
            "lang": "zh-CN",  # 设置语言
            "incognito": False,  # 无痕模式
            "disable_js": False,  # 禁用Javascript
            "window_size": (1200, 800),  # 窗口宽度、高度
            "window_position": (50, 50)  # 窗口位置x、y
        },
        home_url="https://www.denceun.cn",  # 默认启动页
        timeout=60,
        launch_mode=0
    )

    # 获取当前标签页信息
    one_tab = chrome_example.getTabInfo()
    # 等待标签页加载完毕
    chrome_example.wait_until_page_loaded(tab=one_tab, timeout=20)
    one_tab = chrome_example.getTabInfo()
    print(f"标签1:{one_tab}")

    # 新建标签页，并且跳转到 https://www.github.com/s1wei 地址
    new_tab = chrome_example.createNewTab("https://www.s1wei.com")
    two_tab = chrome_example.getTabInfo()
    # chrome_example.wait_until_page_loaded(tab=two_tab, timeout=20)
    print(f"标签2:{two_tab}")

    # 切换到第一页
    chrome_example.switchToTab(one_tab)
    chrome_example.RunJavaScript("alert('当前已切换到one_tab')", one_tab)

    # 获取所有标签并输出
    all_tab = chrome_example.getAllTabInfo()
    print(f"所有标签:{all_tab}")

    # 引用数组下标，切换到第二页
    chrome_example.switchToTab(all_tab[1])
    chrome_example.RunJavaScript("alert('当前已切换到two_tab')", two_tab)

    # 引用数组下标，关闭第一页
    chrome_example.closeTab(all_tab[0])
    chrome_example.RunJavaScript("alert('已关闭one_tab')", two_tab)

    # 关闭整个浏览器实例
    chrome_example.RunJavaScript("alert('接下来关闭整个浏览器实例')")
    chrome_example.close()

except Exception as e:
    print(e)
