import os
import re
import sys
import time
import json
import socket
import random
import string
import requests
from pathlib import Path
from stat import S_IXUSR
from libs.log import logger
from config import settings


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']

domain_regexp = r'\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b'
url_regexp = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def check_dir(dir_path):
    if not dir_path.exists():
        logger.log('INFOR', f'{dir_path} does not exist, directory will be created')
        dir_path.mkdir(parents=True, exist_ok=True)

def check_path(path, name, fmt):
    """
    检查结果输出目录路径

    :param path: 保存路径
    :param name: 导出名字
    :param fmt: 保存格式
    :return: 保存路径
    """
    filename = f'{name}.{fmt}'
    default_path = settings.result_save_dir.joinpath(filename)
    if isinstance(path, str):
        path = repr(path).replace('\\', '/')  # 将路径中的反斜杠替换为正斜杠
        path = path.replace('\'', '')  # 去除多余的转义
    else:
        path = default_path
    path = Path(path)
    if not path.suffix:  # 输入是目录的情况
        path = path.joinpath(filename)
    parent_dir = path.parent
    if not parent_dir.exists():
        logger.log('ALERT', f'{parent_dir} does not exist, directory will be created')
        parent_dir.mkdir(parents=True, exist_ok=True)
    if path.exists():
        logger.log('ALERT', f'The {path} exists and will be overwritten')
    return path

def re_match(string, regexp):
    result = re.search(regexp, string, re.I)
    if result:
        return result.group()
    return None

def match_main_url(url):
    if not isinstance(url, str):
        return None
    item = url.lower().strip()
    return re_match(item, url_regexp)

def get_from_target(target):
    urls = set()
    if isinstance(target, str):
        if target.endswith('.txt'):
            logger.log('FATAL', 'Use targets parameter for multiple url names')
            exit(1)
        url = match_main_url(target)
        if not url:
            return urls
        urls.add(url)
    return urls

def read_target_file(target):
    urls = list()
    with open(target, encoding='utf-8', errors='ignore') as file:
        for line in file:
            url = match_main_url(line)
            if not url:
                continue
            urls.append(url)
    sorted_urls = sorted(set(urls), key=urls.index)
    return sorted_urls

def get_from_targets(targets):
    urls = set()
    if not isinstance(targets, str):
        return urls
    try:
        path = Path(targets)
    except Exception as e:
        logger.log('ERROR', e.args)
        return urls
    if path.exists() and path.is_file():
        urls = read_target_file(targets)
        return urls
    return urls

def get_urls(target, targets=None):
    logger.log('DEBUG', f'Getting urls')
    target_urls = get_from_target(target)
    targets_urls = get_from_targets(targets)
    urls = list(target_urls.union(targets_urls))
    if targets_urls:
        urls = sorted(urls, key=targets_urls.index)  # 按照targets原本的index排序
    if not urls:
        logger.log('ERROR', f'Did not get a valid domain name')
    logger.log('DEBUG', f'The obtained domains \n{urls}')
    return urls


def check_format(fmt):
    """
    检查导出格式

    :param fmt: 传入的导出格式
    :return: 导出格式
    """
    formats = ['csv', 'json', ]
    if fmt in formats:
        return fmt
    else:
        logger.log('ALERT', f'Does not support {fmt} format')
        logger.log('ALERT', 'So use csv format by default')
        return 'csv'


def load_json(path):
    with open(path) as fp:
        return json.load(fp)


def save_to_file(path, data):
    """
    保存数据到文件

    :param path: 保存路径
    :param data: 待存数据
    :return: 保存成功与否
    """
    try:
        with open(path, 'w', errors='ignore', newline='') as file:
            file.write(data)
            return True
    except TypeError:
        with open(path, 'wb') as file:
            file.write(data)
            return True
    except Exception as e:
        logger.log('ERROR', e.args)
        return False


def check_response(method, resp):
    """
    检查响应 输出非正常响应返回json的信息

    :param method: 请求方法
    :param resp: 响应体
    :return: 是否正常响应
    """
    if resp.status_code == 200 and resp.content:
        return True
    logger.log('ALERT', f'{method} {resp.url} {resp.status_code} - '
                        f'{resp.reason} {len(resp.content)}')
    content_type = resp.headers.get('Content-Type')
    if content_type and 'json' in content_type and resp.content:
        try:
            msg = resp.json()
        except Exception as e:
            logger.log('DEBUG', e.args)
        else:
            logger.log('ALERT', msg)
    return False

def get_random_proxy():
    """
    Get random proxy
    """
    try:
        return requests.get("{}pop".format(settings.request_proxy_url)).json()
    except IndexError:
        return None

def get_proxy():
    """
    Get proxy
    """
    try:
        if settings.enable_request_proxy:
            return get_random_proxy()
    except IndexError:
        return None

def gen_fake_header():
    """
    Generate fake request headers
    """
    headers = settings.request_default_headers
    if not isinstance(headers, dict):
        headers = dict()
    if settings.enable_random_ua:
        ua = random.choice(user_agents)
        headers['User-Agent'] = ua
    headers['Accept-Encoding'] = 'gzip, deflate'
    return headers


def get_timestamp():
    return int(time.time())


def get_timestring():
    return time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))


def get_classname(classobj):
    return classobj.__class__.__name__


def python_version():
    return sys.version
