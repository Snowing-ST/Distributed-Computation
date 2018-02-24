# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:02:41 2018
爬虫文本预处理+情感分析

@author: situ
"""

import sys
import numpy as np
import pandas as pd 
from snownlp import SnowNLP
from snownlp import seg
from snownlp import sentiment #加载情感分析模块
import jieba
import jieba.posseg as pseg
import jieba.analyse
import codecs
import os
import re

stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = stdout

df = pd.read_json("C:/Users/situ/eastmoneySpider1-1000.json")
df2 = pd.read_json("C:/Users/situ/eastmoneySpider1001-1500.json")
df = pd.concat([df,df2],ignore_index=True)
#去掉重复的帖子
sum(df.duplicated()) #64列重复
df[df.duplicated()]

df = df.drop_duplicates()


df.tail(5)
df.head(10)
df.shape #(119203, 6)


df["comment"][df["comment"].isnull()] = "全部评论（0）"
df["url"][df["url"].isnull()] = "unknown"
df.isnull().any() #只有内容有缺失值    
         
df.to_excel("C:/Users/situ/eastmoneySpider1-1500.xlsx",encoding = "utf-8",sheet_name="tiezi", index=False)

#去除标题，因为许多股票的标题即内容开头，内容为空的，则用标题代替
len(df["content"][df["content"]==u'']) #8057条内容为空
df["content"][df["content"]==u''] = df["title"][df["content"]==u'']


#内容字数太少的，删除
df["content"][df["content"].str.len()<4] = np.nan
df = df.dropna()
df.shape #(110877, 6)


   
text=df["content"] #提取所有文本数据
text = text.dropna() 
len(text)
text=[i.decode('utf-8') for i in text] 
#上一步提取数据不是字符而是object，所以在这一步进行转码为字符




#分词，去除停用词，看词频-------------------------------------------------

#增加自定义词典
#jieba自定义词典的格式：
#词典格式和 dict.txt 一样，一个词占一行；每一行分三部分：
#词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。
#file_name 若为路径或二进制方式打开的文件，则文件必须为 UTF-8 编码。
#写一个R分词词典到jieba分词词典的转换格式的函数
#def transform(dictname,before_path,after_path):
#    file_obj = open(os.path.join(before_path,dictname))  
#    all_lines = file_obj.readlines()  
#    file_obj.close()  
#    file_write_obj = open(os.path.join(after_path,dictname.split(".")[0]+".txt"), 'w')  
#    for line in all_lines:  
#        word = line.split("\t")[0]
#        cipin = line.split("\t")[2].split("\n")[0]
#        cixing = line.split("\t")[1]+"\n"
#        newline = " ".join([word,cipin,cixing])
#        file_write_obj.writelines(newline)  
#    file_write_obj.close()   

#每次启动前都要加载
R_dict_path = "C:/Users/situ/Documents/R/win-library/3.4/Rwordseg/dict"
jieba_dict_path = "C:/Users/situ/Anaconda2/Lib/site-packages/jieba/userdicts/"

dicts = os.listdir(jieba_dict_path)
for i in range(len(dicts)):
#    transform(dicts[i],R_dict_path,jieba_dict_path)
    jieba.load_userdict(os.path.join(jieba_dict_path,dicts[i].split(".")[0]+".txt"))                     
    #加载自定义词典 
                   
#an example   
jieba.add_word('冲高回落')
jieba.add_word('A股')
jieba.add_word('增持')
example_text = "A股中创业板中午反弹了，再涨3个点，我就撤啦"
example_text = "大盘回调，啥股好跌停？"
example_text = "2015年的几部开年戏都出现了艾翠安娜伊凡丝的身影"
seg_list = jieba.cut(example_text,cut_all = False)                    
print " /".join(seg_list)        

#分词
def segment(one_text):
    one_seg_list = jieba.cut(one_text ,cut_all = True)       
    return " ".join(one_seg_list)   

seg = map(segment,text)        
print seg[0]

#去除停用词
#停用词文件是utf8编码  
#stoplist = {}.fromkeys([ line.strip() for line in 
#           open("E:/graduate/class/distributed/feng.li/final/stopword.txt") ]) 
    
#使用其他编码读取停用词表  
stoplist = codecs.open("E:/graduate/class/distributed/feng.li/final/stopword.txt",'r',encoding='gbk').readlines()  
stoplist = set(w.strip() for w in stoplist)  
def filterStopWords(line):
    line = re.sub("[0-9\n+]+".decode("utf8"), "".decode("utf8"),line)
    line1 = line.split(" ")
    for j in range(line1.count(u'')):
        line1.remove(u'')
    for j in range(line1.count(u'\n')):
        line1.remove(u'')
    newline = []
    for i in line1:
        if i not in stoplist: #千万不能用 in+remove！！！一定要not in +append！！！！
            newline.append(i)
    return newline

#example
print " ".join(filterStopWords(seg[3]))
print seg[0]

#去除停用词
rmstopwords = map(filterStopWords,seg)
print " ".join(rmstopwords[0])
len(rmstopwords) 


#rmstopwords 有的内容全清空了，要删除
df["segment"] = rmstopwords
df["content"][df["segment"].str.len()<1] #本来就是些无意义的内容，直接整行删除
df["segment"][df["segment"].str.len()<1] = np.nan
df = df.dropna()
df.shape #(109696, 7)

#查看词频 
word_dict= {}  
alltext = []
for onetiezi in rmstopwords:
    alltext.extend(onetiezi)
    
for item in alltext:  
    if item not in word_dict: #统计数量  
        word_dict[item] = 1  
    else:  
        word_dict[item] += 1    
word_dict1 = word_dict
len(word_dict1)

items=list(word_dict.items())    
items.sort(key=lambda x:x[1],reverse=True)    


for i in range(50):    
    word,count=items[i]    
    print('{0:<10}{1:>5}'.format(word,count))    
    
 #将统计结果写入文本文件中    
outfile = open('wordcount2.txt', "w")    
lines = []      
lines.append('单词种类：'+str(len(items))+'\n')    
lines.append('词频排序如下:\n')    
lines.append('word\tcounts\n')    
    
s= ''    
for i in range(len(items)):    
    s = '\t'.join([str(items[i][0]), str(items[i][1])])    
    s += '\n'      
    lines.append(s)    
print('\n统计完成！\n')    
outfile.writelines(lines)    
outfile.close()  


   

#找低频词，即频率为1的词
outfile = open('E:/graduate/class/distributed/feng.li/final/lowfreqwords.txt', "w")    
lowfreqwords = []      
s= ''    
for i in reversed(range(len(items))):    
    s = str(items[i][0])
    s += '\n'
    lowfreqwords.append(s)  
    if items[i][1]>1:
        break
print('\n统计完成！\n')    
outfile.writelines(lowfreqwords)    
outfile.close()  
len(lowfreqwords) #居然有23388条。。。。

#去除低频词
df["segment"] = ["/".join(line) for line in df["segment"]]
bf_rm_lf_word=df["segment"] #提取所有文本数据
bf_rm_lf_word = bf_rm_lf_word.dropna() 
len(bf_rm_lf_word) #109696
bf_rm_lf_word=[i.decode('utf-8') for i in bf_rm_lf_word] 

lowfreqwords = codecs.open("E:/graduate/class/distributed/feng.li/final/lowfreqwords.txt",'r',encoding='utf-8').readlines()  
lowfreqwords = set(w.strip() for w in lowfreqwords)  
def filterlfWords(line):
    line = line.decode("utf-8")
    line1 = line.split("/")
    newline = []
    for i in line1:
        if i not in lowfreqwords: #千万不能用 in+remove！！！一定要not in +append！！！！
            newline.append(i)
    return "/".join(newline)

rmlfwords = map(filterlfWords,bf_rm_lf_word)
len(rmlfwords)

df["rmlfwords"] = rmlfwords
df["rmlfwords"][df["rmlfwords"].str.len()<1] = np.nan #有些行被清空了
df = df.dropna()
df.shape #(109606, 8)
#确实去掉了低频词
df[["segment","rmlfwords"]][df["rmlfwords"]!=df["segment"]]


#情绪分析
#训练语料库
sentiment.train("E:/graduate/class/distributed/feng.li/final/NTUSD_simplified/NTUSD_negative_simplified.txt", 
                "E:/graduate/class/distributed/feng.li/final/NTUSD_simplified/NTUSD_positive_simplified.txt") 
#对语料库进行训练，把路径改成相应的位置。我这次练习并没有构建语料库，用了默认的，所以把路径写到了sentiment模块下。
sentiment.save('E:/graduate/class/distributed/feng.li/final/sentiment.marshal')
#这一步是对上一步的训练结果进行保存，如果以后语料库没有改变，下次不用再进行训练，直接使用就可以了，
#所以一定要保存，保存位置可以自己决定，但是要把`snownlp/seg/__init__.py`里的`data_path`也改成你保存的位置，不然下次使用还是默认的。
#example
SnowNLP(" ".join(rmstopwords[8])).sentiments
print " ".join(rmstopwords[5])
SnowNLP(df["segment"][3]).sentiments
SnowNLP(df["rmlfwords"][3]).sentiments

#情绪分析
def getsenti(line):
    return SnowNLP(line).sentiments
df["sentiment"] = map(getsenti,df["rmlfwords"]) #巨久


df.to_excel("E:/graduate/class/distributed/feng.li/final/tiezi(rmlfword).xlsx",encoding = "utf-8",sheet_name="tiezi", index=False)


#人工标记样本
from sklearn.cross_validation import train_test_split
train, test = train_test_split(df, train_size=0.02, random_state=42)
train.shape

train.to_excel("E:/graduate/class/distributed/feng.li/final/train(pyspark).xlsx",encoding = "utf-8",sheet_name="tiezi_train", index=False)
test.to_excel("E:/graduate/class/distributed/feng.li/final/test(pyspark).xlsx",encoding = "utf-8",sheet_name="tiezi_test", index=False)


#根据tf-idf提取关键词
keywords = jieba.analyse.extract_tags(" ".join(alltext), topK=20, withWeight=True, allowPOS=())
# 访问提取结果
for item in keywords:
    # 分别为关键词和相应的权重
    print item[0], item[1]

                   