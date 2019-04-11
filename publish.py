#!/usr/bin/python
# -*- coding: UTF-8 -*-
import feedparser
import requests
import json
from datetime import datetime
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse, parse_qsl

publish_api = "https://bbs.zuqiuxunlian.com/api/v1/topics"
rss_url = "https://www.google.com/alerts/feeds/06602601644343027574/12963537258599994108"
pwd = "/home/ubuntu/publish/"
last_time = datetime.strptime("2019-04-10T05:26:15Z", '%Y-%m-%dT%H:%M:%SZ')
#for test
#accesstoken = ""
#tab = "dev"

#online
accesstoken = "9221248a-2ab9-48dc-ab66-123567696fbb"
tab = "news"

def origin_url(url):
    parsed_url = urlparse(url)
    qs = dict(parse_qsl(parsed_url.query))
    return qs['url']

def topic(entry):
    title = entry['title'].replace("<b>", "").replace("</b>", "")
    title = title.replace("&quot;", "\"")
    summary = entry['summary'].replace("<b>", "").replace("</b>", "")
    summary = summary.replace("&nbsp;", "")
    link = origin_url(entry['link'])
    topic = dict(
        id=entry['id'],
        published=entry['published'],
        title=title,
        summary=summary,
        link=link)
    return topic
    
def publish(topic):
    link = topic['link']
    payload = {
        "title": topic['title'],
        "tab": tab,
        "content": topic['summary']+"\r\n\r\n"+"["+link+"]("+link+")"
    }
    querystring = {"accesstoken":accesstoken}
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        }
    response = requests.request("POST", publish_api, json=payload, headers=headers, params=querystring)

def read_time():
    with open(pwd+'conf.json', 'r') as f:
        data = json.load(f)
    return data
        
def write_time(data):
    with open(pwd+'conf.json', 'w') as f:
        json.dump(data, f)
    
# main
# feed = feedparser.parse(r'data.xml')
feed = feedparser.parse(rss_url)
for entry in reversed(feed['entries']):
    print(topic(entry)['published'])
    last_time = datetime.strptime(read_time()['last_time'], '%Y-%m-%dT%H:%M:%SZ')
    new_time = datetime.strptime(entry['published'], '%Y-%m-%dT%H:%M:%SZ')
    if (last_time < new_time):
        last_time = new_time
        content = topic(entry)
        publish(content)
        print(content['title'].encode('utf-8'))

write_time(dict(last_time=last_time.strftime("%Y-%m-%dT%H:%M:%SZ")))
