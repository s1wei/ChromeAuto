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

    def getOneElement(self, selector=None, xpath=None, js_path=None):
        return Element(self, selector=selector, xpath=xpath, js_path=js_path)

    def getAllElements(self, selector=None, xpath=None, js_path=None):
        """返回一个包含所有匹配元素的 ElementGroup"""
        return ElementGroup(self, selector=selector, xpath=xpath, js_path=js_path)

    def execute_script(self, script):
        """用于在当前 Tab 上执行 JavaScript"""
        from .initiate import ChromeInit
        chrome = ChromeInit(remote_port=self.port)
        result = chrome.RunJavaScript(script, tab=self)
        return result.get('result', {}).get('result', {}).get('value')

    def back(self):
        """实现浏览器后退功能"""
        script = '''
        (function() {
            window.history.back();
            return true;
        })();
        '''
        result = self.execute_script(script)
        if result:
            return 1
        else:
            return 0



class Element:
    def __init__(self, tab, selector=None, xpath=None, js_path=None, object_id=None, index=None):
        self.tab = tab
        self.selector = selector
        self.xpath = xpath
        self.js_path = js_path
        self.object_id = object_id  # RemoteObjectId
        self.index = index  # 用于多元素的索引

    def __repr__(self):
        return f"<Element Selector: {self.selector}, XPath: {self.xpath}, JS Path: {self.js_path}, Object ID: {self.object_id}>"

    def _get_element_script(self):
        """根据是否存在 objectId 或路径生成 JavaScript 以定位元素"""
        if self.object_id:
            return f"({{ objectId: '{self.object_id}' }})"
        elif self.js_path:
            return self.js_path
        elif self.selector:
            if self.index is not None:
                return f'document.querySelectorAll("{self.selector}")[{self.index}]'
            else:
                return f'document.querySelector("{self.selector}")'
        elif self.xpath:
            if self.index is not None:
                return f'''
                (function() {{
                    var snapshot = document.evaluate("{self.xpath}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    return snapshot.snapshotItem({self.index});
                }})();
                '''
            else:
                return f'document.evaluate("{self.xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'
        else:
            raise ValueError("Element must have a selector, xpath, js_path, or objectId.")


    def getParentElements(self):
        """获取当前元素的父元素，并返回 ElementGroup"""
        script = f'''
        (function() {{
            var element = {self._get_element_script()};
            if (element && element.parentElement) {{
                return [element.parentElement];
            }} else {{
                return [];
            }}
        }})();
        '''
        result = self.tab.execute_script(script)
        if result:
            return ElementGroup(self.tab, js_path='element.parentElement')
        else:
            return None

    def getChildElements(self):
        """获取当前元素的所有子元素，并返回 ElementGroup"""
        script = f'''
        (function() {{
            var element = {self._get_element_script()};
            if (element && element.children) {{
                return Array.from(element.children);
            }} else {{
                return [];
            }}
        }})();
        '''
        result = self.tab.execute_script(script)
        if result:
            return ElementGroup(self.tab, js_path='element.children')
        else:
            return None

    def click(self):
        """点击元素"""
        script = f'''
        (function() {{
            var element = {self._get_element_script()};
            if (element) {{
                element.click();
                return true;
            }} else {{
                return false;
            }}
        }})();
        '''
        result = self.tab.execute_script(script)
        if not result:
            print("Element not found or click failed.")

    def get_attribute(self, name):
        """获取元素的指定属性"""
        script = f'''
        (function() {{
            var element = {self._get_element_script()};
            if (element) {{
                return element.getAttribute("{name}");
            }} else {{
                return null;
            }}
        }})();
        '''
        return self.tab.execute_script(script)

    def set_value(self, value):
        """为元素设置值"""
        script = f'''
        (function() {{
            var element = {self._get_element_script()};
            if (element) {{
                element.value = "{value}";
                return true;
            }} else {{
                return false;
            }}
        }})();
        '''
        result = self.tab.execute_script(script)
        if not result:
            print("Element not found or set value failed.")

    def get_text(self):
        """获取元素文本内容"""
        script = f'''
        (function() {{
            var element = {self._get_element_script()};
            if (element) {{
                return element.textContent;
            }} else {{
                return null;
            }}
        }})();
        '''
        return self.tab.execute_script(script)


class ElementGroup:
    def __init__(self, tab, selector=None, xpath=None, js_path=None):
        self.tab = tab
        self.selector = selector
        self.xpath = xpath
        self.js_path = js_path

    def get_elements(self):
        """返回匹配到的元素列表"""
        script = f'''
        (function() {{
            var nodeList = {self._get_elements_script()};
            return nodeList.length;
        }})();
        '''
        count = self.tab.execute_script(script)
        elements = []
        for index in range(count):
            element = Element(
                self.tab,
                selector=self.selector,
                xpath=self.xpath,
                js_path=self.js_path + f'[{index}]' if self.js_path else None,
                index=index
            )
            elements.append(element)
        return elements

    def _get_elements_script(self):
        """生成 JavaScript 获取所有匹配的元素"""
        if self.selector:
            return f'document.querySelectorAll("{self.selector}")'
        elif self.xpath:
            return f'''
            (function() {{
                var snapshot = document.evaluate("{self.xpath}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                var elements = [];
                for (var i = 0; i < snapshot.snapshotLength; i++) {{
                    elements.push(snapshot.snapshotItem(i));
                }}
                return elements;
            }})();
            '''
        elif self.js_path:
            return self.js_path  # 如果是来自 parentElement 或 children 的路径，直接使用
        else:
            raise ValueError("ElementGroup must have a selector, xpath, or js_path.")
    def __iter__(self):
        """使得 ElementGroup 可迭代"""
        return iter(self.get_elements())

    # def click_all(self):
    #     """点击所有元素，不建议使用"""
    #     for element in self.get_elements():
    #         element.click()
