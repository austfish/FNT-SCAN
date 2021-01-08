# coding=utf-8
"""
FNT-SCAN 默认配置
"""

import pathlib
import warnings

# 禁用所有警告信息
warnings.filterwarnings("ignore")

# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent  # FNT-SCAN代码相对路径
module_dir = relative_directory.joinpath('modules')  # FNT-SCAN模块目录
libs_party_dir = relative_directory.joinpath('libs')  # 通用功能目录
result_save_dir = relative_directory.joinpath('results')  # 结果保存目录
thirdparty_save_dir = result_save_dir.joinpath('thirdparty')  # 三方工具目录

# 工具路径

crawlergo_path = thirdparty_save_dir.joinpath('crawlergo.exe')
xray_path = thirdparty_save_dir.joinpath('xray').joinpath('xray_windows_amd64.exe')
version = 'v0.1'

# 默认请求头 可以在headers里添加自定义请求头
request_default_headers = {
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Forwarded-For': '127.0.0.1'
}
enable_random_ua = True  # 使用随机UA(默认True，开启可以覆盖request_default_headers的UA)
