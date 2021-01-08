"""
Module base class
"""

import json
import threading
import time

import requests
from libs.log import logger
from config import settings
from libs import utils


lock = threading.Lock()


class Module(object):
    def __init__(self):
        self.module = 'Module'
        self.source = 'BaseModule'
        self.cookie = None
        self.header = dict()
        self.proxy = None
        self.delay = 1  # 请求睡眠时延
        self.timeout = settings.request_timeout_second  # 请求超时时间
        self.verify = settings.request_ssl_verify  # 请求SSL验证
        self.domain = str()  # 当前进行子域名收集的主域
        self.subdomains = set()  # 存放发现的子域
        self.infos = dict()  # 存放子域有关信息
        self.results = list()  # 存放模块结果
        self.start = time.time()  # 模块开始执行时间
        self.end = None  # 模块结束执行时间
        self.elapse = None  # 模块执行耗时

    def have_api(self, *apis):
        """
        Simply check whether the api information configure or not

        :param  apis: apis set
        :return bool: check result
        """
        if not all(apis):
            logger.log('DEBUG', f'{self.source} module is not configured')
            return False
        return True

    def begin(self):
        """
        begin log
        """
        logger.log('DEBUG', f'Start {self.source} module to '
                            f'collect targets of {self.targets}')

    def finish(self):
        """
        finish log
        """
        self.end = time.time()
        self.elapse = round(self.end - self.start, 1)
        logger.log('DEBUG', f'Finished {self.source} module to '
                            f'collect {self.targets}\'s results')
        logger.log('INFOR', f'{self.source} module took {self.elapse} seconds '
                            f'found {len(self.results)} results')
        logger.log('DEBUG', f'{self.source} module found subdomains of {self.targets}\n'
                            f'{self.subdomains}')

    def head(self, url, params=None, check=True, **kwargs):
        """
        Custom head request

        :param str  url: request url
        :param dict params: request parameters
        :param bool check: check response
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        try:
            resp = session.head(url,
                                params=params,
                                cookies=self.cookie,
                                headers=self.header,
                                proxies=self.proxy,
                                timeout=self.timeout,
                                verify=self.verify,
                                **kwargs)
        except Exception as e:
            logger.log('ERROR', e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('HEAD', resp):
            return resp
        return None

    def get(self, url, params=None, check=True, ignore=False, raise_error=False, **kwargs):
        """
        Custom get request

        :param str  url: request url
        :param dict params: request parameters
        :param bool check: check response
        :param bool ignore: ignore error
        :param bool raise_error: raise error or not
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        level = 'ERROR'
        if ignore:
            level = 'DEBUG'
        try:
            resp = session.get(url,
                               params=params,
                               cookies=self.cookie,
                               headers=self.header,
                               proxies=self.proxy,
                               timeout=self.timeout,
                               verify=self.verify,
                               **kwargs)
        except Exception as e:
            if raise_error:
                if isinstance(e, requests.exceptions.ConnectTimeout):
                    logger.log(level, e.args[0])
                    raise e
            logger.log(level, e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('GET', resp):
            return resp
        return None

    def post(self, url, data=None, check=True, **kwargs):
        """
        Custom post request

        :param str  url: request url
        :param dict data: request data
        :param bool check: check response
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        try:
            resp = session.post(url,
                                data=data,
                                cookies=self.cookie,
                                headers=self.header,
                                proxies=self.proxy,
                                timeout=self.timeout,
                                verify=self.verify,
                                **kwargs)
        except Exception as e:
            logger.log('ERROR', e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('POST', resp):
            return resp
        return None

    def delete(self, url, check=True, **kwargs):
        """
        Custom delete request

        :param str  url: request url
        :param bool check: check response
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        try:
            resp = session.delete(url,
                                  cookies=self.cookie,
                                  headers=self.header,
                                  proxies=self.proxy,
                                  timeout=self.timeout,
                                  verify=self.verify,
                                  **kwargs)
        except Exception as e:
            logger.log('ERROR', e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('DELETE', resp):
            return resp
        return None

    def get_header(self):
        """
        Get request header

        :return: header
        """
        headers = utils.gen_fake_header()
        if isinstance(headers, dict):
            self.header = headers
            return headers
        return self.header

    def get_proxy(self, module):
        """
        Get proxy

        :param str module: module name
        :return: proxy
        """
        if not settings.enable_request_proxy:
            logger.log('TRACE', f'All modules do not use proxy')
            return self.proxy
        if settings.proxy_all_module:
            logger.log('TRACE', f'{module} module uses proxy')
            return utils.get_random_proxy()
        if module in settings.proxy_partial_module:
            logger.log('TRACE', f'{module} module uses proxy')
            return utils.get_random_proxy()
        else:
            logger.log('TRACE', f'{module} module does not use proxy')
            return self.proxy


    def save_json(self):
        """
        Save the results of each module as a json file

        :return bool: whether saved successfully
        """
        if not settings.save_module_result:
            return False
        logger.log('TRACE', f'Save the subdomain results found by '
                            f'{self.source} module as a json file')
        path = settings.result_save_dir.joinpath(self.domain, self.module)
        path.mkdir(parents=True, exist_ok=True)
        name = self.source + '.json'
        path = path.joinpath(name)
        with open(path, mode='w', errors='ignore') as file:
            result = {'domain': self.domain,
                      'name': self.module,
                      'source': self.source,
                      'elapse': self.elapse,
                      'find': len(self.subdomains),
                      'subdomains': list(self.subdomains),
                      'infos': self.infos}
            json.dump(result, file, ensure_ascii=False, indent=4)
        return True

    