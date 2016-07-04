# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from cameo.spiderForWEBACKERS import SpiderForWEBACKERS
from cameo.parserForWEBACKERS import ParserForWEBACKERS
"""
WEBACKERS 自動化 抓取 解析 匯入
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    spider = SpiderForWEBACKERS()
    parser = ParserForWEBACKERS()
    spider.runSpider(["browse"])
    spider.runSpider(["category"])
    parser.runParser(["category"])
    spider.runSpider(["automode"])
    parser.runParser(["automode"])
    
if __name__ == "__main__":
    entry_point()