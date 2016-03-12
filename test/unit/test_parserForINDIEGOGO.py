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
from cameo.parserForINDIEGOGO import ParserForINDIEGOGO
"""
測試
"""

class ParserForINDIEGOGOTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.WARNING)
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
        
    #測試 解析 project 頁面
    def test_parseProjectPage(self):
        logging.info("ParserForINDIEGOGOTest.test_parseProjectPage")
        strCategory = "animals"
        parser = ParserForINDIEGOGO()
        parser.beforeParseProjectPage(strCategory)
        parser.parseProjectDetailsPage(strCategory)
        parser.parseProjectStoryPage(strCategory)
        parser.parseProjectBackersPage(strCategory)
        parser.parseProjectUpdatesPage(strCategory)
        parser.parseProjectCommentsPage(strCategory)
        parser.parseProjectRewardPage(strCategory)
        parser.afterParseProjectPage(strCategory)
        
    #測試 解析 individuals 頁面
    def test_parseIndividualsPage(self):
        logging.info("ParserForINDIEGOGOTest.test_parseIndividualsPage")
        strCategory = "animals"
        parser = ParserForINDIEGOGO()
        parser.beforeParseIndividualsPage(strCategory)
        parser.parseIndividualsProfilePage(strCategory)
        parser.parseIndividualsCampaignsPage(strCategory)
        parser.afterParseIndividualsPage(strCategory)

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


