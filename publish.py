# !/usr/bin/python
# -*- coding: UTF-8 -*-
import feedparser
import requests
import ssl
import json
from datetime import datetime
from datetime import timedelta
from translate import translate

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse, parse_qsl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

publish_api = "https://bbs.zuqiuxunlian.com/api/v1/topics"
time_format = "%Y-%m-%dT%H:%M:%SZ"

# for test
# accesstoken = "eb8b35cc-fb1a-4e0d-822b-4b729617fff8"
# pwd = "./"

# online
pwd = "/home/ubuntu/publish/"

def origin_url(url):
    parsed_url = urlparse(url)
    qs = dict(parse_qsl(parsed_url.query))
    return qs['url']

def read_entry(entry):
    title = entry['title'].replace("<b>", "").replace("</b>", "")
    title = title.replace("&quot;", "\"")
    title = title.replace("&amp;", "&")
    summary = entry['summary'].replace("<b>", "").replace("</b>", "")
    summary = summary.replace("&nbsp;", "")
    link = origin_url(entry['link'])
    topic = dict(
        id=entry['id'],
        author = entry.get('author', ''),
        published=datetime.strptime(entry['published'], time_format),
        title = title,
        summary=summary,
        link = link)
    return topic

def publish(topic, user):
    link = topic['link']
    title = topic['title']
    summary = topic['summary']
    # 翻译 title，content
    if user['lang'] == 'en':
        title = translate(title) +" - "+ title
        summary = translate(summary) +"\r\n\r\n"+ summary

    content = summary +"\r\n\r\n"+"["+link+"]("+link+")"

    print(title.encode('utf-8'))

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
    feed = feedparser.parse(p['rss_url'], agent=agent)
    updated = datetime.strptime(p['updated'], time_format)
    # updated = datetime.strptime("Mon, 18 Mar 2019 00:34:42 GMT", time_format)
    print(p['title'])
    flag = False
    for entry in reversed(feed['entries']):
        print(entry['published'])
        published = datetime.strptime(entry['published'], time_format)
        if (published >= updated):  # 同时间有几个文章
            updated = published
            content = read_entry(entry)
            publish(content, p)
            # print(entry['title'].encode('utf-8'))
            flag = True
        # else:
            # print(entry['title'].encode('utf-8'))
    if (flag):
        updated = updated + timedelta(minutes=1)
    p['updated'] = updated.strftime(time_format)

write_conf(publishes)

# url = "https://cdn.werss.weapp.design/api/v1/feeds/7061a4e1-3d34-472a-942a-e370c7ea2ec4.xml"
# feed = feedparser.parse(url)
# # print(feed['feed'])
# print(feed['entries'][0])
