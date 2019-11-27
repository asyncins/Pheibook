# -*- coding: utf-8 -*-
import scrapy


class SfhfpcSpider(scrapy.Spider):
    name = 'sfhfpc'
    allowed_domains = ['sfhfpc.com']
    start_urls = ['http://sfhfpc.com/']

    def parse(self, response):
        pass
