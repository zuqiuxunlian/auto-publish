# RSS新闻自动发布
从Google搜索`足球``教练``训练`创建快讯的RSS拿到数据，自动发布到bbs.zuqiuxunlian.com网站的新闻板块。
RSS源：https://www.google.com/alerts/feeds/06602601644343027574/4041603352429017360
发布到：https://bbs.zuqiuxunlian.com/?tab=news

## Started
`python publish.py`

## Deploy
`crontab cron.conf`

`0 7 * * * /usr/bin/python /home/ubuntu/publish/publish.py > /home/ubuntu/publish/publish.log 2>&1 &`

每天7点定时运行程序。
