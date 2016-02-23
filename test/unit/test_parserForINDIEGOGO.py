# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.parserForINDIEGOGO import ParserForINDIEGOGO
"""
測試
"""

class ParserForINDIEGOGOTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
        
    #測試 解析 explore 頁面
    def test_parseExplorePage(self):
        logging.info("ParserForINDIEGOGOTest.test_parseExplorePage")
        parser = ParserForINDIEGOGO()
        parser.parseExplorePage()

    #測試 解析 category 頁面
    def test_parseCategoryPage(self):
        logging.info("ParserForINDIEGOGOTest.test_parseCategoryPage")
        parser = ParserForINDIEGOGO()
        parser.parseCategoryPage()
        
    #測試 解析 project_story 頁面
    def test_parseProjectStoryPage(self):
        logging.info("ParserForINDIEGOGOTest.test_parseProjectStoryPage")
        parser = ParserForINDIEGOGO()
        parser.parseProjectStoryPage("animals")

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


