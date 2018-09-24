# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stocklist.html']
    # 爬取股票代码
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.find_all('a')
        for x in a:
            try:
                href = x.attrs['href']
                url = re.findall(r's[hz]\d{6}', href)[0]
                url = 'https://gupiao.baidu.com/stock/' + url + '.html'
                yield scrapy.Request(url,callback=self.parse_stock)
            except:
                continue

    # 爬取详细信息
    def parse_stock(self, response):
        info = {}
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find_all('div', attrs={'class': 'stock-bets'})
        except:
            return
        name = div.find_all('a', attrs={'class': 'bets-name'})[0]
        info.update({'股票名称': name.text})
        keyList = div.find_all('dt')
        valueList = div.find_all('dd')
        for x in range(len(keyList)):
            try:
                info.update({keyList[x].string, valueList[x].string})
            except:
                continue
        yield info
