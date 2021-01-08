# coding=utf-8
"""
FAT-SCAN 配置
"""
import pathlib

# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent  # FAT-SCAN代码相对路径

chromium_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

# FAT-SCAN入口参数设置

# [代理设置]
enable_request_proxy = False  # 是否使用代理(全局开关)
proxy_all_module = False  # 代理所有模块
use_proxy_max_num = 3  # 最大使用次数
proxy_partial_module = ['crawlergo']  # 代理自定义的模块
request_proxy_pool = [{'http': 'http://127.0.0.1:1080',
                       'https': 'https://127.0.0.1:1080'}]  # 代理池

request_proxy_url = 'http://10.0.36.52:3289/'  # 代理服务
# request_proxy_pool = [{'http': 'socks5h://127.0.0.1:10808',
#                        'https': 'socks5h://127.0.0.1:10808'}]  # 代理池