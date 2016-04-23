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
    """
    #測試 解析 index.html
    def test_parseIndexPage(self):
        logging.info("ParserForBNEXTTest.test_parseIndexPage")
        parser = ParserForBNEXT()
        parser.parseIndexPage()
    
    #測試 解析 tag.html
    def test_parseTagPage(self):
        logging.info("ParserForBNEXTTest.test_parseTagPage")
        parser = ParserForBNEXT()
        parser.parseTagPage()
    """
    #測試 解析 news.html 以找出更多 tag
    def test_findMoreTagByParseNewsPage(self):
        logging.info("ParserForBNEXTTest.test_findMoreTagByParseNewsPage")
        parser = ParserForBNEXT()
        parser.findMoreTagByParseNewsPage()
    """
    #測試 解析 news.html 並建立 news.json
    def test_parseNewsPageThenCreateNewsJson(self):
        logging.info("ParserForBNEXTTest.test_parseNewsPageThenCreateNewsJson")
        parser = ParserForBNEXT()
        parser.parseNewsPageThenCreateNewsJson()
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


