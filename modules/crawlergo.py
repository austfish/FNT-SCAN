import simplejson
import subprocess
from libs.log import logger
from config import settings
from libs.module import Module
from libs.utils import gen_fake_header
import json



class Crawlergo(Module):
    def __init__(self, targets):
        self.targets = targets
        self.chromium = settings.chromium_path
        self.crawlergo = settings.crawlergo_path
        self.subdomains = list()
        self.results = list()
        self.module = 'Spider'
        self.source = 'Crawlergo'

    def spider(self, url):
        cmd = [f".\{self.crawlergo}", "-c", f"{self.chromium}","-t", "5","-f","smart","--fuzz-path","--custom-headers",json.dumps(gen_fake_header()), "--push-to-proxy", "http://127.0.0.1:7777/", "--push-pool-max", "10","--output-mode", "json" , url]
        print(cmd)
        rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = rsp.communicate()
        try:
            result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
        except:
            return
        for result in result["req_list"]:
            self.results.append(result)
        
        for subdomain in result["sub_domain_list"]:
            self.subdomainss.append(subdomain)
        logger.log('INFOR', f'Got {url} crawl ok')

    
    def main(self):
        for url in self.targets:
            self.spider(url)

    def run(self):
        """
        类执行入口
        """
        self.begin()

        self.main()
        # self.search()


        self.finish()
        # self.save_json()
        # self.gen_result()
        # self.save_db()

def run(targets):
    """
    类统一调用入口

    :param list targets: 目标
    """
    spider = Crawlergo(targets)
    spider.run()
    return spider.results


if __name__ == '__main__':
    print(run(['https://www.bootschool.net/', 'https://www.wangan.com']))