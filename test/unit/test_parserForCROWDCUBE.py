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
from cameo.parserForCROWDCUBE import ParserForCROWDCUBE
"""
測試 解析 CROWDCUBE 頁面
"""
class ParserForCROWDCUBETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.parser = ParserForCROWDCUBE()
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 companies.html
    def test_parseCompaniesPage(self):
        logging.info("ParserForCROWDCUBETest.test_parseCompaniesPage")
        self.parser.parseCompaniesPage()
    """
    #測試 解析 company.html 並建立 json
    def test_parseProjectPage(self):
        logging.info("ParserForCROWDCUBETest.test_parseProjectPage")
        self.parser.parseProjectPage(strCategoryPage1Url=None)
    
    #測試 解析 funder.html 並建立 json
    def test_parseFunderPage(self):
        logging.info("ParserForJDTest.test_parseFunderPage")
        self.parser.parseFunderPage()
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


