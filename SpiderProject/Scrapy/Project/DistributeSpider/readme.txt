打造分布式Scapy爬虫
共分为两大部分：
1.使用Scrapy将爬取的数据保存到数据库
2.使用Django将数据从数据库取出展示到WEB网页中



各个分节如下：
一、
1).
选取目标网站：伯乐在线
详情见：BoleSpider
2).
选取目标网站；知乎
详情见；ZhiHu
这里涉及到一个新的知识点：Session的调用
3).
选取目标网站：拉钩
详情见：LaGou
这里涉及到一个新的知识点：crawl模版的使用

2、
加入反爬虫策略：设置User-Agent与Proxy代理池

3、
Scrapy-Selenium

4、
Srapy-Redis分布式爬虫

5、
Scrapy-ElasticSearch
ElasticSearch数据库集成到Scrapy

6、
Scrapy融入进Django

注意：使用scrapy shell 进行调试的时候要加上user-agent：
需要注意 网站做了限制爬虫，所以需要加上user-agent
    scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36" url
