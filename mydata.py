# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os,csv
from datetime import datetime
from time import sleep

class MydataSpider(CrawlSpider):
    name = 'mydata'
    allowed_domains = ['seekingalpha.com']
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'


    def start_requests(self):
        yield scrapy.Request(url='https://seekingalpha.com/earnings/earnings-call-transcripts',headers={"User-Agent":self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@sasource="earnings-center-transcripts_article"]'), callback='parse_item', follow=True,process_request="set_user_agent"),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'),follow=True,process_request="set_user_agent")
)


    def set_user_agent(self,request):
        request.headers['User-agent']=self.user_agent
        return request

    def parse_item(self, response):
        date = response.css('#a-hd > div.a-info.clearfix > time::attr(content)').extract()[0]
        month = datetime.strptime(date,"%Y-%m-%dT%H:%M:%SZ").strftime('%B')
        Name=response.xpath('.//h1/text()').get()
        time=response.xpath('.//div[@class="a-info clearfix"]/time/text()').get()
        articles=''
        for article in response.xpath('//*[@id="a-body"]/descendant-or-self::node()/text()').extract():
            articles+=article
            
        self.appendItems(month,Name,time,articles)
        yield {

            "Name":Name,
            "time":time,
            "Attical":articles}
        
    def appendItems(self,*items):
        month = items[0]
        name = items[1]
        time = items[2]
        article = items[3]
        if not os.path.exists(month):
            os.makedirs(month)
        with open(month+'/'+name+'.txt', 'a', encoding='utf-8',newline='') as file:
            csvF = csv.writer(file)
            csvF.writerow([name+'\n\n',time+'\n\n\n',article,''])
            


  




        
