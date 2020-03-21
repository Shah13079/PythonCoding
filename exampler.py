# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from time import sleep
from shutil import which
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector



class ExampleSpider(scrapy.Spider):
    name = 'exampler'
    
    def start_requests(self):

        yield SeleniumRequest(

            url="https://www.duckduckgo.com",

            wait_time=8,
            
            screenshot=True,
            callback=self.parse
        )


    def parse(self, response):

        img=response.meta["screenshot"]
        with open("screenshot.png",'wb') as f:
            f.write(img)

        


      

            
