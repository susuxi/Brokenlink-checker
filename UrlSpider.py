# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import re
import UrlManager
import Downloader
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tld import get_tld
from arg import get_args

class UrlSpider(object):
    def __init__(self, root, threadNum):
        self.urls = UrlManager.UrlManager()
        self.download = Downloader.Downloader()
        self.root = root
        self.threadNum = threadNum

    def _judge(self, root, url):
        domain = get_tld(root, as_object=True).fld
        if url.find(domain) != -1:
            return True
        return False

    def _parse(self, page_url, content):
        if content is None:
            return
        soup = BeautifulSoup(content, 'html.parser')
        _news = self._get_new_urls(page_url, soup)
        return _news

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all(['a', 'img'])
        for link in links:
            if link.name == 'a':
                new_url = link.get('href')
                new_full_url = urljoin(page_url, new_url)
            elif link.name == 'img':
                new_full_url = link.get('src')
            # 如果要限制爬取初始网址域名，则取消该注释
            if new_full_url is None:
                continue
            if (self._judge(self.root,new_full_url)):
               new_urls.add(new_full_url)
            # 如果不限制爬虫爬取所有域名，则取消该注释
            # new_urls.add(new_full_url)
        url_pattern = re.compile(".*?url.*?(http.*?)\"")
        new_url = url_pattern.findall(soup.text)
        for url in new_url:
            if url is None:
                continue
            if self._judge(self.root, url):
                new_urls.add(url)
        return new_urls

    def craw(self):
        data = {}
        self.urls.add_new_url(self.root)
        while self.urls.has_new_url():
            _content = []
            th = []
            for i in list(range(self.threadNum)):
                if self.urls.has_new_url() is False:
                    break
                new_url = self.urls.get_new_url()
                print("craw: " + new_url)
                t = threading.Thread(target=self.download.download, args=(new_url, _content))
                t.start()
                th.append(t)
            for t in th:
                t.join()
            for _str in _content:
                if _str is None:
                    continue
                data[_str["url"]] = _str["status"]
                if _str["status"] == 200:
                    new_urls = self._parse(new_url, _str["html"])
                    self.urls.add_new_urls(new_urls)
            # 测试用
            # if len(data) > 20:
            #     break
        return data


if __name__ == "__main__":
    arg = get_args()
    m = UrlSpider(arg.url, arg.thread)
    urls = m.craw()
    print("共获取到{}条链接".format(len(urls)))
    with open(arg.output, 'w', encoding='utf-8') as f:
        print("正在将链接写入文件...")
        for url in urls:
            f.write(url+' '+str(urls[url])+'\n')
        print("所有链接已保存至{}文件中".format(arg.output))


