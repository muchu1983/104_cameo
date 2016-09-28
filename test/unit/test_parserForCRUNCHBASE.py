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
from cameo.parserForCRUNCHBASE import ParserForCRUNCHBASE
"""
測試 CRUNCHBASE 解析
"""

class ParserForCRUNCHBASETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 explore 頁面
    def test_parseSearchFundingRoundsPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseSearchFundingRoundsPage")
        parser = ParserForCRUNCHBASE()
        parser.parseSearchFundingRoundsPage()
    """
    #測試 解析 category 頁面
    def test_parseCategoryPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseCategoryPage")
        parser = ParserV2ForINDIEGOGO()
        parser.parseCategoryPage()
    
    #測試 解析 project 頁面
    def test_parseProjectPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseProjectPage")
        parser = ParserV2ForINDIEGOGO()
        parser.parseProjectPage("automode")
        
    
    #測試 解析 individuals 頁面
    def test_parseIndividualsPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseIndividualsPage")
        parser = ParserV2ForINDIEGOGO()
        parser.parseIndividualsPage("automode")
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


