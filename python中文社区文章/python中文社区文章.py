# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

from bs4 import BeautifulSoup
import urllib2
import time

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent':user_agent}

# http://www.pythontab.com/html/pythonhexinbiancheng/2.html
url = 'http://www.pythontab.com/html/pythonhexinbiancheng/'
url_list = [url]
for i in range(2,21):
    url_list.append('http://www.pythontab.com/html/pythonhexinbiancheng/%s.html'%i)

# 标题+内容
source_list = []
for j in url_list:
    # 构造一个请求
    requests = urllib2.Request(j);
    requests.add_header("User-Agent", user_agent)
    time.sleep(1)
    response = urllib2.urlopen(requests)
    html = response.read()
    # 查看编码格式转码
    # html = html.decode("gbk").encode("utf-8")
    # print html
    soup = BeautifulSoup(html, 'lxml') # lxml解析器
    titles = soup.select('#catlist > li > a')# css选择器 语法
    # print titles
    links = soup.select('#catlist > li > a')
    # print links
    for title,link in zip(titles, links):
        data = {'title':title.get_text(),# 直接获取标题文本
                'link':link.get('href')# 获取文章的超链接
                }
        source_list.append(data)
        # print source_list
    for l in source_list:
        requests = urllib2.Request(l['link']);
        requests.add_header("User-Agent", user_agent)
        time.sleep(1)
        response = urllib2.urlopen(requests)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        text_p = soup.select('div.content > p') # 查找内容
        text = []
        # print text_p # 内容
        for t in text_p:
            text.append(t.get_text().encode('utf-8'))# 放入空列表
            # print text
        # 标题
        title_text = l['title']
        title_text = title_text.replace('*','').replace('/','or').replace('"',' ').replace('?','wenhao').replace(':',' ')
        # print title_text
        with open('%s.txt'%title_text, 'wb') as f:
            for a in text:
                f.write(a)
