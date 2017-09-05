#coding=utf-8
# -*- coding:uft8 -*-
import requests
from bs4 import BeautifulSoup
import os
import urllib
#import urllib2
import re

#import socket
#import time
#import sys
#
#reload(sys)
#sys.setdefaultencoding('utf8')
#
#timeout=20
#socket.setdefaulttimeout(timeout)
#sleep_download_time=10
#time.sleep(sleep_download_time)


def getHtml(url):
	page=urllib.request.urlopen(url)
	html=page.read()
	return html

def getImg(html):
	reg=r'src="(.+\.jpg)"'
	imgre=re.compile(reg)
	imglist=re.findall(imgre,html)
	x=0
	for imgurl in imglist:
			urllib.urlretrieve(imgurl,'E:\python_workspace\pictures\%s.jpg'%x)
			x+=1
	return imglist

#创建图片目录：不存在就创建，如果已经存在则提示已经存在
def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("E:\python_workspace\pictures", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("E:\python_workspace\pictures", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url='http://finance.ifeng.com/listpage/finance-1318-1354-/1/spelist.shtml'
#all_url='http://finance.ifeng.com/listpage/finance-1318-1354-/8/spelist.shtml'
#start_html=requests.get(all_url,headers=headers)
#soup=BeautifulSoup(start_html.text,'lxml')
#lists2=soup.find('div', class_='newsList').find_all('a')
next_url=all_url
list_next_page=[]
list_next_page.append(all_url)
for b in range(1,15):
#取连环画列表的所有链接放在一个list_next_page里面，初始地址是all_url
    next_html=requests.get(next_url,headers=headers)
    next_soup=BeautifulSoup(next_html.text,'lxml')
    next_list=next_soup.find('div',class_='m_page').find_all('a')
    for a in next_list:
        title=a.get_text()
        href=a['href']
        if (title=='下一页 ') and (href!=next_url):
             list_next_page.append(href)
             print(b,title,href)
             next_url=href
        elif(title==' 上一页'):
            continue

#循环list_next_page,打开每一个链接,将图片下载到本地目录
for lll in list_next_page:
    news_html=requests.get(lll,headers=headers)
    news_soup=BeautifulSoup(news_html.text,'lxml')
    news_list=news_soup.find('div',class_='newsList').find_all('a')   #找到列表中每一个连环画链接并打开返回所有a标签的内容
    for b in news_list:
        news_title=b.get_text()
        news_href=b['href']
        if (news_title!=' 上一页') and (news_title!='下一页 '):#判断a标签是不是上一页下一页
            path = str(news_title).replace(":", "：").strip()#此处将文件夹名字中的英文冒号替换成中文冒号，因为英文冒号不能存在于文件夹名字中
            mkdir(path)
            #os.makedirs(os.path.join("E:\python_workspace\pictures", path)) ##创建一个存放套图的文件夹
            os.chdir("E:\python_workspace\pictures\\"+path) ##切换到上面创建的文件夹
            img_html = requests.get(news_href, headers=headers)
            img_Soup = BeautifulSoup(img_html.text, 'lxml')
            #img_url = img_Soup.find_all('img',class_='pic01')  ##这三行上面都说过啦不解释了哦
            #img_url = img_Soup.find('div',class_='pic01').find_all('img')  ##这三行上面都说过啦不解释了哦
            if img_Soup.find('div',class_='pic01'):  #判断是否为空
                img_url = img_Soup.find('div',class_='pic01').find_all('img') ##这三行上面都说过啦不解释了哦
                i=0
                for img_li in img_url:
                     img_url_i=img_li['src']
                     img_name=os.path.basename(img_url_i).replace("?","_")
                     img=requests.get(img_url_i,headers=headers)
                     if   (img_name!='acdf29584afc6a3.jpg') and len(img_name.split('.'))>1:
                         print(img_name)
                         f=open(path.replace(":","_")+'_'+str(i)+'.'+img_name.split('.')[1],'ab')
                         f.write(img.content)
                         f.close()
                     i=i+1



