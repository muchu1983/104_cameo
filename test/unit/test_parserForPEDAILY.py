# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import json
from cameo.parserForPEDAILY import ParserForPEDAILY
"""
測試 解析 投資界 頁面
"""
class ParserForPEDAILYTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 index.html
    def test_parseIndexPage(self):
        logging.info("ParserForPEDAILYTest.test_parseIndexPage")
        parser = ParserForPEDAILY()
        parser.parseIndexPage()
    
    #測試 解析 category.html
    def test_parseCategoryPage(self):
        logging.info("ParserForPEDAILYTest.test_parseCategoryPage")
        parser = ParserForPEDAILY()
        parser.parseCategoryPage()
    
    #測試 解析 news.html 並建立 news.json
    def test_parseNewsPageThenCreateNewsJson(self):
        logging.info("ParserForPEDAILYTest.test_parseNewsPageThenCreateNewsJson")
        parser = ParserForPEDAILY()
        parser.parseNewsPageThenCreateNewsJson()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


