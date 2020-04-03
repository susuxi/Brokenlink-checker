# Brokenlink-checker
python3 seo小工具

目前只能爬链接，状态检测待补充

检测规则：

递归爬站内所有同域名的跳转链接和图片链接，同时判断返回状态。所以爬的很全，但是慢。。。

使用：
```
python UrlSpider.py -u [url] -t [thread] -o [output]

python UrlSpider.py -u https://github.com -t 1 -o test.txt
```
