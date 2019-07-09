# -*- coding: utf-8 -*-
from scrapy import *
import json
from qd.items import UserItem
from qd.emailSender import emailSender  # 导入发信模块
import datetime
#aa1
class QidianSpider(Spider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com']
    start_urls = ['1011097497', '1004986370', '1012284323', '1013311315','1013719800']

    def start_requests(self):
        for page in self.start_urls:
            url = 'https://book.qidian.com/info/{id}#Catalog'.format(id=page)
            yield Request(url, callback=self.parse_detail)


    def parse_detail(self, response):
        item = UserItem()
        item['title']= response.xpath('//h1/em/text()').extract()
        print(item['title'])
        item['data']=response.xpath('//div[@class="left-wrap fl"]//li[@class="update"]//a/text()').extract()
        # item['data']= response.xpath('//div[@class="volume"][last()]//li[last()]/a/text()').extract()
        print(item['data'])

        yield item

    @staticmethod
    def close(spider,reason):
        emailSenderClient = emailSender()
        toSendEmailLst = ['844916536@qq.com', 'lwj.198@163.com']
        subject='起点小说'
        emailSenderClient.sendEmail(toSendEmailLst, subject)