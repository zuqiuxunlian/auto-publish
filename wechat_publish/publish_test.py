# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""Publish test code."""
import feedparser
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
url = "https://cdn.werss.weapp.design/api/v1/feeds/93743d4b-3fb9-4e60-b6e7-976ad55a2918.xml"
# url = "https://bbs.zuqiuxunlian.com/rss"
feed = feedparser.parse(url, agent=agent)
# if feed['']
print(feed)
print(feed['feed'])
print(feed['entries'][0])
