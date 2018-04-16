# 分布式计算期末论文

### 论文全文[基于spark的股吧情绪指标的构建.pdf](https://github.com/Snowing-ST/distributed_computation/blob/master/final%20homework/%E5%9F%BA%E4%BA%8Espark%E7%9A%84%E8%82%A1%E5%90%A7%E6%83%85%E7%BB%AA%E6%8C%87%E6%A0%87%E7%9A%84%E6%9E%84%E5%BB%BA.pdf)

written by Xueying Situ

    本文通过爬虫获得互联网中大量关于上证指数的帖子文本119203条，时间集中在2017年10月-2018年1月，并对帖子文本进行情绪分析，对投资者的投资心态进行考量，文本情绪分类中采用朴素贝叶斯、随机森林等机器学习的分类方法，利用spark实现分类过程，之后以标记了情绪倾向的帖子为依据，构建股吧的情绪指数。研究结果表明：本文提出的金融市场情绪指标与金融市场股指涨跌之间确实存在一定的关联，对互联网社交媒体进行舆情监测有一定的意义。

### [eastmoneySpider.py](https://github.com/Snowing-ST/distributed_computation/blob/master/final%20homework/eastmoneySpider.py)

基于scrapy的东方财富网上证指数吧帖子爬虫

### [preprocess+sentiment.py](https://github.com/Snowing-ST/distributed_computation/blob/master/final%20homework/preprocess%2Bsentiment.py)

文本预处理和情感分析

### [pyspark.py](https://github.com/Snowing-ST/distributed_computation/blob/master/final%20homework/pyspark.py)

基于pyspark的股吧帖子文本分类



