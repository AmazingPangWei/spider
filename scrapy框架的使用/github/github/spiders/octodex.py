# -*- coding: utf-8 -*-
import scrapy
from ..items import GithubItem

class OctodexSpider(scrapy.Spider):
    name = 'octodex'
    start_urls = ['https://octodex.github.com/']

    def parse(self, response):
        url = response.css('div.item.list a.preview-image img')
        url = url.css('::attr(data-src)').extract()
        for t in range(len(url)):
            url[t] = response.urljoin(url[t])
        real_url = GithubItem()
        real_url['image_urls'] = url
        yield real_url
