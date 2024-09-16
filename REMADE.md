
# ChromeAuto

ChromeAuto 是一个使用 Python 编写的自动化工具包，基于 Chrome DevTools 协议，可用于控制和操作 Google Chrome 浏览器。它允许您以编程方式启动浏览器、管理标签页、执行 JavaScript 代码或浏览器等操作。

## 特性

1. 精细控制浏览器实例：通过自定义配置来启动和管理 Chrome 浏览器实例。
2. 通过 JavaScript 执行用户操作：模拟真实用户行为，通过 JavaScript 执行点击、滚动等操作，提高自动化任务的隐蔽性。

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

快速开始
````
import os
import ChromeAuto

# 示例调用
try:
    remote_port = 9333
    chrome1 = ChromeAuto.ChromeInit(
        remote_port=remote_port,
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        cache_dir=os.path.join(f"ChromeData/{remote_port}"),
        clear_cache=False,
        cache_template=os.path.join(f"ChromeData/{remote_port}"),
        command_line={
            "proxy": "",  # 代理地址
            "user_agent": "",  # UserAgent 标识
            "maximize": False,  # 启动时最大化
            "ignore_certificate_errors": False,  # 忽视证书错误
            "check_default_browser": False,  # 检查默认浏览器
            "skip_first_run": True,  # 跳过首次运行
            "no_referer": True,  # 不发送 Http Referer 头
            "lang": "zh-CN",  # 设置语言
            "incognito": False,  # 无痕模式
            "disable_js": False,  # 禁用 JavaScript
            "window_size": (800, 600),  # 窗口宽度、高度
            "window_position": (0, 0)  # 窗口位置 x、y
        },
        home_url="https://www.denceun.cn",
        timeout=60,
        launch_mode=0
    )


    # 获取所有标签页信息
    current_all_tab = chrome1.getAllTabInfo()
    if current_all_tab:
        print(f"当前所有标签页信息: {current_all_tab}")

    # 新建标签页并导航到指定URL
    new_tab = chrome1.createNewTab("https://www.s1wei.com")
    if new_tab:
        print(f"新建标签页信息: {new_tab}")
    else:
        print("新建标签页失败")

    # 等待新标签页的页面加载完毕
    if new_tab:
        if chrome1.wait_until_page_loaded(tab=new_tab):
            print("页面已加载完毕。")
        else:
            print("页面加载超时或发生错误。")

    # 获取当前所有标签页信息（数组）
    current_all_tab = chrome1.getAllTabInfo()
    if current_all_tab:
        print(f"当前所有标签页信息: {current_all_tab}")

    # 在新建的标签页中执行 JavaScript 代码
    if new_tab:
        chrome1.RunJavaScript("alert('新标签页执行JS')", tab=new_tab)
    else:
        print("无法在新建的标签页中执行 JavaScript 代码，因为标签页创建失败。")

    # 切换回初始标签页
    init_tab = current_all_tab[0]
    if chrome1.switchToTab(init_tab) == 1:
        print(f"成功切换回初始标签页: {init_tab}")
    else:
        print("切换回初始标签页失败")

    # 在初始标签页中执行JavaScript代码
    if init_tab:
        chrome1.RunJavaScript("alert('初始标签页执行JS')", tab=init_tab)
    else:
        print("在一开始标签页中执行 JavaScript 代码。")

    # 关闭新建的标签页
    if init_tab and chrome1.closeTab(init_tab) == 1:
        print(f"成功关闭最初标签页: {init_tab}")
    else:
        print("关闭标签页失败")

    # 截取新标签页的截图并保存到指定目录
    if new_tab:
        chrome1.capture_screenshot(save_dir='./Picture', filename='s1wei.png', tab=new_tab)
    else:
        print("无法截取截图，因为标签页创建失败。")

    # 关闭整个浏览器
    chrome1.close()

except Exception as e:
    print(e)
    
````

## 开发文档

### 依赖项

* Python 3.6+
* requests：用于 HTTP 请求。
* websockets：用于 WebSocket 通信。
* asyncio：用于异步编程。
* json：用于处理 JSON 数据。

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

？？？
