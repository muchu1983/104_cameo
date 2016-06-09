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
from cameo.parserForINSIDE import ParserForINSIDE
"""
測試 解析 硬塞的 頁面
"""
class ParserForINSIDETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 index.html
    def test_parseIndexPage(self):
        logging.info("ParserForINSIDETest.test_parseIndexPage")
        parser = ParserForINSIDE()
        parser.parseIndexPage()
    
    #測試 解析 tag.html
    def test_parseTagPage(self):
        logging.info("ParserForINSIDETest.test_parseTagPage")
        parser = ParserForINSIDE()
        parser.parseTagPage()
    
    #測試 解析 news.html 以找出更多 tag
    def test_findMoreTagByParseNewsPage(self):
        logging.info("ParserForINSIDETest.test_findMoreTagByParseNewsPage")
        parser = ParserForINSIDE()
        parser.findMoreTagByParseNewsPage()
    
    #測試 解析 news.html 並建立 news.json
    def test_parseNewsPageThenCreateNewsJson(self):
        logging.info("ParserForINSIDETest.test_parseNewsPageThenCreateNewsJson")
        parser = ParserForINSIDE()
        parser.parseNewsPageThenCreateNewsJson()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


