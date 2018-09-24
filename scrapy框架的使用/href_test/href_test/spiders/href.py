# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import HrefTestItem

class HrefSpider(scrapy.Spider):
    name = 'href'
    start_urls = ['https://matplotlib.org/examples/index.html']

    #初始页面
    def parse(self, response):
        #采用deny方式过滤掉部门网页
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound' , deny='/index.html$')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(url = link.url , callback=self.download_parse)

    def download_parse(self,response):
        url = response.css('a.reference.external::attr(href)').extract_first()
        url = response.urljoin(url)
        href = HrefTestItem()
        href['file_urls'] = []
        href['file_urls'].append(url)
        return href