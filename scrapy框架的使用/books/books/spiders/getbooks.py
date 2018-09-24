# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import BooksItem

class GetbooksSpider(scrapy.Spider):
    name = 'getbooks'
    start_urls = ['http://books.toscrape.com/']

    #解析书籍列表页面
    def parse(self, response):
        #爬取本页面的书的链接
        le = LinkExtractor(restrict_css='ol.row')
        for links in le.extract_links(response):
            yield scrapy.Request(url = links.url,callback=self.books_parse)
        #
        # #爬取下一页的链接
        # le = LinkExtractor(restrict_css='li.next')
        # #返回列表类型
        # link = le.extract_links(response)
        # if link:
        #     yield scrapy.Request(link[0].url,callback=self.parse)
    #解析书籍详细信息页面
    def books_parse(self,response):
        book = BooksItem()
        sel = response.css('div.product_main')
        book['name'] = sel.xpath('./h1/text()').extract_first()
        book['price'] = sel.css('p.price_color::text').extract_first()
        book['review_rating'] =  sel.css('p.star-rating').re_first('star-rating ([A-Za-z]+)')

        sel = response.css('table.table')
        book['upc'] = sel.xpath('(.//td)[1]/text()').extract_first()
        book['stock']= sel.xpath('(.//td)[last()-1]/text()').re_first('(\d+) available')
        book['review_num'] = sel.xpath('(.//td)[last()]/text()').extract_first()

        yield book
