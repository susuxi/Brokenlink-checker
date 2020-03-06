# -*- coding: utf-8 -*-

import requests


class Downloader(object):
    def get(self, url):
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        _str = r.text
        return _str

    def post(self, url, data):
        r = requests.post(url, data)
        _str = r.text
        return _str

    # 用于多线程下载
    def download(self, url, htmls):
        if url is None:
            return None
        _str = {}
        _str["url"] = url
        try:
            r = requests.get(url, timeout=10)
            _str["status"] = r.status_code
            if r.status_code != 200:
                htmls.append(_str)
                return None
            _str["html"] = r.text
        except Exception as e:
            return None
        htmls.append(_str)

