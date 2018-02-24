# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 19:42:23 2018
东方财富网股吧spider
@author: situ
"""

import scrapy

class eastmoneySpider(scrapy.Spider):
    name = 'eastmoney'
#    start_urls = ['http://guba.eastmoney.com/list,zssh000001.html'] 
    #scrapy自动去请求了，可以先用scrapy shell 先检测网站是否能访问
    start_urls = [
    'http://guba.eastmoney.com/list,zssh000001_%s.html' % p for p in xrange(1001,1500) #页数
    ]

    def parse(self, response):#拿回来的东西就是response
        for href in response.xpath('//span[@class="l3"]/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
#        print response.xpath('//*[@id="zwcontab"]/ul/li[1]/a/@href').extract_first() #url
        print response.xpath('//*[@id="zwconttbt"]/text()').extract_first() #标题
#        print response.xpath('//*[@id="zwconttbn"]/strong/a/text()').extract_first() #作者
#        print "\n".join(response.xpath('//div[@class = "stockcodec"]/text()').extract()) 
#        print ""
        yield {
            "url":response.xpath('//html/head/link[1]/@href').extract_first(),
            'title': response.xpath('//*[@id="zwconttbt"]/text()').extract_first().strip(),
            'time': response.xpath('//div[@class="zwfbtime"]/text()').extract_first().strip()[4:15],  
            "comment":response.xpath('//*[@id="zwcontab"]/ul/li[1]/a/text()').extract_first(),
            'writer':response.xpath('//*[@id="zwconttbn"]/strong/a/text()').extract_first().strip(),
            'content': "\n".join(response.xpath('//div[@class = "stockcodec"]/text()').extract()).strip() 
            #把每一段内容用\n换行
        }

#终端：scrapy runspider eastmoneySpider.py -o eastmoneySpider.json


