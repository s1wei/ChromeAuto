import os
import ChromeAuto

# 示例调用
try:
    remote_port = 9333
    chrome1 = ChromeAuto.ChromeInit(
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
            "window_size": (800, 600),  # 窗口宽度、高度
            "window_position": (0, 0)  # 窗口位置x、y
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

