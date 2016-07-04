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
from cameo.importerForWEBACKERS import ImporterForWEBACKERS
"""
WEBACKERS 自動化 抓取 解析 匯入
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    spider = SpiderForWEBACKERS()
    parser = ParserForWEBACKERS()
    importer = ImporterForWEBACKERS()
    try:
        spider.runSpider(["browse"])
        spider.runSpider(["category"])
        parser.runParser(["category"])
        spider.runSpider(["automode"])
        parser.runParser(["automode"])
        importer.importJsonData()
    except Exception as e:
        logging.warning("automation for WEBACKERS fail: %s"%str(e))
        
if __name__ == "__main__":
    entry_point()