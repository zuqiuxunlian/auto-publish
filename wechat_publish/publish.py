#!/usr/bin/python
# -*- coding: UTF-8 -*-
import feedparser
import requests
import json
from datetime import datetime
from datetime import timedelta

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse, parse_qsl
from markdownify import markdownify as md
from hanziconv import HanziConv

publish_api = "https://bbs.zuqiuxunlian.com/api/v1/topics"
time_format = "%a, %d %b %Y %H:%M:%S GMT"

#for test
# accesstoken = "eb8b35cc-fb1a-4e0d-822b-4b729617fff8"
# pwd = "./"

# online
pwd = "/root/auto-publish/wechat_publish/"

def read_entry(entry):
    topic = dict(
        id=entry['id'],
        author = entry.get('author', ''),
        published=datetime.strptime(entry['published'], time_format),
        title = entry['title'],
        summary=md(entry['summary']),
        link = entry['link'])
    return topic
    
def publish(topic, user):
    title = HanziConv.toSimplified(topic['title'])
    content = topic['author']+" "+user['title']+" [原文链接]"+"("+topic['link']+")\r\n\r\n"+topic['summary']
    content = HanziConv.toSimplified(content)
    payload = {
        "title": title,
        "tab": user['tab'],
        "content": content
    }
    querystring = {"accesstoken": user['accesstoken']}
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        }
    response = requests.request("POST", publish_api, json=payload, headers=headers, params=querystring)

def read_conf():
    with open(pwd+'conf.json', 'r') as f:
        data = json.load(f)
    return data
        
def write_conf(data):
    with open(pwd+'conf.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
# main
publishes = read_conf()
for p in publishes:
    feed = feedparser.parse(p['rss_url'])
    updated = datetime.strptime(p['updated'], time_format)
    # updated = datetime.strptime("Mon, 18 Mar 2019 00:34:42 GMT", time_format)
    print(p['title'])
    flag = False
    for entry in reversed(feed['entries']):
        print(entry['published'])
        published = datetime.strptime(entry['published'], time_format)
        if (published >= updated): # 同时间有几个文章
            updated = published
            content = read_entry(entry)
            publish(content, p)
            print(entry['title'])
            flag = True
        # else:
            # print(entry['title'])
    if (flag):
        updated = updated + timedelta(minutes=1)
    p['updated'] = updated.strftime(time_format)

write_conf(publishes)

# url = "https://cdn.werss.weapp.design/api/v1/feeds/7061a4e1-3d34-472a-942a-e370c7ea2ec4.xml"
# feed = feedparser.parse(url)
# # print(feed['feed'])
# print(feed['entries'][0])
