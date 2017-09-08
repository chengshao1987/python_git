#运行之前先在命令行运行 pip install itchat (微信),pip install pandas(数据分析的包,一维数组，二维数组，三维数组)
## pip install numpy(科学计算) ,pip install matplotlib(2D图表和3D图表),
#pip install pillow(图片,此处用pillow替代PIL,因为)
#pip install wordcloud(词云,下载wordcloud-1.3.2-cp36-cp36m-win32.whl安装,pip install wordcloud-1.3.2-cp36-cp36m-win32.whl)
#pip install jieba(Jieba是一个中文分词组件，可用于中文句子/词性分割、词性标注、未登录词识别，支持用户词典等功能。该组件的分词精度达到了97%以上)

#运行之前首先要在命令行 pip install scipy-0.19.1-cp36-cp36m-win32.whl
# pip install numpy-1.13.1+mkl-cp36-cp36m-win32.whl

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import itchat
#coding=utf-8
# coding=gbk


#import numpy
#from PIL import Image

itchat.login()
friends=itchat.get_friends(update=True)[0:]
male=female=other=0
for i in friends[1:]:
    sex=i["Sex"]
    if sex==1:
        male+=1
    elif sex==2:
        female+=1
    else:
        other+=1
total=len(friends[1:])
print ("男性好友:%d个  %.2f%%      "%(male,float(male)/total*100)+
"女性好友：%d个  %.2f%%     "%(female,float(female)/total*100)+
"不明性别好友：%d个  %.2f%%       "%(other,float(other)/total*100))

#print("男性好友:%.2f%%"%(float(male)/total*100)+"\n"+
#"女性好友：%.2f%%"%(float(female)/total*100)+"\n"+
#"不明性别好友：%.2f%%"%(float(other)/total*100)+"\n")

#定义一个函数,用来爬取各个变量
def get_var(var):
    variable=[]
    for i in friends:
        value=i[var]
        variable.append(value)
    return variable

NickName=get_var("NickName")
Sex=get_var("Sex")
Province=get_var("Province")
City=get_var("City")
Signature=get_var("Signature")

from pandas import DataFrame
data={'NickName':NickName,'Sex':Sex,'Province':Province,'City':City,'Signature':Signature}
frame=DataFrame(data)
frame.to_csv('data.csv',index=True)

import re
siglist=[]
for i in friends:
    signature=i["Signature"].strip().replace("span","").replace("class","").replace("emoji","").replace("1f3b5","").replace("1f451","").replace("1f340","").replace("1f63c","").replace("1f339","").replace("1f3b5","").replace("1f6b2","").replace("1f4f7","").replace("1f370","").replace("1f358","").replace("1f363","").replace("2764","")
    rep=re.compile("1f\d+\w*|[<>/=]]")
    #signature=rep.sub("",signature)
    siglist.append(signature)
text="".join(siglist)

print(text)
import jieba
wordlist=jieba.cut(text,cut_all=True)
word_space_split=" ".join(wordlist)  #把wordlist里面的内容用空格连起来

print(word_space_split)

#simsun.ttc

import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image as Image
coloring=np.array(Image.open("E:\\jobs.jpg"))
#width=600, height=480
my_wordcloud=WordCloud(background_color="white",width=600, height=480,max_words=2000,mask=coloring,max_font_size=60,random_state=42,scale=2,font_path="E:\\simkai.ttf").generate(word_space_split)
image_colors=ImageColorGenerator(coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
plt.close()
my_wordcloud.to_file( "E:\\wordcloud_wechat3.png")



