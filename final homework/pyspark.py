# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 19:12:14 2018
股吧帖子文本分类 pyspark

@author: situ
"""

pyspark
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.feature import HashingTF,IDF,StandardScaler
from pyspark.mllib.classification import NaiveBayes,LogisticRegressionWithLBFGS
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark import SparkContext
sc.stop()
sc = SparkContext(appName="guba")
originData=sc.textFile('file:///home/cufe2/situxueying/train(pyspark).csv') #utf-8的csv
originData.take(10)
emotionDocument=originData.map(lambda line : line.split(','))
emotionDocument.take(10)
emotion=emotionDocument.map(lambda s : s[0])
document=emotionDocument.map(lambda s: s[1])
#print(document.collect()) # collect：返回RDD中的数据
words=document.map(lambda line: line.split("/"))


#统计词频
text=words.flatMap(lambda w:w)
wordCounts = text.map(lambda word: (word, 1))\
.reduceByKey(lambda a, b: a+b).\
sortBy(lambda x: x[1],ascending=False)
wordCounts.take(10)

#[('指数', 325), ('大盘', 305), ('涨', 279), ('市场', 271), ('交易', 256), ('股市', 237), ('跌', 226), ('数据', 221), ('解禁', 208), ('个股', 199)]

#tf-idf------------------------------------------------------------------
hashingTF = HashingTF()
tf = hashingTF.transform(words)
tf.cache()
idfModel = IDF().fit(tf)
tfidf = idfModel.transform(tf)

# zip：将两个RDD对应元素组合为元组
zipped=emotion.zip(tfidf)
data=zipped.map(lambda line:LabeledPoint(line[0],line[1]))
training, test = data.randomSplit([0.6, 0.4], seed = 0)

NBmodel = NaiveBayes.train(training, 1)
predictionAndLabel = test.map(lambda p : (NBmodel.predict(p.features), p.label))
accuracy = 1.0 * predictionAndLabel.filter(lambda x: 1.0 \
if x[0] == x[1] else 0.0).count() / test.count()
print(accuracy) #0.630214

#随机森林 改标签为012
emotion2 = emotion.map(lambda i:int(i)+1)
emotion2.take(5)
zipped=emotion2.zip(tfidf)
data=zipped.map(lambda line:LabeledPoint(line[0]+1,line[1]))
training, test = data.randomSplit([0.6, 0.4], seed = 0)
#是否需要非负矩阵分解？？

model = RandomForest.trainClassifier(training, numClasses=3, categoricalFeaturesInfo={},numTrees=5, featureSubsetStrategy="auto",impurity='gini', maxDepth=2, maxBins=32) 
predictions = model.predict(test.map(lambda x: x.features)) 
labelsAndPredictions = test.map(lambda lp: lp.label).zip(predictions) 
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(test.count()) 
print('Test Error = ' + str(testErr)) 
print('Learned classification forest model:') 
print(model.toDebugString()) 


#分类未分类文本
yourDocument=sc.textFile('file:///home/cufe2/situxueying/test(pyspark).csv') #utf-8的csv
yourDocument.take(10)
yourwords=yourDocument.map(lambda line : line.split('/'))
yourtf = hashingTF.transform(yourwords)
yourtfidf=idfModel.transform(yourtf)
NBmodel.predict(yourtfidf)
predictionAndLabel = yourtfidf.map(lambda p : NBmodel.predict(p))
predictionAndLabel.count()
zipped2=yourDocument.zip(predictionAndLabel)
zipped2.take(10)
zipped2.saveAsTextFile("file:///home/cufe2/situxueying/prediction.csv")


