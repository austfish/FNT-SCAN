#!/usr/bin/python3
# coding=utf-8
# @name:    FNT-SCAN
# @repo:    https://github.com/austfish/FNT-SCAN
# @author:  austfish
# Main-file V1.0
import fire
from libs.banner import banner
from libs.log import logger
from datetime import datetime
from config import settings
from libs import utils

class FntScan(object):
    """
    FNT-SCAN help summary page

    FntScan is a powerful Crawler and passive scanner integration tool!

    Example:
        python3 FntScan.py version
        python3 FntScan.py check
        python3 FntScan.py --target https://www.baidu.com run
        python3 FntScan.py --targets ./urls.txt run

    Note:
        --port   small/medium/large  See details in ./config/setting.py(default small)
        --fmt csv/json (result format)
        --path   Result path (default None, automatically generated)

    :param str  target:     One domain (target or targets must be provided)
    :param str  targets:    File path of one domain per line
    :param bool alive:      Only export alive subdomains (default False)
    :param str  fmt:        Result format (default csv)
    :param str  path:       Result path (default None, automatically generated)
    :param bool takeover:   Scan subdomain takeover (default False)
    """

    def __init__(self, target=None, targets=None):
        self.target = target
        self.targets = targets
        self.subdomain = set()
        self.results = list()
        self.url = str()  # The url currently being collected
        self.urls = set()  # All urls that are to be collected
        self.data = list()  # The spider results of the current url
        self.datas = list()  # All spider results of the url

    def config_param(self):
        """
        Config parameter
        """
        pass

    def check_param(self):
        """
        Check parameter
        """
        if self.target is None and self.targets is None:
            logger.log('FATAL', 'You must provide either target or targets parameter')
            exit(1)

    def run(self):
        banner()
        logger.log('DEBUG', 'Python ' + utils.python_version())
        logger.log('DEBUG', 'FNT-SCAN ' + settings.version)
        logger.log('INFOR', 'Start running FNT-SCAN')
        self.config_param()
        self.check_param()
        self.urls = utils.get_urls(self.target, self.targets)
        count = len(self.urls)
        logger.log('INFOR', f'Got {count} urls')
        if not count:
            logger.log('FATAL', 'Failed to obtain domain')
            exit(1)

    @staticmethod
    def version():
        """
        Print version information and exit
        """
        banner()
        exit(0)
    

if __name__ == '__main__':
    fire.Fire(FntScan)