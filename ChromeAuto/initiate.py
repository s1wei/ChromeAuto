# !/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 
"""

import os
import shutil
import subprocess
import time
import socket
import asyncio
import websockets
import json
import requests
import base64

# 导入 Tab 类
from .comment import Tab

class ChromeInit:

    def __init__(self, remote_port=4555, chrome_path="", cache_dir="", clear_cache=False, cache_template="", command_line=None,
                 home_url="", timeout=60, launch_mode=0):
        self.remote_port = remote_port
        self.chrome_path = chrome_path
        if cache_dir == "":
            self.cache_dir = os.path.join(f"ChromeData/{remote_port}")
        else:
            self.cache_dir = cache_dir
        self.clear_cache = clear_cache
        if self.clear_cache and os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        if cache_template and self.clear_cache:
            shutil.copytree(cache_template, self.cache_dir)
        self.command_line = command_line if command_line else {}
        self.home_url = home_url
        self.timeout = timeout
        self.launch_mode = launch_mode
        self.ws_url = None
        self.browser_ws_url = None

        # 初始化并返回成功或失败
        if not self.initialize_chrome():
            raise Exception("初始化 Chrome 失败")

    def __repr__(self):
        try:
            return f"<Chrome Object at Port - ({self.remote_port})>"
        except:
            return f'<Chrome Object at {hex(id(self))} - (未连接)>'

    def is_port_open(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def initialize_chrome(self):
        if not self.is_port_open(self.remote_port):
            if self.chrome_path:
                chrome_command = [
                    self.chrome_path,
                    f"--remote-debugging-port={self.remote_port}",
                    f"--user-data-dir={self.cache_dir}"
                ]

                if self.home_url:
                    chrome_command.append(self.home_url)

                if self.command_line:
                    chrome_command += self.build_command_line()

                if self.launch_mode == 1:
                    chrome_command = ['runas', '/user:Administrator'] + chrome_command

                subprocess.Popen(chrome_command)
                start_time = time.time()
                while time.time() - start_time < self.timeout:
                    if self.is_port_open(self.remote_port):
                        break
                    time.sleep(1)
                else:
                    return False

        # 连接到 DevTools 协议
        try:
            self.ws_url = self.get_ws_url(self.remote_port)
            self.browser_ws_url = self.get_browser_ws_url(self.remote_port)
            return True
        except Exception as e:
            print(f"Error connecting to Chrome DevTools: {e}")
            return False

    def build_command_line(self):
        cmd_line = []
        if "proxy" in self.command_line:
            cmd_line.append(f"--proxy-server={self.command_line['proxy']}")
        if "user_agent" in self.command_line:
            cmd_line.append(f"--user-agent={self.command_line['user_agent']}")
        if "maximize" in self.command_line and self.command_line["maximize"]:
            cmd_line.append("--start-maximized")
        if "ignore_certificate_errors" in self.command_line and self.command_line["ignore_certificate_errors"]:
            cmd_line.append("--ignore-certificate-errors")
        if "check_default_browser" in self.command_line and not self.command_line["check_default_browser"]:
            cmd_line.append("--no-default-browser-check")
        if "skip_first_run" in self.command_line and self.command_line["skip_first_run"]:
            cmd_line.append("--no-first-run")
        if "no_referer" in self.command_line and self.command_line["no_referer"]:
            cmd_line.append("--no-referrers")
        if "lang" in self.command_line:
            cmd_line.append(f"--lang={self.command_line['lang']}")
        if "incognito" in self.command_line and self.command_line["incognito"]:
            cmd_line.append("--incognito")
        if "disable_js" in self.command_line and self.command_line["disable_js"]:
            cmd_line.append("--disable-javascript")
        if "window_size" in self.command_line:
            width, height = self.command_line["window_size"]
            cmd_line.append(f"--window-size={width},{height}")
        if "window_position" in self.command_line:
            x, y = self.command_line["window_position"]
            cmd_line.append(f"--window-position={x},{y}")

        cmd_line.append("--disable-popup-blocking")  # 允许弹出新窗口

        return cmd_line

    def get_ws_url(self, port):
        url = f"http://localhost:{port}/json"
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                return data[0]["webSocketDebuggerUrl"]
            except (requests.RequestException, KeyError, IndexError):
                time.sleep(1)
        raise Exception("Failed to get WebSocket URL from Chrome")

    def get_browser_ws_url(self, port):
        url = f"http://localhost:{port}/json/version"
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                return data["webSocketDebuggerUrl"]
            except (requests.RequestException, KeyError):
                time.sleep(1)
        raise Exception("Failed to get browser WebSocket URL from Chrome")

    async def send_command(self, websocket, method, params=None):
        if params is None:
            params = {}
        message = {
            "id": 1,
            "method": method,
            "params": params
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        return json.loads(response)

    def send_command_sync(self, method, params=None, ws_url=None):
        if params is None:
            params = {}
        if ws_url is None:
            ws_url = self.ws_url
        result = {}

        async def inner():
            async with websockets.connect(ws_url) as websocket:
                response = await self.send_command(websocket, method, params)
                result['response'] = response

        asyncio.run(inner())
        return result.get('response')

    async def run_javascript(self, script, tab=None):
        if tab:
            ws_url = tab.ws_url or self.get_ws_url_by_tab(tab)
            if not ws_url:
                raise Exception("WebSocket URL not found for the specified tab.")
        else:
            # 未指定 tab，获取当前活动的标签页
            tab = self.getTabInfo()
            if tab:
                ws_url = tab.ws_url or self.get_ws_url_by_tab(tab)
                if not ws_url:
                    raise Exception("WebSocket URL not found for the current active tab.")
            else:
                raise Exception("No active tab found.")
        async with websockets.connect(ws_url) as websocket:
            response = await self.send_command(websocket, "Runtime.evaluate", {"expression": script})
            return response

    def RunJavaScript(self, script, tab=None):
        result = asyncio.run(self.run_javascript(script, tab))
        return result

    def get_ws_url_by_tab(self, tab):
        url = f"http://localhost:{self.remote_port}/json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            tabs = response.json()
            for t in tabs:
                if t['id'] == tab.tab_id:
                    tab.ws_url = t['webSocketDebuggerUrl']
                    return tab.ws_url
            raise Exception("Tab not found")
        except Exception as e:
            print(f"Error getting WebSocket URL for tab: {e}")
            return None

    def close(self):
        """
        关闭整个 Chrome 浏览器实例。
        """
        try:
            if not self.browser_ws_url:
                self.browser_ws_url = self.get_browser_ws_url(self.remote_port)
            self.send_command_sync('Browser.close', ws_url=self.browser_ws_url)
            print("Chrome browser has been closed.")
        except Exception as e:
            print(f"Error closing Chrome browser: {e}")

    # 合并 BrowserManager 中的方法

    def getTabInfo(self):
        '''
        获取标签页信息
        :return:
        '''
        tabs = self._get_tabs()
        if tabs:
            # 假设第一个标签页为当前活动标签页
            current_tab = self._get_current_active_tab(tabs)
            return Tab(
                port=self.remote_port,
                tab_id=current_tab['id'],
                title=current_tab.get('title', ''),
                ws_url=current_tab.get('webSocketDebuggerUrl')
            )
        else:
            return None

    def getAllTabInfo(self):
        '''
        获取所有标签页信息
        :return:
        '''
        tabs = self._get_tabs()
        tab_list = []
        for tab in tabs:
            tab_obj = Tab(
                port=self.remote_port,
                tab_id=tab['id'],
                title=tab.get('title', ''),
                ws_url=tab.get('webSocketDebuggerUrl')
            )
            tab_list.append(tab_obj)
        # 反转列表，使最早的标签页在前
        tab_list.reverse()
        return tab_list

    def createNewTab(self, url):
        '''
        创建新标签页
        :param url: 指定标签页打开url
        :return:
        '''
        try:
            params = {'url': url}
            response = self.send_command_sync('Target.createTarget', params)
            target_id = response.get('result', {}).get('targetId')
            if target_id:
                # 等待新标签页在 /json 中出现
                time.sleep(1)
                # 获取新标签页的信息
                tabs = self._get_tabs()
                for tab in tabs:
                    if tab['id'] == target_id:
                        return Tab(
                            port=self.remote_port,
                            tab_id=tab['id'],
                            title=tab.get('title', ''),
                            ws_url=tab.get('webSocketDebuggerUrl')
                        )
                # 如果未找到，仍然返回 Tab 对象
                return Tab(port=self.remote_port, tab_id=target_id, title='', ws_url=None)
            else:
                print("Failed to create new tab.")
                return None
        except Exception as e:
            print(f"Error creating new tab: {e}")
            return None

    def switchToTab(self, tab):
        '''
        切换到标签页
        :param tab: 标签页
        :return:
        '''
        try:
            params = {'targetId': tab.tab_id}
            response = self.send_command_sync('Target.activateTarget', params)
            return 1  # 成功
        except Exception as e:
            print(f"Error switching to tab: {e}")
            return 0

    def closeTab(self, tab):
        """
        关闭指定的标签页。
        """
        try:
            params = {'targetId': tab.tab_id}
            response = self.send_command_sync('Target.closeTarget', params)
            print(f"Tab {tab.tab_id} has been closed.")
            return 1  # 成功
        except Exception as e:
            print(f"Error closing tab: {e}")
            return 0  # 失败

    def _get_tabs(self):
        try:
            response = requests.get(f'http://localhost:{self.remote_port}/json')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting tabs: {e}")
            return []

    def _get_current_active_tab(self, tabs):
        # 由于 DevTools 协议没有直接的方法获取当前活动标签页，这里假设第一个 'type' 为 'page' 的标签页为当前活动标签页
        for tab in tabs:
            if tab.get('type') == 'page':
                return tab
        return tabs[0]  # 如果没有找到，返回第一个标签页

    # 添加等待页面加载的方法

    async def is_page_loaded(self, tab=None, timeout=30):
        """
        检测网页是否加载完毕，默认超时时间为30秒。
        """
        ws_url = self.ws_url
        if tab:
            ws_url = tab.ws_url or self.get_ws_url_by_tab(tab)
            if not ws_url:
                raise Exception("WebSocket URL not found for the specified tab.")

        start_time = time.time()
        async with websockets.connect(ws_url) as websocket:
            await self.send_command(websocket, 'Runtime.enable')
            while True:
                response = await self.send_command(websocket, "Runtime.evaluate", {"expression": "document.readyState"})
                ready_state = response.get('result', {}).get('result', {}).get('value', '')
                if ready_state == 'complete':
                    return True
                if time.time() - start_time > timeout:
                    raise asyncio.TimeoutError("Timeout waiting for page to load.")
                await asyncio.sleep(0.5)

    def wait_until_page_loaded(self, tab=None, timeout=30):
        """
        等待网页加载完毕，默认超时时间为30秒。
        """
        try:
            result = asyncio.run(self.is_page_loaded(tab=tab, timeout=timeout))
            return result
        except Exception as e:
            print(f"Error waiting for page to load: {e}")
            return False

    def capture_screenshot(self, save_dir='./Picture', filename=None, tab=None):
        """
        截取当前页面的截图，保存到指定目录。
        参数：
        - save_dir: 保存截图的目录，默认 './Picture'。
        - filename: 文件名，默认使用当前时间戳。
        - tab: 指定的标签页，默认当前活动标签页。
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if filename is None:
            timestamp = int(time.time())
            filename = f'screenshot_{timestamp}.png'

        save_path = os.path.join(save_dir, filename)

        ws_url = self.ws_url
        if tab:
            ws_url = tab.ws_url or self.get_ws_url_by_tab(tab)

        async def take_screenshot():
            async with websockets.connect(ws_url) as websocket:
                await self.send_command(websocket, 'Page.enable')
                response = await self.send_command(websocket, 'Page.captureScreenshot', {'format': 'png'})
                screenshot_data = response.get('result', {}).get('data')
                if screenshot_data:
                    with open(save_path, 'wb') as f:
                        f.write(base64.b64decode(screenshot_data))
                    print(f"Screenshot saved to {save_path}")
                else:
                    print("Failed to capture screenshot.")

        asyncio.run(take_screenshot())

