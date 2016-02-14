# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import scrapy

class YahooSpider(scrapy.Spider):
    name = "yahoo"
    start_urls = ["https://tw.yahoo.com/"]
    def parse(self, response):
        item = response.xpath("//body//div/ul/li/a[contains(@href, 'https://tw.bid.yahoo.com/')]/span/text()")[0].extract()
        print(item)