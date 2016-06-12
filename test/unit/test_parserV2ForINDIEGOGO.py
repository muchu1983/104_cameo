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
from cameo.parserV2ForINDIEGOGO import ParserV2ForINDIEGOGO
"""
INDIEGOGO 改版 2016-05-27 改寫
測試 INDIEGOGO 解析
"""

class ParserV2ForINDIEGOGOTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
    """
    #測試 解析 explore 頁面
    def test_parseExplorePage(self):
        logging.info("ParserV2ForINDIEGOGOTest.test_parseExplorePage")
        parser = ParserV2ForINDIEGOGO()
        parser.parseExplorePage()
    
    #測試 解析 category 頁面
    def test_parseCategoryPage(self):
        logging.info("ParserV2ForINDIEGOGOTest.test_parseCategoryPage")
        parser = ParserV2ForINDIEGOGO()
        parser.parseCategoryPage()
    """
    #測試 解析 project 頁面
    def test_parseProjectPage(self):
        logging.info("ParserV2ForINDIEGOGOTest.test_parseProjectPage")
        parser = ParserV2ForINDIEGOGO()
        parser.parseProjectPage("automode")
        
    """
    #測試 解析 individuals 頁面
    def test_parseIndividualsPage(self):
        logging.info("ParserV2ForINDIEGOGOTest.test_parseIndividualsPage")
        strCategory = "animals"
        parser = ParserV2ForINDIEGOGO()
        parser.beforeParseIndividualsPage(strCategory)
        parser.parseIndividualsProfilePage(strCategory)
        parser.parseIndividualsCampaignsPage(strCategory)
        parser.afterParseIndividualsPage(strCategory)
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


