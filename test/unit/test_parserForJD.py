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
from cameo.parserForJD import ParserForJD
"""
測試 解析 京東眾籌 頁面
"""
class ParserForJDTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.parser = ParserForJD()
        pass
        
    #收尾
    def tearDown(self):
        pass
    """
    #測試 解析 index.html
    def test_parseIndexPage(self):
        logging.info("ParserForJDTest.test_parseIndexPage")
        self.parser.parseIndexPage()
    """
    #測試 解析 category.html
    def test_parseCategoryPage(self):
        logging.info("ParserForJDTest.test_parseCategoryPage")
        self.parser.parseCategoryPage(strCategoryPage1Url=None)
    """
    #測試 解析 project.html 並建立 json
    def test_parseProjectPage(self):
        logging.info("ParserForJDTest.test_parseProjectPage")
        self.parser.parseProjectPage()
        
    #測試 解析 funder.html 並建立 json
    def test_parseFunderPage(self):
        logging.info("ParserForJDTest.test_parseFunderPage")
        self.parser.parseFunderPage()
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


