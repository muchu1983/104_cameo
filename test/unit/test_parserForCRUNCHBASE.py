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
    """
    #測試 解析 funding_rounds 頁面
    def test_parseSearchFundingRoundsPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseSearchFundingRoundsPage")
        parser = ParserForCRUNCHBASE()
        parser.parseSearchFundingRoundsPage()
    
    #測試 解析 investors 頁面
    def test_parseSearchInvestorsPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseSearchInvestorsPage")
        parser = ParserForCRUNCHBASE()
        parser.parseSearchInvestorsPage()
    
    #測試 解析 organization 頁面
    def test_parseOrganizationPage(self):
        logging.info("ParserForCRUNCHBASETest.test_parseOrganizationPage")
        parser = ParserForCRUNCHBASE()
        parser.parseOrganizationPage()
    """
    #測試 解析 CB_companies.csv 頁面
    def test_parseCompaniesCsv(self):
        logging.info("ParserForCRUNCHBASETest.test_parseCompaniesCsv")
        parser = ParserForCRUNCHBASE()
        parser.parseCompaniesCsv()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


