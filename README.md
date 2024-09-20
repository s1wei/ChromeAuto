# ChromeAuto
ChromeAuto 是一个使用 Python 编写的Web自动化工具包(爬虫框架)，基于 Chrome DevTools 协议，可用于控制和操作 Google Chrome 浏览器。它允许您以编程方式启动浏览器、管理标签页、执行 JavaScript 代码或浏览器等操作。

## 更新日期
2024年09月20日

## 许可证
[GPL-3.0 license](https://github.com/s1wei/ChromeAuto/blob/main/LICENSE)

## 特性

1. 精细控制浏览器实例：通过自定义配置来启动和管理 Chrome 浏览器实例。
2. 通过 JavaScript 执行用户操作：模拟真实用户行为，通过 JavaScript 执行点击、滚动等操作，提高自动化任务的隐蔽性。
3. 无需WebDriver驱动，有效越过防爬机制检测

## 目录结构

	•	ChromeAuto/
	•	├── __init__.py  初始化模块，导入必要的类。
	•	├── comment.py   包含 Tab 类，用于表示浏览器标签页。
	•	├── initiate.py  核心模块，包含 ChromeInit 类，实现主要功能。
	•	├── manner.py    预留模块，可用于添加通过执行 JavaScript 实现的其他功能。


## 安装
您可以使用以下命令从源码安装 ChromeAuto：
````
git clone https://github.com/yourusername/ChromeAuto.git
cd ChromeAuto
pip install -r requirements.txt
````
请注意，还需要下载最新版谷歌浏览器： https://chrome.google.com

快速开始
````
import os
import ChromeAuto

# 示例调用
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
    
````

## 开发文档

### 依赖项

* Python 3.6+
* requests：用于 HTTP 请求。
* websockets：用于 WebSocket 通信。
* asyncio：用于异步编程。

### API

待完善

## 注意事项
* Chrome 可执行路径：请确保 chrome_path 指向正确的 Chrome 可执行文件路径。
* 端口冲突：remote_port 应选择未被占用的端口，避免冲突。
* 依赖库：请确保已安装所有依赖库，特别是 requests 和 websockets。
* 权限：在保存截图或缓存文件时，确保程序有足够的文件系统权限。

## 贡献
欢迎提交问题和请求。您可以通过以下方式参与项目：
* 提交问题（Issue）
* 提交拉取请求（Pull Request）
* 改进文档

## 联系
![image](https://github.com/user-attachments/assets/d92c1a05-338c-4dbc-923c-e5587fffb5e5)


