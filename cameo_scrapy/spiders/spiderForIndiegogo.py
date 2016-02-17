# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import scrapy
import io

class SpiderForIndiegogo(scrapy.Spider):
    name = "sIndiegogo"
    start_urls = ["https://www.indiegogo.com/explore#/browse/landing"]
    def parse(self, response):
        source = response.body
        f = io.open("explore.html", "w+", encoding="utf-8")
        f.write(unicode(source))
        f.close()