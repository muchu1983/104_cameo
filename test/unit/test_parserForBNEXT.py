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
from cameo.parserForBNEXT import ParserForBNEXT
"""
測試 解析 數位時代 頁面
"""
class ParserForBNEXTTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 index.html
    def test_parseIndexPage(self):
        logging.info("ParserForTECHORANGETest.test_parseIndexPage")
        parser = ParserForTECHORANGE()
        parser.parseIndexPage()
        
    #測試 解析 tag.html
    def test_parseTagPage(self):
        logging.info("ParserForTECHORANGETest.test_parseTagPage")
        parser = ParserForTECHORANGE()
        parser.parseTagPage()
    
    #測試 解析 news.html 以找出更多 tag
    def test_findMoreTagByParseNewsPage(self):
        logging.info("ParserForTECHORANGETest.test_findMoreTagByParseNewsPage")
        parser = ParserForTECHORANGE()
        parser.findMoreTagByParseNewsPage()
    
    #測試 解析 news.html 並建立 news.json
    def test_parseNewsPageThenCreateNewsJson(self):
        logging.info("ParserForTECHORANGETest.test_parseNewsPageThenCreateNewsJson")
        parser = ParserForTECHORANGE()
        parser.parseNewsPageThenCreateNewsJson()
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


