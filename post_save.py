# -*- coding: utf-8 -*-
import os
import pdf_generator2
import re
from newspaper import  Article
import logging
import datetime
#import post_about
now=datetime.datetime.now()
#import generate_word
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
date_str=now.strftime("%Y-%m-%d")
pdf_dir="pdf/"+date_str+"/"
word_dir="word/"+date_str+"/"
text_dir="text/"+date_str+"/"
problem_dir="problem"
print date_str
type_list=["GRE","kaoyan","TOEFL","SAT","IELTS","GMAT"]
keword1_list=[u"啄木鸟",u"天道",u"新通",u"睿途",u"环球",u"环球雅思",u"尚友",u"华恒",]
keword2_list=[u"百利天下",u"前程百利",u"津桥国际",u"津桥",u"新航道",u"出国留学网",u"可可英语",u"乐闻",u"听力课堂",u"嘉卓留学",u"嘉卓",u"沪江留学",u"沪江",u"太傻留学",u"太傻",u"233校网",u"无忧考网"]
for item in type_list:
    if not os.path.isdir(text_dir+item):
       os.makedirs(text_dir+item)
    if not os.path.isdir(pdf_dir+item):
       os.makedirs(pdf_dir+item)
    if not os.path.isdir(word_dir+item):
       os.makedirs(word_dir+item)
def remove_keywords(pretext):
    text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', pretext)
    for item in keword1_list:
        text=text.replace(item,u"智课")
    for item in keword2_list:
        text=text.replace(item,u"智课教育")
    return text
def remvoe_jingpin(pretext):
     content=""
     for line in pretext.split("\n"):
         if "咨询热线" in line  or "咨询电话" in line or "QQ" in line or "电子邮箱" in line or "微信" in line or "400-618-0272" in line or "在线咨询"in line or "免费热线"in line or "点击进入" in line or "推荐文章"in line or"400-890-6000" in line or "考试热线" in line:
             print line
             line=""
         if "推荐阅读" in line or "相关阅读" in line or "猜你喜欢" in line or "指导老师" in line or "相关链接" in line or "免责声明" in line or "您还可能关注" in line :
             print line
             break
         content=content+line+"\n"
     return content
def save_post1(url,name_type):
  print url
  if name_type not in type_list:
      raise NameError
  try:
    a=Article(url,language='zh')
    #title,text=post_about.get_post(url,"tiandao")
    a.download()
    a.parse()
    title=a.title
    text=a.text
  except Exception:
    title=""
    text=""
  if len(text)>500:

    title=remove_keywords(title).encode("utf-8").replace("/","-").replace(".","")
    #content=text.encode("utf-8")
    content=remove_keywords(text).strip()
    content=remvoe_jingpin(content.encode("utf-8"))
    with open(text_dir+"/"+name_type.encode("utf-8")+"//"+title+".txt","w") as f:
        f.write(title+"\n")
        f.write(content)
    #try:
    #print content
    mypdf=pdf_generator2.pdfGenerator(title,content,name_type)
    mypdf.build_pdf(pdf_dir+"/"+name_type.encode("utf-8")+"/"+title+".pdf")
    #print type(content.decode("utf-8").encode("windows-1252"))

    #generate_word.convert_pdf2(title,content,word_dir,name_type)
    #except Exception:
      #logging.warning('some error with'+url)

  else:
      logging.warning("empty content"+url)
def save_post(title,content,name_type):
    content=remvoe_jingpin(content)
    if len(content)>200:
      mypdf=pdf_generator2.pdfGenerator(title,content,name_type)
      mypdf.build_pdf(pdf_dir+"/"+name_type+"/"+title+".pdf")
if __name__ =="__main__":
    save_post("http://www.igo99.cn/ielts/tingli/185884.shtml","GRE")