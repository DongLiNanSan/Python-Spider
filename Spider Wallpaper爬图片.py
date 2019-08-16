#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import random
import os
import time

#请求头伪装
def headers():
        user_agent_list = [
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
        headers = {'User-Agent': random.choice(user_agent_list)}
        return headers

#请求html_1
def get_html(url):
    html = requests.get(url,headers=headers())
    return html

#处理html_1，爬取壁纸链接和标题
def deal_html(html):
    soup = BeautifulSoup(html.content, "lxml")
    soup2 = soup.find('td', align="left")
    soup3 = soup2.find('a')
    img_url = re.findall(r'<a href="(.*?)" title=".*?"><img alt=".*?" src=".*?" title=".*?"/></a>', str(soup3), re.S)
    title = re.findall(r'<a href=".*?" title="(.*?)"><img alt=".*?" src=".*?" title=".*?"/></a', str(soup3), re.S)
    tup_img_url_title=(img_url,title)
    return tup_img_url_title

#get图片，方式多线程
def log_pic(tup_img_url_title):
    img_url = tup_img_url_title[0]
    title = tup_img_url_title[1]
    print(img_url[0])
    pic=get_html(img_url[0])
    print(pic.content)
    with open(r'D:/Spider Wallpaper/%s.jpg ' % title[0], 'wb') as f:
        f.write(pic.content)
    print('正在下载第%s张:%s' % (t,title[0]))

#多线程任务
def task(url):
    log_pic(deal_html(get_html(url)))

if __name__ == '__main__':
    try:
        os.mkdir(r'D:/Spider Wallpaper')
    except:
        pass
    print('-----------壁纸爬取保存在D盘---------------')
    print('程序开始，将同时开启10个线程爬取')
    threadings = ThreadPoolExecutor(10)
    t=0
    for i in range(21570, 21991):
        t+=1
        url = 'http://www.netbian.com/desk/' + str(i) + '-1920x1080.htm'
        print(url)
        u = threadings.submit(task,url)
    threadings.shutdown(wait=True)
    print('------全部爬取完成,保存在D盘,路径：D:/Spider Wallpaper------')
    print('程序休眠20000秒，请自行关闭程序')
    time.sleep(20000)
